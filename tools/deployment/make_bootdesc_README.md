# make_bootdesc.py

`make_bootdesc.py` creates the 512-byte `BT1` boot descriptor sector used by the ROM bootstrap.

## What it is for

The bootloader-only ROM version of my F8-BB CPU does **not** directly hardcode the stage-2 payload block.

Instead:

- the ROM always reads the descriptor from SD block `1002`
- the descriptor tells the ROM which payload block to load
- the ROM then loads that payload into RAM at `0x0200` and jumps there

This script creates that descriptor sector file.

## Basic usage

Create a descriptor file that points to payload block `1003`:

```bash
python3 make_bootdesc.py --payload-block 1003 --load-addr 0x0200 --block-count 1 --out bootdesc_v1.bin
```

## Write directly to the SD card

```bash
sudo env "PATH=$PATH" python3 make_bootdesc.py \
    --payload-block 1003 \
    --load-addr 0x0200 \
    --block-count 1 \
    --out bootdesc_v1.bin \
    --device /dev/mmcblk0 \
    --descriptor-block 1002 \
    --verify-readback
```

## Manual write alternative

If you only create the file and want to write it manually:

```bash
sudo dd if=bootdesc_v1.bin of=/dev/mmcblk0 bs=512 seek=1002 conv=notrunc status=progress
sync
```

## Verify manually

```bash
sudo dd if=/dev/mmcblk0 of=readback_bootdesc.bin bs=512 skip=1002 count=1 status=progress
xxd -g 1 readback_bootdesc.bin | head
```

Expected beginning for the current baseline:

```text
42 54 31 00 00 00 03 EB 02 00 00 01
```

Meaning:

- `42 54 31` = `BT1`
- payload block = `1003`
- load address = `0x0200`
- block count = `1`

## Current assumptions

For the current ROM bootstrap baseline:

- descriptor block = `1002`
- payload block = `1003`
- payload load address = `0x0200`
- block count = `1`

## Future use

This script is intentionally generic enough that later I can point the descriptor at:

- a different payload block
- a different load address
- multiple payload blocks

without changing the ROM bootstrap format right away.
