; ==========================================================
; sd_block_io.asm
; SD card block-I/O helper routines on top of SPI
;
; This file is a library file.
; It should be included by another program.
; Do NOT put a top-level JMP here.
;
; Calling convention:
;   - Higher-level routines preserve $A, $B, $C, $D
;   - Carry flag is used as the return status:
;       C = 0  success
;       C = 1  failure / timeout
;
; Original version: April 2026
; Last Modified: May 2026
; Fadil Isamotu
; ==========================================================

SD_BLOCK_ADDR_MSB = 0x0100
SD_BLOCK_ADDR_B2  = 0x0101
SD_BLOCK_ADDR_B1  = 0x0102
SD_BLOCK_ADDR_LSB = 0x0103

; ----------------------------------------------------------
; SD_INIT_RELIABLE
;
; Keeps retrying SD initialization until it succeeds.
; Preserves: $A, $B, $C, $D
; Returns: carry clear on success
;
; Uses the already-working flow:
;   POWER_UP_SD_CARD
;   CMD0
;   CMD8
;   INIT_SD
; ----------------------------------------------------------
SD_INIT_RELIABLE:
    PSH $A
    PSH $B
    PSH $C
    PSH $D

.RETRY_INIT:
    JSR DESELECT_ALL_SPI_DEVICES
    JSR POWER_UP_SD_CARD

    JSR CMD0
    JC  .RETRY_INIT

    JSR CMD8
    JC  .RETRY_INIT

    JSR INIT_SD
    JC  .RETRY_INIT

    JSR DESELECT_ALL_SPI_DEVICES

    PUL $D
    PUL $C
    PUL $B
    PUL $A

    CLC
    RTS


; ----------------------------------------------------------
; SD_WAIT_DATA_TOKEN
;
; Waits for the single-block read data token 0xFE.
; Preserves: $B, $C, $D
; Returns:
;   carry clear on success ($A = 0xFE)
;   carry set on timeout   ($A = last byte read)
; ----------------------------------------------------------
SD_WAIT_DATA_TOKEN:
    PSH $B
    PSH $C
    PSH $D

    ; 16-bit timeout counter in $CD
    MOV $C, 0x40
    MOV $D, 0x00

.WAIT_LOOP:
    JSR SPI_READ_BYTE

    STC
    CMP $A, 0xFE
    JZ  .SUCCESS

    ; 16-bit decrement of $CD
    ; carry = 1 means no borrow
    ; carry = 0 means borrow
    STC
    SUB $D, 0x01
    JC  .WAIT_LOOP

    STC
    SUB $C, 0x01
    JC  .WAIT_LOOP

    ; timeout
    PUL $D
    PUL $C
    PUL $B
    STC
    RTS

.SUCCESS:
    PUL $D
    PUL $C
    PUL $B
    CLC
    RTS


; ----------------------------------------------------------
; SD_READ_BLOCK_1000_TO_0200_16
;
; Reads SD block 1000 (0x000003E8)
; Copies first 16 bytes into RAM at 0x0200
;
; Preserves: $A, $B, $C, $D
; Returns:
;   carry clear on success
;   carry set on failure
;
; This is the reusable version of the exact path that already
; worked in your test loader.
; ----------------------------------------------------------
SD_READ_BLOCK_1000_TO_0200_16:
    PSH $A
    PSH $B
    PSH $C
    PSH $D

    JSR SELECT_SD_CARD

    ; give card 8 clocks after CS goes low
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; CMD17, block 1000 = 0x000003E8
    MOV $A, 0x51
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0x03
    JSR SPI_WRITE_BYTE

    MOV $A, 0xE8
    JSR SPI_WRITE_BYTE

    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for R1 = 0x00
    JSR WAIT_R1
    STC
    CMP $A, 0x00
    JNZ .FAIL

    ; one-time priming byte after successful R1
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for data token 0xFE
    JSR SD_WAIT_DATA_TOKEN
    JC  .FAIL

    ; destination pointer = 0x0200
    ; $C = low byte, $D = high byte
    MOV $C, 0x00
    MOV $D, 0x02

    ; copy 16 bytes
    MOV $B, 16

.COPY_LOOP:
    JSR SPI_READ_BYTE
    MOV [$CD], $A

    ; increment pointer
    CLC
    ADD $C, 0x01
    JNC .NO_CARRY
    CLC
    ADD $D, 0x01

.NO_CARRY:
    STC
    SUB $B, 0x01
    JNZ .COPY_LOOP

    ; discard 2-byte CRC
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE

    JSR DESELECT_ALL_SPI_DEVICES

    PUL $D
    PUL $C
    PUL $B
    PUL $A

    CLC
    RTS

.FAIL:
    JSR DESELECT_ALL_SPI_DEVICES

    PUL $D
    PUL $C
    PUL $B
    PUL $A

    STC
    RTS


