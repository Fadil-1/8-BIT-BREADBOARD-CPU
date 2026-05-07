; ==========================================================
; monitor_input.asm
; ==========================================================
; Monitor input, command checks, and hex parser helpers.
;
; Original version: April 2026
; Last Modified: May 2026
; Fadil Isamotu
; ==========================================================

; ----------------------------------------------------------
; MON_INPUT_RESET
;
; Clears the current input length.
; Does not clear RAM buffer contents.
; No OLED output.
; ----------------------------------------------------------
MON_INPUT_RESET:
    MOV $A, 0x00
    MOV MON_INPUT_LEN, $A
    RTS

; ----------------------------------------------------------
; MON_INPUT_TERMINATE
;
; Writes a null terminator at:
;   MON_INPUT_BUF[MON_INPUT_LEN]
;
; Converts the current input buffer to a zero-terminated
; command string.
;
; Example:
;   If buffer contains A B D and MON_INPUT_LEN = 3,
;   writes 0x00 at MON_INPUT_BUF + 3.
; ----------------------------------------------------------
MON_INPUT_TERMINATE:
    MOV $C, MON_INPUT_LEN
    MOV $D, MON_INPUT_BUF_HI

    MOV $A, 0x00
    MOV [$CD], $A

    RTS

; ----------------------------------------------------------
; MON_INPUT_EQUALS_STRING
;
; Compares MON_INPUT_BUF to a zero-terminated string.
;
; Input:
;   $C = low byte of comparison string pointer
;   $D = high byte of comparison string pointer
;
; Returns:
;   carry clear = strings match exactly
;   carry set   = strings do not match
;
;   MON_INPUT_BUF must already be zero-terminated.
;   The routine compares byte-by-byte until both strings end
;   or a mismatch is found.
; ----------------------------------------------------------
MON_INPUT_EQUALS_STRING:
    ; Save comparison string pointer.
    MOV MON_CMP_TEST_PTR_LO, $C
    MOV MON_CMP_TEST_PTR_HI, $D

    ; Input pointer starts at MON_INPUT_BUF = 0x7100.
    MOV $A, 0x00
    MOV MON_CMP_INPUT_PTR_LO, $A

    MOV $A, MON_INPUT_BUF_HI
    MOV MON_CMP_INPUT_PTR_HI, $A

.MON_INPUT_EQUALS_LOOP:
    ; Read current input character.
    MOV $C, MON_CMP_INPUT_PTR_LO
    MOV $D, MON_CMP_INPUT_PTR_HI
    MOV $A, [$CD]
    MOV MON_CMP_INPUT_CHAR, $A

    MOV $C, MON_CMP_TEST_PTR_LO
    MOV $D, MON_CMP_TEST_PTR_HI
    MOV $A, [$CD]
    MOV MON_CMP_TEST_CHAR, $A

    ; Compare characters.
    MOV $A, MON_CMP_INPUT_CHAR
    STC
    CMP $A, MON_CMP_TEST_CHAR
    JNZ MON_INPUT_EQUALS_NO

    ; Both characters at 0x00 means the strings matched.
    MOV $A, MON_CMP_INPUT_CHAR
    STC
    CMP $A, 0x00
    JZ MON_INPUT_EQUALS_YES

    ; Advance input pointer.
    MOV $A, MON_CMP_INPUT_PTR_LO
    CLC
    ADD $A, 0x01
    MOV MON_CMP_INPUT_PTR_LO, $A

    JNC .MON_INPUT_EQUALS_INPUT_NO_CARRY

    MOV $A, MON_CMP_INPUT_PTR_HI
    CLC
    ADD $A, 0x01
    MOV MON_CMP_INPUT_PTR_HI, $A

.MON_INPUT_EQUALS_INPUT_NO_CARRY:
    MOV $A, MON_CMP_TEST_PTR_LO
    CLC
    ADD $A, 0x01
    MOV MON_CMP_TEST_PTR_LO, $A

    JNC .MON_INPUT_EQUALS_TEST_NO_CARRY

    MOV $A, MON_CMP_TEST_PTR_HI
    CLC
    ADD $A, 0x01
    MOV MON_CMP_TEST_PTR_HI, $A

