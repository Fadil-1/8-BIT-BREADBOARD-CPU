; ==========================================================
; oled_graphics.asm
; ==========================================================
; SSD1325 graphics helpers for OS-style OLED screens.
;
; Coordinate model:
;   X uses grouped SSD1325 columns, 0..63.
;   one grouped column = two horizontal pixels.
;   Y uses raw pixel rows, 0..62.
;
; Shared rectangle arguments:
;   OLED_ARG_X      grouped column start
;   OLED_ARG_Y      raw row start
;   OLED_ARG_W      grouped column count
;   OLED_ARG_H      raw row count
;   OLED_ARG_COLOR  packed grayscale byte
;
; Caller notes:
;   W and H must be nonzero for drawing routines.
;   Keep rectangles inside columns 0..63 and rows 0..62.
;   Raw row 63 is left unused by these helpers.
; ==========================================================

; ---------- graphics scratch ----------
OLEDG_SAVE_X          = 0x7330
OLEDG_SAVE_Y          = 0x7331
OLEDG_SAVE_W          = 0x7332
OLEDG_SAVE_H          = 0x7333
OLEDG_SAVE_COLOR      = 0x7334
OLEDG_TMP0            = 0x7335
OLEDG_TMP1            = 0x7336
OLEDG_PROGRESS_VALUE  = 0x7337
OLEDG_PROGRESS_COLOR  = 0x7338

OLEDG_SAFE_COLS       = 0x40
OLEDG_SAFE_ROWS       = 0x3F
OLEDG_SAFE_ROW_END    = 0x3E
OLEDG_BLACK_BYTE      = 0x00
OLEDG_DIM_BYTE        = 0x44
OLEDG_BRIGHT_BYTE     = 0xFF

; ==========================================================
; Low-level window helpers
; ==========================================================

OLEDG_SET_WINDOW_ARGS:
    ; Window from OLED_ARG_X/Y/W/H.
    PSH $A

    MOV $A, 0x15
    OLC $A
    MOV $A, OLED_ARG_X
    OLC $A
    MOV $A, OLED_ARG_W
    STC
    NOP
    SUB $A, 0x01
    CLC
    NOP
    ADD $A, OLED_ARG_X
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, OLED_ARG_Y
    OLC $A
    MOV $A, OLED_ARG_H
    STC
    NOP
    SUB $A, 0x01
    CLC
    NOP
    ADD $A, OLED_ARG_Y
    OLC $A

    PUL $A
    RTS

OLEDG_BEGIN_SAFE_FRAME:
    ; Full safe drawing window, rows 0 through 62.
    MOV $A, 0x15
    OLC $A
    MOV $A, 0x00
    OLC $A
    MOV $A, 0x3F
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, 0x00
    OLC $A
    MOV $A, OLEDG_SAFE_ROW_END
    OLC $A

    MOV $A, 0x5C
    OLC $A
    RTS

; ==========================================================
; Filled regions and clears
; ==========================================================

OLEDG_CLEAR_SAFE_AREA:
    ; Clear grouped columns 0..63 and rows 0..62.
    PSH $A
    PSH $B
    PSH $D

    JSR OLEDG_BEGIN_SAFE_FRAME

    MOV $A, OLEDG_BLACK_BYTE
    MOV $D, OLEDG_SAFE_ROWS

.OLEDG_CLEAR_SAFE_ROW:
    MOV $B, OLEDG_SAFE_COLS

.OLEDG_CLEAR_SAFE_COL:
    OLD $A
    STC
    NOP
    SUB $B, 0x01
    JNZ .OLEDG_CLEAR_SAFE_COL

    STC
    NOP
    SUB $D, 0x01
    JNZ .OLEDG_CLEAR_SAFE_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLEDG_FILL_RECT:
    ; Fill the rectangle described by OLED_ARG_X/Y/W/H.
    PSH $A
    PSH $B
    PSH $D

    MOV $A, OLED_ARG_W
    STC
    NOP
    CMP $A, 0x00
    JZ OLEDG_FILL_RECT_DONE

    MOV $A, OLED_ARG_H
    STC
    NOP
    CMP $A, 0x00
    JZ OLEDG_FILL_RECT_DONE

    JSR OLEDG_SET_WINDOW_ARGS

    MOV $A, 0x5C
    OLC $A

    MOV $D, OLED_ARG_H
    MOV $A, OLED_ARG_COLOR

