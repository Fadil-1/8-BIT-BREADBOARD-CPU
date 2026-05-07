; ==========================================================
; monitor_commands.asm
; ==========================================================
; Monitor prompt, command dispatch, and command handlers.
;
; Original version: April 2026
; Last Modified: May 2026
; Fadil Isamotu
; ==========================================================

; ----------------------------------------------------------
; MON_PRINT_FRESH_PROMPT
;
; Resets the input buffer, prints the prompt character, and
; shows the cursor.
;
; Prompt printed:
;   >
; ----------------------------------------------------------
MON_PRINT_FRESH_PROMPT:
    JSR MON_INPUT_RESET

    MOV $A, 0x3E       ; >
    JSR OLED5_PUTC

    JSR OLED5_CURSOR_SHOW
    RTS

; ----------------------------------------------------------
; MON_SUBMIT_COMMAND
;
; Submits the current input line.
;
; Behavior:
;   1. hide cursor
;   2. null-terminate MON_INPUT_BUF
;   3. dispatch command
;
; Command handlers return to a fresh prompt when appropriate.
; ----------------------------------------------------------
MON_SUBMIT_COMMAND:
    JSR OLED5_CURSOR_HIDE
    JSR MON_INPUT_TERMINATE
    JSR MON_DISPATCH_COMMAND
    RTS

; ----------------------------------------------------------
; MON_HANDLE_KEY
;
; Handles one decoded keyboard character/control code.
;
; Input:
;   $A = ASCII character / control code
;
; Behavior:
;   0x0A -> submit command
;   0x0D -> submit command
;   other values -> send to MON_INPUT_TYPE_CHAR
;
;   Backspace is intentionally passed through to
;   MON_INPUT_TYPE_CHAR, because that routine already handles
;   input-buffer length and cursor-aware backspace echo.
; ----------------------------------------------------------
MON_HANDLE_KEY:
    MOV OLED_CHAR_TMP, $A

    ; LF/newline submits command.
    STC
    CMP $A, 0x0A
    JZ MON_HANDLE_KEY_SUBMIT

    ; CR/carriage return submits command.
    STC
    CMP $A, 0x0D
    JZ MON_HANDLE_KEY_SUBMIT

    ; All other values go through the input-line path.
    MOV $A, OLED_CHAR_TMP
    JSR MON_INPUT_TYPE_CHAR
    RTS

MON_HANDLE_KEY_SUBMIT:
    JSR MON_SUBMIT_COMMAND
    RTS

; ----------------------------------------------------------
; MON_PREP_COMMAND_STRINGS
;
; Copies reusable command-name strings into RAM.
;
; Exact-match recognizers use these strings through
; MON_INPUT_EQUALS_STRING. Argument commands use dedicated
; shape recognizers in monitor_input.asm.
; ----------------------------------------------------------
MON_PREP_COMMAND_STRINGS:
    ; HELP at 0x7220
    MOV $A, 0x48       ; H
    MOV MON_CMD_STR_HELP, $A
    MOV $A, 0x45       ; E
    MOV MON_CMD_STR_HELP + 1, $A
    MOV $A, 0x4C       ; L
    MOV MON_CMD_STR_HELP + 2, $A
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_HELP + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_HELP + 4, $A

    ; CLS at 0x7228
    MOV $A, 0x43       ; C
    MOV MON_CMD_STR_CLS, $A
    MOV $A, 0x4C       ; L
    MOV MON_CMD_STR_CLS + 1, $A
    MOV $A, 0x53       ; S
    MOV MON_CMD_STR_CLS + 2, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_CLS + 3, $A

    ; INFO at 0x7230
    MOV $A, 0x49       ; I
    MOV MON_CMD_STR_INFO, $A
    MOV $A, 0x4E       ; N
    MOV MON_CMD_STR_INFO + 1, $A
    MOV $A, 0x46       ; F
    MOV MON_CMD_STR_INFO + 2, $A
    MOV $A, 0x4F       ; O
    MOV MON_CMD_STR_INFO + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_INFO + 4, $A

    ; DMP at 0x7238
    MOV $A, 0x44       ; D
    MOV MON_CMD_STR_DMP, $A
    MOV $A, 0x4D       ; M
    MOV MON_CMD_STR_DMP + 1, $A
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_DMP + 2, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_DMP + 3, $A

    ; PEEK at 0x7248
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_PEEK, $A
    MOV $A, 0x45       ; E
    MOV MON_CMD_STR_PEEK + 1, $A
    MOV $A, 0x45       ; E
    MOV MON_CMD_STR_PEEK + 2, $A
    MOV $A, 0x4B       ; K
    MOV MON_CMD_STR_PEEK + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_PEEK + 4, $A

    ; POKE at 0x7250
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_POKE, $A
    MOV $A, 0x4F       ; O
    MOV MON_CMD_STR_POKE + 1, $A
    MOV $A, 0x4B       ; K
    MOV MON_CMD_STR_POKE + 2, $A
    MOV $A, 0x45       ; E
    MOV MON_CMD_STR_POKE + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_POKE + 4, $A

    ; FILL at 0x7258
    MOV $A, 0x46       ; F
    MOV MON_CMD_STR_FILL, $A
    MOV $A, 0x49       ; I
    MOV MON_CMD_STR_FILL + 1, $A
    MOV $A, 0x4C       ; L
    MOV MON_CMD_STR_FILL + 2, $A
    MOV $A, 0x4C       ; L
    MOV MON_CMD_STR_FILL + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_FILL + 4, $A

    ; LOAD at 0x7260
    MOV $A, 0x4C       ; L
    MOV MON_CMD_STR_LOAD, $A
    MOV $A, 0x4F       ; O
    MOV MON_CMD_STR_LOAD + 1, $A
    MOV $A, 0x41       ; A
    MOV MON_CMD_STR_LOAD + 2, $A
    MOV $A, 0x44       ; D
    MOV MON_CMD_STR_LOAD + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_LOAD + 4, $A

    ; BOOT at 0x7268
    MOV $A, 0x42       ; B
    MOV MON_CMD_STR_BOOT, $A
    MOV $A, 0x4F       ; O
    MOV MON_CMD_STR_BOOT + 1, $A
    MOV $A, 0x4F       ; O
    MOV MON_CMD_STR_BOOT + 2, $A
    MOV $A, 0x54       ; T
    MOV MON_CMD_STR_BOOT + 3, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_BOOT + 4, $A

    ; REG at 0x7270
    MOV $A, 0x52       ; R
    MOV MON_CMD_STR_REG, $A
    MOV $A, 0x45       ; E
    MOV MON_CMD_STR_REG + 1, $A
    MOV $A, 0x47       ; G
    MOV MON_CMD_STR_REG + 2, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_REG + 3, $A

    ; SP at 0x7278
    MOV $A, 0x53       ; S
    MOV MON_CMD_STR_SP, $A
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_SP + 1, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_SP + 2, $A

    ; STACK at 0x7280
    MOV $A, 0x53       ; S
    MOV MON_CMD_STR_STACK, $A
    MOV $A, 0x54       ; T
    MOV MON_CMD_STR_STACK + 1, $A
    MOV $A, 0x41       ; A
    MOV MON_CMD_STR_STACK + 2, $A
    MOV $A, 0x43       ; C
    MOV MON_CMD_STR_STACK + 3, $A
    MOV $A, 0x4B       ; K
    MOV MON_CMD_STR_STACK + 4, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_STACK + 5, $A

    ; CMP at 0x7288
    MOV $A, 0x43       ; C
    MOV MON_CMD_STR_CMP, $A
    MOV $A, 0x4D       ; M
    MOV MON_CMD_STR_CMP + 1, $A
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_CMP + 2, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_CMP + 3, $A

    ; CP at 0x7290
    MOV $A, 0x43       ; C
    MOV MON_CMD_STR_CP, $A
    MOV $A, 0x50       ; P
    MOV MON_CMD_STR_CP + 1, $A
    MOV $A, 0x00
    MOV MON_CMD_STR_CP + 2, $A

    RTS

