#!/usr/bin/env python3
# ==========================================================
# make_oled_text_4x6_library.py
# ==========================================================
# Generates oled_text_4x6.asm.
#
# Purpose:
#   Generate the compact SSD1325 4x6 text/terminal assembly library.
#
# OLED pixel packing:
#   OLED_INIT uses the SSD1325 remap setting A0h = 0x52.
#   Each display data byte contains two horizontal pixels:
#
#       left pixel  -> high nibble
#       right pixel -> low nibble
#
# Text cell format:
#   - visible glyph area: 4x6 pixels
#   - terminal cell size: 4x7 pixels
#   - one vertical spacer row per cell
#   - two SSD1325 data bytes per text row
#   - seven pixel rows per character cell
#   - 32 columns by 9 rows
#   - raw pixel row 63 left unused by normal text
#
# Runtime string behavior:
#   - string pointer passed through $C/$D
#   - $C = low byte of address
#   - $D = high byte of address
#   - strings are null-terminated
#   - newline is 0x0A
#   - printable ASCII coverage from 0x20 through 0x7E
#
# Font source:
#   Project compact 4x6 font table, tested first on Arduino.
#
# Original version: May 2026
# Fadil Isamotu
# ==========================================================

from pathlib import Path

LIB_OUT = "oled_text_4x6.asm"

FG_NIBBLE = 0xA
BG_NIBBLE = 0x0

