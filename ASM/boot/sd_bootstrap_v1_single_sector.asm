; ==========================================================
; sd_bootstrap_v1_single_sector.asm
; Single-sector BT1 SD bootstrap ROM
; ==========================================================
;
; Purpose:
;   Boot a stage-2 payload from SD into RAM at 0x0200 by using
;   the fixed BT1 descriptor block at SD block 1002.
;
; Current flow:
;   1. Start in ROM at 0xC000
;   2. Initialize the SD card in SPI mode
;   3. Read descriptor block 1002 into RAM at 0x0400
;   4. Validate descriptor magic / version
;   5. Copy the payload block number from the descriptor
;   6. Require load address = 0x0200 and block count = 1
;   7. Read the payload block into RAM at 0x0200
;   8. Jump to 0x0200
;
; BT1 descriptor fields used here:
;   0x0400..0x0402 = 'B' 'T' '1'
;   0x0404..0x0407 = payload block number
;   0x0408..0x0409 = load address
;   0x040A..0x040B = block count
;
; Current fixed conventions:
;   descriptor block       = 1002 = 0x000003EA
;   descriptor scratch RAM = 0x0400
;   payload load address   = 0x0200
; ==========================================================

#addr 0xC000
#include "../ruledef.asm"

JMP START

#include "../drivers/spi_sd/SPI_init.asm"
#include "../drivers/spi_sd/SPI_routines.asm"
#include "../drivers/spi_sd/sd_block_io.asm"

START:
    MOV $CLK, 0xFF

    ; Marker: bootstrap entered.
    MOV $A, 0x11
    SDL $A
    SDH $A

    JSR SD_INIT_RELIABLE

    ; Marker: SD initialization completed and descriptor work begins.
    MOV $A, 0x55
    SDL $A
    SDH $A

    ; Read descriptor block 1002 = 0x000003EA into RAM 0x0400.
    MOV $A, 0x00
    MOV 0x0100, $A

    MOV $A, 0x00
    MOV 0x0101, $A

    MOV $A, 0x03
    MOV 0x0102, $A

    MOV $A, 0xEA
    MOV 0x0103, $A

    MOV $C, 0x00
    MOV $D, 0x04

    JSR SD_READ_BLOCK_TO_RAM_512
    JC  FAIL

    ; Validate descriptor magic/version at 0x0400..0x0402.
    MOV $A, 0x0400
    STC
    CMP $A, 0x42
    JNZ FAIL

    MOV $A, 0x0401
    STC
    CMP $A, 0x54
    JNZ FAIL

    MOV $A, 0x0402
    STC
    CMP $A, 0x31
    JNZ FAIL

    ; Copy payload block number into the working SD block buffer
    ; used by SD_READ_BLOCK_TO_RAM_512.
    MOV $A, 0x0404
    MOV 0x0100, $A

    MOV $A, 0x0405
    MOV 0x0101, $A

    MOV $A, 0x0406
    MOV 0x0102, $A

    MOV $A, 0x0407
    MOV 0x0103, $A

    ; This version accepts only a single payload block loaded to 0x0200.
    MOV $A, 0x0408
    STC
    CMP $A, 0x02
    JNZ FAIL

    MOV $A, 0x0409
    STC
    CMP $A, 0x00
    JNZ FAIL

    MOV $A, 0x040A
    STC
    CMP $A, 0x00
    JNZ FAIL

    MOV $A, 0x040B
    STC
    CMP $A, 0x01
    JNZ FAIL

    ; Load the payload into RAM at 0x0200.
    MOV $C, 0x00
    MOV $D, 0x02

    JSR SD_READ_BLOCK_TO_RAM_512
    JC  FAIL

    JMP 0x0200

FAIL:
    MOV $A, 0x99
    SDL $A
    SDH $A
    HLT
