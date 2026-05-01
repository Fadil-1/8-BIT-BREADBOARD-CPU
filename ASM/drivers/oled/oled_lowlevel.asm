; ==========================================================
; oled_lowlevel.asm
; ==========================================================
; SSD1325 OLED initialization.
; ==========================================================

OLED_INIT:
    OLR

    ; Display off while configuring the controller.
    MOV $A, 0xAE
    OLC $A

    ; Full column address range, grouped columns 0..63.
    MOV $A, 0x15
    OLC $A
    MOV $A, 0x00
    OLC $A
    MOV $A, 0x3F
    OLC $A

    ; Full row address range, rows 0..63.
    MOV $A, 0x75
    OLC $A
    MOV $A, 0x00
    OLC $A
    MOV $A, 0x3F
    OLC $A

    ; Contrast.
    MOV $A, 0x81
    OLC $A
    MOV $A, 0x7F
    OLC $A

    ; Remap / address mode.
    ; 0x52 selects the pixel packing used by the text layer.
    MOV $A, 0xA0
    OLC $A
    MOV $A, 0x52
    OLC $A

    ; Display start line.
    MOV $A, 0xA1
    OLC $A
    MOV $A, 0x00
    OLC $A

    ; Display offset.
    MOV $A, 0xA2
    OLC $A
    MOV $A, 0x4B
    OLC $A

    ; Normal display mode using RAM contents.
    MOV $A, 0xA4
    OLC $A

    ; Range / grayscale mode setting.
    MOV $A, 0x86
    OLC $A

    ; Clock divide / oscillator frequency.
    MOV $A, 0xB3
    OLC $A
    MOV $A, 0xF1
    OLC $A

    ; Multiplex ratio.
    MOV $A, 0xA8
    OLC $A
    MOV $A, 0x3F
    OLC $A

    ; Display on.
    MOV $A, 0xAF
    OLC $A

    RTS
