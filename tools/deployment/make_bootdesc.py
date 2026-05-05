#!/usr/bin/env python3
"""
BT1 boot descriptor generator for the F8-BB breadboard CPU.

Creates a 512-byte BT1 descriptor sector for the SD bootstrap flow.

Original version: May 2026
Fadil Isamotu
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.wintypes as wintypes
import os
from contextlib import nullcontext
import pathlib
import sys


def parse_int(value: str) -> int:
    return int(value, 0)


def format_preview(data: bytes, count: int = 16) -> str:
    return " ".join(f"{b:02X}" for b in data[:count])


def build_descriptor(payload_block: int, load_addr: int, block_count: int, flags: int = 0) -> bytes:
    if not (0 <= payload_block <= 0xFFFFFFFF):
        raise ValueError("payload_block must fit in 32 bits")
    if not (0 <= load_addr <= 0xFFFF):
        raise ValueError("load_addr must fit in 16 bits")
    if not (0 <= block_count <= 0xFFFF):
        raise ValueError("block_count must fit in 16 bits")
    if not (0 <= flags <= 0xFF):
        raise ValueError("flags must fit in 8 bits")

    data = bytearray(512)
    data[0] = 0x42  # 'B'
    data[1] = 0x54  # 'T'
    data[2] = 0x31  # version 1
    data[3] = flags & 0xFF

    data[4] = (payload_block >> 24) & 0xFF
    data[5] = (payload_block >> 16) & 0xFF
    data[6] = (payload_block >> 8) & 0xFF
    data[7] = payload_block & 0xFF

    data[8] = (load_addr >> 8) & 0xFF
    data[9] = load_addr & 0xFF

    data[10] = (block_count >> 8) & 0xFF
    data[11] = block_count & 0xFF

    return bytes(data)


def write_file(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


class WindowsRawDevice:
    # Small file-style wrapper for Windows raw disk HANDLE objects.
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080

    def __init__(self, device: str, mode: str):
        self.device = device
        self.mode = mode
        self.handle = None
        self.writable = any(ch in mode for ch in "+wa")

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
        kernel32.SetFilePointerEx.argtypes = [
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        ]
        kernel32.SetFilePointerEx.restype = wintypes.BOOL
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
            raise ValueError("Raw block-device reads require an explicit byte count.")

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
            total += bytes_written.value
            if bytes_written.value != len(chunk):
                raise OSError(f"Short write to {self.device}")
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
    # Windows volume lock remains open during raw disk access.
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


def lock_windows_volume(volume: str | None):
    if volume is None:
        return nullcontext()
    if os.name != "nt":
        raise ValueError("--windows-lock-volume is only supported on Windows.")
    return WindowsVolumeLock(volume)


def is_windows_raw_device(device: str) -> bool:
    windows_raw_prefix = "\\\\.\\"
    return os.name == "nt" and device.startswith(windows_raw_prefix)


def open_block_device(device: str, mode: str):
    # Block-device access uses POSIX file paths on Linux and Win32 handles for Windows raw disks.
    if is_windows_raw_device(device):
        return WindowsRawDevice(device, mode)
    return open(device, mode, buffering=0)



def write_sector_to_device(device: str, block_index: int, sector: bytes) -> None:
    if len(sector) != 512:
        raise ValueError("Sector must be exactly 512 bytes.")

    with open_block_device(device, "r+b") as f:
        f.seek(block_index * 512)
        f.write(sector)


def read_sector_from_device(device: str, block_index: int) -> bytes:
    with open_block_device(device, "rb") as f:
        f.seek(block_index * 512)
        data = f.read(512)
    if len(data) != 512:
        raise RuntimeError(f"Could not read full 512-byte sector from {device} block {block_index}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a BT1 boot descriptor sector file.")
    parser.add_argument("--payload-block", required=True, type=parse_int, help="Payload block number, e.g. 1003 or 0x3EB")
    parser.add_argument("--load-addr", required=True, type=parse_int, help="Payload load address, e.g. 0x0200")
    parser.add_argument("--block-count", required=True, type=parse_int, help="Number of payload blocks, e.g. 1")
    parser.add_argument("--flags", default="0", type=parse_int, help="Descriptor flags byte, default 0")
    parser.add_argument("--out", default="bootdesc_v1.bin", help="Output descriptor file path")
    parser.add_argument("--device", help=r"Optional raw block device, e.g. /dev/mmcblk0 or \\.\PhysicalDrive5")
    parser.add_argument(
        "--windows-lock-volume",
        help=r"Optional Windows volume GUID to lock during direct raw-disk writes, e.g. \\?\Volume{...}",
    )
    parser.add_argument("--descriptor-block", default="1002", type=parse_int, help="SD block to write descriptor to, default 1002")
    parser.add_argument("--verify-readback", action="store_true", help="Read the descriptor block back and compare it")

    args = parser.parse_args()

    out_path = pathlib.Path(args.out)
    descriptor = build_descriptor(
        payload_block=args.payload_block,
        load_addr=args.load_addr,
        block_count=args.block_count,
        flags=args.flags,
    )

    write_file(out_path, descriptor)

    print(f"Wrote descriptor file: {out_path}")
    print(f"Payload block: {args.payload_block} (0x{args.payload_block:08X})")
    print(f"Load address:  0x{args.load_addr:04X}")
    print(f"Block count:   {args.block_count}")
    print(f"First 16 bytes: {format_preview(descriptor, 16)}")

    if args.windows_lock_volume and not args.device:
        raise ValueError("--windows-lock-volume requires --device.")

    if args.device:
        with lock_windows_volume(args.windows_lock_volume):
            write_sector_to_device(args.device, args.descriptor_block, descriptor)
            print(f"Wrote descriptor to {args.device} at block {args.descriptor_block}")

            if args.verify_readback:
                readback = read_sector_from_device(args.device, args.descriptor_block)
        if args.verify_readback:
            matches = readback == descriptor
            print(f"Readback matches: {'yes' if matches else 'no'}")
            print(f"Readback first 16 bytes: {format_preview(readback, 16)}")
            if not matches:
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