.MON_INPUT_EQUALS_TEST_NO_CARRY:
    JMP .MON_INPUT_EQUALS_LOOP

MON_INPUT_EQUALS_YES:
    CLC
    RTS

MON_INPUT_EQUALS_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_HELP
;
; Checks whether the current input buffer is exactly:
;   HELP
;
; Returns:
;   carry clear = command is HELP
;   carry set   = command is not HELP
;
; Uses:
;   MON_INPUT_EQUALS_STRING
; ----------------------------------------------------------
MON_INPUT_IS_HELP:
    MOV $C, 0x20
    MOV $D, MON_KEY_SCRIPT_BUF_HI
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_INFO
;
; Checks whether the current input buffer is exactly:
;   INFO
;
; Returns:
;   carry clear = command is INFO
;   carry set   = command is not INFO
;
; Uses:
;   MON_INPUT_EQUALS_STRING
; ----------------------------------------------------------
MON_INPUT_IS_INFO:
    MOV $C, 0x30
    MOV $D, MON_KEY_SCRIPT_BUF_HI
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_CLS
;
; Checks whether the current input buffer is exactly:
;   CLS
;
; Returns:
;   carry clear = command is CLS
;   carry set   = command is not CLS
;
; Uses:
;   MON_INPUT_EQUALS_STRING
; ----------------------------------------------------------
MON_INPUT_IS_CLS:
    MOV $C, 0x28
    MOV $D, MON_KEY_SCRIPT_BUF_HI
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_DMP
;
; Checks whether the current input buffer is exactly:
;   DMP
;
; Returns:
;   carry clear = command is DMP
;   carry set   = command is not DMP
;
; Uses:
;   MON_INPUT_EQUALS_STRING
; ----------------------------------------------------------
MON_INPUT_IS_DMP:
    MOV $C, 0x38
    MOV $D, MON_KEY_SCRIPT_BUF_HI
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_EMPTY
;
; Checks whether the current input buffer is empty.
;
; Returns:
;   carry clear = input is empty
;   carry set   = input is not empty
; ----------------------------------------------------------
MON_INPUT_IS_EMPTY:
    MOV $A, MON_INPUT_LEN

    STC
    CMP $A, 0x00
    JZ MON_INPUT_IS_EMPTY_YES

MON_INPUT_IS_EMPTY_NO:
    STC
    RTS

MON_INPUT_IS_EMPTY_YES:
    CLC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_DMP_ADDR
;
; Checks whether the input begins with:
;   DMP
;
; Recognizes the argument form:
;   DMP 0200
;
; Returns:
;   carry clear = input begins with "DMP "
;   carry set   = input does not begin with "DMP "
;
;   Only the command prefix is checked. The address itself is
;   parsed later by MON_CMD_DMP_ADDR.
; ----------------------------------------------------------
MON_INPUT_IS_DMP_ADDR:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x44       ; D
    JNZ MON_INPUT_IS_DMP_ADDR_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x4D       ; M
    JNZ MON_INPUT_IS_DMP_ADDR_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x50       ; P
    JNZ MON_INPUT_IS_DMP_ADDR_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x20       ; space
    JNZ MON_INPUT_IS_DMP_ADDR_NO

MON_INPUT_IS_DMP_ADDR_YES:
    CLC
    RTS

MON_INPUT_IS_DMP_ADDR_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_PEEK_ADDR
;
; Checks whether the input begins with:
;   PEEK
;
; Recognizes the argument form:
;   PEEK 0200
;
; Returns:
;   carry clear = input begins with "PEEK "
;   carry set   = input does not begin with "PEEK "
;
;   Only the command prefix is checked. The address itself is
;   parsed later by MON_CMD_PEEK_ADDR.
; ----------------------------------------------------------
MON_INPUT_IS_PEEK_ADDR:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x50       ; P
    JNZ MON_INPUT_IS_PEEK_ADDR_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x45       ; E
    JNZ MON_INPUT_IS_PEEK_ADDR_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x45       ; E
    JNZ MON_INPUT_IS_PEEK_ADDR_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x4B       ; K
    JNZ MON_INPUT_IS_PEEK_ADDR_NO

    MOV $A, MON_INPUT_BUF + 4
    STC
    CMP $A, 0x20       ; space
    JNZ MON_INPUT_IS_PEEK_ADDR_NO

