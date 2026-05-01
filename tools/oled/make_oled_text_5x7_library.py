#!/usr/bin/env python3
# ==========================================================
# make_oled_text_5x7_library.py
# ==========================================================
# Generates oled_text_5x7.asm.
#
# Purpose:
#   Generate the SSD1325 5x7 text/terminal assembly library.
#
# OLED pixel packing:
#   The OLED initialization uses the SSD1325 remap setting
#   A0h = 0x52. With this configuration, each display data
#   byte contains two horizontal pixels:
#
#       left pixel  -> high nibble
#       right pixel -> low nibble
#
# Text cell format:
#   - visible glyph area: 5x7 pixels
#   - terminal cell size: 6x8 pixels
#   - one horizontal spacer pixel per cell
#   - one vertical spacer row per cell
#   - three SSD1325 data bytes per text row
#     because 6 horizontal pixels are packed as 3 byte columns
#   - eight pixel rows per character cell
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
#   Adafruit_GFX glcdfont.c fixed-space ASCII font table.
# ==========================================================

from pathlib import Path

LIB_OUT = "oled_text_5x7.asm"

FG_NIBBLE = 0xA
BG_NIBBLE = 0x0

# Each glyph is 5 vertical columns. Bit 0 is the top row.
FONT5X7 = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00],
    "0": [0x3E, 0x51, 0x49, 0x45, 0x3E],
    "1": [0x00, 0x42, 0x7F, 0x40, 0x00],
    "2": [0x72, 0x49, 0x49, 0x49, 0x46],
    "3": [0x21, 0x41, 0x45, 0x4B, 0x31],
    "4": [0x18, 0x14, 0x12, 0x7F, 0x10],
    "5": [0x27, 0x45, 0x45, 0x45, 0x39],
    "6": [0x3C, 0x4A, 0x49, 0x49, 0x30],
    "7": [0x01, 0x71, 0x09, 0x05, 0x03],
    "8": [0x36, 0x49, 0x49, 0x49, 0x36],
    "9": [0x06, 0x49, 0x49, 0x29, 0x1E],

    # Uppercase characters.
    "A": [0x7C, 0x12, 0x11, 0x12, 0x7C],
    "B": [0x7F, 0x49, 0x49, 0x49, 0x36],
    "C": [0x3E, 0x41, 0x41, 0x41, 0x22],
    "D": [0x7F, 0x41, 0x41, 0x41, 0x3E],
    "E": [0x7F, 0x49, 0x49, 0x49, 0x41],
    "F": [0x7F, 0x09, 0x09, 0x09, 0x01],
    "G": [0x3E, 0x41, 0x41, 0x51, 0x73],
    "H": [0x7F, 0x08, 0x08, 0x08, 0x7F],
    "I": [0x00, 0x41, 0x7F, 0x41, 0x00],
    "J": [0x20, 0x40, 0x41, 0x3F, 0x01],
    "K": [0x7F, 0x08, 0x14, 0x22, 0x41],
    "L": [0x7F, 0x40, 0x40, 0x40, 0x40],
    "M": [0x7F, 0x02, 0x0C, 0x02, 0x7F],
    "N": [0x7F, 0x04, 0x08, 0x10, 0x7F],
    "O": [0x3E, 0x41, 0x41, 0x41, 0x3E],
    "P": [0x7F, 0x09, 0x09, 0x09, 0x06],
    "Q": [0x3E, 0x41, 0x51, 0x21, 0x5E],
    "R": [0x7F, 0x09, 0x19, 0x29, 0x46],
    "S": [0x26, 0x49, 0x49, 0x49, 0x32],
    "T": [0x03, 0x01, 0x7F, 0x01, 0x03],
    "U": [0x3F, 0x40, 0x40, 0x40, 0x3F],
    "V": [0x1F, 0x20, 0x40, 0x20, 0x1F],
    "W": [0x3F, 0x40, 0x38, 0x40, 0x3F],
    "X": [0x63, 0x14, 0x08, 0x14, 0x63],
    "Y": [0x03, 0x04, 0x78, 0x04, 0x03],
    "Z": [0x61, 0x51, 0x49, 0x45, 0x43],
    # Lowercase characters.
    "a": [0x20, 0x54, 0x54, 0x78, 0x40],
    "b": [0x7F, 0x28, 0x44, 0x44, 0x38],
    "c": [0x38, 0x44, 0x44, 0x44, 0x28],
    "d": [0x38, 0x44, 0x44, 0x28, 0x7F],
    "e": [0x38, 0x54, 0x54, 0x54, 0x18],
    "f": [0x00, 0x08, 0x7E, 0x09, 0x02],
    "g": [0x18, 0xA4, 0xA4, 0x9C, 0x78],
    "h": [0x7F, 0x08, 0x04, 0x04, 0x78],
    "i": [0x00, 0x44, 0x7D, 0x40, 0x00],
    "j": [0x20, 0x40, 0x40, 0x3D, 0x00],
    "k": [0x7F, 0x10, 0x28, 0x44, 0x00],
    "l": [0x00, 0x41, 0x7F, 0x40, 0x00],
    "m": [0x7C, 0x04, 0x78, 0x04, 0x78],
    "n": [0x7C, 0x08, 0x04, 0x04, 0x78],
    "o": [0x38, 0x44, 0x44, 0x44, 0x38],
    "p": [0xFC, 0x18, 0x24, 0x24, 0x18],
    "q": [0x18, 0x24, 0x24, 0x18, 0xFC],
    "r": [0x7C, 0x08, 0x04, 0x04, 0x08],
    "s": [0x48, 0x54, 0x54, 0x54, 0x24],
    "t": [0x04, 0x04, 0x3F, 0x44, 0x24],
    "u": [0x3C, 0x40, 0x40, 0x20, 0x7C],
    "v": [0x1C, 0x20, 0x40, 0x20, 0x1C],
    "w": [0x3C, 0x40, 0x30, 0x40, 0x3C],
    "x": [0x44, 0x28, 0x10, 0x28, 0x44],
    "y": [0x4C, 0x90, 0x90, 0x90, 0x7C],
    "z": [0x44, 0x64, 0x54, 0x4C, 0x44],
    "=": [0x14, 0x14, 0x14, 0x14, 0x14],
    "$": [0x24, 0x2A, 0x7F, 0x2A, 0x12],
    ">": [0x00, 0x41, 0x22, 0x14, 0x08],
    ":": [0x00, 0x36, 0x36, 0x00, 0x00],
    "-": [0x08, 0x08, 0x08, 0x08, 0x08],
    "_": [0x40, 0x40, 0x40, 0x40, 0x40],
    ".": [0x00, 0x60, 0x60, 0x00, 0x00],
    "/": [0x20, 0x10, 0x08, 0x04, 0x02],

    # Punctuation glyphs.
    "!": [0x00, 0x00, 0x5F, 0x00, 0x00],
    "\"": [0x00, 0x07, 0x00, 0x07, 0x00],
    "#": [0x14, 0x7F, 0x14, 0x7F, 0x14],
    "%": [0x23, 0x13, 0x08, 0x64, 0x62],
    "&": [0x36, 0x49, 0x56, 0x20, 0x50],
    "'": [0x00, 0x08, 0x07, 0x03, 0x00],
    "(": [0x00, 0x1C, 0x22, 0x41, 0x00],
    ")": [0x00, 0x41, 0x22, 0x1C, 0x00],
    "*": [0x2A, 0x1C, 0x7F, 0x1C, 0x2A],
    "+": [0x08, 0x08, 0x3E, 0x08, 0x08],
    ",": [0x00, 0x80, 0x70, 0x30, 0x00],
    ";": [0x00, 0x40, 0x34, 0x00, 0x00],
    "<": [0x00, 0x08, 0x14, 0x22, 0x41],
    "?": [0x02, 0x01, 0x59, 0x09, 0x06],
    "@": [0x3E, 0x41, 0x5D, 0x59, 0x4E],
    "[": [0x00, 0x7F, 0x41, 0x41, 0x41],
    "\\": [0x02, 0x04, 0x08, 0x10, 0x20],
    "]": [0x00, 0x41, 0x41, 0x41, 0x7F],
    "^": [0x04, 0x02, 0x01, 0x02, 0x04],
    "`": [0x00, 0x03, 0x07, 0x08, 0x00],
    "{": [0x00, 0x08, 0x36, 0x41, 0x00],
    "|": [0x00, 0x00, 0x77, 0x00, 0x00],
    "}": [0x00, 0x41, 0x36, 0x08, 0x00],
    "~": [0x02, 0x01, 0x02, 0x04, 0x02],
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

