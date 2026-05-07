; ==========================================================
; monitor_core.asm
; ==========================================================
; Monitor startup helpers.
;
; Original version: April 2026
; Last Modified: May 2026
; Fadil Isamotu
; ==========================================================

; ----------------------------------------------------------
; MONITOR_INIT
;
; Initializes the OLED terminal and monitor state.
; ----------------------------------------------------------
MONITOR_INIT:
    ; Full speed: 111 = 2.2 MHz.
    MOV $CLK, 0x07

    JSR OLED_INIT
    JSR OLED5_SET_DEFAULT_ORIGIN
    JSR OLED5_HOME
    JSR OLED5_CLEAR_TEXT_SCREEN
    JSR OLED5_HOME

    JSR MON_INPUT_RESET
    JSR MON_REG_RESET
    JSR MON_PREP_COMMAND_STRINGS

    RTS


; ----------------------------------------------------------
; MONITOR_READY
;
; Prints a fresh monitor prompt.
; ----------------------------------------------------------
MONITOR_READY:
    JSR MON_PRINT_FRESH_PROMPT
    RTS
