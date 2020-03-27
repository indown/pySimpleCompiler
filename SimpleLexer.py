from enum import Enum, unique
from TokenType import TokenType


class SimpleLexer:
    token = None
    tokens = None
    token_text = None

    def __init__(self):
        # script = 'int age=111;'
        # token_reader = self.tokenize(script)
        # print('\nparse: ' + script)
        # self.dump(token_reader)
        #
        # script = 'age>=111;'
        # token_reader = self.tokenize(script)
        # print('\nparse: ' + script)
        # self.dump(token_reader)
        #
        # script = 'age>111;'
        # token_reader = self.tokenize(script)
        # print('\nparse: ' + script)
        # self.dump(token_reader)
        pass

    @staticmethod
    def is_alpha(ch):
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'

    @staticmethod
    def is_digit(ch):
        return '0' <= ch <= '9'

    @staticmethod
    def is_blank(ch):
        return ch == ' ' or ch == '\t' or ch == '\n'

    def init_token(self, ch):
        if len(self.token_text) > 0:
            self.token.text = self.token_text
            self.tokens.append(self.token)

            self.token_text = ''
            self.token = self.SimpleToken()

        new_state = DfaState.Initial.value

        if self.is_alpha(ch):
            if ch == 'i':
                self.token_text = ch
                new_state = DfaState.Id_int1.value
            else:
                self.token_text = ch
                new_state = DfaState.Id.value
            self.token.type = TokenType.Identifier.value
        elif self.is_digit(ch):
            self.token_text = ch
            self.token.type = TokenType.IntLiteral.value
            new_state = DfaState.IntLiteral.value
        elif ch == '+':
            self.token_text = ch
            self.token.type = TokenType.Plus.value
            new_state = DfaState.Plus.value
        elif ch == '-':
            self.token_text = ch
            self.token.type = TokenType.Minus.value
            new_state = DfaState.Minus.value
        elif ch == '*':
            self.token_text = ch
            self.token.type = TokenType.Star.value
            new_state = DfaState.Star.value
        elif ch == '/':
            self.token_text = ch
            self.token.type = TokenType.Slash.value
            new_state = DfaState.Slash.value
        elif ch == '(':
            self.token_text = ch
            self.token.type = TokenType.LeftParen.value
            new_state = DfaState.LeftParen.value
        elif ch == ')':
            self.token_text = ch
            self.token.type = TokenType.RightParen.value
            new_state = DfaState.RightParen.value
        elif ch == '>':
            self.token_text = ch
            self.token.type = TokenType.GT.value
            new_state = DfaState.GT.value
        elif ch == '=':
            self.token_text = ch
            self.token.type = TokenType.Assignment.value
            new_state = DfaState.Assignment.value
        elif ch == ';':
            self.token_text = ch
            self.token.type = TokenType.SemiColon.value
            new_state = DfaState.SemiColon.value
        return new_state

    def tokenize(self, code):
        state = DfaState.Initial.value
        self.tokens = []
        self.token = self.SimpleToken()
        self.token_text = ''
        temp_ch = None
        for ch in code:
            if ord(ch) > -1:
                temp_ch = ch
                if state == DfaState.Initial.value:
                    state = self.init_token(ch)
                elif state == DfaState.Id.value:
                    if self.is_alpha(ch) or self.is_digit(ch):
                        self.token_text += ch
                    else:
                        state = self.init_token(ch)
                elif state == DfaState.IntLiteral.value:
                    if self.is_digit(ch):
                        self.token_text += ch
                    else:
                        self.token.type = TokenType.IntLiteral.value
                        state = self.init_token(ch)
                elif state == DfaState.SemiColon.value \
                        or state == DfaState.GE.value \
                        or state == DfaState.Plus.value \
                        or state == DfaState.Minus.value \
                        or state == DfaState.Star.value \
                        or state == DfaState.Slash.value \
                        or state == DfaState.LeftParen.value \
                        or state == DfaState.RightParen.value \
                        or state == DfaState.Assignment.value:
                    state = self.init_token(ch)
                elif state == DfaState.GT.value:
                    if ch == '=':
                        self.token_text += ch
                        self.token.type = TokenType.GE.value
                    else:
                        state = self.init_token(ch)
                elif state == DfaState.Id_int1.value:
                    if self.is_alpha(ch):
                        self.token_text += ch
                        if ch == 'n':
                            state = DfaState.Id_int2.value
                    else:
                        state = self.init_token(ch)
                elif state == DfaState.Id_int2.value:
                    if self.is_alpha(ch):
                        self.token_text += ch
                        if ch == 't':
                            state = DfaState.Id_int3.value
                    else:
                        state = self.init_token(ch)
                elif state == DfaState.Id_int3.value:
                    if self.is_blank(ch):
                        self.token.type = TokenType.Int.value
                        state = self.init_token(ch)
                    else:
                        self.token_text += ch
                        state = DfaState.Id.value

        if len(self.token_text) > 0:
            self.init_token(temp_ch)

        return self.SimpleTokenReader(self.tokens)

    @staticmethod
    def dump(token_reader):
        print("text\ttype")
        while token_reader.peek() is not None:
            token = token_reader.read()
            print(token.get_text() + '\t\t' + token.get_type())

    class SimpleToken:

        def __init__(self):
            self.type = None
            self.text = None

        def get_type(self):
            return self.type

        def get_text(self):
            return self.text

    class SimpleTokenReader:
        pos = 0

        def __init__(self, tokens):
            self.tokens = tokens

        def peek(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return None

        def read(self):
            if self.pos < len(self.tokens):
                self.pos += 1
                return self.tokens[self.pos - 1]
            return None

        def get_pos(self):
            return self.pos

        def set_pos(self, pos):
            self.pos = pos

        def unread(self):
            if self.pos > 0:
                self.pos -= 1


@unique
class DfaState(Enum):
    Initial = 'Initial'  # 初始状态
    Assignment = 'Assignment'  # 赋值
    IntLiteral = 'IntLiteral'
    Id_int1 = 'Id_int1'
    Id_int2 = 'Id_int2'
    Id_int3 = 'Id_int3'
    Int = 'Int'
    Id = 'Id'
    GT = 'GT'
    GE = 'GE'
    Plus = 'Plus'
    Minus = 'Minus'
    Star = 'Star'
    Slash = 'Slash'
    SemiColon = 'SemiColon'
    LeftParen = 'LeftParen'
    RightParen = 'RightParen'


# @unique
# class TokenType(Enum):
#     Int = 'Int'  # Int关键字
#     Identifier = 'Identifier'  # 标识符
#     IntLiteral = 'IntLiteral'  # 数字字面量
#     Assignment = 'Assignment'  # =
#     SemiColon = 'SemiColon'  # ;
#     GT = 'GT'
#     GE = 'GE'


SimpleLexer()
