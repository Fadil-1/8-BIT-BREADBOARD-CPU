; ==========================================================
; oled_constants.asm
; ==========================================================
; Runtime addresses and display constants for the OLED monitor.
;
; Writable state is kept in high RAM so it does not overlap the
; stage-2 program image loaded at 0x0200.
; ==========================================================

; ---------- OLED runtime workspace ----------
OLED_WORK_BASE      = 0x7000

; ---------- OLED argument / window state ----------
OLED_ARG_X          = 0x7000
OLED_ARG_Y          = 0x7001
OLED_ARG_W          = 0x7002
OLED_ARG_H          = 0x7003
OLED_ARG_COLOR      = 0x7004

; ---------- 5x7 text state ----------
OLED_TEXT_ORIGIN_X  = 0x7005
OLED_TEXT_ORIGIN_Y  = 0x7006
OLED_CURSOR_COL     = 0x7007
OLED_CURSOR_ROW     = 0x7008
OLED_TEXT_COLOR     = 0x7009
OLED_CHAR_TMP       = 0x700A
OLED_G0             = 0x700B
OLED_G1             = 0x700C
OLED_G2             = 0x700D
OLED_G3             = 0x700E
OLED_G4             = 0x700F
OLED_GLYPH_BASE_X   = 0x7010
OLED_GLYPH_BASE_Y   = 0x7011
OLED_PIXEL_COL_OFF  = 0x7012
OLED_PIXEL_ROW_OFF  = 0x7013
OLED_ROW_MASK       = 0x7014

; ---------- OLED RAM-write state ----------
OLED_TEXT_BG        = 0x7015
OLED_WIN_COL_START  = 0x7016
OLED_WIN_COL_END    = 0x7017
OLED_WIN_ROW_START  = 0x7018
OLED_WIN_ROW_END    = 0x7019
OLED_RAM_BYTE0      = 0x701A
OLED_RAM_BYTE1      = 0x701B
OLED_HEX_TMP        = 0x701C
OLED_HEX_WORD_LO    = 0x701D
OLED_HEX_WORD_HI    = 0x701E

; ---------- monitor input / parser state ----------
MON_INPUT_LEN       = 0x7020
MON_INPUT_MAX       = 0x11

MON_KEY_SCRIPT_PTR_LO = 0x7021
MON_KEY_SCRIPT_PTR_HI = 0x7022

MON_CMP_INPUT_PTR_LO  = 0x7023
MON_CMP_INPUT_PTR_HI  = 0x7024
MON_CMP_TEST_PTR_LO   = 0x7025
MON_CMP_TEST_PTR_HI   = 0x7026
MON_CMP_INPUT_CHAR    = 0x7027
MON_CMP_TEST_CHAR     = 0x7028

MON_DMP_ADDR_LO       = 0x7029
MON_DMP_ADDR_HI       = 0x702A

MON_HEX_CHAR_TMP      = 0x702B
MON_HEX_TEST_CHAR     = 0x702C
MON_HEX_STATUS        = 0x702D
MON_HEX_NIBBLE_HI     = 0x702E
MON_HEX_NIBBLE_LO     = 0x702F

; ---------- monitor command / status scratch ----------
MON_FILL_START_LO   = 0x7030
MON_FILL_START_HI   = 0x7031
MON_FILL_END_LO     = 0x7032
MON_FILL_END_HI     = 0x7033
MON_FILL_CUR_LO     = 0x7034
MON_FILL_CUR_HI     = 0x7035
MON_FILL_VALUE      = 0x7036
MON_REG_A           = 0x7037
MON_REG_B           = 0x7038
MON_REG_C           = 0x7039
MON_REG_D           = 0x703A
MON_REG_VALID       = 0x703B
MON_SP_LO           = 0x703C
MON_SP_HI           = 0x703D
MON_STACK_PTR_LO    = 0x703E
MON_STACK_PTR_HI    = 0x703F
TITLE_BUF           = 0x7040
STATUS_BUF          = 0x7080

; ---------- monitor input buffer ----------
MON_INPUT_BUF       = 0x7100
MON_INPUT_BUF_HI    = 0x71

; ---------- scripted input and command strings ----------
MON_KEY_SCRIPT_BUF    = 0x7200
MON_KEY_SCRIPT_BUF_HI = 0x72

MON_CMD_STR_HELP    = 0x7220
MON_CMD_STR_CLS     = 0x7228
MON_CMD_STR_INFO    = 0x7230
MON_CMD_STR_DMP     = 0x7238
MON_CMD_STR_PEEK    = 0x7248
MON_CMD_STR_POKE    = 0x7250
MON_CMD_STR_FILL    = 0x7258
MON_CMD_STR_LOAD    = 0x7260
MON_CMD_STR_BOOT    = 0x7268
MON_CMD_STR_REG     = 0x7270
MON_CMD_STR_SP      = 0x7278
MON_CMD_STR_STACK   = 0x7280
MON_CMD_STR_CMP     = 0x7288
MON_CMD_STR_CP      = 0x7290

; ---------- hex parser result state ----------
MON_HEX_BYTE_RESULT   = 0x7240
MON_HEX_WORD_LO       = 0x7241
MON_HEX_WORD_HI       = 0x7242
MON_HEX_PARSE_PTR_LO  = 0x7243
MON_HEX_PARSE_PTR_HI  = 0x7244
MON_MEMCMP_LEFT_LO      = 0x72A0
MON_MEMCMP_LEFT_HI      = 0x72A1
MON_MEMCMP_RIGHT_LO     = 0x72A2
MON_MEMCMP_RIGHT_HI     = 0x72A3
MON_MEMCMP_COUNT        = 0x72A4
MON_MEMCMP_LEFT_BYTE    = 0x72A5
MON_MEMCMP_RIGHT_BYTE   = 0x72A6
MON_MEMCMP_MIS_L_LO     = 0x72A7
MON_MEMCMP_MIS_L_HI     = 0x72A8
MON_MEMCMP_MIS_R_LO     = 0x72A9
MON_MEMCMP_MIS_R_HI     = 0x72AA
MON_CP_SRC_LO       = 0x72B0
MON_CP_SRC_HI       = 0x72B1
MON_CP_DST_LO       = 0x72B2
MON_CP_DST_HI       = 0x72B3
MON_CP_COUNT        = 0x72B4
MON_CP_BYTE_TMP     = 0x72B5

; ---------- display geometry ----------
OLED_SCREEN_W       = 128
OLED_SCREEN_H       = 64

SHELL_TITLE_H       = 12
SHELL_BODY_Y        = 14
SHELL_BODY_H        = 50

; ---------- 5x7 terminal geometry ----------
OLED5_MAX_COLS      = 21
OLED5_MAX_ROWS      = 8
OLED5_DEFAULT_X     = 0x01
OLED5_DEFAULT_Y     = 0x00
OLED5_CLEAR_COLS    = 63
OLED5_CLEAR_ROWS    = 64

; ---------- grayscale constants ----------
OLED_BLACK          = 0x00
OLED_DIM            = 0x22
OLED_BRIGHT         = 0xFF
