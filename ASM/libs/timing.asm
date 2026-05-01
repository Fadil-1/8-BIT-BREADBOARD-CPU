; ------------------------------------------------------------------------------------
; timing.asm
;
; Generic software delay routines.
; These routines are meant for visible pacing during display/debug programs.
;
; They preserve the registers they use.
; They use NOPs only. They do NOT touch OLED reset logic.
; ------------------------------------------------------------------------------------

; ------------------------------------------------------------------------------------
; DELAY_SHORT
;
; Short visible delay.
; Preserves: $A, $B
; ------------------------------------------------------------------------------------
DELAY_SHORT:
    PSH  $A
    PSH  $B

    MOV  $A, 0x20

.DS_OUTER:
    MOV  $B, 0xFF

.DS_INNER:
    NOP
    NOP
    NOP
    NOP

    STC
    NOP
    SUB  $B, 0x01
    JNZ  .DS_INNER

    STC
    NOP
    SUB  $A, 0x01
    JNZ  .DS_OUTER

    PUL  $B
    PUL  $A
    RTS


; ------------------------------------------------------------------------------------
; DELAY_LONG
;
; Longer visible delay.
; Preserves: $A, $B
; ------------------------------------------------------------------------------------
DELAY_LONG:
    PSH  $A
    PSH  $B

    MOV  $A, 0x60

.DL_OUTER:
    MOV  $B, 0xFF

.DL_INNER:
    NOP
    NOP
    NOP
    NOP

    STC
    NOP
    SUB  $B, 0x01
    JNZ  .DL_INNER

    STC
    NOP
    SUB  $A, 0x01
    JNZ  .DL_OUTER

    PUL  $B
    PUL  $A
    RTS


; ------------------------------------------------------------------------------------
; DELAY_VERY_LONG
;
; Very long visible delay.
; Preserves: $A, $B
; ------------------------------------------------------------------------------------
DELAY_VERY_LONG:
    PSH  $A
    PSH  $B

    MOV  $A, 0xC0

.DVL_OUTER:
    MOV  $B, 0xFF

.DVL_INNER:
    NOP
    NOP
    NOP
    NOP

    STC
    NOP
    SUB  $B, 0x01
    JNZ  .DVL_INNER

    STC
    NOP
    SUB  $A, 0x01
    JNZ  .DVL_OUTER

    PUL  $B
    PUL  $A
    RTS


; ------------------------------------------------------------------------------------
; DELAY_VERY_VERY_LONG
;
; Very, very long visible delay.
; Preserves: $A, $B, $C
; ------------------------------------------------------------------------------------
DELAY_VERY_VERY_LONG:
    PSH  $A
    PSH  $B
    PSH  $C

    MOV  $C, 0x04

.DVVL_SUPER:
    MOV  $A, 0xFF

.DVVL_OUTER:
    MOV  $B, 0xFF

.DVVL_INNER:
    NOP
    NOP
    NOP
    NOP

    STC
    NOP
    SUB  $B, 0x01
    JNZ  .DVVL_INNER

    STC
    NOP
    SUB  $A, 0x01
    JNZ  .DVVL_OUTER

    STC
    NOP
    SUB  $C, 0x01
    JNZ  .DVVL_SUPER

    PUL  $C
    PUL  $B
    PUL  $A
    RTS
