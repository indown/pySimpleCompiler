from SimpleLexer import SimpleLexer
from TokenType import TokenType
from ASTNodeType import ASTNodeType


class SimpleParser:

    def __init__(self):
        # script = 'int age = 11; age = 11; age + 11 * 2;'
        # # script = 'int age = aa + 11 + 11;'
        # # script = 'int age = 1 + (2 + 3) / 4;int aaa = 111 + 11;'
        # # script = 'age = 1 + (2 + 3) / 4;'
        # print('parse: ' + script)
        # tree = self.parse(script)
        # self.dump(tree)
        pass

    def parse(self, script):
        lexer = SimpleLexer()
        tokens = lexer.tokenize(script)
        rootNode = self.prog(tokens)
        return rootNode

    def prog(self, tokens):
        node = SimpleASTNode(ASTNodeType.Programm.value, 'pwc')
        while tokens.peek() is not None:
            child = self.int_declare(tokens)
            if child is None:
                child = self.expression_statement(tokens)
            if child is None:
                child = self.assignment_statement(tokens)
            if child is not None:
                node.add_child(child)
            else:
                raise ValueError('unknown statement.')
        return node

    def expression_statement(self, tokens):
        pos = tokens.get_pos()
        node = self.additive(tokens)
        if node is not None:
            token = tokens.peek()
            if token is not None and token.get_type() == TokenType.SemiColon.value:
                tokens.read()
            else:
                node = None
                tokens.set_pos(pos)
        return node

    def assignment_statement(self, tokens):
        node = None
        token = tokens.peek()
        if token is not None and token.get_type() == TokenType.Identifier.value:
            node = SimpleASTNode(ASTNodeType.AssignmentStmt.value, tokens.read().get_text())
            token = tokens.peek()
            if token is not None and token.get_type() == TokenType.Assignment.value:
                tokens.read()
                child = self.additive(tokens)
                if child is None:
                    raise ValueError('invalid assignment statement, expecting an expression.')
                else:
                    node.add_child(child)
                    token = tokens.peek()
                    if token is not None and token.get_type() == TokenType.SemiColon.value:
                        tokens.read()
                    else:
                        raise ValueError('invalid statement, expecting semicolon.')
            else:
                tokens.unread()
                node = None

        return node

    def int_declare(self, tokens):
        node = None
        token = tokens.peek()
        if token is not None and token.get_type() == TokenType.Int.value:
            tokens.read()
            if tokens.peek() is not None and tokens.peek().get_type() == TokenType.Identifier.value:
                node = SimpleASTNode(ASTNodeType.IntDeclaration.value, tokens.read().get_text())
                token = tokens.peek()
                if token is not None and token.get_type() == TokenType.Assignment.value:
                    tokens.read()
                    child = self.additive(tokens)
                    if child is None:
                        raise ValueError('invalid variable initialization, expecting an expression.')
                    else:
                        node.add_child(child)
            else:
                raise ValueError('variable name expected')
        if node is not None:
            if tokens.peek() is not None and tokens.peek().get_type() == TokenType.SemiColon.value:
                tokens.read()
            else:
                raise ValueError('invalid statement, expecting semicolon.')
        return node

    def additive(self, tokens):
        child1 = self.multiplicative(tokens)
        node = child1
        while True:
            if tokens.peek() is not None and (
                    tokens.peek().get_type() == TokenType.Plus.value
                    or tokens.peek().get_type() == TokenType.Minus.value):
                token = tokens.read()
                child2 = self.multiplicative(tokens)
                if child2 is not None:
                    node = SimpleASTNode(ASTNodeType.Additive.value, token.get_text())
                    node.add_child(child1)
                    node.add_child(child2)
                    child1 = node
            else:
                break

        return node

    def multiplicative(self, tokens):
        child1 = self.primary(tokens)
        node = child1

        while True:
            if tokens.peek() is not None and (
                    tokens.peek().get_type() == TokenType.Star.value
                    or tokens.peek().get_type() == TokenType.Slash.value):
                token = tokens.read()
                child2 = self.primary(tokens)
                if child2 is not None:
                    node = SimpleASTNode(ASTNodeType.Multiplicative.value, token.get_text())
                    node.add_child(child1)
                    node.add_child(child2)
                    child1 = node
            else:
                break
        return node

    def primary(self, tokens):
        node = None
        token = tokens.peek()
        if token is not None:
            if token.get_type() == TokenType.Identifier.value:
                node = SimpleASTNode(ASTNodeType.Identifier.value, tokens.read().get_text())
            if token.get_type() == TokenType.IntLiteral.value:
                node = SimpleASTNode(ASTNodeType.IntLiteral.value, tokens.read().get_text())
            elif token.get_type() == TokenType.LeftParen.value:
                tokens.read()
                node = self.additive(tokens)
                if tokens.peek().get_type() == TokenType.RightParen.value:
                    tokens.read()
                else:
                    raise ValueError('expecting right paren')
        else:
            raise ValueError('primary expecting normal"s token ')
        return node

    def dump(self, tree, indent=''):

        print(indent + tree.get_node_type() + '\t\t' + tree.get_text())
        if len(tree.get_children()) > 0:
            for node in tree.get_children():
                self.dump(node, indent + '\t')


class SimpleASTNode:
    def __init__(self, node_type, text):
        self.node_type = node_type
        self.text = text
        self.children = []
        self.parent = None

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_node_type(self):
        return self.node_type

    def get_text(self):
        return self.text

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


SimpleParser()