.OLEDG_FILL_RECT_ROW:
    MOV $B, OLED_ARG_W

.OLEDG_FILL_RECT_COL:
    OLD $A
    STC
    NOP
    SUB $B, 0x01
    JNZ .OLEDG_FILL_RECT_COL

    STC
    NOP
    SUB $D, 0x01
    JNZ .OLEDG_FILL_RECT_ROW

OLEDG_FILL_RECT_DONE:
    PUL $D
    PUL $B
    PUL $A
    RTS

OLEDG_CLEAR_RECT:
    ; Clear the current rectangle, then restore OLED_ARG_COLOR.
    PSH $A

    MOV $A, OLED_ARG_COLOR
    MOV OLEDG_TMP0, $A

    MOV $A, OLEDG_BLACK_BYTE
    MOV OLED_ARG_COLOR, $A
    JSR OLEDG_FILL_RECT

    MOV $A, OLEDG_TMP0
    MOV OLED_ARG_COLOR, $A

    PUL $A
    RTS

OLEDG_HIGHLIGHT_RECT:
    ; Fill the current rectangle with a medium-gray UI highlight.
    PSH $A

    MOV $A, OLED_ARG_COLOR
    MOV OLEDG_TMP0, $A

    MOV $A, OLEDG_DIM_BYTE
    MOV OLED_ARG_COLOR, $A
    JSR OLEDG_FILL_RECT

    MOV $A, OLEDG_TMP0
    MOV OLED_ARG_COLOR, $A

    PUL $A
    RTS

; ==========================================================
; Lines and rectangle outlines
; ==========================================================

OLEDG_DRAW_HLINE:
    ; Draw a one-row horizontal line. W gives the line length.
    PSH $A

    MOV $A, OLED_ARG_H
    MOV OLEDG_TMP0, $A

    MOV $A, 0x01
    MOV OLED_ARG_H, $A
    JSR OLEDG_FILL_RECT

    MOV $A, OLEDG_TMP0
    MOV OLED_ARG_H, $A

    PUL $A
    RTS

OLEDG_DRAW_VLINE:
    ; Draw a one-column vertical line. H gives the line height.
    PSH $A

    MOV $A, OLED_ARG_W
    MOV OLEDG_TMP0, $A

    MOV $A, 0x01
    MOV OLED_ARG_W, $A
    JSR OLEDG_FILL_RECT

    MOV $A, OLEDG_TMP0
    MOV OLED_ARG_W, $A

    PUL $A
    RTS

OLEDG_SAVE_RECT_ARGS:
    MOV $A, OLED_ARG_X
    MOV OLEDG_SAVE_X, $A
    MOV $A, OLED_ARG_Y
    MOV OLEDG_SAVE_Y, $A
    MOV $A, OLED_ARG_W
    MOV OLEDG_SAVE_W, $A
    MOV $A, OLED_ARG_H
    MOV OLEDG_SAVE_H, $A
    MOV $A, OLED_ARG_COLOR
    MOV OLEDG_SAVE_COLOR, $A
    RTS

OLEDG_RESTORE_RECT_ARGS:
    MOV $A, OLEDG_SAVE_X
    MOV OLED_ARG_X, $A
    MOV $A, OLEDG_SAVE_Y
    MOV OLED_ARG_Y, $A
    MOV $A, OLEDG_SAVE_W
    MOV OLED_ARG_W, $A
    MOV $A, OLEDG_SAVE_H
    MOV OLED_ARG_H, $A
    MOV $A, OLEDG_SAVE_COLOR
    MOV OLED_ARG_COLOR, $A
    RTS

