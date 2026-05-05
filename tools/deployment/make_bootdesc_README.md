# make_bootdesc.py

`make_bootdesc.py` creates the 512-byte `BT1` boot descriptor sector used by the ROM bootstrap.

## What it is for

The bootloader-only ROM version of my F8-BB CPU does **not** directly hardcode the stage-2 payload block.

Instead:

- the ROM always reads the descriptor from SD block `1002`
- the descriptor tells the ROM which payload block to load
- the ROM then loads that payload into RAM at `0x0200` and jumps there

The script creates that descriptor sector file.

## Basic usage

Create a descriptor file that points to payload block `1003`:

```bash
python3 make_bootdesc.py --payload-block 1003 --load-addr 0x0200 --block-count 1 --out bootdesc_v1.bin
```

## Write directly to the SD card

Linux example:

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

Windows PowerShell example:

```powershell
python make_bootdesc.py `
    --payload-block 1003 `
    --load-addr 0x0200 `
    --block-count 1 `
    --out bootdesc_v1.bin `
    --device "\\.\PhysicalDrive5" `
    --descriptor-block 1002 `
    --verify-readback
```

If Windows requires a volume lock, add `--windows-lock-volume`:

```powershell
python make_bootdesc.py `
    --payload-block 1003 `
    --load-addr 0x0200 `
    --block-count 1 `
    --out bootdesc_v1.bin `
    --device "\\.\PhysicalDrive5" `
    --windows-lock-volume "\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\" `
    --descriptor-block 1002 `
    --verify-readback
```

Run PowerShell as Administrator for a direct SD-card write.

## Find the SD device name

On Linux, use one of these commands before and after card insertion:

```bash
lsblk
sudo fdisk -l
```

Common Linux raw device names include `/dev/mmcblk0` and `/dev/sdb`. Use the whole-card device, not a partition such as `/dev/sdb1`.

On Windows PowerShell, run:

```powershell
Get-Disk
```

If the card has drive letter `E:`, map that letter back to the disk number:

```powershell
Get-Partition -DriveLetter E | Get-Disk | Format-List Number,FriendlyName,BusType,Size,PartitionStyle
```

If the card appears as disk `5`, use this raw device path:

```text
\\.\PhysicalDrive5
```

Do not use `E:` for descriptor block writes. The descriptor block is a raw SD-card sector.

If Windows blocks the raw disk write, find the volume GUID for the SD card:

```powershell
Get-CimInstance Win32_Volume | Select-Object DriveLetter, Label, FileSystem, Capacity, DeviceID
```

The SD-card volume should match the card size. For a 32 GB card, Windows often reports about `29.1 GB`. A volume GUID looks like:

```text
\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\
```

Use that GUID with `--windows-lock-volume` when Windows rejects the direct `\\.\PhysicalDriveN` write.

## Manual write alternative

If you only create the file and want to write it manually on Linux:

```bash
sudo dd if=bootdesc_v1.bin of=/dev/mmcblk0 bs=512 seek=1002 conv=notrunc status=progress
sync
```

Manual descriptor write on Windows PowerShell:

```powershell
python -c "dev=r'\\.\PhysicalDrive5'; data=open('bootdesc_v1.bin','rb').read(); f=open(dev,'r+b',buffering=0); f.seek(1002*512); f.write(data); f.close()"
```

On Windows systems that block normal raw-device file access, use the script path with `--windows-lock-volume` instead.

## Verify manually

Linux:

```bash
sudo dd if=/dev/mmcblk0 of=readback_bootdesc.bin bs=512 skip=1002 count=1 status=progress
xxd -g 1 readback_bootdesc.bin | head
```

Windows PowerShell:

```powershell
python -c "dev=r'\\.\PhysicalDrive5'; f=open(dev,'rb',buffering=0); f.seek(1002*512); data=f.read(512); f.close(); open('readback_bootdesc.bin','wb').write(data)"
Format-Hex .\readback_bootdesc.bin | Select-Object -First 2
fc.exe /b bootdesc_v1.bin readback_bootdesc.bin
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

The script is generic enough that later I can point the descriptor at:

- a different payload block
- a different load address
- multiple payload blocks

without changing the ROM bootstrap format right away.


### `[Errno 5] Access is denied` on Windows

Run PowerShell as Administrator first. If the SD card is not read-only and Windows still rejects `\\.\PhysicalDriveN`, find the SD-card volume GUID:

```powershell
Get-CimInstance Win32_Volume | Select-Object DriveLetter, Label, FileSystem, Capacity, DeviceID
```

Then add `--windows-lock-volume` to the command:

```powershell
python make_bootdesc.py --payload-block 1003 --load-addr 0x0200 --block-count 1 --out bootdesc_v1.bin --device "\\.\PhysicalDrive5" --windows-lock-volume "\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\" --descriptor-block 1002 --verify-readback
```

Do not use a Linux partition or Google Drive volume GUID. Match the SD-card size before the write.

### `[Errno 9] Bad file descriptor` on Windows

Use the Windows-compatible script version for direct raw-disk writes. Windows raw disk paths such as `\\.\PhysicalDrive5` use the Win32 device API inside the script.

Run PowerShell as Administrator. If the card has drive letter `E:`, close File Explorer windows pointed at the card or dismount the volume first:

```powershell
Dismount-Volume -DriveLetter E -Force
```
