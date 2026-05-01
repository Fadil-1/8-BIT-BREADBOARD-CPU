#!/usr/bin/env python3
"""
Assembly deployment helper for the F8-BB breadboard CPU.

Assembles a CustomASM source file and deploys it either as:
  - a trimmed ROM payload
  - an SD-card payload

In SD mode, it automatically chooses between:
  - a one-sector path when the trimmed payload fits in 512 bytes
  - a BT1 multi-sector install path when the payload is larger

Original version: May 2026
Fadil Isamotu
"""

from __future__ import annotations

import argparse
import math
import pathlib
import re
import shutil
import subprocess
import sys
from typing import List, Optional


# Matches bytes written like 0x12 inside customasm hexcomma output.
HEX_BYTE_RE = re.compile(r"0x([0-9a-fA-F]{1,2})")

# Matches a source-level #addr directive so the script can auto-detect origin.
ADDR_RE = re.compile(r"^\s*#addr\s+(0x[0-9a-fA-F]+|\d+)\s*$", re.MULTILINE)

SECTOR_SIZE = 512
DEFAULT_DESCRIPTOR_BLOCK = 1002


def eprint(*args, **kwargs):
    # Convenience stderr print helper for user-facing errors.
    print(*args, file=sys.stderr, **kwargs)


def find_customasm() -> str:
    # Resolves customasm from PATH once, so the rest of the script can invoke it directly.
    exe = shutil.which("customasm")
    if not exe:
        raise FileNotFoundError(
            "customasm was not found on PATH. Install it or add it to PATH first."
        )
    return exe


def parse_int(s: str) -> int:
    # Accepts either decimal or 0x-prefixed integers.
    return int(s, 0)


def detect_origin_from_source(source_text: str) -> Optional[int]:
    # Reads the first #addr from the source file and uses it as the default trim origin.
    m = ADDR_RE.search(source_text)
    if not m:
        return None
    return parse_int(m.group(1))


