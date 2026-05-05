# deploy_asm.py

`deploy_asm.py` is a helper script for my F8-BB workflow.


It automates two different build paths:

1. **ROM builds**: assemble a ROM-side program, trim the output from the ROM origin address, and generate programmer-friendly output files.
2. **SD builds**: assemble a RAM-targeted payload program, trim the output from the RAM execution address, and package it for SD deployment.

In SD mode, the script automatically chooses between:

- a **single-sector install path** when the trimmed payload fits in one 512-byte sector
- a **BT1 multi-sector install path** when the trimmed payload is larger than one sector

The workflow assumes:

- ROM code typically starts at `0xC000`
- RAM-loaded payloads typically start at addresses like `0x0200`
- `customasm` is used as the assembler
- SD cards are accessed as raw block devices such as `/dev/mmcblk0` on Linux or `\\.\PhysicalDrive5` on Windows

---

## What the script does

For both ROM and SD modes, the script:

- runs `customasm`
- determines the actual used address span of the assembled program
- trims the output from the requested origin
- saves useful build artifacts
- optionally saves an annotated assembly listing
- writes a manifest file for traceability

### In ROM mode

The script:

- assembles the source file
- trims the generated image from the ROM origin
- saves a formatted hex text file
- saves a raw binary file
- saves an optional annotated listing
- saves a manifest file

### In SD mode

The script:

- assembles the source file
- trims the generated image from the RAM payload origin
- saves a formatted trimmed hex file
- saves a trimmed binary file
- saves an optional annotated listing
- saves a manifest file
- automatically chooses between:
  - a single 512-byte sector image if the trimmed payload fits in one sector
  - a padded multi-sector payload plus a BT1 descriptor if the trimmed payload is larger than one sector
- optionally writes the payload directly to a raw SD device
- optionally reads the written payload back and reports whether it matched exactly
- in multi-sector mode, optionally writes the BT1 descriptor sector and verifies that as well

---

## Requirements

You need:

- Python 3
- `customasm` available on your shell `PATH`
- permission to access the SD block device when using direct writes
- the script file itself: `deploy_asm.py`

### Check that `customasm` is available

Run:

```bash
which customasm
```

If that prints a path, you are good.

You can also check the version:

```bash
customasm --version
```

On Windows PowerShell, use:

```powershell
where.exe customasm
customasm --version
```

---

## Basic usage

The script has two modes:

- `rom`
- `sd`

General form:

```bash
python3 deploy_asm.py <mode> <source.asm> [options]
```

---

## ROM mode

Use ROM mode for code that will be burned into the ROM chip.

### Example

```bash
python3 deploy_asm.py rom sd_bootstrap_v2_multi_sector.asm --origin 0xC000 --dump-annotated
```

### What this does

- assembles `sd_bootstrap_v2_multi_sector.asm`
- trims the build from `0xC000`
- writes output files into the `build/` directory
- generates an annotated listing if requested

### Typical ROM outputs

For `sd_bootstrap_v2_multi_sector.asm`, the script produces files like:

- `build/sd_bootstrap_v2_multi_sector_trimmed_hex.txt`
- `build/sd_bootstrap_v2_multi_sector_trimmed.bin`
- `build/sd_bootstrap_v2_multi_sector_annotated.txt`
- `build/sd_bootstrap_v2_multi_sector_manifest.txt`

### When to use the ROM hex file

Use the trimmed hex file if your ROM programmer expects comma-separated hex bytes(Like in the Ben Eater Arduino-based programmer).

### When to use the ROM binary file

Use the trimmed binary file if your programmer expects raw binary bytes.

---

## SD mode

Use SD mode for code that is meant to be loaded into RAM by the ROM loader.

The SD path supports both:

- **single-sector payloads**
- **multi-sector BT1 payloads**

The script decides automatically based on the trimmed byte count.

### Single-sector build without direct device write

```bash
python3 deploy_asm.py sd ram_test_program.asm --origin 0x0200 --dump-annotated
```

The command assembles the RAM payload and creates the needed output files in `build/`, but it will not write anything to the card.

