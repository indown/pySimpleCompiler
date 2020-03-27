import sys
from SimpleParser import SimpleParser
from ASTNodeType import ASTNodeType


class SimpleScript:
    verbose = False
    variables = {}

    def __init__(self):
        if '-v' in sys.argv:
            self.verbose = True
            print('verbose mode')
        print('welcome simple script language!')

        parser = SimpleParser()

        while True:
            try:
                line = input('\n> ')
                if line == 'exit();':
                    print('good bye!')
                    break
                if line[-1] is ';':
                    tree = parser.parse(line)
                    if self.verbose is True:
                        parser.dump(tree, '')
                    self.evaluate(tree, '')
            except ValueError:
                print('error.')
                break

    def evaluate(self, node, indent):
        result = None
        if self.verbose is True:
            print(indent + 'calculating: ' + node.get_node_type())
        node_type = node.get_node_type()
        if node_type == ASTNodeType.Programm.value:
            for child in node.get_children()[:]:
                result = self.evaluate(child, indent)
        elif node_type == ASTNodeType.Additive.value:
            child1 = node.get_children()[0]
            value1 = self.evaluate(child1, indent + '\t')
            child2 = node.get_children()[1]
            value2 = self.evaluate(child2, indent + '\t')
            if '+' in node.get_text():
                result = value1 + value2
            else:
                result = value1 - value2
        elif node_type == ASTNodeType.Multiplicative.value:
            child1 = node.get_children()[0]
            value1 = self.evaluate(child1, indent + '\t')
            child2 = node.get_children()[1]
            value2 = self.evaluate(child2, indent + '\t')
            if '*' in node.get_text():
                result = value1 * value2
            else:
                result = value1 / value2
        elif node_type == ASTNodeType.IntLiteral.value:
            result = int(node.get_text())
        elif node_type == ASTNodeType.Identifier.value:
            varName = node.get_text()
            if varName in list(self.variables):
                value = self.variables[varName]
                if value is not None:
                    result = int(value)
                else:
                    raise ValueError('variable ' + varName + ' has not been set any value.')
            else:
                raise ValueError('unknown variable: ' + varName)
        elif node_type == ASTNodeType.AssignmentStmt.value:
            varName = node.get_text()
            if varName not in list(self.variables):
                raise ValueError('unknown variable: ' + varName)
            varValue = None
            if len(node.get_children()) > 0:
                child = node.get_children()[0]
                result = self.evaluate(child, indent + '\t')
                varValue = int(result)
            self.variables[varName] = varValue
        elif node_type == ASTNodeType.IntDeclaration.value:
            varName = node.get_text()
            varValue = None
            if len(node.get_children()) > 0:
                child = node.get_children()[0]
                result = self.evaluate(child, indent + '\t')
                varValue = int(result)
            self.variables[varName] = varValue
        if self.verbose is True:
            print(indent + "Result: " + str(result))
        elif '' == indent:
            if node.get_node_type() == ASTNodeType.IntDeclaration.value or node.get_node_type() == ASTNodeType.AssignmentStmt.value:
                print(node.get_text() + ': ' + str(result))
            elif node.get_node_type() is not ASTNodeType.Programm.value:
                print(result)
        return result


SimpleScript()