MON_INPUT_IS_PEEK_ADDR_YES:
    CLC
    RTS

MON_INPUT_IS_PEEK_ADDR_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_POKE_ADDR_BYTE
;
; Checks whether the input has the command shape:
;   POKE XXXX YY
;
; Only the fixed command structure is checked:
;   POKE
;   space after POKE
;   space between address and byte
;   null terminator after the byte
;
; The address and byte characters themselves are parsed later
; by MON_CMD_POKE_ADDR_BYTE.
;
; Returns:
;   carry clear = input shape matches "POKE XXXX YY"
;   carry set   = input shape does not match
; ----------------------------------------------------------
MON_INPUT_IS_POKE_ADDR_BYTE:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x50       ; P
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x4F       ; O
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x4B       ; K
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x45       ; E
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 4
    STC
    CMP $A, 0x20       ; space after POKE
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 9
    STC
    CMP $A, 0x20       ; space between address and byte
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

    MOV $A, MON_INPUT_BUF + 12
    STC
    CMP $A, 0x00       ; require exact end after two byte digits
    JNZ MON_INPUT_IS_POKE_ADDR_BYTE_NO

MON_INPUT_IS_POKE_ADDR_BYTE_YES:
    CLC
    RTS

MON_INPUT_IS_POKE_ADDR_BYTE_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_FILL_RANGE_BYTE
;
; Checks whether the input has the command shape:
;   FILL XXXX YYYY YY
;
; Only the fixed structure is checked:
;   FILL
;   space after FILL
;   space between START and END
;   space between END and BYTE
;   null terminator after BYTE
;
; The actual hex fields are parsed later by MON_CMD_FILL_RANGE_BYTE.
;
; Returns:
;   carry clear = input shape matches "FILL XXXX YYYY YY"
;   carry set   = input shape does not match
; ----------------------------------------------------------
MON_INPUT_IS_FILL_RANGE_BYTE:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x46       ; F
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x49       ; I
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x4C       ; L
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x4C       ; L
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 4
    STC
    CMP $A, 0x20       ; space after FILL
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 9
    STC
    CMP $A, 0x20       ; space between START and END
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 14
    STC
    CMP $A, 0x20       ; space between END and BYTE
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

    MOV $A, MON_INPUT_BUF + 17
    STC
    CMP $A, 0x00       ; exact end after byte
    JNZ MON_INPUT_IS_FILL_RANGE_BYTE_NO

MON_INPUT_IS_FILL_RANGE_BYTE_YES:
    CLC
    RTS

MON_INPUT_IS_FILL_RANGE_BYTE_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_RUN_ADDR
;
; Checks whether the input has the command shape:
;   RUN XXXX
;
; Only checks:
;   RUN
;   space after RUN
;   null terminator after the 4 address digits
;
; The actual address characters are parsed later by
; MON_CMD_RUN_ADDR.
;
; Returns:
;   carry clear = input shape matches "RUN XXXX"
;   carry set   = input does not match
; ----------------------------------------------------------
MON_INPUT_IS_RUN_ADDR:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x52       ; R
    JNZ MON_INPUT_IS_RUN_ADDR_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x55       ; U
    JNZ MON_INPUT_IS_RUN_ADDR_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x4E       ; N
    JNZ MON_INPUT_IS_RUN_ADDR_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x20       ; space after RUN
    JNZ MON_INPUT_IS_RUN_ADDR_NO

    MOV $A, MON_INPUT_BUF + 8
    STC
    CMP $A, 0x00       ; exact end after address
    JNZ MON_INPUT_IS_RUN_ADDR_NO

MON_INPUT_IS_RUN_ADDR_YES:
    CLC
    RTS

