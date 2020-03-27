from enum import Enum, unique


@unique
class TokenType(Enum):
    Int = 'Int'  # Int关键字
    Identifier = 'Identifier'  # 标识符
    IntLiteral = 'IntLiteral'  # 数字字面量
    Assignment = 'Assignment'  # =
    SemiColon = 'SemiColon'  # ;
    GT = 'GT'
    GE = 'GE'
    LeftParen = 'LeftParen'
    RightParen = 'RightParen'

    Plus = 'Plus'
    Minus = 'Minus'
    Star = 'Star'
    Slash = 'Slash'