; ----------------------------------------------------------
; MON_FEED_KEY_STRING
;
; Feeds a zero-terminated key script into MON_HANDLE_KEY.
;
; Input:
;   $C = low byte of script pointer
;   $D = high byte of script pointer
;
; Script format:
;   bytes are ASCII/control codes
;   0x00 terminates the script
;
; Example script:
;   H E L P 0x0A B A D 0x0A 0x00
;
; The script pointer is saved in RAM because MON_HANDLE_KEY
; and the command dispatcher may use $C/$D internally.
; ----------------------------------------------------------
MON_FEED_KEY_STRING:
    MOV MON_KEY_SCRIPT_PTR_LO, $C
    MOV MON_KEY_SCRIPT_PTR_HI, $D

.MON_FEED_KEY_STRING_LOOP:
    ; Reload script pointer.
    MOV $C, MON_KEY_SCRIPT_PTR_LO
    MOV $D, MON_KEY_SCRIPT_PTR_HI

    ; Read next scripted key.
    MOV $A, [$CD]

    ; 0x00 terminates the script.
    STC
    CMP $A, 0x00
    JZ MON_FEED_KEY_STRING_DONE

    ; Advance pointer before MON_HANDLE_KEY, which may reuse $C/$D.
    CLC
    ADD $C, 0x01
    MOV MON_KEY_SCRIPT_PTR_LO, $C
    JNC .MON_FEED_KEY_STRING_NO_CARRY

    CLC
    ADD $D, 0x01
    MOV MON_KEY_SCRIPT_PTR_HI, $D

.MON_FEED_KEY_STRING_NO_CARRY:
    JSR MON_HANDLE_KEY

    JMP .MON_FEED_KEY_STRING_LOOP

MON_FEED_KEY_STRING_DONE:
    RTS

; ----------------------------------------------------------
; MON_DISPATCH_COMMAND
;
; Dispatches the zero-terminated command in MON_INPUT_BUF.
; ----------------------------------------------------------
MON_DISPATCH_COMMAND:
    JSR MON_INPUT_IS_EMPTY
    JNC MON_CMD_EMPTY

    JSR MON_INPUT_IS_HELP
    JNC MON_CMD_HELP

    JSR MON_INPUT_IS_CLS
    JNC MON_CMD_CLS

    JSR MON_INPUT_IS_INFO
    JNC MON_CMD_INFO

    JSR MON_INPUT_IS_DMP
    JNC MON_CMD_DMP

    JSR MON_INPUT_IS_DMP_ADDR
    JNC MON_CMD_DMP_ADDR

    JSR MON_INPUT_IS_PEEK_ADDR
    JNC MON_CMD_PEEK_ADDR

    JSR MON_INPUT_IS_POKE_ADDR_BYTE
    JNC MON_CMD_POKE_ADDR_BYTE

    JSR MON_INPUT_IS_FILL_RANGE_BYTE
    JNC MON_CMD_FILL_RANGE_BYTE

    JSR MON_INPUT_IS_RUN_ADDR
    JNC MON_CMD_RUN_ADDR

    JSR MON_INPUT_IS_LOAD
    JNC MON_CMD_LOAD_DEFAULT

    JSR MON_INPUT_IS_BOOT
    JNC MON_CMD_BOOT_DEFAULT

    JSR MON_INPUT_IS_CALL_ADDR
    JNC MON_CMD_CALL_ADDR

    JSR MON_INPUT_IS_REG
    JNC MON_CMD_REG

    JSR MON_INPUT_IS_SP
    JNC MON_CMD_SP

    JSR MON_INPUT_IS_STACK
    JNC MON_CMD_STACK

    JSR MON_INPUT_IS_CMP_RANGE_COUNT
    JNC MON_CMD_CMP_RANGE_COUNT

    JSR MON_INPUT_IS_CP_RANGE_COUNT
    JNC MON_CMD_CP_RANGE_COUNT

    JMP MON_CMD_UNKNOWN

; ----------------------------------------------------------
; MON_CMD_INFO
;
; Prints basic monitor information and returns to a fresh prompt.
;
; Output:
;   MONITOR INFO
;   LOAD 0X0200
;   INBUF 0X7100
;   CMDS 16
; ----------------------------------------------------------
MON_CMD_INFO:
    JSR OLED5_NEWLINE

    JSR MON_PREP_INFO_TITLE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE

    JSR MON_PREP_INFO_LOAD
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    ; Print load address as 0X0200.
    MOV $A, 0x30       ; 0
    JSR OLED5_PUTC
    MOV $A, 0x58       ; X
    JSR OLED5_PUTC

    MOV $C, 0x00
    MOV $D, 0x02
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE

    JSR MON_PREP_INFO_INBUF
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    ; Print input buffer address as 0X7100.
    MOV $A, 0x30       ; 0
    JSR OLED5_PUTC
    MOV $A, 0x58       ; X
    JSR OLED5_PUTC

    MOV $C, 0x00
    MOV $D, 0x71
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE

    JSR MON_PREP_INFO_CMDS
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    ; Print command count in decimal: 16.
    MOV $A, 0x31       ; 1
    JSR OLED5_PUTC
    MOV $A, 0x36       ; 6
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_PREP_INFO_TITLE
;
; Writes:
;   MONITOR INFO
; ----------------------------------------------------------
MON_PREP_INFO_TITLE:
    MOV $A, 0x4D       ; M
    MOV TITLE_BUF, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x49       ; I
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x54       ; T
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x52       ; R
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 7, $A
    MOV $A, 0x49       ; I
    MOV TITLE_BUF + 8, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 9, $A
    MOV $A, 0x46       ; F
    MOV TITLE_BUF + 10, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 11, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 12, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_INFO_LOAD