MON_INPUT_IS_RUN_ADDR_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_CALL_ADDR
;
; Checks whether the input has the command shape:
;   CALL XXXX
;
; Only checks:
;   CALL
;   space after CALL
;   null terminator after the 4 address digits
;
; The actual address characters are parsed later by
; MON_CMD_CALL_ADDR.
;
; Returns:
;   carry clear = input shape matches "CALL XXXX"
;   carry set   = input does not match
; ----------------------------------------------------------
MON_INPUT_IS_CALL_ADDR:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x43       ; C
    JNZ MON_INPUT_IS_CALL_ADDR_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x41       ; A
    JNZ MON_INPUT_IS_CALL_ADDR_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x4C       ; L
    JNZ MON_INPUT_IS_CALL_ADDR_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x4C       ; L
    JNZ MON_INPUT_IS_CALL_ADDR_NO

    MOV $A, MON_INPUT_BUF + 4
    STC
    CMP $A, 0x20       ; space after CALL
    JNZ MON_INPUT_IS_CALL_ADDR_NO

    MOV $A, MON_INPUT_BUF + 9
    STC
    CMP $A, 0x00       ; exact end after address
    JNZ MON_INPUT_IS_CALL_ADDR_NO

MON_INPUT_IS_CALL_ADDR_YES:
    CLC
    RTS

MON_INPUT_IS_CALL_ADDR_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_LOAD
;
; Checks whether the input is exactly:
;   LOAD
;
; Returns:
;   carry clear = input equals LOAD
;   carry set   = input does not equal LOAD
; ----------------------------------------------------------
MON_INPUT_IS_LOAD:
    MOV $C, 0x60
    MOV $D, 0x72
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_BOOT
;
; Checks whether the input is exactly:
;   BOOT
;
; Returns:
;   carry clear = input equals BOOT
;   carry set   = input does not equal BOOT
; ----------------------------------------------------------
MON_INPUT_IS_BOOT:
    MOV $C, 0x68
    MOV $D, 0x72
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_REG
;
; Checks whether the input is exactly:
;   REG
;
; Returns:
;   carry clear = input equals REG
;   carry set   = input does not equal REG
; ----------------------------------------------------------
MON_INPUT_IS_REG:
    MOV $C, 0x70
    MOV $D, 0x72
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_SP
;
; Checks whether the input is exactly:
;   SP
;
; Returns:
;   carry clear = input equals SP
;   carry set   = input does not equal SP
; ----------------------------------------------------------
MON_INPUT_IS_SP:
    MOV $C, 0x78
    MOV $D, 0x72
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_STACK
;
; Checks whether the input is exactly:
;   STACK
;
; Returns:
;   carry clear = input equals STACK
;   carry set   = input does not equal STACK
; ----------------------------------------------------------
MON_INPUT_IS_STACK:
    MOV $C, 0x80
    MOV $D, 0x72
    JSR MON_INPUT_EQUALS_STRING
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_CMP_RANGE_COUNT
;
; Checks whether the input has the command shape:
;   CMP XXXX YYYY NN
;
; Only the fixed structure is checked:
;   CMP
;   space after CMP
;   space between LEFT and RIGHT
;   space between RIGHT and COUNT
;   null terminator after COUNT
;
; The actual hex fields are parsed later by
; MON_CMD_CMP_RANGE_COUNT.
;
; Returns:
;   carry clear = input shape matches "CMP XXXX YYYY NN"
;   carry set   = input shape does not match
; ----------------------------------------------------------
MON_INPUT_IS_CMP_RANGE_COUNT:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x43       ; C
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x4D       ; M
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x50       ; P
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 3
    STC
    CMP $A, 0x20       ; space after CMP
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 8
    STC
    CMP $A, 0x20       ; space between LEFT and RIGHT
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 13
    STC
    CMP $A, 0x20       ; space between RIGHT and COUNT
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 16
    STC
    CMP $A, 0x00       ; exact end after count byte
    JNZ MON_INPUT_IS_CMP_RANGE_COUNT_NO

MON_INPUT_IS_CMP_RANGE_COUNT_YES:
    CLC
    RTS

