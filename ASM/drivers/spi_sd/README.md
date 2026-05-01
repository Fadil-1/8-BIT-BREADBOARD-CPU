# SPI and SD Assembly Libraries

This directory contains the current SPI / SD assembly files.

## Files

### `SPI_routines.asm`
Low-level SPI bus helpers.

This file contains the routines that directly manipulate the SPI register through `INP` and `OUT`. It covers:
- selecting and deselecting devices on the shared SPI bus
- generating the SD-card startup clocks with all devices deselected
- sending one byte over SPI
- reading one byte over SPI

These routines are the hardware-near foundation used by the SD initialization and SD block-I/O code.

### `SPI_init.asm`
SD-card SPI initialization helpers.

This file contains the command-level SD initialization flow that runs on top of the raw SPI byte routines. It includes:
- waiting for an R1 response byte
- `CMD0`
- `CMD8`
- the `CMD55` / `ACMD41` initialization loop

These routines assume the SPI byte-send / byte-read primitives already work.

### `sd_block_io.asm`
Reusable SD block-read helpers built on top of SPI.

This file contains routines that use the initialized SD card to perform block reads. In the current version it includes:
- a reliable SD initialization wrapper
- a wait-for-data-token routine
- a small test read of block 1000 into RAM at `0x0200`

This file is intended to be included by other programs rather than assembled as a standalone top-level program.

### `sd_bootstrap_v1_single_sector.asm`
Single-sector descriptor-driven ROM bootstrap.

This ROM bootstrap:
- initializes the SD card
- reads the BT1 descriptor from fixed block `1002`
- validates that it points to a single payload block for load address `0x0200`
- reads that block into RAM
- jumps to `0x0200`

This is the simpler single-sector version.

### `sd_bootstrap_v2_multi_sector.asm`
Multi-sector descriptor-driven ROM bootstrap.

This ROM bootstrap:
- initializes the SD card
- reads the BT1 descriptor from fixed block `1002`
- validates the descriptor
- extracts payload block, load address, and sector count
- loads all payload sectors into RAM
- jumps to the descriptor-provided entry / load address

This is the current multi-sector version and includes helper routines to increment the SD block number, advance the RAM destination by one sector, and decrement the remaining sector count.