For a single-sector payload, it produces a padded 512-byte sector file named like:

```text
build/ram_test_program_sector.bin
```

### Single-sector build with direct device write

```bash
sudo env "PATH=$PATH" python3 deploy_asm.py sd ram_test_program.asm --origin 0x0200 --device /dev/mmcblk0 --block 1003 --dump-annotated
```

The command assembles the RAM payload, writes one padded 512-byte sector to block `1003`, and reads that block back to verify the write.

### Multi-sector build without direct device write

```bash
python3 deploy_asm.py sd stage2_monitor.asm --origin 0x0200 --block 1003 --descriptor-block 1002 --dump-annotated
```

For a multi-sector payload, `--block` is required because the BT1 descriptor needs to record the payload start block.

The command creates:

- a padded payload file
- a BT1 descriptor file
- trimmed hex and binary payload files
- an optional annotated listing
- a manifest file

No card write occurs unless `--device` is also provided.

### Multi-sector build with direct device write

```bash
sudo env "PATH=$PATH" python3 deploy_asm.py sd stage2_monitor.asm --origin 0x0200 --device /dev/mmcblk0 --block 1003 --descriptor-block 1002 --dump-annotated
```

The command assembles the RAM payload and then:

- writes the padded payload starting at block `1003`
- writes the BT1 descriptor to block `1002`
- reads the payload back and verifies that it matched
- reads the descriptor back and verifies that it matched

### Load address behavior

In multi-sector SD mode, the script records a load address in the BT1 descriptor.

By default, the load address is the same as `--origin`.

You can override it explicitly with:

```bash
--load-addr 0x0200
```

---

## Why `sudo env "PATH=$PATH"` may be needed

Direct writes to `/dev/mmcblk0` usually require root permission.

If you simply run:

```bash
sudo python3 deploy_asm.py ...
```

`customasm` may not be found because `sudo` often uses a different `PATH`.

Use this form to preserve your current `PATH`:

```bash
sudo env "PATH=$PATH" python3 deploy_asm.py ...
```

Use that form for direct SD writes.

---

## Direct SD writes on Windows

On Windows, run PowerShell as Administrator for direct card writes.

Find the SD card disk number before a direct write:

```powershell
Get-Disk
```

A simple check is to run `Get-Disk`, insert the card, and run `Get-Disk` again. The new removable-sized disk is the SD card.

If Windows assigned the card a drive letter, you can map that drive letter back to its disk number. For example, for drive `E:`:

```powershell
Get-Partition -DriveLetter E | Get-Disk | Format-List Number,FriendlyName,BusType,Size,PartitionStyle
```

If the card appears as disk `5`, the raw device name is:

```text
\\.\PhysicalDrive5
```

Use that raw device path with `--device`:

```powershell
python tools\deployment\deploy_asm.py sd ASM\programs\probe_oled_monitor\PROBE.asm --origin 0x0200 --device "\\.\PhysicalDrive5" --block 1003 --descriptor-block 1002 --dump-annotated
```

Do not use a mounted drive path such as `E:` for descriptor and payload blocks. The block numbers in this workflow are raw SD-card block numbers.

If Windows blocks the raw disk write, find the volume GUID for the SD card:

```powershell
Get-CimInstance Win32_Volume | Select-Object DriveLetter, Label, FileSystem, Capacity, DeviceID
```

The SD-card volume should match the card size. For a 32 GB card, Windows often reports about `29.1 GB`. A volume GUID looks like:

```text
\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\
```

Pass that GUID with `--windows-lock-volume`:

```powershell
python tools\deployment\deploy_asm.py sd ASM\programs\probe_oled_monitor\PROBE.asm --origin 0x0200 --device "\\.\PhysicalDrive5" --windows-lock-volume "\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\" --block 1003 --descriptor-block 1002 --dump-annotated
```

`--windows-lock-volume` keeps the SD-card volume locked during the raw block-device write. The option is only needed on Windows setups that reject a direct `\\.\PhysicalDriveN` write.

