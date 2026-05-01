; ==========================================================
; sd_bootstrap_v2_multi_sector.asm
; Multi-sector BT1 SD bootstrap ROM
; ==========================================================
;
; Purpose:
;   Boot a stage-2 payload from SD into RAM by using the fixed
;   BT1 descriptor block at SD block 1002.
;
; Current flow:
;   1. Start in ROM at 0xC000
;   2. Initialize the SD card
;   3. Read descriptor block 1002 into RAM at 0x0400
;   4. Validate descriptor magic / version
;   5. Copy payload block, load address, and sector count
;   6. Read all payload sectors into RAM
;   7. Jump to the descriptor-provided load address
;
; BT1 descriptor fields used here:
;   0x0400..0x0402 = 'B' 'T' '1'
;   0x0404..0x0407 = payload start block
;   0x0408..0x0409 = load address
;   0x040A..0x040B = sector count
;
; Pointer convention on this CPU:
;   C = low byte
;   D = high byte
;
; Scratch RAM used by this loader:
;   0x0100..0x0103 = current SD block number (big-endian u32)
;   0x0104         = entry/load low
;   0x0105         = entry/load high
;   0x0106         = remaining sector count high
;   0x0107         = remaining sector count low
;   0x0108         = current destination low
;   0x0109         = current destination high
;   0x010A         = successful sector-read counter used by the
;                    current ROM-side debug display markers
; ==========================================================

#addr 0xC000
#include "../ruledef.asm"

JMP START

#include "../libs/timing.asm"
#include "../drivers/spi_sd/SPI_init.asm"
#include "../drivers/spi_sd/SPI_routines.asm"
#include "../drivers/spi_sd/sd_block_io.asm"

START:
    MOV $CLK, 0xFF

    ; Marker: bootstrap entered.
    MOV $A, 0xA1
    SDL $A
    SDH $A

    JSR SD_INIT_RELIABLE

    ; Marker: SD initialization completed.
    MOV $A, 0xB2
    SDL $A
    SDH $A

    ; Read descriptor block 1002 = 0x000003EA into RAM 0x0400.
    MOV $A, 0x00
    MOV 0x0100, $A
    MOV 0x0101, $A

    MOV $A, 0x03
    MOV 0x0102, $A

    MOV $A, 0xEA
    MOV 0x0103, $A

    MOV $C, 0x00
    MOV $D, 0x04

    JSR SD_READ_BLOCK_TO_RAM_512
    JC  FAIL

    ; Marker: descriptor block read succeeded.
    MOV $A, 0x23
    SDL $A
    SDH $A
    JSR DELAY_VERY_LONG
    
    ; Validate descriptor magic/version: "BT1".
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

    ; Marker: descriptor magic validated.
    MOV $A, 0x33
    SDL $A
    SDH $A

    ; Copy payload start block into the working SD block buffer.
    MOV $A, 0x0404
    MOV 0x0100, $A

    MOV $A, 0x0405
    MOV 0x0101, $A

    MOV $A, 0x0406
    MOV 0x0102, $A

    MOV $A, 0x0407
    MOV 0x0103, $A

    ; Copy the descriptor load address into both:
    ;   - the preserved entry/load address
    ;   - the current working RAM destination pointer
    MOV $A, 0x0409
    MOV 0x0104, $A
    MOV 0x0108, $A

    MOV $A, 0x0408
    MOV 0x0105, $A
    MOV 0x0109, $A

    ; Copy the descriptor sector count.
    MOV $A, 0x040A
    MOV 0x0106, $A

    MOV $A, 0x040B
    MOV 0x0107, $A

    ; Require block count != 0.
    MOV $A, 0x0106
    MOV $B, 0x0107
    OR  $A, $B
    JZ  FAIL

    ; Marker: descriptor fields copied and load phase begins.
    MOV $A, 0x44
    SDL $A
    SDH $A

    MOV $A, 0x00
    MOV 0x010A, $A

    JSR LOAD_STAGE2_N_SECTORS
    JC  FAIL

    ; Marker: all payload sectors loaded.
    MOV $A, 0x55
    SDL $A
    SDH $A

    ; Jump to the descriptor-provided entry / load address.
    MOV $C, 0x0104
    MOV $D, 0x0105
    JMP [$CD]