def run_customasm(source: pathlib.Path, fmt: str) -> str:
    # Runs customasm in a requested output format and returns stdout.
    exe = find_customasm()
    cmd = [exe, str(source), "-f", fmt, "-p"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if not output:
        raise RuntimeError(f"customasm produced no stdout for format {fmt}")
    return result.stdout



def get_addrspan(source: pathlib.Path) -> tuple[int, int]:
    """
    Returns (start_addr, end_addr_exclusive) by parsing customasm annotated output.
    """
    # The annotated listing is used as the trusted way to recover the true occupied address span.
    text = run_customasm(source, "annotated")

    entries: list[tuple[int, int]] = []

    for line in text.splitlines():
        line = line.rstrip()

        if not line:
            continue
        if line.startswith("customasm") or line.startswith("assembling"):
            continue
        if line.startswith("resolved in"):
            continue
        if " | " not in line:
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue

        outp_field = parts[0]
        addr_field = parts[1]
        data_field = parts[2]

        if ":" not in outp_field:
            continue

        try:
            logical_addr = int(addr_field, 16)
        except ValueError:
            continue

        data_only = data_field.split(";")[0].strip()
        if not data_only:
            continue

        # Count how many output bytes appear on this annotated line.
        byte_tokens = re.findall(r"\b[0-9a-fA-F]{2}\b", data_only)
        if not byte_tokens:
            continue

        byte_count = len(byte_tokens)
        entries.append((logical_addr, byte_count))

    if not entries:
        raise RuntimeError(f"Could not parse annotated output for addr span:\n{text}")

    start_addr = entries[0][0]
    last_addr, last_size = entries[-1]
    end_exclusive = last_addr + last_size

    return start_addr, end_exclusive



def parse_hexcomma_output(text: str) -> List[int]:
    # Converts customasm hexcomma text into a plain list of byte values.
    values = [int(m.group(1), 16) for m in HEX_BYTE_RE.finditer(text)]
    if not values:
        raise ValueError("No hex bytes were found in customasm hexcomma output.")
    return values



def trim_from_origin(all_bytes: List[int], origin: int, end_exclusive: Optional[int] = None) -> List[int]:
    # Trims the assembled byte stream down to the occupied program region.
    if origin < 0:
        raise ValueError("Origin cannot be negative.")
    if origin >= len(all_bytes):
        raise ValueError(
            f"Trim origin 0x{origin:X} is beyond output length ({len(all_bytes)} bytes)."
        )

    if end_exclusive is None:
        return all_bytes[origin:]

    if end_exclusive <= origin:
        raise ValueError(
            f"End address 0x{end_exclusive:X} must be greater than origin 0x{origin:X}."
        )

    if end_exclusive > len(all_bytes):
        raise ValueError(
            f"End address 0x{end_exclusive:X} is beyond output length ({len(all_bytes)} bytes)."
        )

    return all_bytes[origin:end_exclusive]



def write_hexcomma_file(path: pathlib.Path, byte_values: List[int], columns: int = 16) -> None:
    # Writes bytes back out in the same comma-separated style used elsewhere in this workflow.
    lines = []
    for i in range(0, len(byte_values), columns):
        row = byte_values[i:i + columns]
        parts = []
        for j, b in enumerate(row):
            parts.append(f"0x{b:02x},")
            if j == 7 and j != len(row) - 1:
                parts.append(" ")
        lines.append(" ".join(parts))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def write_binary_file(path: pathlib.Path, byte_values: List[int]) -> None:
    # Writes a raw binary version of the same payload.
    path.write_bytes(bytes(byte_values))



def build_sector_payload(program_bytes: List[int], sector_size: int = SECTOR_SIZE) -> bytes:
    # Legacy single-sector SD path: payload must fit in exactly one 512-byte sector.
    if len(program_bytes) > sector_size:
        raise ValueError(
            f"Program is {len(program_bytes)} bytes, which does not fit in one {sector_size}-byte sector."
        )
    return bytes(program_bytes) + bytes(sector_size - len(program_bytes))



def pad_payload_to_sector_boundary(program_bytes: List[int], sector_size: int = SECTOR_SIZE) -> bytes:
    # Multi-sector SD path: payload is padded to a whole number of sectors.
    payload = bytes(program_bytes)
    padded_len = math.ceil(len(payload) / sector_size) * sector_size
    return payload + bytes(padded_len - len(payload))



def build_bt1_descriptor(payload_block: int, load_addr: int, block_count: int, flags: int = 0) -> bytes:
    # Builds one 512-byte BT1 boot descriptor sector.
    if not (0 <= payload_block <= 0xFFFFFFFF):
        raise ValueError("payload_block must fit in 32 bits")
    if not (0 <= load_addr <= 0xFFFF):
        raise ValueError("load_addr must fit in 16 bits")
    if not (0 <= block_count <= 0xFFFF):
        raise ValueError("block_count must fit in 16 bits")
    if not (0 <= flags <= 0xFF):
        raise ValueError("flags must fit in 8 bits")

    data = bytearray(SECTOR_SIZE)
    data[0] = 0x42
    data[1] = 0x54
    data[2] = 0x31
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



def write_sector_to_device(device: str, block_index: int, sector: bytes) -> None:
    # Writes exactly one 512-byte sector to the block device at the requested block offset.
    if len(sector) != SECTOR_SIZE:
        raise ValueError("Sector write currently expects exactly 512 bytes.")
    path = pathlib.Path(device)
    if not path.exists():
        raise FileNotFoundError(f"Device not found: {device}")
    offset = block_index * SECTOR_SIZE
    with open(path, "r+b", buffering=0) as f:
        f.seek(offset)
        f.write(sector)
        f.flush()



def write_blocks_to_device(device: str, start_block: int, payload: bytes, sector_size: int = SECTOR_SIZE) -> None:
    # Writes a whole multi-sector payload contiguously starting at start_block.
    if len(payload) % sector_size != 0:
        raise ValueError("Payload length must be a whole number of sectors.")
    path = pathlib.Path(device)
    if not path.exists():
        raise FileNotFoundError(f"Device not found: {device}")
    offset = start_block * sector_size
    with open(path, "r+b", buffering=0) as f:
        f.seek(offset)
        f.write(payload)
        f.flush()



def read_sector_from_device(device: str, block_index: int, sector_size: int = SECTOR_SIZE) -> bytes:
    # Reads exactly one sector back for verification.
    path = pathlib.Path(device)
    if not path.exists():
        raise FileNotFoundError(f"Device not found: {device}")
    offset = block_index * sector_size
    with open(path, "rb", buffering=0) as f:
        f.seek(offset)
        data = f.read(sector_size)
    if len(data) != sector_size:
        raise RuntimeError(f"Could not read full sector from {device} at block {block_index}.")
    return data



def read_blocks_from_device(device: str, start_block: int, block_count: int, sector_size: int = SECTOR_SIZE) -> bytes:
    # Reads a contiguous set of sectors back for verification.
    path = pathlib.Path(device)
    if not path.exists():
        raise FileNotFoundError(f"Device not found: {device}")
    total = block_count * sector_size
    offset = start_block * sector_size
    with open(path, "rb", buffering=0) as f:
        f.seek(offset)
        data = f.read(total)
    if len(data) != total:
        raise RuntimeError(
            f"Could not read {block_count} full sectors from {device} starting at block {start_block}."
        )
    return data



def format_byte_preview(data: bytes, count: int = 16) -> str:
    # Formats the first few bytes for manifest / console preview.
    return " ".join(f"{b:02X}" for b in data[:count])



def format_tail_preview(data: bytes, count: int = 16) -> str:
    # Formats the last few bytes for manifest / console preview.
    return " ".join(f"{b:02X}" for b in data[-count:])



def save_annotated_if_requested(source: pathlib.Path, dump_annotated: bool, out_dir: pathlib.Path) -> Optional[pathlib.Path]:
    # Saves customasm annotated listing only when explicitly requested.
    if not dump_annotated:
        return None
    annotated_text = run_customasm(source, "annotated")
    out_path = out_dir / f"{source.stem}_annotated.txt"
    out_path.write_text(annotated_text, encoding="utf-8")
    return out_path



def write_manifest(path: pathlib.Path, fields: dict[str, str]) -> None:
    # Simple key:value manifest for later traceability.
    lines = [f"{k}: {v}" for k, v in fields.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def rom_mode(args: argparse.Namespace) -> int:
    # ROM mode: assemble, trim to occupied span, then write hex and binary outputs.
    source = pathlib.Path(args.source)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    source_text = source.read_text(encoding="utf-8")
    origin = parse_int(args.origin) if args.origin else detect_origin_from_source(source_text)
    if origin is None:
        raise ValueError("Could not detect #addr in source. Supply --origin explicitly.")

    hexcomma_text = run_customasm(source, "hexcomma")
    all_bytes = parse_hexcomma_output(hexcomma_text)
    span_start, span_end = get_addrspan(source)
    print(f"Program addrspan: 0x{span_start:04X}..0x{span_end:04X}")

    trimmed = trim_from_origin(all_bytes, origin, span_end)

    hex_out = pathlib.Path(args.out) if args.out else out_dir / f"{source.stem}_trimmed_hex.txt"
    bin_out = out_dir / f"{source.stem}_trimmed.bin"
    manifest_out = out_dir / f"{source.stem}_manifest.txt"

    write_hexcomma_file(hex_out, trimmed)
    write_binary_file(bin_out, trimmed)
    annotated_path = save_annotated_if_requested(source, args.dump_annotated, out_dir)

    manifest = {
        "mode": "rom",
        "source": str(source.resolve()),
        "origin_hex": f"0x{origin:04X}",
        "origin_dec": str(origin),
        "trimmed_byte_count": str(len(trimmed)),
        "trimmed_hex_output": str(hex_out.resolve()),
        "trimmed_binary_output": str(bin_out.resolve()),
        "annotated_output": str(annotated_path.resolve()) if annotated_path else "not requested",
    }
    write_manifest(manifest_out, manifest)

    print(f"ROM origin: 0x{origin:04X}")
    print(f"Trimmed ROM byte count: {len(trimmed)}")
    print(f"Trimmed hex output: {hex_out}")
    print(f"Trimmed binary output: {bin_out}")
    print(f"Manifest output: {manifest_out}")
    if annotated_path:
        print(f"Annotated output: {annotated_path}")
    return 0



def sd_mode(args: argparse.Namespace) -> int:
    # SD mode: assemble, trim, then choose single-sector or multi-sector install automatically.
    source = pathlib.Path(args.source)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    source_text = source.read_text(encoding="utf-8")
    origin = parse_int(args.origin) if args.origin else detect_origin_from_source(source_text)
    if origin is None:
        raise ValueError("Could not detect #addr in source. Supply --origin explicitly.")

    hexcomma_text = run_customasm(source, "hexcomma")
    all_bytes = parse_hexcomma_output(hexcomma_text)
    span_start, span_end = get_addrspan(source)
    print(f"Program addrspan: 0x{span_start:04X}..0x{span_end:04X}")

    if origin < span_start:
        raise ValueError(
            f"Requested SD origin 0x{origin:X} is before the program start 0x{span_start:X}."
        )

    trimmed = trim_from_origin(all_bytes, origin, span_end)
    block_count = math.ceil(len(trimmed) / SECTOR_SIZE)
    is_multisector = block_count > 1
    load_addr = parse_int(args.load_addr) if args.load_addr else origin
    descriptor_block = parse_int(args.descriptor_block) if args.descriptor_block else DEFAULT_DESCRIPTOR_BLOCK

    trimmed_hex_out = out_dir / f"{source.stem}_sd_trimmed_hex.txt"
    trimmed_bin_out = out_dir / f"{source.stem}_sd_trimmed.bin"
    manifest_out = out_dir / f"{source.stem}_manifest.txt"
    annotated_path = save_annotated_if_requested(source, args.dump_annotated, out_dir)

    write_hexcomma_file(trimmed_hex_out, trimmed)
    write_binary_file(trimmed_bin_out, trimmed)

    block_value = args.block if args.block is not None else "not written"
    device_value = args.device if args.device is not None else "not written"

    legacy_sector_out: Optional[pathlib.Path] = None
    padded_payload_out: Optional[pathlib.Path] = None
    descriptor_out: Optional[pathlib.Path] = None
    readback_match = "not checked"
    readback_first16 = "not checked"
    readback_last16 = "not checked"
    descriptor_readback_match = "not checked"
    descriptor_first16 = "not checked"

    print(f"SD payload origin: 0x{origin:04X}")
    print(f"Program byte count before sector padding: {len(trimmed)}")
    print(f"Sector count: {block_count}")
    print(f"Trimmed hex output: {trimmed_hex_out}")
    print(f"Trimmed binary output: {trimmed_bin_out}")
    if annotated_path:
        print(f"Annotated output: {annotated_path}")

    if not is_multisector:
        # Legacy path: build exactly one padded 512-byte sector.
        sector = build_sector_payload(trimmed, sector_size=SECTOR_SIZE)
        legacy_sector_out = pathlib.Path(args.sector_out) if args.sector_out else out_dir / f"{source.stem}_sector.bin"
        legacy_sector_out.write_bytes(sector)
        print(f"Sector file: {legacy_sector_out}")

        if args.device is not None:
            if args.block is None:
                raise ValueError("--device requires --block.")
            block_index = parse_int(args.block)
            write_sector_to_device(args.device, block_index, sector)
            print(f"Wrote sector to {args.device} at block {block_index}")
            readback = read_sector_from_device(args.device, block_index, sector_size=SECTOR_SIZE)
            readback_match = "yes" if readback == sector else "no"
            readback_first16 = format_byte_preview(readback, 16)
            readback_last16 = format_tail_preview(readback, 16)
            print(f"Readback matches written sector: {readback_match}")
            print(f"Readback first 16 bytes: {readback_first16}")
            print(f"Readback last 16 bytes:  {readback_last16}")
    else:
        # Multi-sector path: build padded payload + BT1 descriptor.
        if args.block is None:
            raise ValueError("Multi-sector SD mode requires --block for the payload start block.")
        payload_block = parse_int(args.block)
        padded_payload = pad_payload_to_sector_boundary(trimmed, sector_size=SECTOR_SIZE)
        padded_payload_out = out_dir / f"{source.stem}_payload_padded.bin"
        padded_payload_out.write_bytes(padded_payload)
        descriptor = build_bt1_descriptor(payload_block, load_addr, block_count)
        descriptor_out = out_dir / f"{source.stem}_bootdesc_bt1.bin"
        descriptor_out.write_bytes(descriptor)

        print(f"Multi-sector payload file: {padded_payload_out}")
        print(f"BT1 descriptor file: {descriptor_out}")
        print(f"Payload start block: {payload_block}")
        print(f"Descriptor block: {descriptor_block}")
        print(f"Load / entry address: 0x{load_addr:04X}")

        if args.device is not None:
            write_blocks_to_device(args.device, payload_block, padded_payload, sector_size=SECTOR_SIZE)
            print(f"Wrote {block_count} sectors to {args.device} starting at block {payload_block}")
            payload_readback = read_blocks_from_device(args.device, payload_block, block_count, sector_size=SECTOR_SIZE)
            readback_match = "yes" if payload_readback == padded_payload else "no"
            readback_first16 = format_byte_preview(payload_readback, 16)
            readback_last16 = format_tail_preview(payload_readback, 16)
            print(f"Payload readback matches: {readback_match}")
            print(f"Payload first 16 bytes: {readback_first16}")
            print(f"Payload last 16 bytes:  {readback_last16}")

            write_sector_to_device(args.device, descriptor_block, descriptor)
            print(f"Wrote descriptor to {args.device} at block {descriptor_block}")
            descriptor_readback = read_sector_from_device(args.device, descriptor_block, sector_size=SECTOR_SIZE)
            descriptor_readback_match = "yes" if descriptor_readback == descriptor else "no"
            descriptor_first16 = format_byte_preview(descriptor_readback, 16)
            print(f"Descriptor readback matches: {descriptor_readback_match}")
            print(f"Descriptor first 16 bytes: {descriptor_first16}")

    manifest = {
        "mode": "sd",
        "source": str(source.resolve()),
        "origin_hex": f"0x{origin:04X}",
        "origin_dec": str(origin),
        "trimmed_byte_count": str(len(trimmed)),
        "sector_size": str(SECTOR_SIZE),
        "sector_count": str(block_count),
        "install_mode": "multi-sector" if is_multisector else "single-sector",
        "trimmed_hex_output": str(trimmed_hex_out.resolve()),
        "trimmed_binary_output": str(trimmed_bin_out.resolve()),
        "sector_output": str(legacy_sector_out.resolve()) if legacy_sector_out else "not used",
        "padded_payload_output": str(padded_payload_out.resolve()) if padded_payload_out else "not used",
        "descriptor_output": str(descriptor_out.resolve()) if descriptor_out else "not used",
        "annotated_output": str(annotated_path.resolve()) if annotated_path else "not requested",
        "device": device_value,
        "block": block_value,
        "load_address": f"0x{load_addr:04X}",
        "descriptor_block": str(descriptor_block),
        "payload_readback_match": readback_match,
        "payload_readback_first_16_bytes": readback_first16,
        "payload_readback_last_16_bytes": readback_last16,
        "descriptor_readback_match": descriptor_readback_match,
        "descriptor_readback_first_16_bytes": descriptor_first16,
    }

    write_manifest(manifest_out, manifest)
    print(f"Manifest output: {manifest_out}")
    return 0



def build_parser() -> argparse.ArgumentParser:
    # CLI layout:
    #   deploy_asm.py rom ...
    #   deploy_asm.py sd  ...
    parser = argparse.ArgumentParser(
        description="Assemble and deploy customasm programs for ROM or SD-card use."
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # Shared arguments used by both rom and sd subcommands.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("source", help="Assembly source file")
    common.add_argument(
        "--origin",
        help="Trim origin address, like 0xC000 or 0x0200. Defaults to the first #addr in the source.",
    )
    common.add_argument(
        "--out-dir",
        default="build",
        help="Directory for generated outputs (default: build)",
    )
    common.add_argument(
        "--dump-annotated",
        action="store_true",
        help="Also save customasm annotated output",
    )

    rom = sub.add_parser("rom", parents=[common], help="Build trimmed ROM payload")
    rom.add_argument(
        "--out",
        help="Path for trimmed ROM hexcomma text output. Default: build/<stem>_trimmed_hex.txt",
    )

    sd = sub.add_parser("sd", parents=[common], help="Build SD payload and auto-select single-sector or multi-sector install path")
    sd.add_argument(
        "--sector-out",
        help="Path for legacy single-sector 512-byte sector file. Default: build/<stem>_sector.bin",
    )
    sd.add_argument(
        "--device",
        help="Optional block device path, e.g. /dev/mmcblk0",
    )
    sd.add_argument(
        "--block",
        help="Payload start block to write when --device is used, e.g. 1003",
    )
    sd.add_argument(
        "--descriptor-block",
        default=str(DEFAULT_DESCRIPTOR_BLOCK),
        help=f"Descriptor block for automatic BT1 multi-sector installs (default: {DEFAULT_DESCRIPTOR_BLOCK})",
    )
    sd.add_argument(
        "--load-addr",
        help="Descriptor load address for automatic BT1 multi-sector installs. Defaults to --origin.",
    )

    return parser



def main() -> int:
    # Top-level dispatcher with user-friendly error reporting.
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.mode == "rom":
            return rom_mode(args)
        if args.mode == "sd":
            return sd_mode(args)
        raise ValueError(f"Unknown mode: {args.mode}")
    except subprocess.CalledProcessError as e:
        eprint("customasm failed.")
        if e.stdout:
            eprint(e.stdout)
        if e.stderr:
            eprint(e.stderr)
        return 1
    except Exception as e:
        eprint(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())