If Windows has the card mounted as drive `E:`, close File Explorer windows pointed at the card. You can also dismount the volume before a direct write:

```powershell
Dismount-Volume -DriveLetter E -Force
```

After a card reinsertion or card-reader change, recheck the disk number and volume GUID before any direct write.

---

## Output files

The script writes files into the `build/` directory by default.

### ROM mode outputs

- `*_trimmed_hex.txt`
- `*_trimmed.bin`
- `*_annotated.txt` if `--dump-annotated` is used
- `*_manifest.txt`

### SD mode outputs

Single-sector SD builds produce:

- `*_sector.bin`
- `*_sd_trimmed_hex.txt`
- `*_sd_trimmed.bin`
- `*_annotated.txt` if `--dump-annotated` is used
- `*_manifest.txt`

Multi-sector SD builds produce:

- `*_payload_padded.bin`
- `*_bootdesc_bt1.bin`
- `*_sd_trimmed_hex.txt`
- `*_sd_trimmed.bin`
- `*_annotated.txt` if `--dump-annotated` is used
- `*_manifest.txt`

---

## Manifest file

Each build creates a small manifest file that records what was built.

### ROM manifest fields

A ROM manifest typically includes:

- build mode
- source file path
- origin address in hex and decimal
- trimmed byte count
- trimmed hex output path
- trimmed binary output path
- annotated output path if requested

### SD manifest fields

An SD manifest typically includes:

- build mode
- source file path
- origin address in hex and decimal
- trimmed byte count
- sector size
- sector count
- install mode, either `single-sector` or `multi-sector`
- trimmed hex output path
- trimmed binary output path
- single-sector output path if used
- padded payload output path if used
- descriptor output path if used
- annotated output path if requested
- target device
- payload start block
- load address
- descriptor block
- payload readback match result
- first 16 bytes read back from the payload
- last 16 bytes read back from the payload
- descriptor readback match result when applicable
- first 16 descriptor bytes read back when applicable

The SD manifest is useful for documenting exactly what was built, what was written, where it was written, and whether direct-device readback verification passed.

---

## Formatted hex output

The generated hex text output is formatted for easier viewing and use with programmer workflows.

It uses:

- 16 values per line
- an extra visual gap between the 8th and 9th byte
- commas after every byte, including the last byte on each line

Example:

```text
0xec, 0xfa, 0xc2, 0xe6, 0x18, 0x14, 0xed, 0x1b,   0xc1, 0x01, 0x09, 0xff, 0xf5, 0x16, 0xc0, 0x01,
0xfe, 0x1a, 0x01, 0xf5, 0x06, 0xc0, 0xe7, 0xf0,   0xed, 0xe8, 0xc0, 0x03, 0x40, 0xed, 0x41, 0xc1,
```

---

## Example project workflow

The workflow below covers a descriptor-driven SD load-and-execute flow.

### 1. Build and write the RAM payload to SD

RAM payload source:

```asm
#addr 0x0200
#include "ruledef.asm"

; Stage-2 RAM payload code goes here.
; If the trimmed payload is larger than 512 bytes,
; deploy_asm.py will package it as a BT1 multi-sector payload.
```

Build and write it to SD on Linux:

```bash
sudo env "PATH=$PATH" python3 deploy_asm.py sd stage2_monitor.asm --origin 0x0200 --device /dev/mmcblk0 --block 1003 --descriptor-block 1002 --dump-annotated
```

Build and write it to SD on Windows PowerShell:

```powershell
python tools\deployment\deploy_asm.py sd ASM\programs\probe_oled_monitor\PROBE.asm --origin 0x0200 --device "\\.\PhysicalDrive5" --block 1003 --descriptor-block 1002 --dump-annotated
```

If Windows requires a volume lock, add `--windows-lock-volume`:

```powershell
python tools\deployment\deploy_asm.py sd ASM\programs\probe_oled_monitor\PROBE.asm --origin 0x0200 --device "\\.\PhysicalDrive5" --windows-lock-volume "\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\" --block 1003 --descriptor-block 1002 --dump-annotated
```