; ----------------------------------------------------------
; SD_READ_BLOCK_1000_TO_RAM_512
;
; Reads SD block 1000 (0x000003E8)
; Copies full 512-byte block into RAM starting at address in $CD
;
; CALLER MUST SET:
;   $C = low byte of RAM destination
;   $D = high byte of RAM destination
;
; Preserves:
;   $A, $B
;
; Modifies:
;   $C, $D   (advanced by 512 bytes)
;
; Returns:
;   carry clear on success
;   carry set on failure
; ----------------------------------------------------------
SD_READ_BLOCK_1000_TO_RAM_512:
    PSH $A
    PSH $B

    JSR SELECT_SD_CARD

    ; give card 8 clocks after CS goes low
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; CMD17, block 1000 = 0x000003E8
    MOV $A, 0x51
    JSR SPI_WRITE_BYTE

    MOV $A, 0x00
    JSR SPI_WRITE_BYTE
    JSR SPI_WRITE_BYTE

    MOV $A, 0x03
    JSR SPI_WRITE_BYTE

    MOV $A, 0xE8
    JSR SPI_WRITE_BYTE

    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for R1 = 0x00
    JSR WAIT_R1
    STC
    CMP $A, 0x00
    JNZ .FAIL

    ; one-time priming byte after successful R1
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for data token 0xFE
    JSR SD_WAIT_DATA_TOKEN
    JC  .FAIL

    ; two 256-byte pages = 512 bytes total
    MOV $B, 2

.COPY_LOOP:
    JSR SPI_READ_BYTE
    MOV [$CD], $A

    ; increment pointer low byte
    CLC
    ADD $C, 0x01
    JNC .COPY_LOOP

    ; low byte wrapped, increment high byte
    CLC
    ADD $D, 0x01

    ; one 256-byte page completed
    STC
    SUB $B, 0x01
    JNZ .COPY_LOOP

    ; discard 2-byte CRC
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE

    JSR DESELECT_ALL_SPI_DEVICES

    PUL $B
    PUL $A

    CLC
    RTS

.FAIL:
    JSR DESELECT_ALL_SPI_DEVICES

    PUL $B
    PUL $A

    STC
    RTS

; ----------------------------------------------------------
; SD_READ_BLOCK_TO_RAM_512
;
; Reads one full 512-byte SD block into RAM starting at $CD.
;
; CALLER MUST SET:
;   $C = low byte of RAM destination
;   $D = high byte of RAM destination
;
; BLOCK ADDRESS SOURCE:
;   0x0100 = most significant byte
;   0x0101 = next byte
;   0x0102 = next byte
;   0x0103 = least significant byte
;
; Preserves:
;   $A, $B
;
; Modifies:
;   $C, $D   (advanced by 512 bytes)
;
; Returns:
;   carry clear on success
;   carry set on failure
; ----------------------------------------------------------
SD_READ_BLOCK_TO_RAM_512:
    PSH $A
    PSH $B

    JSR SELECT_SD_CARD

    ; give card 8 clocks after CS goes low
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; CMD17
    MOV $A, 0x51
    JSR SPI_WRITE_BYTE

    ; send 32-bit block address from RAM
    MOV $A, 0x0100
    JSR SPI_WRITE_BYTE

    MOV $A, 0x0101
    JSR SPI_WRITE_BYTE

    MOV $A, 0x0102
    JSR SPI_WRITE_BYTE

    MOV $A, 0x0103
    JSR SPI_WRITE_BYTE

    ; dummy CRC in SPI mode
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for R1 = 0x00
    JSR WAIT_R1
    STC
    CMP $A, 0x00
    JNZ .FAIL

    ; one-time priming byte after successful R1
    MOV $A, 0xFF
    JSR SPI_WRITE_BYTE

    ; wait for data token 0xFE
    JSR SD_WAIT_DATA_TOKEN
    JC  .FAIL

    ; copy full 512 bytes = two 256-byte pages
    MOV $B, 2

.COPY_LOOP:
    JSR SPI_READ_BYTE
    MOV [$CD], $A

    ; increment pointer low byte
    CLC
    ADD $C, 0x01
    JNC .COPY_LOOP

    ; low byte wrapped, increment high byte
    CLC
    ADD $D, 0x01

    ; one 256-byte page completed
    STC
    SUB $B, 0x01
    JNZ .COPY_LOOP

    ; discard 2-byte CRC
    JSR SPI_READ_BYTE
    JSR SPI_READ_BYTE

    JSR DESELECT_ALL_SPI_DEVICES

    PUL $B
    PUL $A

    CLC
    RTS

.FAIL:
    JSR DESELECT_ALL_SPI_DEVICES

    PUL $B
    PUL $A

    STC
    RTS