MON_INPUT_IS_CMP_RANGE_COUNT_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_IS_CP_RANGE_COUNT
;
; Checks whether the input has the command shape:
;   CP XXXX YYYY NN
;
; Fields:
;   XXXX = source address
;   YYYY = destination address
;   NN   = byte count
;
; Only the fixed structure is checked:
;   CP
;   space after CP
;   space between source and destination
;   space between destination and count
;   null terminator after count
;
; The actual hex fields are parsed later by
; MON_CMD_CP_RANGE_COUNT.
;
; Returns:
;   carry clear = input shape matches "CP XXXX YYYY NN"
;   carry set   = input shape does not match
; ----------------------------------------------------------
MON_INPUT_IS_CP_RANGE_COUNT:
    MOV $A, MON_INPUT_BUF
    STC
    CMP $A, 0x43       ; C
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 1
    STC
    CMP $A, 0x50       ; P
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 2
    STC
    CMP $A, 0x20       ; space after CP
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 7
    STC
    CMP $A, 0x20       ; space between source and destination
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 12
    STC
    CMP $A, 0x20       ; space between destination and count
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

    MOV $A, MON_INPUT_BUF + 15
    STC
    CMP $A, 0x00       ; exact end after count byte
    JNZ MON_INPUT_IS_CP_RANGE_COUNT_NO

MON_INPUT_IS_CP_RANGE_COUNT_YES:
    CLC
    RTS

MON_INPUT_IS_CP_RANGE_COUNT_NO:
    STC
    RTS

; ----------------------------------------------------------
; MON_INPUT_TYPE_CHAR
;
; Input:
;   $A = ASCII character / control code
;
; Behavior:
;   printable char:
;       if input length < MON_INPUT_MAX:
;           store char into MON_INPUT_BUF[len]
;           len++
;           echo char with OLED5_TYPE_CHAR_WITH_CURSOR
;
;   backspace 0x08:
;       if len > 0:
;           len--
;           echo backspace with OLED5_TYPE_CHAR_WITH_CURSOR
;
;   newline 0x0A:
;       echo newline with OLED5_TYPE_CHAR_WITH_CURSOR
;
;   translates a key into ASCII/control code.
; ----------------------------------------------------------
MON_INPUT_TYPE_CHAR:
    MOV OLED_CHAR_TMP, $A

    ; Backspace?
    STC
    CMP $A, 0x08
    JZ MON_INPUT_BACKSPACE

    ; Newline?
    STC
    CMP $A, 0x0A
    JZ MON_INPUT_ECHO_ONLY

    ; Treat all other values as printable.

MON_INPUT_PRINTABLE:
    ; If len == MON_INPUT_MAX, ignore the character.
    MOV $A, MON_INPUT_LEN
    STC
    CMP $A, MON_INPUT_MAX
    JZ MON_INPUT_DONE

    ; Convert printable input to uppercase before store and echo.
    MOV $A, OLED_CHAR_TMP
    JSR MON_ASCII_TO_UPPER
    MOV OLED_CHAR_TMP, $A

    ; Store character at MON_INPUT_BUF + len.
    ; MON_INPUT_BUF is page-aligned at 0x7100, so:
    ;   C = len
    ;   D = 0x71
    MOV $C, MON_INPUT_LEN
    MOV $D, MON_INPUT_BUF_HI

    MOV $A, OLED_CHAR_TMP
    MOV [$CD], $A

    ; len++
    MOV $A, MON_INPUT_LEN
    CLC
    ADD $A, 0x01
    MOV MON_INPUT_LEN, $A

    ; Echo typed character with cursor behavior.
    MOV $A, OLED_CHAR_TMP
    JSR OLED5_TYPE_CHAR_WITH_CURSOR
    RTS

MON_INPUT_BACKSPACE:
    ; If len == 0, ignore backspace.
    MOV $A, MON_INPUT_LEN
    STC
    CMP $A, 0x00
    JZ MON_INPUT_DONE

    ; len--
    STC
    SUB $A, 0x01
    MOV MON_INPUT_LEN, $A

    ; Echo backspace with cursor behavior.
    MOV $A, 0x08
    JSR OLED5_TYPE_CHAR_WITH_CURSOR
    RTS

