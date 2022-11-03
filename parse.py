import Datatypes


# TODO: update comments

# RECURSIVE DESCENT PARSER
# Is responsible for recursively generating a tree of operations based on the lexer output using the pre-defined Nodes
# from the Datatypes.py file.
class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.current_token_type = None
        self.optional_open_blocks = 0
        self.ast_list = []
        self.skipped_linebreak = False
        self.next_token()

    # Advances the iterator to the next token, returns None at the end of the list
    # The token type is defined separately to avoid errors being caused by "self.current_token.type" if
    # the current token is None.
    def next_token(self):
        try:
            self.current_token = next(self.tokens)
            self.current_token_type = self.current_token.type
        except StopIteration:
            self.current_token = None
            self.current_token_type = None

    def parse(self):
        while self.current_token is not None:
            while self.current_token_type == Datatypes.LINEBREAK:
                self.next_token()
            # If there are no tokens, None will be returned
            if self.current_token is not None:
                self.ast_list.append(
                    self.statement())
            if self.current_token_type not in (Datatypes.LINEBREAK, None) and not self.skipped_linebreak:
                raise SyntaxError(f"Expected end of statement, got token type"
                                  f" {Datatypes.type_dict.get(self.current_token_type)}")
            self.skipped_linebreak = False
        return self.ast_list

    # Following, there are the valid elements of an expression, following the common order top-down.
    # These elements are grouped in "layers", which are statement, expression, term, "exponential" and factor
    # The statement is an if statement which consists of the if keyword and multiple expressions
    # An expression will have a plus or minus sign
    # A term will be any multiplication, division, modulus, assignment operation or a comparison
    # An "exponential" will have the exponentiation operator. The reason this has its own layer is that exponential
    # operations have to be evaluated before a term, but after a factor.
    # Finally, the factor can be a number, identifier or a statement between brackets.
    def statement_block(self, func_block=False):
        if self.current_token_type != Datatypes.ARROW:
            raise SyntaxError("Expected '=>'")
        self.next_token()
        if self.current_token_type != Datatypes.LINEBREAK:
            return self.statement() if func_block else [self.statement()]
        block = []
        while self.current_token_type not in (Datatypes.BLOCK_END, None):
            while self.current_token_type == Datatypes.LINEBREAK:
                self.next_token()
            self.skipped_linebreak = False
            block.append(self.statement())
            if self.current_token_type is None:
                raise SyntaxError("Expected expression")
        if self.current_token_type != Datatypes.BLOCK_END:
            raise SyntaxError(f"Expected block ending operator")
        self.next_token()
        return block

    def statement(self):
        result = self.expression()
        while self.current_token_type in (
                Datatypes.IF, Datatypes.SOLVE_ASSIGN, Datatypes.SOLVE
        ) and not self.skipped_linebreak:
            if self.current_token_type == Datatypes.SOLVE:
                self.next_token()
                result = Datatypes.SolveNode(result, self.expression())
            elif self.current_token_type == Datatypes.SOLVE_ASSIGN:
                self.next_token()
                result = Datatypes.SolveAssignNode(result, self.expression())
            else:
                if_expr = result
                result = Datatypes.IfNode()
                self.next_token()
                condition = self.statement()
                result.add_block(Datatypes.IF, [if_expr], condition)
                if self.current_token_type == Datatypes.ELSE:
                    self.next_token()
                    else_expr = self.statement()
                    result.add_block(Datatypes.ELSE, [else_expr])
        return result

    def expression(self):
        result = self.term()
        while self.current_token_type in (Datatypes.PLUS_SIGN, Datatypes.MINUS_SIGN, Datatypes.AND, Datatypes.OR) \
                and not self.skipped_linebreak:
            if self.current_token_type in (Datatypes.PLUS_SIGN, Datatypes.MINUS_SIGN):
                token_type = self.current_token_type
                self.next_token()
                result = Datatypes.OPERATOR_NODE_DICT[token_type](a=result, b=self.term())
            elif self.current_token_type in (Datatypes.AND, Datatypes.OR):
                operation_type = self.current_token_type
                self.next_token()
                result = Datatypes.LogicalOperationNode(a=result, b=self.term(), operation=operation_type)
        return result

    def term(self):
        result = self.exponential()
        while self.current_token_type in (
                Datatypes.MULT_SIGN, Datatypes.DIV_SIGN, Datatypes.MODULUS_SIGN, Datatypes.EQUALS,
                Datatypes.PLUS_ASSIGN,
                Datatypes.MINUS_ASSIGN, Datatypes.MULT_ASSIGN, Datatypes.DIV_ASSIGN, Datatypes.MODULUS_ASSIGN,
                Datatypes.ARRAYAPPLY_ASSIGN, Datatypes.COMP_EQUALS, Datatypes.COMP_NOT_EQUALS, Datatypes.GREATER_THAN,
                Datatypes.LESS_THAN, Datatypes.GREATER_OR_EQUALS, Datatypes.LESS_OR_EQUALS, Datatypes.IN, Datatypes.NOT,
                Datatypes.ARRAYAPPLY, Datatypes.COLON) and not self.skipped_linebreak:
            if self.current_token_type in (Datatypes.MULT_SIGN, Datatypes.DIV_SIGN, Datatypes.MODULUS_SIGN):
                token_type = self.current_token_type
                self.next_token()
                result = Datatypes.OPERATOR_NODE_DICT[token_type](a=result, b=self.exponential())
            elif self.current_token_type == Datatypes.EQUALS:
                # Will throw an exception if an equals sign comes after anything other than a variable
                if type(result).__name__ == "VariableNode":
                    self.next_token()
                    result = Datatypes.AssignNode(identifier=result.identifier, value=self.statement())
                else:
                    self.next_token()
                    result = Datatypes.AssignNode(identifier=result, value=self.statement())
            elif self.current_token_type in (
                    Datatypes.PLUS_ASSIGN, Datatypes.MINUS_ASSIGN, Datatypes.MULT_ASSIGN, Datatypes.DIV_ASSIGN,
                    Datatypes.MODULUS_ASSIGN, Datatypes.ARRAYAPPLY_ASSIGN):
                # Will first make a check if assign operator comes after a variable , then will match the operator
                # and return assign nodes accordingly
                if type(result).__name__ == "VariableNode":
                    operator_node = Datatypes.OPERATOR_NODE_DICT[self.current_token_type]
                    self.next_token()
                    result = Datatypes.AssignNode(identifier=result.identifier,
                                                  value=operator_node(Datatypes.VariableNode(result.identifier),
                                                                      self.statement()))
                else:
                    operator_node = Datatypes.OPERATOR_NODE_DICT[self.current_token_type]
                    self.next_token()
                    result = Datatypes.AssignNode(identifier=result, value=operator_node(result, self.statement()))
            elif self.current_token_type == Datatypes.ARRAYAPPLY:
                self.next_token()
                result = Datatypes.ArrayApplyNode(identifier=result, function=self.statement())
            elif self.current_token_type == Datatypes.IN:
                self.next_token()
                result = Datatypes.ContainsNode(iterable=self.exponential(), item=result)
            elif self.current_token_type == Datatypes.COLON:
                start = result
                self.next_token()
                stop = self.exponential()
                if self.current_token_type == Datatypes.COLON:
                    self.next_token()
                    step = self.exponential()
                else:
                    step = 1
                return Datatypes.RangeNode(start=start, stop=stop, step=step)
            elif self.current_token_type == Datatypes.NOT:
                self.next_token()
                if self.current_token_type == Datatypes.IN:
                    self.next_token()
                    result = Datatypes.BooleanNegationNode(
                        Datatypes.ContainsNode(iterable=self.exponential(), item=result))
                else:
                    Datatypes.ComparisonNode(a=result, b=self.exponential(), operator=Datatypes.COMP_NOT_EQUALS)
            else:
                comparison_type = self.current_token_type
                self.next_token()
                result = Datatypes.ComparisonNode(a=result, b=self.exponential(), operator=comparison_type)
        return result

    def exponential(self):
        result = self.factor()
        while self.current_token_type in (Datatypes.EXP, Datatypes.PERIOD_CALL):
            if self.current_token_type == Datatypes.EXP:
                self.next_token()
                result = Datatypes.ExpNode(a=result, b=self.factor())
            elif self.current_token_type == Datatypes.PERIOD_CALL:
                self.next_token()
                right_side = self.factor()
                result = Datatypes.PeriodCallNode(left_side=result, right_side=right_side)

        return result

    def factor(self):
        token = self.current_token
        token_type = self.current_token_type
        if token_type is None:
            raise SyntaxError("Expected number or identifier")
        # Will return the float value for a number token
        if token_type in (Datatypes.NUMBER, Datatypes.STRING):
            self.next_token()
            if self.current_token_type == Datatypes.IDENTIFIER:
                return Datatypes.MultNode(token.value, self.exponential())
            elif self.current_token_type == Datatypes.LBRACKET:
                return self.gen_bracketcall(token.value)
            return token.value
        # In case of a FUNCTION_KEYWORD, the parsing process will continue declare_function() function
        elif token_type == Datatypes.FUNCTION_KEYWORD:
            self.next_token()
            return self.declare_function()
        elif self.current_token_type == Datatypes.RETURN:
            self.next_token()
            if self.current_token_type == Datatypes.LINEBREAK:
                return Datatypes.ReturnNode(statement=None)
            else:
                return Datatypes.ReturnNode(statement=self.statement())
        # In case of the loop keyword REP, the parsing process will continue declare_function() function
        elif token_type == Datatypes.BREAK:
            self.next_token()
            return Datatypes.BreakNode()
        elif token_type == Datatypes.CONTINUE:
            self.next_token()
            return Datatypes.ContinueNode()
        elif token_type == Datatypes.REP:
            self.next_token()
            return self.gen_rep()
        elif token_type == Datatypes.FOR:
            self.next_token()
            return self.gen_for()
        elif token_type == Datatypes.IF:
            return self.gen_if()
        elif token_type == Datatypes.ITERATE:
            return self.gen_iterate()
        elif token_type == Datatypes.WHILE:
            return self.gen_while()
        elif token_type == Datatypes.LBRACKET:
            arr = self.gen_arr()
            self.next_token()
            if self.current_token_type == Datatypes.LBRACKET:
                return self.gen_bracketcall(arr)
            return arr
        elif token_type == Datatypes.LCURLY:
            new_dict = self.gen_dict()
            self.next_token()
            if self.current_token_type == Datatypes.LBRACKET:
                return self.gen_bracketcall(new_dict)
            return new_dict
        elif token_type == Datatypes.TRUE:
            self.next_token()
            return Datatypes.Bool(True)
        elif token_type == Datatypes.FALSE:
            self.next_token()
            return Datatypes.Bool(False)
        elif token_type == Datatypes.NOT:
            self.next_token()
            return Datatypes.BooleanNegationNode(value=self.term())
        # Will handle unary plus und minus signs
        elif token_type == Datatypes.PLUS_SIGN:
            self.next_token()
            return self.exponential()
        elif token_type == Datatypes.MINUS_SIGN:
            self.next_token()
            return Datatypes.MultNode(a=-1.0, b=self.factor())
        # Will handle parentheses and throw an exception in case of a missing parenthesis
        elif token_type == Datatypes.LPAREN:
            self.next_token()
            if self.current_token_type == Datatypes.RPAREN:
                raise SyntaxError("Empty parentheses cannot be evaluated.")
            result = self.statement()
            if self.current_token is None or self.current_token_type != Datatypes.RPAREN:
                raise SyntaxError("Expected a closing parenthesis")
            elif type(result).__name__ == "ComparisonNode":
                self.next_token()
                return Datatypes.BooleanConversionNode(value=result)
            else:
                self.next_token()
                return result
        # Will return either a variable node or a function call node if brackets or a period come after the identifier
        elif token_type == Datatypes.IDENTIFIER:
            identifier = token.value
            self.next_token()
            if self.current_token_type == Datatypes.DOUBLE_PLUS:
                self.next_token()
                return Datatypes.AssignNode(identifier, Datatypes.AddNode(Datatypes.VariableNode(identifier), 1.0))
            elif self.current_token_type == Datatypes.DOUBLE_MINUS:
                self.next_token()
                return Datatypes.AssignNode(identifier, Datatypes.SubNode(Datatypes.VariableNode(identifier), 1.0))
            elif self.current_token_type == Datatypes.LPAREN:
                return self.gen_funccall(identifier)
            elif self.current_token_type == Datatypes.LBRACKET:
                return self.gen_bracketcall(Datatypes.VariableNode(identifier))
            else:
                return Datatypes.VariableNode(identifier=identifier)
        elif token_type == Datatypes.DEL:
            self.next_token()
            if self.current_token_type == Datatypes.LPAREN:
                return self.gen_funccall("del")
            return token
        elif token_type == Datatypes.LET:
            self.next_token()
            identifier = self.current_token.value
            self.next_token()
            return Datatypes.AssignNode(identifier=identifier, value=self.statement())
        elif token_type == Datatypes.BLOCK_END:
            return
        else:
            msg = f"Expected any factor, got {Datatypes.type_dict.get(token_type)}"
            if token.value is not None:
                msg += token.value
            raise SyntaxError(msg)

    # Will follow the pre-defined syntax of a function declaration linearly
    # and will throw exceptions if the syntax is incorrect
    def declare_function(self):
        arguments = []
        if self.current_token_type != Datatypes.IDENTIFIER:
            raise SyntaxError("Expected an identifier")
        else:
            identifier = self.current_token.value
            self.next_token()
        while self.current_token_type == Datatypes.IDENTIFIER:
            arguments.append(self.current_token.value)
            self.next_token()
        else:
            return Datatypes.FuncDeclareNode(identifier=identifier, arguments=arguments,
                                             body=self.statement_block(func_block=True))

    # Will follow the pre-defined syntax of a function call linearly
    # and will throw exceptions if the syntax is incorrect
    def gen_funccall(self, identifier):
        arguments = []
        self.next_token()
        while self.current_token is not None and self.current_token_type != Datatypes.RPAREN:
            arguments.append(self.statement())
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RPAREN:
                raise SyntaxError("Expected comma or closing parenthesis")
        if self.current_token_type != Datatypes.RPAREN:
            raise SyntaxError("Expected closing parenthesis")
        self.next_token()
        return Datatypes.FuncCallNode(identifier=identifier, arguments=arguments)

    def gen_rep(self):
        count_identifier = "_c"
        loop_reps = self.statement()
        if self.current_token_type == Datatypes.AS:
            self.next_token()
            if self.current_token_type != Datatypes.IDENTIFIER:
                raise SyntaxError("Expected identifier after 'as' keyword")
            else:
                count_identifier = self.current_token.value
                self.next_token()
        return Datatypes.RepNode(repetitions=loop_reps, count_identifier=count_identifier,
                                 statements=self.statement_block())

    def gen_for(self):
        assignment = self.statement()
        if self.current_token_type == Datatypes.COMMA:
            self.next_token()
            condition = self.statement()
            if self.current_token_type != Datatypes.COMMA:
                raise SyntaxError("Expected comma after condition")
            self.next_token()
            increment = self.statement()
            return Datatypes.ForNode(assignment=assignment, condition=condition, increment=increment,
                                     statements=self.statement_block())
        elif type(assignment).__name__ == "ContainsNode":
            return Datatypes.IterateNode(iterable=assignment.iterable, items=[assignment.item.identifier],
                                         statements=self.statement_block())
        else:
            raise SyntaxError("Expected comma or \"in\" after statement")

    def gen_iterate(self):
        self.next_token()
        iterable = self.term()
        items = []
        if self.current_token_type == Datatypes.AS:
            self.next_token()
            items.append(self.factor())
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
                items.append(self.factor())
        return Datatypes.IterateNode(iterable=iterable, items=[item.identifier for item in items],
                                     statements=self.statement_block())

    def gen_while(self):
        self.next_token()
        condition = self.statement()
        return Datatypes.WhileNode(condition=condition, statements=self.statement_block())

    def gen_if(self):
        if_node = Datatypes.IfNode()
        self.next_token()
        condition = self.statement()
        block = self.statement_block()
        if_node.add_block(Datatypes.IF, block, condition)
        self.next_token()
        while self.current_token_type in (Datatypes.OR, Datatypes.ELSE):
            keyword = self.current_token_type
            self.next_token()
            if keyword != Datatypes.ELSE:
                condition = self.statement()
            else:
                condition = None
            block = self.statement_block()
            if_node.add_block(keyword, block, condition)
            self.next_token()
        self.skipped_linebreak = True
        return if_node

    def gen_arr(self):
        self.next_token()
        contents = []
        while self.current_token is not None and self.current_token_type != Datatypes.RBRACKET:
            contents.append(self.statement())
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RBRACKET:
                raise SyntaxError("Expected comma or closing parenthesis")
            while self.current_token_type == Datatypes.LINEBREAK:
                self.next_token()
        if self.current_token_type != Datatypes.RBRACKET:
            raise SyntaxError("Expected closing parenthesis")
        return Datatypes.Array(contents)

    def gen_dict(self):
        self.next_token()
        contents = []
        while self.current_token is not None and self.current_token_type != Datatypes.RCURLY:
            key = self.expression()
            if self.current_token_type != Datatypes.BIND:
                raise SyntaxError("Expected bind keyword between key and value.")
            self.next_token()
            value = self.statement()
            contents.append([key, value])
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RCURLY:
                raise SyntaxError("Expected comma or closing parenthesis")
            while self.current_token_type == Datatypes.LINEBREAK:
                self.next_token()
        if self.current_token_type != Datatypes.RCURLY:
            raise SyntaxError("Expected closing parenthesis")
        return Datatypes.DictCreateNode(items=contents)

    def gen_bracketcall(self, identifier):
        indexes = []
        while self.current_token_type == Datatypes.LBRACKET:
            self.next_token()
            index = self.statement()
            if self.current_token_type != Datatypes.RBRACKET:
                raise SyntaxError("Expected ]")
            self.next_token()
            indexes.append(index)
        return Datatypes.BracketCallNode(identifier=identifier, index=indexes)