# Each glyph row is four bits. Bit 3 is the leftmost pixel.
FONT4X6 = {
    " ": [0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
    "-": [0x0, 0x0, 0xF, 0x0, 0x0, 0x0],
    ":": [0x0, 0x6, 0x6, 0x0, 0x6, 0x6],
    "#": [0x5, 0xF, 0x5, 0xF, 0x5, 0x0],
    ">": [0x8, 0x4, 0x2, 0x4, 0x8, 0x0],
    "=": [0x0, 0xF, 0x0, 0xF, 0x0, 0x0],
    "?": [0x6, 0x9, 0x1, 0x2, 0x0, 0x2],
    ".": [0x0, 0x0, 0x0, 0x0, 0x6, 0x6],
    "/": [0x1, 0x1, 0x2, 0x4, 0x8, 0x8],
    "_": [0x0, 0x0, 0x0, 0x0, 0x0, 0xF],

    "0": [0x6, 0x9, 0xB, 0xD, 0x9, 0x6],
    "1": [0x2, 0x6, 0x2, 0x2, 0x2, 0x7],
    "2": [0x6, 0x9, 0x1, 0x2, 0x4, 0xF],
    "3": [0xE, 0x1, 0x6, 0x1, 0x9, 0x6],
    "4": [0x2, 0x6, 0xA, 0xF, 0x2, 0x2],
    "5": [0xF, 0x8, 0xE, 0x1, 0x9, 0x6],
    "6": [0x6, 0x8, 0xE, 0x9, 0x9, 0x6],
    "7": [0xF, 0x1, 0x2, 0x4, 0x4, 0x4],
    "8": [0x6, 0x9, 0x6, 0x9, 0x9, 0x6],
    "9": [0x6, 0x9, 0x9, 0x7, 0x1, 0x6],

    "A": [0x6, 0x9, 0x9, 0xF, 0x9, 0x9],
    "B": [0xE, 0x9, 0xE, 0x9, 0x9, 0xE],
    "C": [0x7, 0x8, 0x8, 0x8, 0x8, 0x7],
    "D": [0xE, 0x9, 0x9, 0x9, 0x9, 0xE],
    "E": [0xF, 0x8, 0xE, 0x8, 0x8, 0xF],
    "F": [0xF, 0x8, 0xE, 0x8, 0x8, 0x8],
    "G": [0x7, 0x8, 0xB, 0x9, 0x9, 0x7],
    "H": [0x9, 0x9, 0xF, 0x9, 0x9, 0x9],
    "I": [0x7, 0x2, 0x2, 0x2, 0x2, 0x7],
    "J": [0x1, 0x1, 0x1, 0x9, 0x9, 0x6],
    "K": [0x9, 0xA, 0xC, 0xA, 0xA, 0x9],
    "L": [0x8, 0x8, 0x8, 0x8, 0x8, 0xF],
    "M": [0x9, 0xF, 0xF, 0x9, 0x9, 0x9],
    "N": [0x9, 0xD, 0xB, 0x9, 0x9, 0x9],
    "O": [0x6, 0x9, 0x9, 0x9, 0x9, 0x6],
    "P": [0xE, 0x9, 0x9, 0xE, 0x8, 0x8],
    "Q": [0x6, 0x9, 0x9, 0xB, 0xD, 0x7],
    "R": [0xE, 0x9, 0x9, 0xE, 0xA, 0x9],
    "S": [0x7, 0x8, 0x6, 0x1, 0x9, 0x6],
    "T": [0xF, 0x2, 0x2, 0x2, 0x2, 0x2],
    "U": [0x9, 0x9, 0x9, 0x9, 0x9, 0x6],
    "V": [0x9, 0x9, 0x9, 0x9, 0x6, 0x6],
    "W": [0x9, 0x9, 0x9, 0xF, 0xF, 0x9],
    "X": [0x9, 0x9, 0x6, 0x6, 0x9, 0x9],
    "Y": [0x9, 0x9, 0x6, 0x2, 0x2, 0x2],
    "Z": [0xF, 0x1, 0x2, 0x4, 0x8, 0xF],

    "!": [0x4, 0x4, 0x4, 0x4, 0x0, 0x4],
    "\"": [0xA, 0xA, 0x0, 0x0, 0x0, 0x0],
    "$": [0x7, 0xA, 0x6, 0x3, 0xA, 0xE],
    "%": [0x9, 0x1, 0x2, 0x4, 0x8, 0x9],
    "&": [0x6, 0x9, 0x6, 0xA, 0x9, 0x7],
    "'": [0x4, 0x4, 0x0, 0x0, 0x0, 0x0],
    "(": [0x2, 0x4, 0x8, 0x8, 0x4, 0x2],
    ")": [0x8, 0x4, 0x2, 0x2, 0x4, 0x8],
    "*": [0x0, 0xA, 0x4, 0xE, 0x4, 0xA],
    "+": [0x0, 0x4, 0x4, 0xE, 0x4, 0x4],
    ",": [0x0, 0x0, 0x0, 0x0, 0x4, 0x8],
    ";": [0x0, 0x4, 0x0, 0x0, 0x4, 0x8],
    "<": [0x1, 0x2, 0x4, 0x8, 0x4, 0x2],
    "@": [0x6, 0x9, 0xB, 0xB, 0x8, 0x7],
    "[": [0xE, 0x8, 0x8, 0x8, 0x8, 0xE],
    "\\": [0x8, 0x8, 0x4, 0x2, 0x1, 0x1],
    "]": [0xE, 0x2, 0x2, 0x2, 0x2, 0xE],
    "^": [0x4, 0xA, 0x0, 0x0, 0x0, 0x0],
    "`": [0x8, 0x4, 0x0, 0x0, 0x0, 0x0],
    "{": [0x3, 0x4, 0xC, 0x4, 0x4, 0x3],
    "|": [0x4, 0x4, 0x4, 0x4, 0x4, 0x4],
    "}": [0xC, 0x2, 0x3, 0x2, 0x2, 0xC],
    "~": [0x0, 0x5, 0xA, 0x0, 0x0, 0x0],
}

LABEL_NAMES = {
    " ": "SPACE",
    "!": "EXCLAMATION",
    "\"": "DOUBLE_QUOTE",
    "#": "HASH",
    "$": "DOLLAR",
    "%": "PERCENT",
    "&": "AMPERSAND",
    "'": "APOSTROPHE",
    "(": "LPAREN",
    ")": "RPAREN",
    "*": "ASTERISK",
    "+": "PLUS",
    ",": "COMMA",
    "-": "DASH",
    ".": "DOT",
    "/": "SLASH",
    ":": "COLON",
    ";": "SEMICOLON",
    "<": "LT",
    "=": "EQUALS",
    ">": "GT",
    "?": "QUESTION",
    "@": "AT",
    "[": "LBRACKET",
    "\\": "BACKSLASH",
    "]": "RBRACKET",
    "^": "CARET",
    "_": "UNDERSCORE",
    "`": "BACKTICK",
    "{": "LBRACE",
    "|": "PIPE",
    "}": "RBRACE",
    "~": "TILDE",
}

ORDER_GROUP_1 = [" "] + list("0123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SYMBOLS = ["!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]
CHAR_ORDER = ORDER_GROUP_1 + SYMBOLS
LOWERCASE_ORDER = list("abcdefghijklmnopqrstuvwxyz")

assert len(set(CHAR_ORDER)) == len(CHAR_ORDER)
assert all(ch in FONT4X6 for ch in CHAR_ORDER)

POST_GLYPH_ROUTINES = """; ==========================================================
; Terminal helper routines
; ==========================================================

OLED4_HOME:
    MOV $A, 0x00
    MOV OLED_CURSOR_COL, $A
    MOV OLED_CURSOR_ROW, $A
    MOV OLED4_PENDING_WRAP, $A
    RTS

OLED4_SET_DEFAULT_ORIGIN:
    MOV $A, OLED4_DEFAULT_X
    MOV OLED_TEXT_ORIGIN_X, $A
    MOV $A, OLED4_DEFAULT_Y
    MOV OLED_TEXT_ORIGIN_Y, $A
    RTS

OLED4_CLEAR_TEXT_SCREEN:
    PSH $A
    PSH $B
    PSH $D

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
    MOV $A, OLED4_SAFE_MAX_RAW_ROW
    OLC $A

    MOV $A, 0x5C
    OLC $A

    MOV $A, 0x00
    MOV $D, OLED4_CLEAR_ROWS

.OLED4_CLEAR_TEXT_ROW:
    MOV $B, OLED4_CLEAR_COLS

.OLED4_CLEAR_TEXT_COL:
    OLD $A
    STC
    SUB $B, 0x01
    JNZ .OLED4_CLEAR_TEXT_COL

    STC
    SUB $D, 0x01
    JNZ .OLED4_CLEAR_TEXT_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED4_PUTC:
    STC
    CMP $A, 0x0A
    JZ OLED4_PUTC_NEWLINE

    STC
    CMP $A, 0x0D
    JZ OLED4_PUTC_CR

    STC
    CMP $A, 0x08
    JZ OLED4_PUTC_BACKSPACE

    MOV OLED_CHAR_TMP, $A
    JSR OLED4_APPLY_PENDING_WRAP
    MOV $A, OLED_CHAR_TMP
    JSR OLED4_DRAW_CHAR
    RTS

OLED4_PUTC_NEWLINE:
    JSR OLED4_NEWLINE
    RTS

OLED4_PUTC_CR:
    JSR OLED4_CARRIAGE_RETURN
    RTS

OLED4_PUTC_BACKSPACE:
    JSR OLED4_BACKSPACE
    RTS

OLED4_CARRIAGE_RETURN:
    MOV $A, 0x00
    MOV OLED_CURSOR_COL, $A
    MOV OLED4_PENDING_WRAP, $A
    RTS

OLED4_BACKSPACE:
    MOV $A, OLED4_PENDING_WRAP
    STC
    CMP $A, 0x00
    JNZ .OLED4_BACKSPACE_CLEAR_CURRENT

    MOV $A, OLED_CURSOR_COL
    STC
    CMP $A, 0x00
    JZ OLED4_BACKSPACE_DONE

    STC
    SUB $A, 0x01
    MOV OLED_CURSOR_COL, $A

.OLED4_BACKSPACE_CLEAR_CURRENT:
    MOV $A, 0x00
    MOV OLED4_PENDING_WRAP, $A
    JSR OLED4_CLEAR_CURRENT_CELL_DIRECT

OLED4_BACKSPACE_DONE:
    RTS

OLED4_APPLY_PENDING_WRAP:
    MOV $A, OLED4_PENDING_WRAP
    STC
    CMP $A, 0x00
    JNZ .OLED4_APPLY_WRAP

    RTS

.OLED4_APPLY_WRAP:
    MOV $A, 0x00
    MOV OLED4_PENDING_WRAP, $A
    MOV OLED_CURSOR_COL, $A

    MOV $A, OLED_CURSOR_ROW
    CLC
    ADD $A, 0x01
    MOV OLED_CURSOR_ROW, $A

    STC
    CMP $A, OLED4_MAX_ROWS
    JZ .OLED4_APPLY_WRAP_TOP

    RTS

.OLED4_APPLY_WRAP_TOP:
    MOV $A, 0x00
    MOV OLED_CURSOR_ROW, $A
    RTS

OLED4_CLEAR_CURRENT_CELL_DIRECT:
    PSH $A
    PSH $B
    PSH $D

    JSR OLED4_COMPUTE_CURSOR_BASE

    MOV $A, 0x15
    OLC $A
    MOV $A, OLED_GLYPH_BASE_X
    OLC $A
    CLC
    ADD $A, 0x01
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, OLED_GLYPH_BASE_Y
    OLC $A
    CLC
    ADD $A, 0x06
    OLC $A

    MOV $A, 0x5C
    OLC $A
    MOV $A, 0x00
    MOV $D, OLED4_CELL_H

.OLED4_CLEAR_CELL_ROW:
    MOV $B, OLED4_CELL_BYTES

.OLED4_CLEAR_CELL_COL:
    OLD $A
    STC
    SUB $B, 0x01
    JNZ .OLED4_CLEAR_CELL_COL

    STC
    SUB $D, 0x01
    JNZ .OLED4_CLEAR_CELL_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED4_DRAW_CURRENT_CELL_BLOCK_DIRECT:
    PSH $A
    PSH $B
    PSH $D

    JSR OLED4_COMPUTE_CURSOR_BASE

    MOV $A, 0x15
    OLC $A
    MOV $A, OLED_GLYPH_BASE_X
    OLC $A
    CLC
    ADD $A, 0x01
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, OLED_GLYPH_BASE_Y
    OLC $A
    CLC
    ADD $A, 0x06
    OLC $A

    MOV $A, 0x5C
    OLC $A
    MOV $A, 0xFF
    MOV $D, OLED4_CELL_H

.OLED4_DRAW_CELL_BLOCK_ROW:
    MOV $B, OLED4_CELL_BYTES

.OLED4_DRAW_CELL_BLOCK_COL:
    OLD $A
    STC
    SUB $B, 0x01
    JNZ .OLED4_DRAW_CELL_BLOCK_COL

    STC
    SUB $D, 0x01
    JNZ .OLED4_DRAW_CELL_BLOCK_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED4_CURSOR_SHOW:
    JSR OLED4_DRAW_CURRENT_CELL_BLOCK_DIRECT
    RTS

OLED4_CURSOR_HIDE:
    JSR OLED4_CLEAR_CURRENT_CELL_DIRECT
    RTS

OLED4_TYPE_CHAR_WITH_CURSOR:
    MOV OLED_CHAR_TMP, $A
    JSR OLED4_CURSOR_HIDE
    MOV $A, OLED_CHAR_TMP
    JSR OLED4_PUTC
    JSR OLED4_CURSOR_SHOW
    RTS

OLED4_PRINT_HEX_NIBBLE:
    STC
    CMP $A, 0x0A
    JC .OLED4_HEX_LETTER

.OLED4_HEX_DIGIT:
    CLC
    ADD $A, 0x30
    JSR OLED4_PUTC
    RTS

.OLED4_HEX_LETTER:
    STC
    SUB $A, 0x0A
    CLC
    ADD $A, 0x41
    JSR OLED4_PUTC
    RTS

OLED4_PRINT_HEX_BYTE:
    MOV OLED_HEX_TMP, $A
    AND $A, 0xF0
    LSR $A
    LSR $A
    LSR $A
    LSR $A
    JSR OLED4_PRINT_HEX_NIBBLE

    MOV $A, OLED_HEX_TMP
    AND $A, 0x0F
    JSR OLED4_PRINT_HEX_NIBBLE
    RTS

OLED4_PRINT_HEX_WORD_CD:
    MOV OLED_HEX_WORD_LO, $C
    MOV OLED_HEX_WORD_HI, $D

    MOV $A, OLED_HEX_WORD_HI
    JSR OLED4_PRINT_HEX_BYTE

    MOV $A, OLED_HEX_WORD_LO
    JSR OLED4_PRINT_HEX_BYTE
    RTS"""


def label_for_char(ch: str) -> str:
    if ch in LABEL_NAMES:
        return LABEL_NAMES[ch]
    if ch.isdigit():
        return f"DIGIT_{ch}"
    return ch


def comment_for_char(ch: str) -> str:
    if ch == " ":
        return "; Character: SPACE (' ')"
    return f"; Character: {ch}"


def cmp_comment_for_char(ch: str) -> str:
    if ch == " ":
        return "SPACE"
    return ch


def pack_pair(left_on: int, right_on: int) -> int:
    lo = FG_NIBBLE if right_on else BG_NIBBLE
    hi = FG_NIBBLE if left_on else BG_NIBBLE
    return (hi << 4) | lo


def glyph_rows(ch: str):
    rows = FONT4X6[ch]

    for row_bits in rows:
        yield [
            pack_pair(row_bits & 0x8, row_bits & 0x4),
            pack_pair(row_bits & 0x2, row_bits & 0x1),
        ]

    yield [0x00, 0x00]


def emit_mov_old(lines: list[str], value: int) -> None:
    lines.append(f"    MOV $A, 0x{value:02X}")
    lines.append("    OLD $A")


def emit_glyph_routine(lines: list[str], ch: str) -> None:
    label = label_for_char(ch)

    lines.extend([
        "",
        comment_for_char(ch),
        f"OLED4_CHAR_{label}:",
        "    JSR OLED4_RENDER_BEGIN",
    ])

    for row_bytes in glyph_rows(ch):
        for b in row_bytes:
            emit_mov_old(lines, b)

    lines.extend([
        "    JSR OLED4_ADVANCE_CURSOR",
        "    RTS",
    ])


def build_library() -> str:
    lines: list[str] = []

    lines.extend([
        "; ==========================================================",
        "; oled_text_4x6.asm",
        "; ==========================================================",
        "; Generated by make_oled_text_4x6_library.py",
        "; SSD1325 compact 4x6 monitor text layer.",
        ";",
        "; Cell size:",
        ";   4 pixels wide  = 2 grouped SSD1325 columns",
        ";   7 pixels tall  = 6 font rows + 1 spacer row",
        ";",
        "; Pixel packing for OLED_INIT / A0h = 0x52:",
        ";   left pixel  -> high nibble",
        ";   right pixel -> low nibble",
        ";",
        "; Safe drawing area:",
        ";   text rows use raw pixel rows 0 through 62",
        ";   raw pixel row 63 is left unused by normal text",
        ";",
        "; API:",
        ";   OLED4_SET_CURSOR",
        ";   OLED4_DRAW_CHAR",
        ";   OLED4_DRAW_STRING",
        ";   OLED4_PUTC",
        ";",
        "; Calling convention:",
        ";   OLED4_SET_CURSOR:",
        ";       A = column",
        ";       B = row",
        ";",
        ";   OLED4_DRAW_CHAR:",
        ";       A = ASCII character",
        ";",
        ";   OLED4_DRAW_STRING:",
        ";       CD = pointer to null-terminated RAM string",
        ";       newline = 0x0A",
        "; ==========================================================",
        "",
        "; ---------- 4x6 terminal geometry ----------",
        "OLED4_MAX_COLS         = 0x20",
        "OLED4_MAX_ROWS         = 0x09",
        "OLED4_LAST_COL         = 0x1F",
        "OLED4_CELL_BYTES       = 0x02",
        "OLED4_CELL_H           = 0x07",
        "OLED4_DEFAULT_X        = 0x00",
        "OLED4_DEFAULT_Y        = 0x00",
        "OLED4_CLEAR_COLS       = 0x40",
        "OLED4_CLEAR_ROWS       = 0x3F",
        "OLED4_SAFE_MAX_RAW_ROW = 0x3E",
        "OLED4_PENDING_WRAP     = 0x701F",
        "",
        "OLED4_SET_CURSOR:",
        "    ; in: A = col, B = row",
        "    MOV OLED_CURSOR_COL, $A",
        "    MOV OLED_CURSOR_ROW, $B",
        "    MOV $A, 0x00",
        "    MOV OLED4_PENDING_WRAP, $A",
        "    RTS",
        "",
        "OLED4_NEWLINE:",
        "    MOV $A, 0x00",
        "    MOV OLED_CURSOR_COL, $A",
        "    MOV OLED4_PENDING_WRAP, $A",
        "",
        "    MOV $A, OLED_CURSOR_ROW",
        "    CLC",
        "    ADD $A, 0x01",
        "    MOV OLED_CURSOR_ROW, $A",
        "",
        "    STC",
        "    CMP $A, OLED4_MAX_ROWS",
        "    JZ OLED4_NEWLINE_WRAP_TOP",
        "",
        "    RTS",
        "",
        "OLED4_NEWLINE_WRAP_TOP:",
        "    MOV $A, 0x00",
        "    MOV OLED_CURSOR_ROW, $A",
        "    RTS",
        "",
        "OLED4_ADVANCE_CURSOR:",
        "    MOV $A, OLED_CURSOR_COL",
        "    STC",
        "    CMP $A, OLED4_LAST_COL",
        "    JZ OLED4_ADVANCE_CURSOR_PENDING",
        "",
        "    CLC",
        "    ADD $A, 0x01",
        "    MOV OLED_CURSOR_COL, $A",
        "    RTS",
        "",
        "OLED4_ADVANCE_CURSOR_PENDING:",
        "    MOV $A, 0x01",
        "    MOV OLED4_PENDING_WRAP, $A",
        "    RTS",
        "",
        "OLED4_INC_CD:",
        "    CLC",
        "    ADD $C, 0x01",
        "    JNC OLED4_INC_CD_DONE",
        "",
        "    CLC",
        "    ADD $D, 0x01",
        "",
        "OLED4_INC_CD_DONE:",
        "    RTS",
        "",
        "OLED4_DRAW_STRING:",
        "OLED4_DRAW_STRING_LOOP:",
        "    MOV $A, [$CD]",
        "",
        "    STC",
        "    CMP $A, 0x00",
        "    JZ OLED4_DRAW_STRING_DONE",
        "",
        "    JSR OLED4_PUTC",
        "    JSR OLED4_INC_CD",
        "    JMP OLED4_DRAW_STRING_LOOP",
        "",
        "OLED4_DRAW_STRING_DONE:",
        "    RTS",
        "",
        "OLED4_DRAW_CHAR:",
        "    MOV OLED_CHAR_TMP, $A",
        "",
    ])

    for ch in CHAR_ORDER:
        label = label_for_char(ch)
        lines.extend([
            "    MOV $A, OLED_CHAR_TMP",
            "    STC",
            f"    CMP $A, 0x{ord(ch):02X}       ; {cmp_comment_for_char(ch)}",
            f"    JZ OLED4_CHAR_{label}",
            "",
        ])

    for ch in LOWERCASE_ORDER:
        upper = ch.upper()
        label = label_for_char(upper)
        lines.extend([
            "    MOV $A, OLED_CHAR_TMP",
            "    STC",
            f"    CMP $A, 0x{ord(ch):02X}       ; {ch}",
            f"    JZ OLED4_CHAR_{label}",
            "",
        ])

    lines.extend([
        "    JMP OLED4_CHAR_QUESTION",
        "",
        "OLED4_COMPUTE_CURSOR_BASE:",
        "    ; base grouped column = origin_x + col * 2",
        "    MOV $A, OLED_TEXT_ORIGIN_X",
        "    MOV $B, OLED_CURSOR_COL",
        "",
        "OLED4_CURSOR_X_LOOP:",
        "    STC",
        "    CMP $B, 0x00",
        "    JZ OLED4_CURSOR_X_DONE",
        "",
        "    CLC",
        "    ADD $A, 0x02",
        "",
        "    STC",
        "    SUB $B, 0x01",
        "    JMP OLED4_CURSOR_X_LOOP",
        "",
        "OLED4_CURSOR_X_DONE:",
        "    MOV OLED_GLYPH_BASE_X, $A",
        "",
        "    ; base row = origin_y + row * 7",
        "    MOV $A, OLED_TEXT_ORIGIN_Y",
        "    MOV $B, OLED_CURSOR_ROW",
        "",
        "OLED4_CURSOR_Y_LOOP:",
        "    STC",
        "    CMP $B, 0x00",
        "    JZ OLED4_CURSOR_Y_DONE",
        "",
        "    CLC",
        "    ADD $A, 0x07",
        "",
        "    STC",
        "    SUB $B, 0x01",
        "    JMP OLED4_CURSOR_Y_LOOP",
        "",
        "OLED4_CURSOR_Y_DONE:",
        "    MOV OLED_GLYPH_BASE_Y, $A",
        "    RTS",
        "",
        "OLED4_RENDER_BEGIN:",
        "    JSR OLED4_COMPUTE_CURSOR_BASE",
        "",
        "    ; column window: 2 grouped columns",
        "    MOV $A, 0x15",
        "    OLC $A",
        "    MOV $A, OLED_GLYPH_BASE_X",
        "    OLC $A",
        "    CLC",
        "    ADD $A, 0x01",
        "    OLC $A",
        "",
        "    ; row window: 7 pixel rows",
        "    MOV $A, 0x75",
        "    OLC $A",
        "    MOV $A, OLED_GLYPH_BASE_Y",
        "    OLC $A",
        "    CLC",
        "    ADD $A, 0x06",
        "    OLC $A",
        "",
        "    MOV $A, 0x5C",
        "    OLC $A",
        "    RTS",
        "",
    ])

    for ch in CHAR_ORDER:
        emit_glyph_routine(lines, ch)

    lines.append(POST_GLYPH_ROUTINES.rstrip())

    return "\n".join(lines) + "\n"


def main() -> None:
    lib = build_library()
    Path(LIB_OUT).write_text(lib, encoding="utf-8")

    print(f"Wrote {LIB_OUT}")
    print(f"Glyphs: {len(CHAR_ORDER)} printable ASCII characters")
    print(f"Lowercase aliases: {len(LOWERCASE_ORDER)}")
    print(f"Foreground nibble: 0x{FG_NIBBLE:X}")
    print(f"Background nibble: 0x{BG_NIBBLE:X}")
    print("Packing: left pixel -> high nibble, right pixel -> low nibble")


if __name__ == "__main__":
    main()