;
; Writes:
;   LOAD
; ----------------------------------------------------------
MON_PREP_INFO_LOAD:
    MOV $A, 0x4C       ; L
    MOV TITLE_BUF, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 5, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_INFO_INBUF
;
; Writes:
;   INBUF
; ----------------------------------------------------------
MON_PREP_INFO_INBUF:
    MOV $A, 0x49       ; I
    MOV TITLE_BUF, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x42       ; B
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x55       ; U
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x46       ; F
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 6, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_INFO_CMDS
;
; Writes:
;   CMDS
; ----------------------------------------------------------
MON_PREP_INFO_CMDS:
    MOV $A, 0x43       ; C
    MOV TITLE_BUF, $A
    MOV $A, 0x4D       ; M
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x53       ; S
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 5, $A
    RTS

; ----------------------------------------------------------
; MON_CMD_HELP
;
; Prints the help text and returns to a fresh prompt.
; ----------------------------------------------------------
MON_CMD_HELP:
    JSR OLED5_NEWLINE

    JSR MON_PREP_HELP_TEXT
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_CLS
;
; Clears the OLED text screen and redraws a fresh prompt.
; ----------------------------------------------------------
MON_CMD_CLS:
    JSR OLED5_CLEAR_TEXT_SCREEN
    JSR OLED5_HOME

    JSR MON_PREP_CLS_OK
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_DMP
;
; Dumps eight bytes from fixed address 0x0200.
;
; Output:
;   0200 XX XX XX XX
;   0204 XX XX XX XX
; ----------------------------------------------------------
MON_CMD_DMP:
    JSR OLED5_NEWLINE

    MOV $C, 0x00
    MOV $D, 0x02
    JSR MON_DMP_PRINT_8_BYTES_AT_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_DMP_ADDR
;
; Parses and runs:
;   DMP XXXX
;
; Example:
;   DMP 0200
;
; The four hex digits after "DMP " are parsed into a 16-bit
; address, then eight bytes are dumped from that address.
;
; Output:
;   XXXX XX XX XX XX
;   XXXX+4 XX XX XX XX
;
; Invalid address:
;   BAD ADDR
; ----------------------------------------------------------
MON_CMD_DMP_ADDR:
    JSR OLED5_NEWLINE

    ; Parse four hex characters from MON_INPUT_BUF + 4.
    MOV $C, 0x04
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    ; Check parser status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_DMP_ADDR_BAD

    ; Parsed address is already returned in $CD.
    JSR MON_DMP_PRINT_8_BYTES_AT_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_DMP_ADDR_BAD:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_PEEK_ADDR
;
; Parses and runs:
;   PEEK XXXX
;
; Example:
;   PEEK 0200
;
; The four hex digits after "PEEK " are parsed into a 16-bit
; address, then one byte is read and printed from that address.
;
; Output:
;   XXXX XX
;
; Invalid address:
;   BAD ADDR
; ----------------------------------------------------------
MON_CMD_PEEK_ADDR:
    JSR OLED5_NEWLINE

    ; Parse four hex characters from MON_INPUT_BUF + 5.
    MOV $C, 0x05
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    ; Check parser status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_PEEK_ADDR_BAD

    ; Save parsed address.
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; Print address.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Read and print one byte at the parsed address.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    MOV $A, [$CD]
    JSR OLED5_PRINT_HEX_BYTE

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_PEEK_ADDR_BAD:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_POKE_ADDR_BYTE
;
; Parses and runs:
;   POKE XXXX YY
;
; Example:
;   POKE 7300 A5
;
; Behavior:
;   - Parses XXXX as a 16-bit address.
;   - Parses YY as one byte.
;   - Writes YY to memory[XXXX].
;   - Prints the address and byte written.
;
; Output:
;   XXXX YY
;
; Errors:
;   BAD ADDR  if the address field is invalid
;   BAD BYTE  if the byte field is invalid
; ----------------------------------------------------------
MON_CMD_POKE_ADDR_BYTE:
    JSR OLED5_NEWLINE

    ; Parse address from MON_INPUT_BUF + 5.
    MOV $C, 0x05
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    ; Check address parse status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_POKE_ADDR_BYTE_BAD_ADDR

    ; Save parsed address.
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; Parse byte from MON_INPUT_BUF + 10.
    MOV $C, 0x0A
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_BYTE_AT_CD

    ; Save parsed byte.
    MOV MON_HEX_BYTE_RESULT, $A

    ; Check byte parse status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_POKE_ADDR_BYTE_BAD_BYTE

    ; Write byte to parsed address.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    MOV $A, MON_HEX_BYTE_RESULT
    MOV [$CD], $A

    ; Print address.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    ; Print space.
    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print written byte.
    MOV $A, MON_HEX_BYTE_RESULT
    JSR OLED5_PRINT_HEX_BYTE

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_POKE_ADDR_BYTE_BAD_ADDR:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_POKE_ADDR_BYTE_BAD_BYTE:
    JSR MON_PREP_BAD_BYTE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_FILL_RANGE_BYTE
;
; Parses and runs:
;   FILL XXXX YYYY YY
;
; Example:
;   FILL 7300 7303 A5
;
; Behavior:
;   - Parses XXXX as the start address.
;   - Parses YYYY as the inclusive end address.
;   - Parses YY as the byte value.
;   - Writes YY to every address from XXXX through YYYY.
;
; Output:
;   XXXX YYYY YY
;
; Errors:
;   BAD ADDR   if either address field is invalid
;   BAD BYTE   if the byte field is invalid
;   BAD RANGE  if START > END
; ----------------------------------------------------------
MON_CMD_FILL_RANGE_BYTE:
    JSR OLED5_NEWLINE

    ; Parse START from MON_INPUT_BUF + 5.
    MOV $C, 0x05
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_FILL_RANGE_BYTE_BAD_ADDR

    MOV MON_FILL_START_LO, $C
    MOV MON_FILL_START_HI, $D
    MOV MON_FILL_CUR_LO, $C
    MOV MON_FILL_CUR_HI, $D

    ; Parse END from MON_INPUT_BUF + 10.
    MOV $C, 0x0A
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_FILL_RANGE_BYTE_BAD_ADDR

    MOV MON_FILL_END_LO, $C
    MOV MON_FILL_END_HI, $D

    ; Parse BYTE from MON_INPUT_BUF + 15.
    MOV $C, 0x0F
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_BYTE_AT_CD

    MOV MON_FILL_VALUE, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_FILL_RANGE_BYTE_BAD_BYTE

    ; Reject START > END.
    MOV $A, MON_FILL_START_HI
    STC
    CMP $A, MON_FILL_END_HI
    JNC MON_CMD_FILL_RANGE_BYTE_RANGE_OK
    JZ MON_CMD_FILL_RANGE_BYTE_CHECK_LO
    JMP MON_CMD_FILL_RANGE_BYTE_BAD_RANGE