; ----------------------------------------------------------
; LOAD_STAGE2_N_SECTORS
;
; Generic ROM-side payload loader.
;
; Working state in RAM:
;   0x0100..0x0103 = current SD block number (big-endian u32)
;   0x0106..0x0107 = sectors remaining      (big-endian u16)
;   0x0108..0x0109 = current RAM destination (low, high)
;
; Per iteration:
;   - read one 512-byte SD block into RAM[CD]
;   - increment the current SD block number
;   - advance the RAM destination by 0x0200 bytes
;   - decrement the remaining sector count
;
; Returns:
;   carry clear = success
;   carry set   = failure
; ----------------------------------------------------------
LOAD_STAGE2_N_SECTORS:

LOAD_LOOP:
    MOV $A, 0x0106
    MOV $B, 0x0107
    OR  $A, $B
    JZ  LOAD_DONE

    MOV $C, 0x0108
    MOV $D, 0x0109

    JSR SD_READ_BLOCK_TO_RAM_512
    JC  LOAD_FAIL

    ; ROM-side debug counter for completed sector reads.
    CLC
    NOP
    MOV $A, 0x010A
    ADD $A, 0x01
    MOV 0x010A, $A

    SDL $A
    SDH $A
    JSR DELAY_VERY_LONG

    JSR INC_BLOCK_U32_BE_0100
    JSR ADD_0200_TO_PTR_0108
    JSR DEC_U16_BE_0106

    JMP LOAD_LOOP

LOAD_DONE:
    CLC
    RTS

LOAD_FAIL:
    STC
    RTS


; ----------------------------------------------------------
; INC_BLOCK_U32_BE_0100
;
; Increments the current SD block number stored as a
; big-endian 32-bit value at 0x0100..0x0103.
; ----------------------------------------------------------
INC_BLOCK_U32_BE_0100:
    CLC
    NOP
    MOV $A, 0x0103
    ADD $A, 0x01
    MOV 0x0103, $A
    JNC INC32_DONE

    CLC
    NOP
    MOV $A, 0x0102
    ADD $A, 0x01
    MOV 0x0102, $A
    JNC INC32_DONE

    CLC
    NOP
    MOV $A, 0x0101
    ADD $A, 0x01
    MOV 0x0101, $A
    JNC INC32_DONE

    CLC
    NOP
    MOV $A, 0x0100
    ADD $A, 0x01
    MOV 0x0100, $A

INC32_DONE:
    RTS


; ----------------------------------------------------------
; ADD_0200_TO_PTR_0108
;
; Advances the current RAM destination by one 512-byte sector.
;
; Working pointer layout:
;   0x0108 = low
;   0x0109 = high
;
; Since one sector is 0x0200 bytes, the current implementation
; advances only the high byte by 0x02.
; ----------------------------------------------------------
ADD_0200_TO_PTR_0108:
    CLC
    NOP
    MOV $A, 0x0109
    ADD $A, 0x02
    MOV 0x0109, $A
    RTS


; ----------------------------------------------------------
; DEC_U16_BE_0106
;
; Decrements the remaining sector count stored as a big-endian
; 16-bit value.
;
; Layout:
;   0x0106 = high
;   0x0107 = low
; ----------------------------------------------------------
DEC_U16_BE_0106:
    STC
    NOP
    MOV $A, 0x0107
    SUB $A, 0x01
    MOV 0x0107, $A
    JC  DEC16_DONE

    STC
    NOP
    MOV $A, 0x0106
    SUB $A, 0x01
    MOV 0x0106, $A

DEC16_DONE:
    RTS

FAIL:
    MOV $A, 0x99
    SDL $A
    SDH $A
    HLT