ORDER_GROUP_1 = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "=", "$", ">", ":", "-", "_", ".", "/"]
ORDER_GROUP_2 = list("abcdefghijklmnopqrstuvwxyz")
SYMBOLS = ["!", "\"", "#", "%", "&", "'", "(", ")", "*", "+", ",", ";", "<", "?", "@", "[", "\\", "]", "^", "`", "{", "|", "}", "~"]

CHAR_ORDER = ORDER_GROUP_1 + ORDER_GROUP_2 + SYMBOLS

assert len(SYMBOLS) <= 30
assert len(set(CHAR_ORDER)) == len(CHAR_ORDER)
assert all(ch in FONT5X7 for ch in CHAR_ORDER)

POST_GLYPH_ROUTINES = """; ==========================================================
; Terminal helper routines
; ==========================================================

OLED5_HOME:
    MOV $A, 0x00
    MOV OLED_CURSOR_COL, $A
    MOV OLED_CURSOR_ROW, $A
    RTS

OLED5_SET_DEFAULT_ORIGIN:
    MOV $A, OLED5_DEFAULT_X
    MOV OLED_TEXT_ORIGIN_X, $A
    MOV $A, OLED5_DEFAULT_Y
    MOV OLED_TEXT_ORIGIN_Y, $A
    RTS

OLED5_CLEAR_TEXT_SCREEN:
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
    MOV $A, 0x3F
    OLC $A

    MOV $A, 0x5C
    OLC $A

    MOV $A, 0x00
    MOV $D, OLED5_CLEAR_ROWS

.OLED5_CLEAR_TEXT_ROW:
    MOV $B, OLED5_CLEAR_COLS

.OLED5_CLEAR_TEXT_COL:
    OLD $A
    STC
    NOP
    SUB $B, 0x01
    JNZ .OLED5_CLEAR_TEXT_COL

    STC
    NOP
    SUB $D, 0x01
    JNZ .OLED5_CLEAR_TEXT_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED5_PUTC:
    STC
    NOP
    CMP $A, 0x0A
    JZ OLED5_PUTC_NEWLINE

    STC
    NOP
    CMP $A, 0x0D
    JZ OLED5_PUTC_CR

    STC
    NOP
    CMP $A, 0x08
    JZ OLED5_PUTC_BACKSPACE

    JSR OLED5_DRAW_CHAR
    RTS

OLED5_PUTC_NEWLINE:
    JSR OLED5_NEWLINE
    RTS

OLED5_PUTC_CR:
    JSR OLED5_CARRIAGE_RETURN
    RTS

OLED5_PUTC_BACKSPACE:
    JSR OLED5_BACKSPACE
    RTS

OLED5_CARRIAGE_RETURN:
    MOV $A, 0x00
    MOV OLED_CURSOR_COL, $A
    RTS

OLED5_BACKSPACE:
    MOV $A, OLED_CURSOR_COL
    STC
    NOP
    CMP $A, 0x00
    JZ OLED5_BACKSPACE_DONE

    STC
    NOP
    SUB $A, 0x01
    MOV OLED_CURSOR_COL, $A

    MOV $A, 0x20
    JSR OLED5_DRAW_CHAR

    MOV $A, OLED_CURSOR_COL
    STC
    NOP
    SUB $A, 0x01
    MOV OLED_CURSOR_COL, $A

OLED5_BACKSPACE_DONE:
    RTS

OLED5_CLEAR_CURRENT_CELL_DIRECT:
    PSH $A
    PSH $B
    PSH $D

    MOV $A, OLED_CURSOR_COL
    MOV $B, $A
    CLC
    NOP
    ADD $A, $B
    CLC
    NOP
    ADD $A, $B
    CLC
    NOP
    ADD $A, OLED_TEXT_ORIGIN_X
    MOV OLED_WIN_COL_START, $A
    CLC
    NOP
    ADD $A, 0x02
    MOV OLED_WIN_COL_END, $A

    MOV $A, OLED_CURSOR_ROW
    LSL $A
    LSL $A
    LSL $A
    CLC
    NOP
    ADD $A, OLED_TEXT_ORIGIN_Y
    MOV OLED_WIN_ROW_START, $A
    CLC
    NOP
    ADD $A, 0x07
    MOV OLED_WIN_ROW_END, $A

    MOV $A, 0x15
    OLC $A
    MOV $A, OLED_WIN_COL_START
    OLC $A
    MOV $A, OLED_WIN_COL_END
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, OLED_WIN_ROW_START
    OLC $A
    MOV $A, OLED_WIN_ROW_END
    OLC $A

    MOV $A, 0x5C
    OLC $A
    MOV $A, 0x00
    MOV $D, 0x08

.OLED5_CLEAR_CELL_ROW:
    MOV $B, 0x03

.OLED5_CLEAR_CELL_COL:
    OLD $A
    STC
    NOP
    SUB $B, 0x01
    JNZ .OLED5_CLEAR_CELL_COL

    STC
    NOP
    SUB $D, 0x01
    JNZ .OLED5_CLEAR_CELL_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED5_DRAW_CURRENT_CELL_BLOCK_DIRECT:
    PSH $A
    PSH $B
    PSH $D

    MOV $A, OLED_CURSOR_COL
    MOV $B, $A
    CLC
    NOP
    ADD $A, $B
    CLC
    NOP
    ADD $A, $B
    CLC
    NOP
    ADD $A, OLED_TEXT_ORIGIN_X
    MOV OLED_WIN_COL_START, $A
    CLC
    NOP
    ADD $A, 0x02
    MOV OLED_WIN_COL_END, $A

    MOV $A, OLED_CURSOR_ROW
    LSL $A
    LSL $A
    LSL $A
    CLC
    NOP
    ADD $A, OLED_TEXT_ORIGIN_Y
    MOV OLED_WIN_ROW_START, $A
    CLC
    NOP
    ADD $A, 0x07
    MOV OLED_WIN_ROW_END, $A

    MOV $A, 0x15
    OLC $A
    MOV $A, OLED_WIN_COL_START
    OLC $A
    MOV $A, OLED_WIN_COL_END
    OLC $A

    MOV $A, 0x75
    OLC $A
    MOV $A, OLED_WIN_ROW_START
    OLC $A
    MOV $A, OLED_WIN_ROW_END
    OLC $A

    MOV $A, 0x5C
    OLC $A
    MOV $A, 0xFF
    MOV $D, 0x08

.OLED5_DRAW_CELL_BLOCK_ROW:
    MOV $B, 0x03

.OLED5_DRAW_CELL_BLOCK_COL:
    OLD $A
    STC
    NOP
    SUB $B, 0x01
    JNZ .OLED5_DRAW_CELL_BLOCK_COL

    STC
    NOP
    SUB $D, 0x01
    JNZ .OLED5_DRAW_CELL_BLOCK_ROW

    PUL $D
    PUL $B
    PUL $A
    RTS

OLED5_PRINT_READY_PROMPT:
    MOV $A, 0x52
    JSR OLED5_PUTC
    MOV $A, 0x45
    JSR OLED5_PUTC
    MOV $A, 0x41
    JSR OLED5_PUTC
    MOV $A, 0x44
    JSR OLED5_PUTC
    MOV $A, 0x59
    JSR OLED5_PUTC
    MOV $A, 0x3E
    JSR OLED5_PUTC
    RTS

OLED5_CURSOR_SHOW:
    JSR OLED5_DRAW_CURRENT_CELL_BLOCK_DIRECT
    RTS

OLED5_CURSOR_HIDE:
    JSR OLED5_CLEAR_CURRENT_CELL_DIRECT
    RTS

OLED5_TYPE_CHAR_WITH_CURSOR:
    MOV OLED_CHAR_TMP, $A
    JSR OLED5_CURSOR_HIDE
    MOV $A, OLED_CHAR_TMP
    JSR OLED5_PUTC
    JSR OLED5_CURSOR_SHOW
    RTS

OLED5_PRINT_HEX_NIBBLE:
    STC
    NOP
    CMP $A, 0x0A
    JC .OLED5_HEX_LETTER

.OLED5_HEX_DIGIT:
    CLC
    NOP
    ADD $A, 0x30
    JSR OLED5_PUTC
    RTS

.OLED5_HEX_LETTER:
    STC
    NOP
    SUB $A, 0x0A
    CLC
    NOP
    ADD $A, 0x41
    JSR OLED5_PUTC
    RTS

OLED5_PRINT_HEX_BYTE:
    MOV OLED_HEX_TMP, $A
    AND $A, 0xF0
    LSR $A
    LSR $A
    LSR $A
    LSR $A
    JSR OLED5_PRINT_HEX_NIBBLE

    MOV $A, OLED_HEX_TMP
    AND $A, 0x0F
    JSR OLED5_PRINT_HEX_NIBBLE
    RTS

OLED5_PRINT_HEX_WORD_CD:
    MOV OLED_HEX_WORD_LO, $C
    MOV OLED_HEX_WORD_HI, $D

    MOV $A, OLED_HEX_WORD_HI
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, OLED_HEX_WORD_LO
    JSR OLED5_PRINT_HEX_BYTE
    RTS"""