MON_CMD_FILL_RANGE_BYTE_CHECK_LO:
    MOV $A, MON_FILL_START_LO
    STC
    CMP $A, MON_FILL_END_LO
    JNC MON_CMD_FILL_RANGE_BYTE_RANGE_OK
    JZ MON_CMD_FILL_RANGE_BYTE_RANGE_OK
    JMP MON_CMD_FILL_RANGE_BYTE_BAD_RANGE

MON_CMD_FILL_RANGE_BYTE_RANGE_OK:
    JMP MON_FILL_LOOP

MON_FILL_LOOP:
    ; Write value to current address.
    MOV $C, MON_FILL_CUR_LO
    MOV $D, MON_FILL_CUR_HI
    MOV $A, MON_FILL_VALUE
    MOV [$CD], $A

    ; current address == END marks fill completion.
    MOV $A, MON_FILL_CUR_HI
    STC
    CMP $A, MON_FILL_END_HI
    JNZ MON_FILL_ADVANCE

    MOV $A, MON_FILL_CUR_LO
    STC
    CMP $A, MON_FILL_END_LO
    JZ MON_FILL_DONE

MON_FILL_ADVANCE:
    ; current++
    MOV $A, MON_FILL_CUR_LO
    CLC
    ADD $A, 0x01
    MOV MON_FILL_CUR_LO, $A
    JNC MON_FILL_LOOP

    MOV $A, MON_FILL_CUR_HI
    CLC
    ADD $A, 0x01
    MOV MON_FILL_CUR_HI, $A

    JMP MON_FILL_LOOP

MON_FILL_DONE:
    ; Print START.
    MOV $C, MON_FILL_START_LO
    MOV $D, MON_FILL_START_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print END.
    MOV $C, MON_FILL_END_LO
    MOV $D, MON_FILL_END_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print value.
    MOV $A, MON_FILL_VALUE
    JSR OLED5_PRINT_HEX_BYTE

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_FILL_RANGE_BYTE_BAD_ADDR:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_FILL_RANGE_BYTE_BAD_BYTE:
    JSR MON_PREP_BAD_BYTE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_FILL_RANGE_BYTE_BAD_RANGE:
    JSR MON_PREP_BAD_RANGE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_RUN_ADDR
;
; Parses and runs:
;   RUN XXXX
;
; Example:
;   RUN 0203
;
; Behavior:
;   - Parses XXXX as a 16-bit address.
;   - Hides the cursor.
;   - Transfers execution to that address.
;
; The command does not return to the monitor. The launched
; program owns execution after the jump.
;
; Errors:
;   BAD ADDR if the address field is invalid.
; ----------------------------------------------------------
MON_CMD_RUN_ADDR:
    JSR OLED5_NEWLINE

    ; Parse address from MON_INPUT_BUF + 4.
    MOV $C, 0x04
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    ; Check address parse status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_RUN_ADDR_BAD

    ; Save parsed target address in case display routines touch C/D.
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; RUN transfers control away from the monitor, so hide the cursor.
    JSR OLED5_CURSOR_HIDE

    ; Restore target address and jump to it.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JMP [$CD]

MON_CMD_RUN_ADDR_BAD:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_LOAD_DEFAULT
;
; Runs:
;   LOAD
;
; Behavior:
;   - Reads SD block 1003.
;   - Copies 512 bytes into RAM at 0x8000.
;   - Leaves execution in the monitor.
;
; Command roles:
;   LOAD      = copy program/data into RAM
;   RUN XXXX  = transfer execution
;
; Output on success:
;   LOAD 8000
;
; Output on failure:
;   LOAD FAIL
; ----------------------------------------------------------
MON_CMD_LOAD_DEFAULT:
    JSR OLED5_NEWLINE

    ; SD block 1003 = 0x000003EB.
    ; SD_READ_BLOCK_TO_RAM_512 reads the block number from
    ; 0x0100..0x0103 in big-endian order.
    MOV $A, 0x00
    MOV 0x0100, $A
    MOV 0x0101, $A

    MOV $A, 0x03
    MOV 0x0102, $A

    MOV $A, 0xEB
    MOV 0x0103, $A

    ; Destination = 0x8000.
    ; C = low byte, D = high byte.
    MOV $C, 0x00
    MOV $D, 0x80

    JSR SD_READ_BLOCK_TO_RAM_512
    JC MON_CMD_LOAD_DEFAULT_FAIL

MON_CMD_LOAD_DEFAULT_OK:
    ; Print "LOAD ".
    MOV $A, 0x4C       ; L
    JSR OLED5_PUTC
    MOV $A, 0x4F       ; O
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x44       ; D
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print destination address 8000.
    MOV $C, 0x00
    MOV $D, 0x80
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_LOAD_DEFAULT_FAIL:
    ; Print "LOAD FAIL".
    MOV $A, 0x4C       ; L
    JSR OLED5_PUTC
    MOV $A, 0x4F       ; O
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x44       ; D
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC
    MOV $A, 0x46       ; F
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x49       ; I
    JSR OLED5_PUTC
    MOV $A, 0x4C       ; L
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_BOOT_DEFAULT
;
; Runs:
;   BOOT
;
; Behavior:
;   - Hides the OLED cursor.
;   - Executes RST.
;
; BOOT transfers control to the ROM bootstrap, which loads the
; default SD payload per the configured boot descriptor
; and SD layout.
;
; The command does not return to the monitor.
; ----------------------------------------------------------
MON_CMD_BOOT_DEFAULT:
    JSR OLED5_NEWLINE
    JSR OLED5_CURSOR_HIDE

    RST