OLEDG_DRAW_RECT:
    ; Draw the outline of the current rectangle.
    JSR OLEDG_SAVE_RECT_ARGS

    ; top edge
    JSR OLEDG_DRAW_HLINE

    ; bottom edge
    MOV $A, OLEDG_SAVE_H
    STC
    NOP
    CMP $A, 0x01
    JZ OLEDG_DRAW_RECT_SKIP_BOTTOM

    MOV $A, OLEDG_SAVE_H
    STC
    NOP
    SUB $A, 0x01
    CLC
    NOP
    ADD $A, OLEDG_SAVE_Y
    MOV OLED_ARG_Y, $A
    MOV $A, OLEDG_SAVE_X
    MOV OLED_ARG_X, $A
    MOV $A, OLEDG_SAVE_W
    MOV OLED_ARG_W, $A
    JSR OLEDG_DRAW_HLINE

OLEDG_DRAW_RECT_SKIP_BOTTOM:
    ; left edge
    MOV $A, OLEDG_SAVE_X
    MOV OLED_ARG_X, $A
    MOV $A, OLEDG_SAVE_Y
    MOV OLED_ARG_Y, $A
    MOV $A, OLEDG_SAVE_H
    MOV OLED_ARG_H, $A
    JSR OLEDG_DRAW_VLINE

    ; right edge
    MOV $A, OLEDG_SAVE_W
    STC
    NOP
    CMP $A, 0x01
    JZ OLEDG_DRAW_RECT_DONE

    MOV $A, OLEDG_SAVE_W
    STC
    NOP
    SUB $A, 0x01
    CLC
    NOP
    ADD $A, OLEDG_SAVE_X
    MOV OLED_ARG_X, $A
    MOV $A, OLEDG_SAVE_Y
    MOV OLED_ARG_Y, $A
    MOV $A, OLEDG_SAVE_H
    MOV OLED_ARG_H, $A
    JSR OLEDG_DRAW_VLINE

OLEDG_DRAW_RECT_DONE:
    JSR OLEDG_RESTORE_RECT_ARGS
    RTS

; ==========================================================
; OS UI helpers
; ==========================================================

OLEDG_DRAW_CURSOR_BLOCK:
    ; Draw a block cursor using OLED_ARG_X/Y/W/H.
    PSH $A

    MOV $A, OLED_ARG_COLOR
    MOV OLEDG_TMP0, $A

    MOV $A, OLEDG_BRIGHT_BYTE
    MOV OLED_ARG_COLOR, $A
    JSR OLEDG_FILL_RECT

    MOV $A, OLEDG_TMP0
    MOV OLED_ARG_COLOR, $A

    PUL $A
    RTS

OLEDG_CLEAR_CURSOR_BLOCK:
    ; Clear a block cursor using OLED_ARG_X/Y/W/H.
    JSR OLEDG_CLEAR_RECT
    RTS

OLEDG_DRAW_PROGRESS_BAR:
    ; Draw a framed progress bar.
    ; OLEDG_PROGRESS_VALUE gives the filled inner width.
    ; OLEDG_PROGRESS_COLOR gives the fill byte.
    JSR OLEDG_SAVE_RECT_ARGS

    JSR OLEDG_DRAW_RECT

    ; Clear the bar interior.
    MOV $A, OLEDG_SAVE_X
    CLC
    NOP
    ADD $A, 0x01
    MOV OLED_ARG_X, $A

    MOV $A, OLEDG_SAVE_Y
    CLC
    NOP
    ADD $A, 0x01
    MOV OLED_ARG_Y, $A

    MOV $A, OLEDG_SAVE_W
    STC
    NOP
    SUB $A, 0x02
    MOV OLED_ARG_W, $A

    MOV $A, OLEDG_SAVE_H
    STC
    NOP
    SUB $A, 0x02
    MOV OLED_ARG_H, $A

    JSR OLEDG_CLEAR_RECT

    ; Draw the filled part.
    MOV $A, OLEDG_PROGRESS_VALUE
    STC
    NOP
    CMP $A, 0x00
    JZ OLEDG_DRAW_PROGRESS_BAR_DONE

    MOV OLED_ARG_W, $A
    MOV $A, OLEDG_PROGRESS_COLOR
    MOV OLED_ARG_COLOR, $A
    JSR OLEDG_FILL_RECT

OLEDG_DRAW_PROGRESS_BAR_DONE:
    JSR OLEDG_RESTORE_RECT_ARGS
    RTS
