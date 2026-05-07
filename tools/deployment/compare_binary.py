#!/usr/bin/env python3
"""
Binary file comparison helper for the F8-BB breadboard CPU.

Compares two files byte-for-byte and reports whether they match. When the
files differ, the script reports the first differing byte offset.

Exit status:
  0 = files match
  1 = files differ
  2 = error
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys


DEFAULT_CHUNK_SIZE = 1024 * 1024


def eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def parse_positive_int(value: str) -> int:
    try:
        parsed = int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value}") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")

    return parsed


def validate_file(path: pathlib.Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Path is not a regular file: {path}")


def sha256_file(path: pathlib.Path, chunk_size: int = DEFAULT_CHUNK_SIZE) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def byte_at(path: pathlib.Path, offset: int) -> int | None:
    with path.open("rb") as file:
        file.seek(offset)
        data = file.read(1)

    if not data:
        return None

    return data[0]


def find_first_mismatch(
    file_a: pathlib.Path,
    file_b: pathlib.Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> int | None:
    offset = 0

    with file_a.open("rb") as a, file_b.open("rb") as b:
        while True:
            chunk_a = a.read(chunk_size)
            chunk_b = b.read(chunk_size)

            if chunk_a != chunk_b:
                common_length = min(len(chunk_a), len(chunk_b))

                for i in range(common_length):
                    if chunk_a[i] != chunk_b[i]:
                        return offset + i

                return offset + common_length

            if not chunk_a:
                return None

            offset += len(chunk_a)


def compare_files(
    file_a: pathlib.Path,
    file_b: pathlib.Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> tuple[bool, int | None]:
    size_a = file_a.stat().st_size
    size_b = file_b.stat().st_size

    mismatch_offset = find_first_mismatch(file_a, file_b, chunk_size)

    return size_a == size_b and mismatch_offset is None, mismatch_offset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two binary files byte-for-byte."
    )
    parser.add_argument("file_a", help="First file to compare")
    parser.add_argument("file_b", help="Second file to compare")
    parser.add_argument(
        "--chunk-size",
        type=parse_positive_int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Read chunk size in bytes (default: {DEFAULT_CHUNK_SIZE})",
    )
    parser.add_argument(
        "--sha256",
        action="store_true",
        help="Print SHA-256 hashes for both files",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only return the exit status",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    file_a = pathlib.Path(args.file_a)
    file_b = pathlib.Path(args.file_b)

    try:
        validate_file(file_a)
        validate_file(file_b)

        size_a = file_a.stat().st_size
        size_b = file_b.stat().st_size
        match, mismatch_offset = compare_files(file_a, file_b, args.chunk_size)

        if args.quiet:
            return 0 if match else 1

        print(f"File A: {file_a}")
        print(f"File B: {file_b}")
        print(f"Size A: {size_a} bytes")
        print(f"Size B: {size_b} bytes")

        if args.sha256:
            print(f"SHA-256 A: {sha256_file(file_a, args.chunk_size)}")
            print(f"SHA-256 B: {sha256_file(file_b, args.chunk_size)}")

        if match:
            print("Result: files match exactly.")
            return 0

        print("Result: files differ.")

        if mismatch_offset is not None:
            print(
                f"First mismatch: byte {mismatch_offset} "
                f"(0x{mismatch_offset:X})"
            )

            value_a = byte_at(file_a, mismatch_offset)
            value_b = byte_at(file_b, mismatch_offset)

            value_a_text = "EOF" if value_a is None else f"0x{value_a:02X}"
            value_b_text = "EOF" if value_b is None else f"0x{value_b:02X}"

            print(f"File A byte: {value_a_text}")
            print(f"File B byte: {value_b_text}")

        return 1

    except Exception as exc:
        if not args.quiet:
            eprint(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())