; ----------------------------------------------------------
; MON_CMD_CALL_ADDR
;
; Parses and runs:
;   CALL XXXX
;
; Example:
;   CALL 0203
;
; Behavior:
;   - Parses XXXX as a 16-bit address.
;   - Calls the routine at that address with JSR [$CD].
;   - Expects the called routine to return with RTS.
;   - Prints a fresh monitor prompt after the routine returns.
;
; Difference from RUN:
;   RUN XXXX   transfers execution and does not return
;   CALL XXXX  calls a subroutine and returns to the monitor
;
; Errors:
;   BAD ADDR if the address field is invalid.
; ----------------------------------------------------------
MON_CMD_CALL_ADDR:
    JSR OLED5_NEWLINE

    ; Parse address from MON_INPUT_BUF + 5.
    MOV $C, 0x05
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    ; Check address parse status.
    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CALL_ADDR_BAD

    ; Save parsed target address in case display routines touch C/D.
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; The called routine owns the screen while it runs.
    JSR OLED5_CURSOR_HIDE

    ; Restore target and call it.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JSR [$CD]

    ; Capture returned A/B/C/D before monitor display code
    ; clobbers the registers.
    JSR MON_REG_CAPTURE_ABCD

    ; After the target returns, resume the monitor.
    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_CALL_ADDR_BAD:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_REG_RESET
;
; Clears the saved register snapshot.
; ----------------------------------------------------------
MON_REG_RESET:
    MOV $A, 0x00
    MOV MON_REG_A, $A
    MOV MON_REG_B, $A
    MOV MON_REG_C, $A
    MOV MON_REG_D, $A
    MOV MON_REG_VALID, $A
    RTS


; ----------------------------------------------------------
; MON_REG_CAPTURE_ABCD
;
; Captures A/B/C/D at the call site.
;
; MON_CMD_CALL_ADDR invokes this immediately after the target
; routine returns, before display routines reuse the registers.
; ----------------------------------------------------------
MON_REG_CAPTURE_ABCD:
    MOV MON_REG_A, $A
    MOV MON_REG_B, $B
    MOV MON_REG_C, $C
    MOV MON_REG_D, $D

    MOV $A, 0x01
    MOV MON_REG_VALID, $A
    RTS

; ----------------------------------------------------------
; MON_CMD_REG
;
; Runs:
;   REG
;
; Prints the last A/B/C/D snapshot captured after a CALL target
; returned to the monitor.
;
; Output if a snapshot exists:
;   REG SNAP
;   A=xx B=xx
;   C=xx D=xx
;
; Output if no snapshot exists:
;   NO REG
; ----------------------------------------------------------
MON_CMD_REG:
    JSR OLED5_NEWLINE

    MOV $A, MON_REG_VALID
    STC
    CMP $A, 0x00
    JZ MON_CMD_REG_NONE

    ; Print "REG SNAP".
    MOV $A, 0x52       ; R
    JSR OLED5_PUTC
    MOV $A, 0x45       ; E
    JSR OLED5_PUTC
    MOV $A, 0x47       ; G
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC
    MOV $A, 0x53       ; S
    JSR OLED5_PUTC
    MOV $A, 0x4E       ; N
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x50       ; P
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE

    ; Print A=xx B=xx.
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x3D       ; =
    JSR OLED5_PUTC
    MOV $A, MON_REG_A
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, 0x20
    JSR OLED5_PUTC

    MOV $A, 0x42       ; B
    JSR OLED5_PUTC
    MOV $A, 0x3D       ; =
    JSR OLED5_PUTC
    MOV $A, MON_REG_B
    JSR OLED5_PRINT_HEX_BYTE

    JSR OLED5_NEWLINE

    ; Print C=xx D=xx.
    MOV $A, 0x43       ; C
    JSR OLED5_PUTC
    MOV $A, 0x3D       ; =
    JSR OLED5_PUTC
    MOV $A, MON_REG_C
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, 0x20
    JSR OLED5_PUTC

    MOV $A, 0x44       ; D
    JSR OLED5_PUTC
    MOV $A, 0x3D       ; =
    JSR OLED5_PUTC
    MOV $A, MON_REG_D
    JSR OLED5_PRINT_HEX_BYTE

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

MON_CMD_REG_NONE:
    ; Print "NO REG".
    MOV $A, 0x4E       ; N
    JSR OLED5_PUTC
    MOV $A, 0x4F       ; O
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC
    MOV $A, 0x52       ; R
    JSR OLED5_PUTC
    MOV $A, 0x45       ; E
    JSR OLED5_PUTC
    MOV $A, 0x47       ; G
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_SP
;
; Runs:
;   SP
;
; Prints the stack pointer captured at the start of this
; command handler.
;
; Output:
;   SP XXXX
;
; Note:
;   The value reflects the monitor call depth while the command
;   is active.
; ----------------------------------------------------------
MON_CMD_SP:
    JSR OLED5_NEWLINE

    ; Capture SP into C/D, then save it before display code
    ; can reuse C/D.
    MOV $CD, $SP
    MOV MON_SP_LO, $C
    MOV MON_SP_HI, $D

    ; Print "SP ".
    MOV $A, 0x53       ; S
    JSR OLED5_PUTC
    MOV $A, 0x50       ; P
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print captured SP.
    MOV $C, MON_SP_LO
    MOV $D, MON_SP_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_STACK
;
; Runs:
;   STACK
;
; Saves the stack pointer at the start of this command
; handler, then dumps eight bytes from that saved SP.
;
; Output:
;   STACK XXXX
;   XXXX XX XX XX XX
;   XXXX+4 XX XX XX XX
;
; Note:
;   The dump reflects the monitor call depth while the command
;   is active.
; ----------------------------------------------------------
MON_CMD_STACK:
    ; Capture SP before display calls use the stack further.
    MOV $CD, $SP
    MOV MON_STACK_PTR_LO, $C
    MOV MON_STACK_PTR_HI, $D

    JSR OLED5_NEWLINE

    ; Print "STACK ".
    MOV $A, 0x53       ; S
    JSR OLED5_PUTC
    MOV $A, 0x54       ; T
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x43       ; C
    JSR OLED5_PUTC
    MOV $A, 0x4B       ; K
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print captured SP.
    MOV $C, MON_STACK_PTR_LO
    MOV $D, MON_STACK_PTR_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE

    ; Dump eight bytes from saved SP.
    MOV $C, MON_STACK_PTR_LO
    MOV $D, MON_STACK_PTR_HI
    JSR MON_DMP_PRINT_8_BYTES_AT_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_CMP_RANGE_COUNT