Replace `PhysicalDrive5` with the SD card disk number from `Get-Disk`. Replace the volume GUID with the SD-card GUID from `Get-CimInstance Win32_Volume`.

If the payload fits in one sector, the script writes one padded 512-byte sector at block `1003`.

If the payload is larger than one sector, the script writes:

- a padded multi-sector payload starting at block `1003`
- a BT1 descriptor at block `1002`

### 2. Verify the SD contents manually

The script already performs readback verification when `--device` is used. Manual verification is still useful when you want to inspect the card yourself.

For a multi-sector BT1 payload, read back the descriptor block:

```bash
sudo dd if=/dev/mmcblk0 of=readback_bootdesc.bin bs=512 skip=1002 count=1 status=progress
sync
```

Inspect the first bytes:

```bash
xxd -g 1 readback_bootdesc.bin | head
```

For a BT1 descriptor, the first bytes should begin with:

```text
42 54 31
```

Read back the payload. Use the sector count shown in the build output or in the manifest file.

For example, if the manifest says `sector_count: 3`, read back three sectors starting at block `1003`:

```bash
sudo dd if=/dev/mmcblk0 of=readback_payload.bin bs=512 skip=1003 count=3 status=progress
sync
```

Inspect the first bytes:

```bash
xxd -g 1 readback_payload.bin | head
```

Compare the generated files against the readback:

```bash
cmp -l build/stage2_monitor_bootdesc_bt1.bin readback_bootdesc.bin
cmp -l build/stage2_monitor_payload_padded.bin readback_payload.bin
```

If the payload fit in one sector, read back one block and compare against the single-sector image:

```bash
sudo dd if=/dev/mmcblk0 of=readback_block1003.bin bs=512 skip=1003 count=1 status=progress
sync
cmp -l build/stage2_monitor_sector.bin readback_block1003.bin
```

If `cmp` prints nothing, the two files match exactly.

Windows PowerShell readback for the descriptor block:

```powershell
python -c "dev=r'\\.\PhysicalDrive5'; f=open(dev,'rb',buffering=0); f.seek(1002*512); data=f.read(512); f.close(); open('readback_bootdesc.bin','wb').write(data)"
Format-Hex .\readback_bootdesc.bin | Select-Object -First 2
```

Windows PowerShell readback for a three-sector payload at block `1003`:

```powershell
python -c "dev=r'\\.\PhysicalDrive5'; count=3; f=open(dev,'rb',buffering=0); f.seek(1003*512); data=f.read(count*512); f.close(); open('readback_payload.bin','wb').write(data)"
Format-Hex .\readback_payload.bin | Select-Object -First 2
```

Compare the generated files against the Windows readback files:

```powershell
fc.exe /b build\stage2_monitor_bootdesc_bt1.bin readback_bootdesc.bin
fc.exe /b build\stage2_monitor_payload_padded.bin readback_payload.bin
```

For a single-sector payload, read back one block and compare against the single-sector image:

```powershell
python -c "dev=r'\\.\PhysicalDrive5'; f=open(dev,'rb',buffering=0); f.seek(1003*512); data=f.read(512); f.close(); open('readback_block1003.bin','wb').write(data)"
fc.exe /b build\stage2_monitor_sector.bin readback_block1003.bin
```

### 3. Build the ROM loader

Build the ROM-side bootstrap:

```bash
python3 deploy_asm.py rom sd_bootstrap_v2_multi_sector.asm --origin 0xC000 --dump-annotated
```

### 4. Burn the ROM

Program the ROM using one of these outputs:

- `build/sd_bootstrap_v2_multi_sector_trimmed_hex.txt`
- `build/sd_bootstrap_v2_multi_sector_trimmed.bin`

### 5. Run the CPU

Insert the SD card and power the system.

Expected result for a BT1 multi-sector payload:

- ROM bootstrap initializes SD
- ROM bootstrap reads the BT1 descriptor
- ROM bootstrap reads the payload sector or sectors into RAM
- ROM bootstrap jumps to the RAM load address
- stage-2 payload runs