MON_INPUT_ECHO_ONLY:
    MOV $A, OLED_CHAR_TMP
    JSR OLED5_TYPE_CHAR_WITH_CURSOR
    RTS

MON_INPUT_DONE:
    RTS

; ----------------------------------------------------------
; MON_ASCII_TO_UPPER
;
; Input:
;   $A = ASCII character
;
; Output:
;   $A = uppercase version if input was 'a'..'z'
;        otherwise unchanged
;
; Converts:
;   'a'..'z' -> 'A'..'Z'
;
; Carry/no-borrow convention:
;   after CMP/SUB, C = 1 means A >= operand
;   after CMP/SUB, C = 0 means A < operand
; ----------------------------------------------------------
MON_ASCII_TO_UPPER:
    ; Leave A unchanged when A < 'a' / 0x61.
    STC
    CMP $A, 0x61
    JNC MON_ASCII_TO_UPPER_DONE

    ; Leave A unchanged when A >= '{' / 0x7B.
    STC
    CMP $A, 0x7B
    JC MON_ASCII_TO_UPPER_DONE

    ; Convert lowercase to uppercase with A - 0x20.
    STC
    SUB $A, 0x20

MON_ASCII_TO_UPPER_DONE:
    RTS

; ----------------------------------------------------------
; MON_ASCII_HEX_TO_NIBBLE
;
; Converts one ASCII hex character into a 4-bit value.
;
; Input:
;   $A = ASCII hex character
;
; Output:
;   MON_HEX_STATUS = 0x00 for valid
;                    0x01 for invalid
;
;   If valid:
;       $A = nibble value 0x00..0x0F
;       carry clear
;
;   If invalid:
;       $A has no defined value
;       carry set
;
; Accepted:
;   '0'..'9'
;   'A'..'F'
;
; Notes:
;   Compact range-check parser for ASCII hex input.
;   Accepts digits and uppercase A through F.
; ----------------------------------------------------------
MON_ASCII_HEX_TO_NIBBLE:
    MOV MON_HEX_CHAR_TMP, $A

    ; Check digit range: '0' <= char < ':'
    MOV $A, MON_HEX_CHAR_TMP
    STC
    CMP $A, 0x30       ; '0'
    JNC MON_ASCII_HEX_INVALID

    MOV $A, MON_HEX_CHAR_TMP
    STC
    CMP $A, 0x3A       ; one past '9'
    JNC MON_ASCII_HEX_DIGIT

    ; Check letter range: 'A' <= char < 'G'
    MOV $A, MON_HEX_CHAR_TMP
    STC
    CMP $A, 0x41       ; 'A'
    JNC MON_ASCII_HEX_INVALID

    MOV $A, MON_HEX_CHAR_TMP
    STC
    CMP $A, 0x47       ; one past 'F'
    JC MON_ASCII_HEX_INVALID

MON_ASCII_HEX_LETTER:
    MOV $A, MON_HEX_CHAR_TMP

    ; A = char - 'A'
    STC
    SUB $A, 0x41

    ; A = A + 10
    CLC
    ADD $A, 0x0A

    MOV MON_HEX_BYTE_RESULT, $A

    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    MOV $A, MON_HEX_BYTE_RESULT
    CLC
    RTS

MON_ASCII_HEX_DIGIT:
    MOV $A, MON_HEX_CHAR_TMP

    ; A = char - '0'
    STC
    SUB $A, 0x30

    MOV MON_HEX_BYTE_RESULT, $A

    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    MOV $A, MON_HEX_BYTE_RESULT
    CLC
    RTS

MON_ASCII_HEX_INVALID:
    MOV $A, 0x01
    MOV MON_HEX_STATUS, $A
    STC
    RTS