;
; Runs:
;   CMP XXXX YYYY NN
;
; Behavior:
;   - Parses XXXX as the left/start address.
;   - Parses YYYY as the right/start address.
;   - Parses NN as the byte count.
;   - Compares NN bytes from both regions.
;
; Output if all compared bytes match:
;   CMP SAME
;
; Output if a mismatch is found:
;   DIFF XXXX YYYY
;
; where XXXX and YYYY are the first different addresses.
;
; Errors:
;   BAD ADDR if either address field is invalid.
;   BAD BYTE if the count field is invalid.
; ----------------------------------------------------------
MON_CMD_CMP_RANGE_COUNT:
    JSR OLED5_NEWLINE

    ; Parse LEFT address from MON_INPUT_BUF + 4.
    MOV $C, 0x04
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CMP_RANGE_COUNT_BAD_ADDR

    MOV MON_MEMCMP_LEFT_LO, $C
    MOV MON_MEMCMP_LEFT_HI, $D

    ; Parse RIGHT address from MON_INPUT_BUF + 9.
    MOV $C, 0x09
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CMP_RANGE_COUNT_BAD_ADDR

    MOV MON_MEMCMP_RIGHT_LO, $C
    MOV MON_MEMCMP_RIGHT_HI, $D

    ; Parse COUNT byte from MON_INPUT_BUF + 14.
    MOV $C, 0x0E
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_BYTE_AT_CD

    MOV MON_MEMCMP_COUNT, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CMP_RANGE_COUNT_BAD_BYTE

    ; Count 00 is valid and means an empty range matches.
    MOV $A, MON_MEMCMP_COUNT
    STC
    CMP $A, 0x00
    JZ MON_CMD_CMP_RANGE_COUNT_SAME

MON_MEMCMP_LOOP:
    ; Read left byte.
    MOV $C, MON_MEMCMP_LEFT_LO
    MOV $D, MON_MEMCMP_LEFT_HI
    MOV $A, [$CD]
    MOV MON_MEMCMP_LEFT_BYTE, $A

    ; Read right byte.
    MOV $C, MON_MEMCMP_RIGHT_LO
    MOV $D, MON_MEMCMP_RIGHT_HI
    MOV $A, [$CD]
    MOV MON_MEMCMP_RIGHT_BYTE, $A

    ; Compare bytes.
    MOV $A, MON_MEMCMP_LEFT_BYTE
    STC
    CMP $A, MON_MEMCMP_RIGHT_BYTE
    JNZ MON_CMD_CMP_RANGE_COUNT_DIFF

    ; One byte matched. Decrement count.
    MOV $A, MON_MEMCMP_COUNT
    STC
    SUB $A, 0x01
    MOV MON_MEMCMP_COUNT, $A

    STC
    CMP $A, 0x00
    JZ MON_CMD_CMP_RANGE_COUNT_SAME

    ; left++
    MOV $A, MON_MEMCMP_LEFT_LO
    CLC
    ADD $A, 0x01
    MOV MON_MEMCMP_LEFT_LO, $A
    JNC .MON_MEMCMP_LEFT_INC_DONE

    MOV $A, MON_MEMCMP_LEFT_HI
    CLC
    ADD $A, 0x01
    MOV MON_MEMCMP_LEFT_HI, $A

.MON_MEMCMP_LEFT_INC_DONE:
    ; right++
    MOV $A, MON_MEMCMP_RIGHT_LO
    CLC
    ADD $A, 0x01
    MOV MON_MEMCMP_RIGHT_LO, $A
    JNC .MON_MEMCMP_RIGHT_INC_DONE

    MOV $A, MON_MEMCMP_RIGHT_HI
    CLC
    ADD $A, 0x01
    MOV MON_MEMCMP_RIGHT_HI, $A

.MON_MEMCMP_RIGHT_INC_DONE:
    JMP MON_MEMCMP_LOOP


MON_CMD_CMP_RANGE_COUNT_SAME:
    ; Print "CMP SAME".
    MOV $A, 0x43       ; C
    JSR OLED5_PUTC
    MOV $A, 0x4D       ; M
    JSR OLED5_PUTC
    MOV $A, 0x50       ; P
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC
    MOV $A, 0x53       ; S
    JSR OLED5_PUTC
    MOV $A, 0x41       ; A
    JSR OLED5_PUTC
    MOV $A, 0x4D       ; M
    JSR OLED5_PUTC
    MOV $A, 0x45       ; E
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS


MON_CMD_CMP_RANGE_COUNT_DIFF:
    ; Save mismatch addresses before display code clobbers C/D.
    ; Memory-to-memory MOV is not supported, so copy through A.

    MOV $A, MON_MEMCMP_LEFT_LO
    MOV MON_MEMCMP_MIS_L_LO, $A

    MOV $A, MON_MEMCMP_LEFT_HI
    MOV MON_MEMCMP_MIS_L_HI, $A

    MOV $A, MON_MEMCMP_RIGHT_LO
    MOV MON_MEMCMP_MIS_R_LO, $A

    MOV $A, MON_MEMCMP_RIGHT_HI
    MOV MON_MEMCMP_MIS_R_HI, $A

    ; Print "DIFF ".
    MOV $A, 0x44       ; D
    JSR OLED5_PUTC
    MOV $A, 0x49       ; I
    JSR OLED5_PUTC
    MOV $A, 0x46       ; F
    JSR OLED5_PUTC
    MOV $A, 0x46       ; F
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print left mismatch address.
    MOV $C, MON_MEMCMP_MIS_L_LO
    MOV $D, MON_MEMCMP_MIS_L_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Print right mismatch address.
    MOV $C, MON_MEMCMP_MIS_R_LO
    MOV $D, MON_MEMCMP_MIS_R_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS


MON_CMD_CMP_RANGE_COUNT_BAD_ADDR:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS


MON_CMD_CMP_RANGE_COUNT_BAD_BYTE:
    JSR MON_PREP_BAD_BYTE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_CMD_CP_RANGE_COUNT
;
; Runs:
;   CP XXXX YYYY NN
;
; Behavior:
;   - Parses XXXX as the source address.
;   - Parses YYYY as the destination address.
;   - Parses NN as the byte count.
;   - Copies NN bytes from source to destination.
;
; Output on success:
;   CP DONE
;
; Errors:
;   BAD ADDR if either address field is invalid.
;   BAD BYTE if the count field is invalid.
;
; Note:
;   Simple forward copy. Overlap follows normal forward-copy
;   semantics.
; ----------------------------------------------------------
MON_CMD_CP_RANGE_COUNT:
    JSR OLED5_NEWLINE

    ; Parse source address from MON_INPUT_BUF + 3.
    MOV $C, 0x03
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CP_RANGE_COUNT_BAD_ADDR

    MOV MON_CP_SRC_LO, $C
    MOV MON_CP_SRC_HI, $D

    ; Parse destination address from MON_INPUT_BUF + 8.
    MOV $C, 0x08
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_WORD_AT_CD

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CP_RANGE_COUNT_BAD_ADDR

    MOV MON_CP_DST_LO, $C
    MOV MON_CP_DST_HI, $D

    ; Parse count byte from MON_INPUT_BUF + 13.
    MOV $C, 0x0D
    MOV $D, MON_INPUT_BUF_HI
    JSR MON_PARSE_HEX_BYTE_AT_CD

    MOV MON_CP_COUNT, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_CMD_CP_RANGE_COUNT_BAD_BYTE

    ; Count 00 is valid and means no bytes are copied.
    MOV $A, MON_CP_COUNT
    STC
    CMP $A, 0x00
    JZ MON_CMD_CP_RANGE_COUNT_DONE