---

## BT1 descriptor behavior in SD mode

In multi-sector SD mode, the script creates a 512-byte descriptor sector with this layout:

- byte 0 = `0x42` = `B`
- byte 1 = `0x54` = `T`
- byte 2 = `0x31` = version 1
- byte 3 = flags / reserved
- byte 4..7 = payload start block
- byte 8..9 = load address
- byte 10..11 = block count

The descriptor is saved as `*_bootdesc_bt1.bin` and can also be written directly to the descriptor block on the SD card.

---

## Notes on address trimming

The script trims from the real occupied address span reported by customasm, not blindly from the chosen origin to the end of a padded image.

Reason:

- ROM code may start at `0xC000`
- RAM payloads may start at `0x0200`
- `customasm` output may include padded address space
- only the actual occupied bytes should be packaged for ROM output or SD payload output

For RAM payloads, only the true program bytes should appear at the beginning of the SD payload image.

---

## Troubleshooting

### `customasm was not found on PATH`

Check:

```bash
which customasm
```

If the command works normally but fails under `sudo`, use:

```bash
sudo env "PATH=$PATH" python3 deploy_asm.py ...
```

### `Permission denied: '/dev/mmcblk0'`

Use `sudo` when writing directly to the SD card.

### `A device attached to the system is not functioning` on Windows

Check that the device path has no trailing slash. Use:

```text
\\.\PhysicalDrive5
```

Do not use:

```text
\\.\PhysicalDrive5\
```

Also confirm that PowerShell has Administrator permission and that the SD card is still the same disk number shown by `Get-Disk`.


### `[Errno 5] Access is denied` on Windows

Run PowerShell as Administrator first. If the SD card is not read-only and Windows still rejects `\\.\PhysicalDriveN`, find the SD-card volume GUID:

```powershell
Get-CimInstance Win32_Volume | Select-Object DriveLetter, Label, FileSystem, Capacity, DeviceID
```

Then add `--windows-lock-volume` to the deploy command:

```powershell
python tools\deployment\deploy_asm.py sd ASM\programs\probe_oled_monitor\PROBE.asm --origin 0x0200 --device "\\.\PhysicalDrive5" --windows-lock-volume "\\?\Volume{2a7913e0-4753-11f1-a6cb-28cdc480a7e2}\" --block 1003 --descriptor-block 1002 --dump-annotated
```

Do not use a Linux partition or Google Drive volume GUID. Match the SD-card size before the write.

### `[Errno 9] Bad file descriptor` on Windows

Run the current Windows-compatible script version. Windows raw disk paths such as `\\.\PhysicalDrive5` use the Win32 device API inside the script rather than Python's normal file-path layer.

Also confirm that PowerShell was opened as Administrator and that the SD-card volume is not open in File Explorer. If the card has drive letter `E:`, you can dismount it before the write:

```powershell
Dismount-Volume -DriveLetter E -Force
```

### Windows card appears as `No Media`

Some USB card readers expose an empty slot and the inserted card as separate disk entries. Use the entry with the real card size and `Online` status. For a 32 GB card, Windows may report about `29.12 GB`.

### The payload is larger than one 512-byte sector

The script supports that automatically.

If the trimmed payload fits in one sector, the script uses the single-sector path.

If it is larger than one sector, the script switches to the multi-sector BT1 path automatically.

For multi-sector SD builds, provide `--block` so the descriptor can record where the payload starts.

### Multi-sector SD mode says `--block` is required

Expected behavior.

The script needs the payload start block in order to generate the BT1 descriptor. The same requirement applies even when you only generate files and do not write directly to the SD card.

### The script writes files into `build/`, not next to the script

Expected behavior unless you change `--out-dir`.

### The manifest says `payload_readback_match: not checked`

The script built files but did not perform a direct device write in that run.

### The manifest says `descriptor_readback_match: not checked`

Usually, one of these is true:

- the run did not use direct device write
- or the build used the single-sector path, so no BT1 descriptor was written

---