; ----------------------------------------------------------
; MON_PARSE_HEX_BYTE_AT_CD
;
; Parses two ASCII hex characters at [$CD] into one byte.
;
; Input:
;   $C = low byte of pointer
;   $D = high byte of pointer
;
; Output:
;   MON_HEX_STATUS = 0x00 for valid
;                    0x01 for invalid
;
;   If valid:
;       $A = parsed byte
;       MON_HEX_BYTE_RESULT = parsed byte
;
; Example:
;   memory: 'A' '5'
;   result: $A = 0xA5
;
;   Uses MON_ASCII_HEX_TO_NIBBLE and relies on the
;   RAM status byte instead of carry.
; ----------------------------------------------------------
MON_PARSE_HEX_BYTE_AT_CD:
    ; Parse high nibble.
    MOV $A, [$CD]
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_NIBBLE_HI, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_BYTE_INVALID

    ; Advance pointer to second character.
    CLC
    ADD $C, 0x01
    JNC .MON_PARSE_HEX_BYTE_PTR_OK

    CLC
    ADD $D, 0x01

.MON_PARSE_HEX_BYTE_PTR_OK:
    ; Parse low nibble.
    MOV $A, [$CD]
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_NIBBLE_LO, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_BYTE_INVALID

    ; Build byte:
    ;   result = high nibble shifted left 4 times, OR low nibble.
    MOV $A, MON_HEX_NIBBLE_HI
    LSL $A
    LSL $A
    LSL $A
    LSL $A

    OR $A, MON_HEX_NIBBLE_LO
    MOV MON_HEX_BYTE_RESULT, $A

    ; valid status
    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    MOV $A, MON_HEX_BYTE_RESULT
    RTS

MON_PARSE_HEX_BYTE_INVALID:
    MOV $A, 0x01
    MOV MON_HEX_STATUS, $A
    RTS

; ----------------------------------------------------------
; MON_PARSE_HEX_BYTE_AT_CD_COMPACT
;
; Alternate compact-byte parser.
;
; Parses two ASCII hex characters at [$CD] into one byte.
; Same structure as MON_PARSE_HEX_BYTE_AT_CD,
; but it calls MON_ASCII_HEX_TO_NIBBLE.
;
; Input:
;   $C = low byte of pointer
;   $D = high byte of pointer
;
; Output:
;   MON_HEX_STATUS = 0x00 for valid
;                    0x01 for invalid
;
;   If valid:
;       $A = parsed byte
;       MON_HEX_BYTE_RESULT = parsed byte
;
; Kept as an alternate parser path for hardware comparison.
; ----------------------------------------------------------
MON_PARSE_HEX_BYTE_AT_CD_COMPACT:
    ; Parse high nibble.
    MOV $A, [$CD]
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_NIBBLE_HI, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_BYTE_COMPACT_INVALID

    ; Advance pointer to second character.
    CLC
    ADD $C, 0x01
    JNC .MON_PARSE_HEX_BYTE_COMPACT_PTR_OK

    CLC
    ADD $D, 0x01

.MON_PARSE_HEX_BYTE_COMPACT_PTR_OK:
    ; Parse low nibble.
    MOV $A, [$CD]
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_NIBBLE_LO, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_BYTE_COMPACT_INVALID

    ; Build byte:
    ;   result = high nibble shifted left 4 times, OR low nibble.
    MOV $A, MON_HEX_NIBBLE_HI
    LSL $A
    LSL $A
    LSL $A
    LSL $A

    OR $A, MON_HEX_NIBBLE_LO
    MOV MON_HEX_BYTE_RESULT, $A

    ; valid status
    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    MOV $A, MON_HEX_BYTE_RESULT
    RTS

MON_PARSE_HEX_BYTE_COMPACT_INVALID:
    MOV $A, 0x01
    MOV MON_HEX_STATUS, $A
    RTS