MON_CP_LOOP:
    ; Read byte from source.
    MOV $C, MON_CP_SRC_LO
    MOV $D, MON_CP_SRC_HI
    MOV $A, [$CD]
    MOV MON_CP_BYTE_TMP, $A

    ; Write byte to destination.
    MOV $C, MON_CP_DST_LO
    MOV $D, MON_CP_DST_HI
    MOV $A, MON_CP_BYTE_TMP
    MOV [$CD], $A

    ; One byte copied. Decrement count.
    MOV $A, MON_CP_COUNT
    STC
    SUB $A, 0x01
    MOV MON_CP_COUNT, $A

    STC
    CMP $A, 0x00
    JZ MON_CMD_CP_RANGE_COUNT_DONE

    ; source++
    MOV $A, MON_CP_SRC_LO
    CLC
    ADD $A, 0x01
    MOV MON_CP_SRC_LO, $A
    JNC .MON_CP_SRC_INC_DONE

    MOV $A, MON_CP_SRC_HI
    CLC
    ADD $A, 0x01
    MOV MON_CP_SRC_HI, $A

.MON_CP_SRC_INC_DONE:
    ; destination++
    MOV $A, MON_CP_DST_LO
    CLC
    ADD $A, 0x01
    MOV MON_CP_DST_LO, $A
    JNC .MON_CP_DST_INC_DONE

    MOV $A, MON_CP_DST_HI
    CLC
    ADD $A, 0x01
    MOV MON_CP_DST_HI, $A

.MON_CP_DST_INC_DONE:
    JMP MON_CP_LOOP


MON_CMD_CP_RANGE_COUNT_DONE:
    ; Print "CP DONE".
    MOV $A, 0x43       ; C
    JSR OLED5_PUTC
    MOV $A, 0x50       ; P
    JSR OLED5_PUTC
    MOV $A, 0x20
    JSR OLED5_PUTC
    MOV $A, 0x44       ; D
    JSR OLED5_PUTC
    MOV $A, 0x4F       ; O
    JSR OLED5_PUTC
    MOV $A, 0x4E       ; N
    JSR OLED5_PUTC
    MOV $A, 0x45       ; E
    JSR OLED5_PUTC

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS


MON_CMD_CP_RANGE_COUNT_BAD_ADDR:
    JSR MON_PREP_BAD_ADDR
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS


MON_CMD_CP_RANGE_COUNT_BAD_BYTE:
    JSR MON_PREP_BAD_BYTE
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_DMP_PRINT_4_BYTES_AT_CD
;
; Input:
;   $C = low byte of start address
;   $D = high byte of start address
;
; Output:
;   AAAA XX XX XX XX
;
; Example:
;   CD = 0x0200 -> prints:
;      0200 xx xx xx xx
;
;   The start address is stored in RAM because hex-print
;   routines and memory reads reuse $C/$D.
; ----------------------------------------------------------
MON_DMP_PRINT_4_BYTES_AT_CD:
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; Print start address.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JSR OLED5_PRINT_HEX_WORD_CD

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Byte 0.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    MOV $A, [$CD]
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Byte 1.
    MOV $C, MON_DMP_ADDR_LO
    CLC
    ADD $C, 0x01
    JNC .MON_DMP_BYTE1_NO_CARRY
    MOV $D, MON_DMP_ADDR_HI
    CLC
    ADD $D, 0x01
    JMP .MON_DMP_BYTE1_READY

.MON_DMP_BYTE1_NO_CARRY:
    MOV $D, MON_DMP_ADDR_HI

.MON_DMP_BYTE1_READY:
    MOV $A, [$CD]
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Byte 2.
    MOV $C, MON_DMP_ADDR_LO
    CLC
    ADD $C, 0x02
    JNC .MON_DMP_BYTE2_NO_CARRY
    MOV $D, MON_DMP_ADDR_HI
    CLC
    ADD $D, 0x01
    JMP .MON_DMP_BYTE2_READY

.MON_DMP_BYTE2_NO_CARRY:
    MOV $D, MON_DMP_ADDR_HI

.MON_DMP_BYTE2_READY:
    MOV $A, [$CD]
    JSR OLED5_PRINT_HEX_BYTE

    MOV $A, 0x20
    JSR OLED5_PUTC

    ; Byte 3.
    MOV $C, MON_DMP_ADDR_LO
    CLC
    ADD $C, 0x03
    JNC .MON_DMP_BYTE3_NO_CARRY
    MOV $D, MON_DMP_ADDR_HI
    CLC
    ADD $D, 0x01
    JMP .MON_DMP_BYTE3_READY

.MON_DMP_BYTE3_NO_CARRY:
    MOV $D, MON_DMP_ADDR_HI

.MON_DMP_BYTE3_READY:
    MOV $A, [$CD]
    JSR OLED5_PRINT_HEX_BYTE

    RTS

; ----------------------------------------------------------
; MON_DMP_PRINT_8_BYTES_AT_CD
;
; Input:
;   $C = low byte of start address
;   $D = high byte of start address
;
; Output:
;   AAAA XX XX XX XX
;   AAAA+4 XX XX XX XX
;
;   Shared dump body used by:
;      DMP
;      DMP XXXX
; ----------------------------------------------------------
MON_DMP_PRINT_8_BYTES_AT_CD:
    ; Save base address.
    MOV MON_DMP_ADDR_LO, $C
    MOV MON_DMP_ADDR_HI, $D

    ; First row: base + 0.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI
    JSR MON_DMP_PRINT_4_BYTES_AT_CD

    JSR OLED5_NEWLINE

    ; Second row: base + 4.
    MOV $C, MON_DMP_ADDR_LO
    MOV $D, MON_DMP_ADDR_HI

    CLC
    ADD $C, 0x04
    JNC .MON_DMP_PRINT_8_PLUS4_OK

    CLC
    ADD $D, 0x01

.MON_DMP_PRINT_8_PLUS4_OK:
    JSR MON_DMP_PRINT_4_BYTES_AT_CD

    RTS

; ----------------------------------------------------------
; MON_CMD_UNKNOWN
;
; Prints UNKNOWN and returns to a fresh prompt.
; ----------------------------------------------------------
MON_CMD_UNKNOWN:
    JSR OLED5_NEWLINE

    JSR MON_PREP_UNKNOWN_TEXT
    MOV $C, 0x40
    MOV $D, 0x70
    JSR OLED5_DRAW_STRING

    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    STC
    RTS