def label_for_char(ch: str) -> str:
    if ch in LABEL_NAMES:
        return LABEL_NAMES[ch]
    if ch.isdigit():
        return f"DIGIT_{ch}"
    if "a" <= ch <= "z":
        return f"LOWER_{ch.upper()}"
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
    # Pixel packing:
    #   left pixel  -> high nibble
    #   right pixel -> low nibble
    lo = FG_NIBBLE if right_on else BG_NIBBLE
    hi = FG_NIBBLE if left_on else BG_NIBBLE
    return (hi << 4) | lo


def glyph_rows(ch: str):
    cols = FONT5X7[ch]

    for y in range(8):
        pixels = [((cols[x] >> y) & 1) for x in range(5)]
        pixels.append(0)  # 6th pixel is horizontal cell spacing.

        yield [
            pack_pair(pixels[0], pixels[1]),
            pack_pair(pixels[2], pixels[3]),
            pack_pair(pixels[4], pixels[5]),
        ]


def emit_mov_olc(lines: list[str], value: str) -> None:
    lines.append(f"    MOV $A, {value}")
    lines.append("    OLC $A")


def emit_mov_old(lines: list[str], value: int) -> None:
    lines.append(f"    MOV $A, 0x{value:02X}")
    lines.append("    OLD $A")


