package Constantina;

enum TokenType {
    // Single-character tokens.
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, LEFT_QPAREN, RIGHT_QPAREN,
    COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,

    // One or two character tokens.
    NOT, NOT_EQUAL,
    EQUAL,
    GREATER, GREATER_EQUAL,
    LESS, LESS_EQUAL,
    ASSIGN,

    // Literals.
    IDENTIFIER, STRING, NUMBER,

    // Keywords.
    AND, GROUP_TYPE, ELSE, FALSE, FOR, IF, EMPTY, OR, DO, UNTIL, IN,
    PRINT, RETURN, TRUE, PRODUCT, QUANTITY, PROCESS, WHILE, MAIN,

    EOF
}
