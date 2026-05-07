; ==========================================================
; SPI_routines.asm
; Low-level SPI bus helpers for the custom breadboard CPU
; ==========================================================
;
; This file contains the routines that directly drive the SPI
; register through the port selector.
;
; Shared SPI-line usage in the current design:
;   bit 0 = MOSI
;   bit 1 = SCLK
;   bit 2 = SD card chip select (active low)
;   bit 3 = BLE module chip select (active low)
;   bit 7 = MISO when reading the SPI port back
;
; These routines operate on the current live SPI bus image:
;   - read the SPI register state with INP SPI_PORT
;   - modify the relevant control bits
;   - write the updated state back with OUT SPI_PORT
;
; Notes:
;   - Chip-select signals are active low.
;   - SCLK idles low in the sequences used here.
;   - MOSI is explicitly updated before each write clock edge.
;
; Original version: April 2026
; Last Modified: May 2026
; Fadil Isamotu
; ==========================================================


; Bit meanings inside the SPI register image
MOSI        = 0b00000001
SCLK        = 0b00000010
SD_CARD_CS  = 0b00000100
BLE_CS      = 0b00001000

SPI_PORT    = 0


; ----------------------------------------------------------
; SELECT_SD_CARD
;
; Selects the SD card and deselects the BLE module.
; The routine preserves the current SCLK state low.
; ----------------------------------------------------------
SELECT_SD_CARD:
    INP  $A, SPI_PORT
    AND  $A, 0xFF - SD_CARD_CS
    OR   $A, BLE_CS
    AND  $A, 0xFF - SCLK
    OUT  SPI_PORT, $A
    RTS


; ----------------------------------------------------------
; DESELECT_ALL_SPI_DEVICES
;
; Sets both chip-select lines high so that no SPI device is
; selected. A dummy byte is then clocked out to provide eight
; trailing clocks on the idle bus.
; ----------------------------------------------------------
DESELECT_ALL_SPI_DEVICES:
    INP  $A, SPI_PORT
    OR   $A, SD_CARD_CS | BLE_CS
    AND  $A, 0xFF - SCLK
    OUT  SPI_PORT, $A
    MOV  $A, 0xFF
    JSR  SPI_WRITE_BYTE
    RTS


; ----------------------------------------------------------
; POWER_UP_SD_CARD
;
; Sends the SD-card startup clocks with all devices deselected.
;
; The routine places the SPI bus in this idle state first:
;   - SD card deselected
;   - BLE deselected
;   - MOSI high
;   - SCLK low
;
; It then shifts out ten dummy bytes (80 clock pulses total),
; which is sufficient for the SD-card power-up entry into SPI
; mode.
; ----------------------------------------------------------
POWER_UP_SD_CARD:
    MOV  $A, SD_CARD_CS | BLE_CS | MOSI
    OUT  SPI_PORT, $A

    MOV  $D, 10

.START_SPI_LOOP:
    MOV  $A, 0xFF
    JSR  SPI_WRITE_BYTE

    STC
    SUB  $D, 1
    JNZ  .START_SPI_LOOP

    RTS


; ----------------------------------------------------------
; SPI_READ_BYTE
;
; Reads one byte from the selected SPI device.
;
; Returns:
;   $A = received byte
;
; Preserves:
;   caller's $B and $C
;
; Operation summary:
;   - raise SCLK
;   - sample the bus
;   - shift the sampled MISO bit into the result byte in $B
;   - lower SCLK
;   - repeat for 8 bits
; ----------------------------------------------------------
SPI_READ_BYTE:
    PSH  $B
    PSH  $C

    MOV  $C, 8
    MOV  $B, 0
    INP  $A, SPI_PORT
    CLC

.READ_LOOP:
    OR   $A, SCLK
    OUT  SPI_PORT, $A

    INP  $A, SPI_PORT

    ; Shift the current result byte left to make room for the
    ; next bit, then shift the sampled SPI input left so that
    ; the MISO bit reaches carry.
    LSL  $B
    LSL  $A
    ; Add only the carry contribution into the low bit of $B.
    ADD  $B, 0

    ; Restore $A toward its original control-bit alignment.
    LSR  $A

    AND  $A, 0xFF - SCLK
    OUT  SPI_PORT, $A

    STC
    SUB  $C, 1
    JNZ  .READ_LOOP

    MOV  $A, $B

    PUL  $C
    PUL  $B
    RTS


; ----------------------------------------------------------
; SPI_WRITE_BYTE
;
; Input:
;   $A = byte to send
;
; Preserves:
;   caller's $A, $B, $C
;
; Operation summary:
;   - copy the outgoing byte to $B
;   - shift one bit out of $B per iteration
;   - drive MOSI from the carry flag
;   - pulse SCLK high then low
;   - repeat for 8 bits
; ----------------------------------------------------------
SPI_WRITE_BYTE:
    PSH  $A
    PSH  $B
    PSH  $C
    
    MOV  $C, 8
    MOV  $B, $A
    INP  $A, SPI_PORT
    CLC

.SEND_LOOP:
    ; LSL captures the outgoing MSB into carry. The carry bit
    ; is then used to choose the next MOSI level.
    LSL  $B
    JNC  .ZERO_BIT

    OR   $A, MOSI
    JMP  .SHOW_BIT

.ZERO_BIT:
    AND  $A, 0xFF - MOSI

.SHOW_BIT:
    OUT  SPI_PORT, $A

    OR   $A, SCLK
    OUT  SPI_PORT, $A
    AND  $A, 0xFF - SCLK
    OUT  SPI_PORT, $A

    STC
    SUB  $C, 1
    JNZ  .SEND_LOOP

    PUL  $C
    PUL  $B
    PUL  $A
    RTS