; ----------------------------------------------------------
; MON_PARSE_HEX_WORD_AT_CD
;
; Parses four ASCII hex characters at [$CD] into a 16-bit word.
;
; Input:
;   $C = low byte of pointer
;   $D = high byte of pointer
;
; Output:
;   MON_HEX_STATUS = 0x00 for valid
;                    0x01 for invalid
;
;   If valid:
;       $C = low byte of parsed word
;       $D = high byte of parsed word
;
;       MON_HEX_WORD_LO = low byte
;       MON_HEX_WORD_HI = high byte
;
; Example:
;   memory: '0' '2' '0' '0'
;   result: D:C = 0x0200
;           $D = 0x02
;           $C = 0x00
;
;   Uses MON_PARSE_HEX_BYTE_AT_CD twice.
;   First two chars become the high byte.
;   Second two chars become the low byte.
; ----------------------------------------------------------
MON_PARSE_HEX_WORD_AT_CD:
    ; Save source pointer.
    MOV MON_HEX_PARSE_PTR_LO, $C
    MOV MON_HEX_PARSE_PTR_HI, $D

    ; Parse high byte.
    JSR MON_PARSE_HEX_BYTE_AT_CD

    MOV MON_HEX_WORD_HI, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_WORD_INVALID

    ; Restore source pointer and advance by 2.
    MOV $C, MON_HEX_PARSE_PTR_LO
    MOV $D, MON_HEX_PARSE_PTR_HI

    CLC
    ADD $C, 0x02
    JNC .MON_PARSE_HEX_WORD_PTR_OK

    CLC
    ADD $D, 0x01

.MON_PARSE_HEX_WORD_PTR_OK:
    ; Parse low byte.
    JSR MON_PARSE_HEX_BYTE_AT_CD

    MOV MON_HEX_WORD_LO, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_WORD_INVALID

    ; Return parsed word in CD.
    MOV $C, MON_HEX_WORD_LO
    MOV $D, MON_HEX_WORD_HI

    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    RTS

MON_PARSE_HEX_WORD_INVALID:
    MOV $A, 0x01
    MOV MON_HEX_STATUS, $A
    RTS

; ----------------------------------------------------------
; MON_PARSE_HEX_WORD_AT_CD_COMPACT
;
; Alternate compact-word parser.
;
; Parses four ASCII hex characters at [$CD] into a 16-bit word.
; Same structure as MON_PARSE_HEX_WORD_AT_CD,
; but it calls MON_PARSE_HEX_BYTE_AT_CD_COMPACT.
;
; Input:
;   $C = low byte of pointer
;   $D = high byte of pointer
;
; Output:
;   MON_HEX_STATUS = 0x00 for valid
;                    0x01 for invalid
;
;   If valid:
;       $C = low byte of parsed word
;       $D = high byte of parsed word
;
;       MON_HEX_WORD_LO = low byte
;       MON_HEX_WORD_HI = high byte
;
; Kept as an alternate parser path for hardware comparison.
; ----------------------------------------------------------
MON_PARSE_HEX_WORD_AT_CD_COMPACT:
    ; Save source pointer.
    MOV MON_HEX_PARSE_PTR_LO, $C
    MOV MON_HEX_PARSE_PTR_HI, $D

    ; Parse high byte.
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_WORD_HI, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_WORD_COMPACT_INVALID

    ; Restore source pointer and advance by 2.
    MOV $C, MON_HEX_PARSE_PTR_LO
    MOV $D, MON_HEX_PARSE_PTR_HI

    CLC
    ADD $C, 0x02
    JNC .MON_PARSE_HEX_WORD_COMPACT_PTR_OK

    CLC
    ADD $D, 0x01

.MON_PARSE_HEX_WORD_COMPACT_PTR_OK:
    ; Parse low byte.
    JSR MON_ASCII_HEX_TO_NIBBLE

    MOV MON_HEX_WORD_LO, $A

    MOV $A, MON_HEX_STATUS
    STC
    CMP $A, 0x00
    JNZ MON_PARSE_HEX_WORD_COMPACT_INVALID

    ; Return parsed word in CD.
    MOV $C, MON_HEX_WORD_LO
    MOV $D, MON_HEX_WORD_HI

    MOV $A, 0x00
    MOV MON_HEX_STATUS, $A

    RTS

MON_PARSE_HEX_WORD_COMPACT_INVALID:
    MOV $A, 0x01
    MOV MON_HEX_STATUS, $A
    RTS
