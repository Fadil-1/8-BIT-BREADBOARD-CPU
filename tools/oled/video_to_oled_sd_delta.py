#!/usr/bin/env python3
"""
Build an SD-backed delta-run OLED video payload for F8-BB.

The player keeps code in RAM and reads compact frame slots from SD.
Each frame stores horizontal byte-runs that differ from the previous frame.

Original version: May 2026
Fadil Isamotu
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.wintypes as wintypes
import math
import os
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

try:
    from PIL import Image, ImageOps, ImageSequence
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install pillow") from exc


SAFE_WIDTH = 128
SAFE_HEIGHT = 63
GROUPED_COLS = 64
SECTOR_SIZE = 512
DEFAULT_VIDEO_BLOCK = 2000
DEFAULT_THRESHOLD = 220
MAX_SLOT_SECTORS = 8
FRAME_BUFFER_ADDR = 0x6000


@dataclass(frozen=True)
class RunRecord:
    row: int
    col: int
    data: bytes


@dataclass(frozen=True)
class FrameInfo:
    index: int
    source_index: int
    run_count: int
    encoded_bytes: int
    changed_bytes: int
    lit_pixels: int


class WindowsRawDevice:
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080

    def __init__(self, device: str, mode: str):
        if mode not in {"rb", "r+b"}:
            raise ValueError("Windows raw device mode must be rb or r+b")

        self.device = device
        self.writable = "+" in mode
        self.handle = None
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel32 = kernel32

        kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.ReadFile.argtypes = [
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        kernel32.ReadFile.restype = wintypes.BOOL
        kernel32.WriteFile.argtypes = [
            wintypes.HANDLE,
            wintypes.LPCVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        kernel32.WriteFile.restype = wintypes.BOOL
        kernel32.SetFilePointerEx.argtypes = [
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        ]
        kernel32.SetFilePointerEx.restype = wintypes.BOOL
        kernel32.FlushFileBuffers.argtypes = [wintypes.HANDLE]
        kernel32.FlushFileBuffers.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        access = self.GENERIC_READ
        if self.writable:
            access |= self.GENERIC_WRITE

        handle = kernel32.CreateFileW(
            device,
            access,
            self.FILE_SHARE_READ | self.FILE_SHARE_WRITE,
            None,
            self.OPEN_EXISTING,
            self.FILE_ATTRIBUTE_NORMAL,
            None,
        )
        if handle == wintypes.HANDLE(-1).value:
            self._raise_last_error()
        self.handle = handle

    def _raise_last_error(self) -> None:
        code = ctypes.get_last_error()
        raise OSError(code, ctypes.FormatError(code), self.device)

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        new_pos = ctypes.c_longlong(0)
        if not self.kernel32.SetFilePointerEx(
            self.handle,
            ctypes.c_longlong(offset),
            ctypes.byref(new_pos),
            whence,
        ):
            self._raise_last_error()
        return new_pos.value

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            raise ValueError("raw block-device reads need an explicit byte count")
        buffer = ctypes.create_string_buffer(size)
        bytes_read = wintypes.DWORD(0)
        if not self.kernel32.ReadFile(
            self.handle,
            buffer,
            size,
            ctypes.byref(bytes_read),
            None,
        ):
            self._raise_last_error()
        return buffer.raw[:bytes_read.value]

    def write(self, data: bytes) -> int:
        view = memoryview(data)
        total = 0
        while total < len(view):
            chunk = view[total:total + 0x100000].tobytes()
            buffer = ctypes.create_string_buffer(chunk)
            bytes_written = wintypes.DWORD(0)
            if not self.kernel32.WriteFile(
                self.handle,
                buffer,
                len(chunk),
                ctypes.byref(bytes_written),
                None,
            ):
                self._raise_last_error()
            if bytes_written.value != len(chunk):
                raise OSError(f"Short write to {self.device}")
            total += bytes_written.value
        return total

    def flush(self) -> None:
        if self.writable and not self.kernel32.FlushFileBuffers(self.handle):
            self._raise_last_error()

    def close(self) -> None:
        if self.handle is not None:
            self.kernel32.CloseHandle(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class WindowsVolumeLock:
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080
    FSCTL_LOCK_VOLUME = 0x00090018
    FSCTL_UNLOCK_VOLUME = 0x0009001C
    FSCTL_DISMOUNT_VOLUME = 0x00090020

    def __init__(self, volume: str):
        self.volume = volume.rstrip(r"\/")
        self.handle = None
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel32 = kernel32

        kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.DeviceIoControl.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        kernel32.DeviceIoControl.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL

        handle = kernel32.CreateFileW(
            self.volume,
            self.GENERIC_READ | self.GENERIC_WRITE,
            self.FILE_SHARE_READ | self.FILE_SHARE_WRITE,
            None,
            self.OPEN_EXISTING,
            self.FILE_ATTRIBUTE_NORMAL,
            None,
        )
        if handle == wintypes.HANDLE(-1).value:
            self._raise_last_error()
        self.handle = handle
        self._device_io_control(self.FSCTL_LOCK_VOLUME)
        self._device_io_control(self.FSCTL_DISMOUNT_VOLUME)

    def _raise_last_error(self) -> None:
        code = ctypes.get_last_error()
        raise OSError(code, ctypes.FormatError(code), self.volume)

    def _device_io_control(self, code: int) -> None:
        bytes_returned = wintypes.DWORD(0)
        if not self.kernel32.DeviceIoControl(
            self.handle,
            code,
            None,
            0,
            None,
            0,
            ctypes.byref(bytes_returned),
            None,
        ):
            self._raise_last_error()

    def close(self) -> None:
        if self.handle is not None:
            self.kernel32.DeviceIoControl(
                self.handle,
                self.FSCTL_UNLOCK_VOLUME,
                None,
                0,
                None,
                0,
                ctypes.byref(wintypes.DWORD(0)),
                None,
            )
            self.kernel32.CloseHandle(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


def lock_windows_volume(volume: Optional[str]):
    if volume is None:
        return nullcontext()
    if os.name != "nt":
        raise ValueError("--windows-lock-volume is only supported on Windows")
    return WindowsVolumeLock(volume)


def is_windows_raw_device(device: str) -> bool:
    return os.name == "nt" and device.startswith("\\\\.\\")


def open_block_device(device: str, mode: str):
    if is_windows_raw_device(device):
        return WindowsRawDevice(device, mode)
    return open(device, mode, buffering=0)


def write_blocks_to_device(device: str, start_block: int, payload: bytes) -> None:
    if len(payload) % SECTOR_SIZE != 0:
        raise ValueError("payload length must be a whole number of sectors")
    with open_block_device(device, "r+b") as f:
        f.seek(start_block * SECTOR_SIZE)
        f.write(payload)
        if hasattr(f, "flush"):
            f.flush()


def read_blocks_from_device(device: str, start_block: int, block_count: int) -> bytes:
    with open_block_device(device, "rb") as f:
        f.seek(start_block * SECTOR_SIZE)
        data = f.read(block_count * SECTOR_SIZE)
    if len(data) != block_count * SECTOR_SIZE:
        raise RuntimeError("could not read the full video payload back")
    return data


def load_frames(path: Path) -> List[Image.Image]:
    suffix = path.suffix.lower()
    if suffix in {".gif", ".webp"}:
        img = Image.open(path)
        return [frame.convert("RGB") for frame in ImageSequence.Iterator(img)]
    if suffix in {".png", ".jpg", ".jpeg", ".bmp"}:
        return [Image.open(path).convert("RGB")]

    try:
        import imageio.v3 as iio  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Video input needs imageio: python -m pip install imageio imageio-ffmpeg"
        ) from exc

    frames: List[Image.Image] = []
    for frame in iio.imiter(path):
        frames.append(Image.fromarray(frame).convert("RGB"))
    return frames


def fit_frame(frame: Image.Image, fit: str, invert: bool) -> Image.Image:
    source = frame.convert("RGB")
    if fit == "stretch":
        return source.resize((SAFE_WIDTH, SAFE_HEIGHT), Image.Resampling.LANCZOS).convert("L")

    pad = 255 if invert else 0
    if fit == "contain":
        canvas = Image.new("RGB", (SAFE_WIDTH, SAFE_HEIGHT), (pad, pad, pad))
        fitted = ImageOps.contain(source, (SAFE_WIDTH, SAFE_HEIGHT), Image.Resampling.LANCZOS)
        x = (SAFE_WIDTH - fitted.width) // 2
        y = (SAFE_HEIGHT - fitted.height) // 2
        canvas.paste(fitted, (x, y))
        return canvas.convert("L")

    if fit == "crop":
        return ImageOps.fit(source, (SAFE_WIDTH, SAFE_HEIGHT), Image.Resampling.LANCZOS).convert("L")

    raise ValueError(f"unknown fit mode: {fit}")


def select_frames(frames: Sequence[Image.Image], step: int, max_frames: int) -> List[tuple[int, Image.Image]]:
    chosen = [(i, frame) for i, frame in enumerate(frames) if i % step == 0]
    if max_frames > 0:
        chosen = chosen[:max_frames]
    return chosen


def conversion_mode(args: argparse.Namespace) -> str:
    if args.threshold is not None:
        return "threshold"
    if args.grayscale:
        return "grayscale"
    return "threshold"


def effective_threshold(args: argparse.Namespace) -> int:
    return args.threshold if args.threshold is not None else DEFAULT_THRESHOLD


def quantize_frame(frame: Image.Image, args: argparse.Namespace) -> List[int]:
    img = fit_frame(frame, args.fit, args.invert)
    pixels = list(img.tobytes())

    if args.invert:
        pixels = [255 - value for value in pixels]

    nibbles: List[int] = []
    if conversion_mode(args) == "threshold":
        threshold = effective_threshold(args)
        for value in pixels:
            nibbles.append(args.fg if value >= threshold else 0)
    else:
        levels = args.gray_levels
        if levels < 2 or levels > 16:
            raise ValueError("gray levels must be 2..16")
        scale = levels - 1
        for value in pixels:
            level = int(round((value / 255.0) * scale))
            nibble = int(round((level / scale) * 15.0))
            nibbles.append(max(0, min(15, nibble)))

    if args.inset_x or args.inset_y:
        x0 = args.inset_x
        x1 = SAFE_WIDTH - args.inset_x
        y0 = args.inset_y
        y1 = SAFE_HEIGHT - args.inset_y
        for y in range(SAFE_HEIGHT):
            row = y * SAFE_WIDTH
            for x in range(SAFE_WIDTH):
                if x < x0 or x >= x1 or y < y0 or y >= y1:
                    nibbles[row + x] = 0

    return nibbles


def pack_frame(nibbles: Sequence[int]) -> bytes:
    packed = bytearray()
    for y in range(SAFE_HEIGHT):
        row = y * SAFE_WIDTH
        for x in range(0, SAFE_WIDTH, 2):
            left = nibbles[row + x]
            right = nibbles[row + x + 1]
            packed.append((left << 4) | right)
    return bytes(packed)


def frame_delta_runs(current: bytes, previous: bytes) -> List[RunRecord]:
    if len(current) != GROUPED_COLS * SAFE_HEIGHT:
        raise ValueError("unexpected current frame size")
    if len(previous) != GROUPED_COLS * SAFE_HEIGHT:
        raise ValueError("unexpected previous frame size")

    runs: List[RunRecord] = []
    for row in range(SAFE_HEIGHT):
        base = row * GROUPED_COLS
        col = 0
        while col < GROUPED_COLS:
            if current[base + col] == previous[base + col]:
                col += 1
                continue
            start = col
            data = bytearray()
            while col < GROUPED_COLS and current[base + col] != previous[base + col]:
                data.append(current[base + col])
                col += 1
            runs.append(RunRecord(row=row, col=start, data=bytes(data)))
    return runs


def encode_runs(runs: Sequence[RunRecord]) -> bytes:
    if len(runs) > 255:
        raise ValueError(
            f"frame has {len(runs)} runs; the current player supports at most 255 runs per frame"
        )
    out = bytearray()
    out.append(len(runs))
    out.append(0x00)
    for run in runs:
        if not 0 <= run.col <= 63:
            raise ValueError("run column is outside 0..63")
        if not 0 <= run.row <= 62:
            raise ValueError("run row is outside 0..62")
        if not 1 <= len(run.data) <= 64:
            raise ValueError("run byte count must be 1..64")
        out.extend([run.col, run.row, len(run.data)])
        out.extend(run.data)
    return bytes(out)


def block_bytes(block: int) -> tuple[int, int, int, int]:
    if not 0 <= block <= 0xFFFFFFFF:
        raise ValueError("video block must fit in 32 bits")
    return (
        (block >> 24) & 0xFF,
        (block >> 16) & 0xFF,
        (block >> 8) & 0xFF,
        block & 0xFF,
    )


def asm_putc(lines: List[str], value: int, comment: str = "") -> None:
    suffix = f" ; {comment}" if comment else ""
    lines.append(f"    MOV $A, 0x{value:02X}{suffix}")
    lines.append("    JSR OLED4_PUTC")


def asm_puts(lines: List[str], text: str) -> None:
    for ch in text:
        if ch == "\n":
            lines.append("    MOV $A, 0x0A")
            lines.append("    JSR OLED4_PUTC")
        else:
            asm_putc(lines, ord(ch), ch if ch != " " else "space")


def make_player_asm(args: argparse.Namespace, frame_count: int, slot_sectors: int) -> str:
    b0, b1, b2, b3 = block_bytes(args.video_block)
    lines: List[str] = []
    delay_calls = max(0, args.delay_calls)

    lines.extend([
        "#addr 0x0200",
        f"#include \"{args.ruledef}\"",
        f"#include \"{args.constants}\"",
        "",
        "JMP START",
        "",
        f"#include \"{args.lowlevel}\"",
        f"#include \"{args.text4}\"",
        f"#include \"{args.graphics}\"",
        f"#include \"{args.spi_routines}\"",
        f"#include \"{args.spi_init}\"",
        f"#include \"{args.sd_block_io}\"",
        "",
        "; ---------- SD delta video state ----------",
        "VID_FRAME_LEFT    = 0x7340",
        "VID_SECTORS_LEFT  = 0x7341",
        "VID_RUNS_LEFT     = 0x7342",
        "VID_RUN_COL       = 0x7343",
        "VID_RUN_ROW       = 0x7344",
        "VID_RUN_COUNT     = 0x7345",
        "VID_PTR_LO        = 0x7346",
        "VID_PTR_HI        = 0x7347",
        "",
        "VID_BUFFER_LO     = 0x00",
        "VID_BUFFER_HI     = 0x60",
        f"VID_FRAME_COUNT   = 0x{frame_count:02X}",
        f"VID_SLOT_SECTORS  = 0x{slot_sectors:02X}",
        "",
        "START:",
        "    MOV $CLK, 0x07",
        "    JSR OLED_INIT",
        "    JSR OLED4_SET_DEFAULT_ORIGIN",
        "    JSR OLED4_HOME",
        "    JSR OLEDG_CLEAR_SAFE_AREA",
        "    JSR VID_PRINT_START_TEXT",
        "    JSR SD_INIT_RELIABLE",
        "",
        "VID_LOOP:",
        "    JSR OLEDG_CLEAR_SAFE_AREA",
        "    JSR VID_SET_START_BLOCK",
        "    MOV $A, VID_FRAME_COUNT",
        "    MOV VID_FRAME_LEFT, $A",
        "",
        "VID_FRAME_LOOP:",
        "    JSR VID_LOAD_SLOT_TO_BUFFER",
        "    JC VID_READ_FAIL",
        "",
        "    JSR VID_DRAW_DELTA_SLOT",
    ])
    for _ in range(delay_calls):
        lines.append("    JSR VID_DELAY_FRAME")
    lines.extend([
        "",
        "    MOV $A, VID_FRAME_LEFT",
        "    STC",
        "    SUB $A, 0x01",
        "    PSF",
        "    MOV VID_FRAME_LEFT, $A",
        "    PLF",
        "    JNZ VID_FRAME_LOOP",
        "",
        "    JMP VID_LOOP",
        "",
        "VID_SET_START_BLOCK:",
        f"    MOV $A, 0x{b0:02X}",
        "    MOV SD_BLOCK_ADDR_MSB, $A",
        f"    MOV $A, 0x{b1:02X}",
        "    MOV SD_BLOCK_ADDR_B2, $A",
        f"    MOV $A, 0x{b2:02X}",
        "    MOV SD_BLOCK_ADDR_B1, $A",
        f"    MOV $A, 0x{b3:02X}",
        "    MOV SD_BLOCK_ADDR_LSB, $A",
        "    RTS",
        "",
        "VID_INC_SD_BLOCK:",
        "    MOV $A, SD_BLOCK_ADDR_LSB",
        "    CLC",
        "    ADD $A, 0x01",
        "    PSF",
        "    MOV SD_BLOCK_ADDR_LSB, $A",
        "    PLF",
        "    JNC .VID_INC_DONE",
        "",
        "    MOV $A, SD_BLOCK_ADDR_B1",
        "    CLC",
        "    ADD $A, 0x01",
        "    PSF",
        "    MOV SD_BLOCK_ADDR_B1, $A",
        "    PLF",
        "    JNC .VID_INC_DONE",
        "",
        "    MOV $A, SD_BLOCK_ADDR_B2",
        "    CLC",
        "    ADD $A, 0x01",
        "    PSF",
        "    MOV SD_BLOCK_ADDR_B2, $A",
        "    PLF",
        "    JNC .VID_INC_DONE",
        "",
        "    MOV $A, SD_BLOCK_ADDR_MSB",
        "    CLC",
        "    ADD $A, 0x01",
        "    MOV SD_BLOCK_ADDR_MSB, $A",
        "",
        ".VID_INC_DONE:",
        "    RTS",
        "",
        "VID_LOAD_SLOT_TO_BUFFER:",
        "    MOV $C, VID_BUFFER_LO",
        "    MOV $D, VID_BUFFER_HI",
        "    MOV $A, VID_SLOT_SECTORS",
        "    MOV VID_SECTORS_LEFT, $A",
        "",
        ".VID_LOAD_SECTOR:",
        "    JSR SD_READ_BLOCK_TO_RAM_512",
        "    JC .VID_LOAD_FAIL",
        "    JSR VID_INC_SD_BLOCK",
        "",
        "    MOV $A, VID_SECTORS_LEFT",
        "    STC",
        "    SUB $A, 0x01",
        "    PSF",
        "    MOV VID_SECTORS_LEFT, $A",
        "    PLF",
        "    JNZ .VID_LOAD_SECTOR",
        "",
        "    CLC",
        "    RTS",
        "",
        ".VID_LOAD_FAIL:",
        "    STC",
        "    RTS",
        "",
        "VID_INC_CD:",
        "    CLC",
        "    ADD $C, 0x01",
        "    JNC .VID_INC_CD_DONE",
        "    CLC",
        "    ADD $D, 0x01",
        "",
        ".VID_INC_CD_DONE:",
        "    RTS",
        "",
        "VID_SAVE_PTR:",
        "    MOV VID_PTR_LO, $C",
        "    MOV VID_PTR_HI, $D",
        "    RTS",
        "",
        "VID_RESTORE_PTR:",
        "    MOV $C, VID_PTR_LO",
        "    MOV $D, VID_PTR_HI",
        "    RTS",
        "",
        "VID_DRAW_DELTA_SLOT:",
        "    MOV $C, VID_BUFFER_LO",
        "    MOV $D, VID_BUFFER_HI",
        "    MOV $A, [$CD]",
        "    MOV VID_RUNS_LEFT, $A",
        "    JSR VID_INC_CD",
        "    JSR VID_INC_CD",
        "",
        ".VID_RUN_LOOP:",
        "    MOV $A, VID_RUNS_LEFT",
        "    STC",
        "    CMP $A, 0x00",
        "    JZ .VID_RUNS_DONE",
        "",
        "    MOV $A, [$CD]",
        "    MOV VID_RUN_COL, $A",
        "    JSR VID_INC_CD",
        "",
        "    MOV $A, [$CD]",
        "    MOV VID_RUN_ROW, $A",
        "    JSR VID_INC_CD",
        "",
        "    MOV $A, [$CD]",
        "    MOV VID_RUN_COUNT, $A",
        "    JSR VID_INC_CD",
        "",
        "    JSR VID_SAVE_PTR",
        "    JSR VID_BEGIN_RUN_WINDOW",
        "    JSR VID_RESTORE_PTR",
        "",
        "    MOV $B, VID_RUN_COUNT",
        "",
        ".VID_DATA_LOOP:",
        "    MOV $A, [$CD]",
        "    OLD $A",
        "    JSR VID_INC_CD",
        "    STC",
        "    SUB $B, 0x01",
        "    JNZ .VID_DATA_LOOP",
        "",
        "    MOV $A, VID_RUNS_LEFT",
        "    STC",
        "    SUB $A, 0x01",
        "    MOV VID_RUNS_LEFT, $A",
        "    JMP .VID_RUN_LOOP",
        "",
        ".VID_RUNS_DONE:",
        "    RTS",
        "",
        "VID_BEGIN_RUN_WINDOW:",
        "    MOV $A, 0x15",
        "    OLC $A",
        "    MOV $A, VID_RUN_COL",
        "    OLC $A",
        "    MOV $A, VID_RUN_COUNT",
        "    STC",
        "    SUB $A, 0x01",
        "    CLC",
        "    ADD $A, VID_RUN_COL",
        "    OLC $A",
        "",
        "    MOV $A, 0x75",
        "    OLC $A",
        "    MOV $A, VID_RUN_ROW",
        "    OLC $A",
        "    MOV $A, VID_RUN_ROW",
        "    OLC $A",
        "",
        "    MOV $A, 0x5C",
        "    OLC $A",
        "    RTS",
        "",
        "VID_DELAY_FRAME:",
        "    PSH $A",
        "    PSH $B",
        "    MOV $A, 0x20",
        "",
        ".VID_DELAY_FRAME_OUTER:",
        "    MOV $B, 0xFF",
        "",
        ".VID_DELAY_FRAME_INNER:",
        "    NOP",
        "    NOP",
        "    STC",
        "    SUB $B, 0x01",
        "    JNZ .VID_DELAY_FRAME_INNER",
        "",
        "    STC",
        "    SUB $A, 0x01",
        "    JNZ .VID_DELAY_FRAME_OUTER",
        "",
        "    PUL $B",
        "    PUL $A",
        "    RTS",
        "",
        "VID_DELAY_HOLD:",
        "    JSR VID_DELAY_FRAME",
        "    JSR VID_DELAY_FRAME",
        "    RTS",
        "",
        "VID_READ_FAIL:",
        "    JSR OLEDG_CLEAR_SAFE_AREA",
        "    JSR OLED4_HOME",
        "    JSR VID_PRINT_READ_FAIL",
        "",
        ".VID_FAIL_HOLD:",
        "    JSR VID_DELAY_HOLD",
        "    JMP .VID_FAIL_HOLD",
        "",
        "VID_PRINT_START_TEXT:",
    ])
    asm_puts(lines, "SD DELTA VIDEO\n")
    asm_puts(lines, f"BLOCK {args.video_block}\n")
    asm_puts(lines, f"FRAMES {frame_count}\n")
    asm_puts(lines, f"SLOT {slot_sectors}\n")
    lines.extend([
        "    RTS",
        "",
        "VID_PRINT_READ_FAIL:",
    ])
    asm_puts(lines, "SD READ FAIL")
    lines.append("    RTS")
    return "\n".join(lines) + "\n"


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    frame_infos: Sequence[FrameInfo],
    payload: bytes,
    slot_sectors: int,
) -> None:
    total_sectors = len(payload) // SECTOR_SIZE
    max_encoded = max(item.encoded_bytes for item in frame_infos)
    max_runs = max(item.run_count for item in frame_infos)
    lines = [
        "OLED SD delta video manifest",
        f"input: {args.input}",
        f"video_block: {args.video_block}",
        f"frame_count: {len(frame_infos)}",
        f"frame_step: {args.frame_step}",
        f"max_frames: {args.max_frames}",
        f"mode: {conversion_mode(args)}",
        f"threshold: {effective_threshold(args) if conversion_mode(args) == 'threshold' else 'none'}",
        f"grayscale: {args.grayscale}",
        f"gray_levels: {args.gray_levels}",
        f"invert: {args.invert}",
        f"fit: {args.fit}",
        f"inset_x: {args.inset_x}",
        f"inset_y: {args.inset_y}",
        f"fg: 0x{args.fg:X}",
        f"safe_width: {SAFE_WIDTH}",
        f"safe_height: {SAFE_HEIGHT}",
        f"slot_sectors: {slot_sectors}",
        f"slot_bytes: {slot_sectors * SECTOR_SIZE}",
        f"total_bytes: {len(payload)}",
        f"total_sectors: {total_sectors}",
        f"max_encoded_frame_bytes: {max_encoded}",
        f"max_runs_per_frame: {max_runs}",
        f"player_buffer: 0x{FRAME_BUFFER_ADDR:04X}..0x{FRAME_BUFFER_ADDR + slot_sectors * SECTOR_SIZE - 1:04X}",
        "",
        "frame format:",
        "  byte 0: run count",
        "  byte 1: flags / reserved",
        "  each run: column, row, byte count, data bytes",
        "",
        "frames:",
    ]
    for item in frame_infos:
        lines.append(
            f"  frame {item.index:03d}: source={item.source_index} runs={item.run_count} encoded={item.encoded_bytes} changed={item.changed_bytes} lit_pixels={item.lit_pixels}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an SD-backed delta-run OLED video payload and player.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("build/oled_video_sd_delta"))
    parser.add_argument("--out-asm", type=Path, default=Path("ASM/programs/oled_video_sd_delta_player/VIDEO_PLAYER.asm"))
    parser.add_argument("--video-bin", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--video-block", type=int, default=DEFAULT_VIDEO_BLOCK)
    parser.add_argument("--max-frames", type=int, default=24)
    parser.add_argument("--frame-step", type=int, default=2)
    parser.add_argument("--threshold", type=int, default=None, help="Black/white cutoff. Overrides grayscale mode when present.")
    parser.add_argument("--grayscale", action="store_true", help="Use quantized grayscale when --threshold is not present.")
    parser.add_argument("--gray-levels", "--levels", dest="gray_levels", type=int, default=4, help="Number of gray levels for grayscale mode, 2..16.")
    parser.add_argument("--fg", type=lambda s: int(s, 0), default=0x0F)
    parser.add_argument("--invert", action="store_true")
    parser.add_argument("--fit", choices=("stretch", "contain", "crop"), default="contain")
    parser.add_argument("--inset-x", type=int, default=0)
    parser.add_argument("--inset-y", type=int, default=0)
    parser.add_argument("--delay-calls", type=int, default=1)
    parser.add_argument("--slot-sectors", type=int, default=0, help="0 selects the smallest slot that fits every frame")
    parser.add_argument("--device", help=r"Raw block device, e.g. /dev/sdb or \\.\PhysicalDrive5")
    parser.add_argument("--windows-lock-volume", help="Optional Windows volume GUID lock, e.g. \\\\?\\Volume{...}\\")
    parser.add_argument("--ruledef", default="../../../../ruledef.asm")
    parser.add_argument("--constants", default="../../../../drivers/oled/oled_constants.asm")
    parser.add_argument("--lowlevel", default="../../../../drivers/oled/oled_lowlevel.asm")
    parser.add_argument("--text4", default="../../../../drivers/oled/oled_text_4x6.asm")
    parser.add_argument("--graphics", default="../../../../drivers/oled/oled_graphics.asm")
    parser.add_argument("--spi-routines", default="../../../../drivers/spi_sd/SPI_routines.asm")
    parser.add_argument("--spi-init", default="../../../../drivers/spi_sd/SPI_init.asm")
    parser.add_argument("--sd-block-io", default="../../../../drivers/spi_sd/sd_block_io.asm")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.frame_step < 1:
        raise SystemExit("--frame-step must be 1 or greater")
    if args.max_frames < 1 or args.max_frames > 255:
        raise SystemExit("--max-frames must be 1..255 for the generated player")
    if args.threshold is not None and not 0 <= args.threshold <= 255:
        raise SystemExit("--threshold must be 0..255")
    if args.gray_levels < 2 or args.gray_levels > 16:
        raise SystemExit("--gray-levels must be 2..16")
    if not 0 <= args.fg <= 15:
        raise SystemExit("--fg must be 0..15")
    if not 0 <= args.inset_x <= 63:
        raise SystemExit("--inset-x must be 0..63")
    if not 0 <= args.inset_y <= 31:
        raise SystemExit("--inset-y must be 0..31")
    if args.slot_sectors < 0 or args.slot_sectors > MAX_SLOT_SECTORS:
        raise SystemExit(f"--slot-sectors must be 0..{MAX_SLOT_SECTORS}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    video_bin = args.video_bin or (args.out_dir / "video_delta_frames.bin")
    manifest = args.manifest or (args.out_dir / "video_delta_manifest.txt")

    source_frames = load_frames(args.input)
    chosen = select_frames(source_frames, args.frame_step, args.max_frames)
    if not chosen:
        raise SystemExit("No frames selected")

    encoded_frames: List[bytes] = []
    infos: List[FrameInfo] = []
    previous = bytes(GROUPED_COLS * SAFE_HEIGHT)

    for out_index, (source_index, frame) in enumerate(chosen):
        nibbles = quantize_frame(frame, args)
        packed = pack_frame(nibbles)
        runs = frame_delta_runs(packed, previous)
        encoded = encode_runs(runs)
        encoded_frames.append(encoded)
        changed = sum(len(run.data) for run in runs)
        lit_pixels = sum(1 for value in nibbles if value)
        infos.append(FrameInfo(out_index, source_index, len(runs), len(encoded), changed, lit_pixels))
        previous = packed

    max_frame_bytes = max(len(frame) for frame in encoded_frames)
    if args.slot_sectors == 0:
        slot_sectors = max(1, math.ceil(max_frame_bytes / SECTOR_SIZE))
    else:
        slot_sectors = args.slot_sectors

    if slot_sectors > MAX_SLOT_SECTORS:
        raise SystemExit(
            f"Largest encoded frame needs {math.ceil(max_frame_bytes / SECTOR_SIZE)} sectors; max supported is {MAX_SLOT_SECTORS}. "
            "Use a higher threshold, larger frame step, fewer frames, or more inset."
        )

    slot_bytes = slot_sectors * SECTOR_SIZE
    too_large = [(i, len(frame)) for i, frame in enumerate(encoded_frames) if len(frame) > slot_bytes]
    if too_large:
        index, size = too_large[0]
        raise SystemExit(
            f"Frame {index} needs {size} bytes, but --slot-sectors {slot_sectors} gives {slot_bytes} bytes. "
            "Use more slot sectors or reduce frame complexity."
        )

    payload = bytearray()
    for frame in encoded_frames:
        payload.extend(frame)
        payload.extend(bytes(slot_bytes - len(frame)))

    video_bin.parent.mkdir(parents=True, exist_ok=True)
    video_bin.write_bytes(bytes(payload))

    args.out_asm.parent.mkdir(parents=True, exist_ok=True)
    args.out_asm.write_text(make_player_asm(args, len(infos), slot_sectors), encoding="utf-8")

    manifest.parent.mkdir(parents=True, exist_ok=True)
    write_manifest(manifest, args, infos, bytes(payload), slot_sectors)

    block_count = len(payload) // SECTOR_SIZE
    print(f"Wrote delta video binary: {video_bin}")
    print(f"Wrote delta player ASM:   {args.out_asm}")
    print(f"Wrote manifest:           {manifest}")
    print(f"Frames: {len(infos)}")
    print(f"Mode: {conversion_mode(args)}")
    if conversion_mode(args) == "threshold":
        print(f"Threshold: {effective_threshold(args)}")
    else:
        print(f"Gray levels: {args.gray_levels}")
    print(f"Slot sectors: {slot_sectors}")
    print(f"Total video sectors: {block_count}")
    print(f"Video start block: {args.video_block}")
    print(f"Largest encoded frame: {max_frame_bytes} bytes")
    print(f"Max runs per frame: {max(item.run_count for item in infos)}")

    if args.device:
        with lock_windows_volume(args.windows_lock_volume):
            write_blocks_to_device(args.device, args.video_block, bytes(payload))
            readback = read_blocks_from_device(args.device, args.video_block, block_count)
        print(f"Wrote {block_count} video sectors to {args.device} at block {args.video_block}")
        print(f"Video readback matches: {'yes' if readback == bytes(payload) else 'no'}")
        print("Video first 16 bytes: " + " ".join(f"{b:02X}" for b in payload[:16]))
        print("Video last 16 bytes:  " + " ".join(f"{b:02X}" for b in payload[-16:]))


if __name__ == "__main__":
    main()