; ----------------------------------------------------------
; MON_CMD_EMPTY
;
; Handles Enter on an empty prompt.
;
; Behavior:
;   Move to the next line and print a fresh prompt.
; ----------------------------------------------------------
MON_CMD_EMPTY:
    JSR OLED5_NEWLINE
    JSR MON_PRINT_FRESH_PROMPT

    CLC
    RTS

; ----------------------------------------------------------
; MON_PREP_HELP_TEXT
;
; Writes a compact command overview:
;
;   HELP CLS INFO
;   MEM DMP PEEK POKE
;   MEM FILL CMP CP LOAD
;   EXEC RUN CALL BOOT
;   REG SP STACK
;
; The compact format fits the 21-column by 8-row OLED terminal.
;
;   CMP compares two memory ranges and reports same or first mismatch.
;   CP copies bytes from one memory range to another.
; ----------------------------------------------------------
MON_PREP_HELP_TEXT:
    ; Build text at TITLE_BUF = 0x7040.
    MOV $C, 0x40
    MOV $D, 0x70

    ; Line 1: HELP CLS INFO
    MOV $A, 0x48       ; H
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x53       ; S
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x49       ; I
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4E       ; N
    JSR MON_HELP_APPEND_A
    MOV $A, 0x46       ; F
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4F       ; O
    JSR MON_HELP_APPEND_A
    MOV $A, 0x0A
    JSR MON_HELP_APPEND_A

    ; Line 2: MEM DMP PEEK POKE
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x44       ; D
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4B       ; K
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4F       ; O
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4B       ; K
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x0A
    JSR MON_HELP_APPEND_A

    ; Line 3: MEM FILL CMP CP LOAD
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A

    MOV $A, 0x46       ; F
    JSR MON_HELP_APPEND_A
    MOV $A, 0x49       ; I
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A

    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4D       ; M
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A

    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A

    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4F       ; O
    JSR MON_HELP_APPEND_A
    MOV $A, 0x41       ; A
    JSR MON_HELP_APPEND_A
    MOV $A, 0x44       ; D
    JSR MON_HELP_APPEND_A

    MOV $A, 0x0A
    JSR MON_HELP_APPEND_A

    ; Line 4: EXEC RUN CALL BOOT
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x58       ; X
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x52       ; R
    JSR MON_HELP_APPEND_A
    MOV $A, 0x55       ; U
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4E       ; N
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x41       ; A
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4C       ; L
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x42       ; B
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4F       ; O
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4F       ; O
    JSR MON_HELP_APPEND_A
    MOV $A, 0x54       ; T
    JSR MON_HELP_APPEND_A
    MOV $A, 0x0A
    JSR MON_HELP_APPEND_A

    ; Line 5: REG SP STACK
    MOV $A, 0x52       ; R
    JSR MON_HELP_APPEND_A
    MOV $A, 0x45       ; E
    JSR MON_HELP_APPEND_A
    MOV $A, 0x47       ; G
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x53       ; S
    JSR MON_HELP_APPEND_A
    MOV $A, 0x50       ; P
    JSR MON_HELP_APPEND_A
    MOV $A, 0x20
    JSR MON_HELP_APPEND_A
    MOV $A, 0x53       ; S
    JSR MON_HELP_APPEND_A
    MOV $A, 0x54       ; T
    JSR MON_HELP_APPEND_A
    MOV $A, 0x41       ; A
    JSR MON_HELP_APPEND_A
    MOV $A, 0x43       ; C
    JSR MON_HELP_APPEND_A
    MOV $A, 0x4B       ; K
    JSR MON_HELP_APPEND_A

    ; Null terminator.
    MOV $A, 0x00
    JSR MON_HELP_APPEND_A

    RTS


; ----------------------------------------------------------
; MON_HELP_APPEND_A
;
; Appends the byte in $A to the help text buffer pointed to
; by $C/$D, then increments $C/$D.
;
; Input:
;   $A = byte to write
;   $C/$D = destination pointer
;
; Output:
;   $C/$D points to the next byte
; ----------------------------------------------------------
MON_HELP_APPEND_A:
    MOV [$CD], $A

    CLC
    ADD $C, 0x01
    JNC MON_HELP_APPEND_A_DONE

    CLC
    ADD $D, 0x01

MON_HELP_APPEND_A_DONE:
    RTS

; ----------------------------------------------------------
; MON_PREP_CLS_OK
;
; Writes:
;   CLS OK\n
; ----------------------------------------------------------
MON_PREP_CLS_OK:
    MOV $A, 0x43       ; C
    MOV TITLE_BUF, $A
    MOV $A, 0x4C       ; L
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x53       ; S
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x4B       ; K
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x0A
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 7, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_UNKNOWN_TEXT
;
; Writes:
;   UNKNOWN
; ----------------------------------------------------------
MON_PREP_UNKNOWN_TEXT:
    MOV $A, 0x55       ; U
    MOV TITLE_BUF, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x4B       ; K
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x4F       ; O
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x57       ; W
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 7, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_BAD_ADDR
;
; Writes:
;   BAD ADDR
; ----------------------------------------------------------
MON_PREP_BAD_ADDR:
    MOV $A, 0x42       ; B
    MOV TITLE_BUF, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x52       ; R
    MOV TITLE_BUF + 7, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 8, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_BAD_BYTE
;
; Writes:
;   BAD BYTE
; ----------------------------------------------------------
MON_PREP_BAD_BYTE:
    MOV $A, 0x42       ; B
    MOV TITLE_BUF, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x42       ; B
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x59       ; Y
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x54       ; T
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x45       ; E
    MOV TITLE_BUF + 7, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 8, $A
    RTS

; ----------------------------------------------------------
; MON_PREP_BAD_RANGE
;
; Writes:
;   BAD RANGE
; ----------------------------------------------------------
MON_PREP_BAD_RANGE:
    MOV $A, 0x42       ; B
    MOV TITLE_BUF, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 1, $A
    MOV $A, 0x44       ; D
    MOV TITLE_BUF + 2, $A
    MOV $A, 0x20
    MOV TITLE_BUF + 3, $A
    MOV $A, 0x52       ; R
    MOV TITLE_BUF + 4, $A
    MOV $A, 0x41       ; A
    MOV TITLE_BUF + 5, $A
    MOV $A, 0x4E       ; N
    MOV TITLE_BUF + 6, $A
    MOV $A, 0x47       ; G
    MOV TITLE_BUF + 7, $A
    MOV $A, 0x45       ; E
    MOV TITLE_BUF + 8, $A
    MOV $A, 0x00
    MOV TITLE_BUF + 9, $A
    RTS
