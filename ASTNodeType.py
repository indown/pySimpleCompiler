from enum import Enum, unique


@unique
class ASTNodeType(Enum):
    Programm = 'Programm'
    IntDeclaration = 'IntDeclaration'
    ExpressionStmt = 'ExpressionStmt'
    AssignmentStmt = 'AssignmentStmt'
    Primary = 'Primary'
    Multiplicative = 'Multiplicative'
    Additive = 'Additive'
    Identifier = 'Identifier'
    IntLiteral = 'IntLiteral'