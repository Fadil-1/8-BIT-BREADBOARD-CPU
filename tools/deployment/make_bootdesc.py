#!/usr/bin/env python3
"""
BT1 boot descriptor generator for the F8-BB breadboard CPU.

Creates a 512-byte BT1 descriptor sector for the SD bootstrap flow.

Original version: May 2026
Fadil Isamotu
"""

from __future__ import annotations

import argparse
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


def write_sector_to_device(device: str, block_index: int, sector: bytes) -> None:
    if len(sector) != 512:
        raise ValueError("Sector must be exactly 512 bytes.")

    with open(device, "r+b", buffering=0) as f:
        f.seek(block_index * 512)
        f.write(sector)
        f.flush()


def read_sector_from_device(device: str, block_index: int) -> bytes:
    with open(device, "rb", buffering=0) as f:
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
    parser.add_argument("--device", help="Optional raw block device, e.g. /dev/mmcblk0")
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

    if args.device:
        write_sector_to_device(args.device, args.descriptor_block, descriptor)
        print(f"Wrote descriptor to {args.device} at block {args.descriptor_block}")

        if args.verify_readback:
            readback = read_sector_from_device(args.device, args.descriptor_block)
            matches = readback == descriptor
            print(f"Readback matches: {'yes' if matches else 'no'}")
            print(f"Readback first 16 bytes: {format_preview(readback, 16)}")
            if not matches:
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