def emit_glyph_routine(lines: list[str], ch: str) -> None:
    label = label_for_char(ch)

    lines.extend([
        "",
        comment_for_char(ch),
        f"OLED5_CHAR_{label}:",
        "    JSR OLED5_RENDER_BEGIN",
    ])

    for row_bytes in glyph_rows(ch):
        for b in row_bytes:
            emit_mov_old(lines, b)

    lines.extend([
        "    JSR OLED5_ADVANCE_CURSOR",
        "    RTS",
    ])


def build_library() -> str:
    lines: list[str] = []

    lines.extend([
        "; ==========================================================",
        "; oled_text_5x7.asm",
        "; ==========================================================",
        "; Generated by make_oled_text_5x7_library.py",
        "; SSD1325 5x7 monitor text layer.",
        ";",
        "; Cell size:",
        ";   6 pixels wide  = 3 grouped SSD1325 columns",
        ";   8 pixels tall  = 8 font rows",
        ";",
        "; Pixel packing for OLED_INIT / A0h = 0x52:",
        ";   left pixel  -> high nibble",
        ";   right pixel -> low nibble",
        ";",
        "; API:",
        ";   OLED5_SET_CURSOR",
        ";   OLED5_DRAW_CHAR",
        ";   OLED5_DRAW_STRING",
        ";",
        "; Calling convention:",
        ";   OLED5_SET_CURSOR:",
        ";       A = column",
        ";       B = row",
        ";",
        ";   OLED5_DRAW_CHAR:",
        ";       A = ASCII character",
        ";",
        ";   OLED5_DRAW_STRING:",
        ";       CD = pointer to null-terminated RAM string",
        ";       newline = 0x0A",
        ";",
        ";   This renderer uses fixed foreground/background bytes for",
        ";   monitor text output.",
        "; ==========================================================",
        "",
    ])

    lines.extend([
        "OLED5_SET_CURSOR:",
        "    ; in: A = col, B = row",
        "    MOV OLED_CURSOR_COL, $A",
        "    MOV OLED_CURSOR_ROW, $B",
        "    RTS",
        "",
        "OLED5_NEWLINE:",
        "    ; Move to column 0.",
        "    MOV $A, 0x00",
        "    MOV OLED_CURSOR_COL, $A",
        "",
        "    ; row++",
        "    MOV $A, OLED_CURSOR_ROW",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x01",
        "    MOV OLED_CURSOR_ROW, $A",
        "",
        "    ; If row == OLED5_MAX_ROWS, wrap back to row 0.",
        "    STC",
        "    NOP",
        "    CMP $A, OLED5_MAX_ROWS",
        "    JZ OLED5_NEWLINE_WRAP_TOP",
        "",
        "    RTS",
        "",
        "OLED5_NEWLINE_WRAP_TOP:",
        "    MOV $A, 0x00",
        "    MOV OLED_CURSOR_ROW, $A",
        "    RTS",
        "",
        "OLED5_ADVANCE_CURSOR:",
        "    ; col++",
        "    MOV $A, OLED_CURSOR_COL",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x01",
        "    MOV OLED_CURSOR_COL, $A",
        "",
        "    ; If col == OLED5_MAX_COLS, wrap to the next row.",
        "    STC",
        "    NOP",
        "    CMP $A, OLED5_MAX_COLS",
        "    JZ OLED5_ADVANCE_CURSOR_WRAP",
        "",
        "    RTS",
        "",
        "OLED5_ADVANCE_CURSOR_WRAP:",
        "    JSR OLED5_NEWLINE",
        "    RTS",
        "",
        "OLED5_CLEAR_CURRENT_LINE_LOOP:",
        "    STC",
        "    NOP",
        "    CMP $B, 0x00",
        "    JZ OLED5_CLEAR_CURRENT_LINE_DONE",
        "",
        "    JSR OLED5_CHAR_SPACE",
        "",
        "    STC",
        "    NOP",
        "    SUB $B, 0x01",
        "    JMP OLED5_CLEAR_CURRENT_LINE_LOOP",
        "",
        "OLED5_CLEAR_CURRENT_LINE_DONE:",
        "    MOV $A, 0x00",
        "    MOV OLED_CURSOR_COL, $A",
        "    RTS",
        "",
        "OLED5_INC_CD:",
        "    CLC",
        "    NOP",
        "    ADD $C, 0x01",
        "    JNC OLED5_INC_CD_DONE",
        "",
        "    CLC",
        "    NOP",
        "    ADD $D, 0x01",
        "",
        "OLED5_INC_CD_DONE:",
        "    RTS",
        "",
        "OLED5_DRAW_STRING:",
        "OLED5_DRAW_STRING_LOOP:",
        "    MOV $A, [$CD]",
        "",
        "    STC",
        "    NOP",
        "    CMP $A, 0x00",
        "    JZ OLED5_DRAW_STRING_DONE",
        "",
        "    STC",
        "    NOP",
        "    CMP $A, 0x0A",
        "    JZ OLED5_DRAW_STRING_NEWLINE",
        "",
        "    JSR OLED5_DRAW_CHAR",
        "    JSR OLED5_INC_CD",
        "    JMP OLED5_DRAW_STRING_LOOP",
        "",
        "OLED5_DRAW_STRING_NEWLINE:",
        "    JSR OLED5_NEWLINE",
        "    JSR OLED5_INC_CD",
        "    JMP OLED5_DRAW_STRING_LOOP",
        "",
        "OLED5_DRAW_STRING_DONE:",
        "    RTS",
        "",
        "OLED5_DRAW_CHAR:",
        "    MOV OLED_CHAR_TMP, $A",
        "",
    ])

    for ch in CHAR_ORDER:
        label = label_for_char(ch)
        lines.extend([
            "    MOV $A, OLED_CHAR_TMP",
            "    STC",
            "    NOP",
            f"    CMP $A, 0x{ord(ch):02X}       ; {cmp_comment_for_char(ch)}",
            f"    JZ OLED5_CHAR_{label}",
            "",
        ])

    lines.extend([
        "    ; Unsupported character: draw a space-sized blank cell.",
        "    JMP OLED5_CHAR_SPACE",
        "",
        "OLED5_COMPUTE_CURSOR_BASE:",
        "    ; base grouped column = origin_x + col * 3",
        "    MOV $A, OLED_TEXT_ORIGIN_X",
        "    MOV $B, OLED_CURSOR_COL",
        "",
        "OLED5_CURSOR_X_LOOP:",
        "    STC",
        "    NOP",
        "    CMP $B, 0x00",
        "    JZ OLED5_CURSOR_X_DONE",
        "",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x03",
        "",
        "    STC",
        "    NOP",
        "    SUB $B, 0x01",
        "    JMP OLED5_CURSOR_X_LOOP",
        "",
        "OLED5_CURSOR_X_DONE:",
        "    MOV OLED_GLYPH_BASE_X, $A",
        "",
        "    ; base row = origin_y + row * 8",
        "    MOV $A, OLED_TEXT_ORIGIN_Y",
        "    MOV $B, OLED_CURSOR_ROW",
        "",
        "OLED5_CURSOR_Y_LOOP:",
        "    STC",
        "    NOP",
        "    CMP $B, 0x00",
        "    JZ OLED5_CURSOR_Y_DONE",
        "",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x08",
        "",
        "    STC",
        "    NOP",
        "    SUB $B, 0x01",
        "    JMP OLED5_CURSOR_Y_LOOP",
        "",
        "OLED5_CURSOR_Y_DONE:",
        "    MOV OLED_GLYPH_BASE_Y, $A",
        "    RTS",
        "",
        "OLED5_RENDER_BEGIN:",
        "    JSR OLED5_COMPUTE_CURSOR_BASE",
        "",
        "    ; column window: 3 grouped columns",
        "    MOV $A, 0x15",
        "    OLC $A",
        "    MOV $A, OLED_GLYPH_BASE_X",
        "    OLC $A",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x02",
        "    OLC $A",
        "",
        "    ; row window: 8 pixel rows",
        "    MOV $A, 0x75",
        "    OLC $A",
        "    MOV $A, OLED_GLYPH_BASE_Y",
        "    OLC $A",
        "    CLC",
        "    NOP",
        "    ADD $A, 0x07",
        "    OLC $A",
        "",
        "    ; begin GDDRAM burst",
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
    print(f"Foreground nibble: 0x{FG_NIBBLE:X}")
    print(f"Background nibble: 0x{BG_NIBBLE:X}")
    print("Packing: left pixel -> high nibble, right pixel -> low nibble")


if __name__ == "__main__":
    main()