; ==========================================================
; SPI_init.asm
; SD-card SPI initialization helpers
; ==========================================================
;
; This file contains the SD-card command sequences that run on
; top of the raw SPI byte-send / byte-read routines.
;
; Current initialization sequence:
;   1. CMD0   -> reset card into idle state
;   2. CMD8   -> interface-condition check
;   3. CMD55 + ACMD41 loop -> leave idle state
;
; Return-status convention:
;   carry clear = success
;   carry set   = failure / unexpected response / timeout
; ==========================================================


; ----------------------------------------------------------
; WAIT_R1
;
; Waits for the first non-0xFF response byte from the card.
;
; Returns:
;   $A = response byte
;
; Preserves:
;   caller's $D
; ----------------------------------------------------------
WAIT_R1:
    PSH $D
    MOV $D, 20

.WAIT_R1_LOOP:
    JSR SPI_READ_BYTE

    STC
    CMP $A, 0xFF
    JNZ .DONE

    STC
    NOP
    SUB $D, 1
    JNZ .WAIT_R1_LOOP

.DONE:
    PUL $D
    RTS


; ----------------------------------------------------------
; CMD0
;
; Sends the SD reset command.
;
; Expected response:
;   R1 = 0x01
; ----------------------------------------------------------
CMD0:
    JSR SELECT_SD_CARD

    MOV $A, 0x40
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0x95
    JSR SPI_WRITE_BYTE

    JSR WAIT_R1
    STC
    CMP $A, 0x01
    JNZ .EXIT
    CLC

.EXIT:
    ; Deselecting devices can disturb flags, so the carry result
    ; is saved and restored around the deselect helper.
    PSF
    NOP
    JSR DESELECT_ALL_SPI_DEVICES
    PLF
    RTS


; ----------------------------------------------------------
; CMD8
;
; Sends CMD8 and checks the trailing echo pattern.
;
; Expected response:
;   R1 = 0x01
;   final trailing byte = 0xAA
; ----------------------------------------------------------
CMD8:
    JSR SELECT_SD_CARD

    MOV $A, 0x48
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0x01
    JSR SPI_WRITE_BYTE

    MOV $A, 0xAA
    JSR SPI_WRITE_BYTE

    MOV $A, 0x87
    JSR SPI_WRITE_BYTE

    JSR WAIT_R1
    STC
    CMP $A, 0x01
    JNZ .EXIT

    ; Read the 32-bit trailing response and keep the final byte
    ; in $A for the echo-pattern check.
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE

    STC
    CMP $A, 0xAA
    JNZ .EXIT
    CLC

.EXIT:
    PSF
    JSR DESELECT_ALL_SPI_DEVICES
    PLF
    RTS


; ----------------------------------------------------------
; INIT_SD
;
; Repeats CMD55 + ACMD41 until the card reports ready.
;
; For the current flow, ACMD41 is sent with the HCS argument.
;
; Returns:
;   carry clear = card became ready
;   carry set   = timed out or got an unexpected response
; ----------------------------------------------------------
INIT_SD:
    PSH $D
    MOV $D, 50

.INIT_LOOP:
    JSR SELECT_SD_CARD

    ; CMD55
    MOV $A, 0x77
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    JSR WAIT_R1
    STC
    CMP $A, 0x01
    JNZ .ITERATION_FAIL
    
    JSR DESELECT_ALL_SPI_DEVICES

    ; ACMD41 with HCS bit set
    JSR SELECT_SD_CARD
    MOV $A, 0x69
    JSR SPI_WRITE_BYTE

    MOV $A, 0x40
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    JSR WAIT_R1
    STC
    CMP $A, 0x00
    JZ  .SUCCESS

.ITERATION_FAIL:
    JSR DESELECT_ALL_SPI_DEVICES
    STC
    NOP
    SUB $D, 1
    JNZ .INIT_LOOP

    STC
    PUL $D
    RTS

.SUCCESS:
    JSR DESELECT_ALL_SPI_DEVICES
    CLC
    PUL $D
    RTS
