import Datatypes

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = -1
        self.current_token = None
        self.current_token_type = None
        self.optional_open_blocks = 0
        self.ast_list = []
        self.next_token()

    def update_token(self, token_delta):
        try:
            self.n += token_delta
            self.current_token = self.tokens[self.n]
            self.current_token_type = self.current_token.type
        except IndexError:
            self.current_token = None
            self.current_token_type = None

    def next_token(self):
        self.update_token(1)
    
    def previous_token(self):
        self.update_token(-1)
    
    def skip_linebreaks(self):
        while self.current_token_type == Datatypes.LINEBREAK:
            self.next_token()

    def parse(self):
        while self.current_token is not None:
            self.skip_linebreaks()
            if self.current_token is not None:
                self.ast_list.append(self.compound_statement())
            if self.current_token_type not in (Datatypes.LINEBREAK, None):
                raise SyntaxError(f"Expected end of statement, got token type {Datatypes.type_dict.get(self.current_token_type)}")
        return self.ast_list

    def statement_block(self, func_block=False, block_starter=Datatypes.ARROW, block_ender=Datatypes.BLOCK_END):
        if self.current_token_type != block_starter:
            raise SyntaxError("Expected '=>'")
        self.next_token()
        if self.current_token_type != Datatypes.LINEBREAK:
            return self.compound_statement() if func_block else [self.compound_statement()]
        block = []
        while self.current_token_type not in (Datatypes.BLOCK_END, None):
            self.skip_linebreaks()
            block.append(self.compound_statement())
            if self.current_token_type is None:
                raise SyntaxError("Expected expression")
        if self.current_token_type != Datatypes.BLOCK_END:
            raise SyntaxError(f"Expected block ending operator")
        self.next_token()
        return block

    def compound_statement(self):
        result = self.statement()
        while self.current_token_type in (Datatypes.AND, Datatypes.OR, Datatypes.NOT):
            token_type = self.current_token_type
            self.next_token()
            match token_type:
                case Datatypes.NOT:
                    if self.current_token_type == Datatypes.IN:
                        self.next_token()
                        result = Datatypes.BooleanNegationNode(
                            Datatypes.ComparisonNode(a=result, b=self.statement(), operator=Datatypes.IN))
                case Datatypes.AND | Datatypes.OR:
                    result = Datatypes.LogicalOperationNode(a=result, b=self.statement(), operation=token_type)
        return result


    def statement(self):
        result = self.expression()
        while self.current_token_type in Datatypes.STATEMENT_TOKENS:
            token_type = self.current_token_type
            if token_type != Datatypes.ITERATE_ARROW:
                self.next_token()
            if token_type == Datatypes.SOLVE:
                result = Datatypes.SolveNode(result, self.expression())
            elif token_type == Datatypes.SOLVE_ASSIGN:
                result = Datatypes.SolveAssignNode(result, self.expression())
            elif token_type == Datatypes.ITERATE_ARROW:
                result = Datatypes.IterateNode(iterable=result, items=[], statements=self.statement_block(block_starter=Datatypes.ITERATE_ARROW))
            elif token_type == Datatypes.IF:
                if_expr = result
                result = Datatypes.IfNode()
                condition = self.compound_statement()
                result.add_block(Datatypes.IF, [if_expr], condition)
                if self.current_token_type == Datatypes.ELSE:
                    self.next_token()
                    else_expr = self.compound_statement()
                    result.add_block(Datatypes.ELSE, [else_expr])
            else:
                result = Datatypes.ComparisonNode(a=result, b=self.expression(), operator=token_type)
        return result

    def expression(self):
        result = self.term()
        while self.current_token_type in Datatypes.EXPRESSION_TOKENS:
            token_type = self.current_token_type
            self.next_token()
            if token_type in (Datatypes.PLUS_SIGN, Datatypes.MINUS_SIGN):
                result = Datatypes.OPERATOR_NODE_DICT[token_type](a=result, b=self.term())
        return result

    def term(self):
        result = self.exponential()
        while self.current_token_type in Datatypes.TERM_TOKENS:
            token_type = self.current_token_type
            self.next_token()
            match token_type:
                case Datatypes.MULT_SIGN | Datatypes.DIV_SIGN | Datatypes.MODULUS_SIGN | Datatypes.FLOORDIV_SIGN:
                    result = Datatypes.OPERATOR_NODE_DICT[token_type](a=result, b=self.exponential())
                case Datatypes.EQUALS:
                    result = Datatypes.AssignNode(variable=result, value=self.compound_statement())
                case token_type if token_type in Datatypes.OP_ASSIGN_TOKENS:
                    operator_node = Datatypes.OPERATOR_NODE_DICT[token_type]
                    result = Datatypes.AssignNode(variable=result, value=operator_node(result, self.compound_statement()))
                case Datatypes.ARRAYAPPLY:
                    result = Datatypes.ArrayApplyNode(identifier=result, function=self.compound_statement())
                case Datatypes.DOUBLE_PERIOD:
                    start = result
                    stop = self.exponential()
                    if self.current_token_type == Datatypes.DOUBLE_PERIOD:
                        self.next_token()
                        step = self.exponential()
                    else:
                        step = 1
                    return Datatypes.RangeNode(start=start, stop=stop, step=step)
        return result

    def exponential(self):
        result = self.factor()
        while self.current_token_type in Datatypes.EXPONENTIAL_TOKENS:
            token_type = self.current_token_type
            if token_type != Datatypes.IDENTIFIER:
                self.next_token()
            if token_type == Datatypes.EXP:
                result = Datatypes.ExpNode(a=result, b=self.factor())
            elif token_type == Datatypes.IDENTIFIER:
                result = Datatypes.FuncCallNode(variable=self.factor(), arguments=[result])
            elif token_type == Datatypes.COLON:
                if isinstance(result, Datatypes.VariableNode):
                    result = Datatypes.FuncCallNode(variable=result, arguments=[self.factor()])
                    while self.current_token_type == Datatypes.COMMA:
                        self.next_token()
                        result.arguments.append(self.factor())
                elif isinstance(result, Datatypes.FuncCallNode):
                    result.arguments.append(self.factor())
                    while self.current_token_type == Datatypes.COMMA:
                        self.next_token()
                        result.arguments.append(self.factor())
                else:
                    raise SyntaxError("No colon allowed here.")
            elif token_type == Datatypes.DOUBLE_PLUS:
                result = Datatypes.PostIncrementNode(factor=result, value=1.0)
            elif token_type == Datatypes.DOUBLE_MINUS:
                result = Datatypes.PostIncrementNode(factor=result, value=-1.0)
            elif token_type == Datatypes.LBRACKET:
                self.previous_token()
                result = self.gen_bracketcall(result)
        return result

    def factor(self):
        token = self.current_token
        token_type = self.current_token_type
        if token_type not in (None, Datatypes.BLOCK_END):
            self.next_token()
        match token_type:
            case Datatypes.NUMBER:
                return token.value
            case Datatypes.STRING:
                new_tokens = []
                for tokens in token.value.tokens:
                    ast = Parser(tokens).parse()
                    if len(ast) > 1:
                        raise SyntaxError("Too many statements inside dstring argument.")
                    new_tokens.append(ast[0])
                return Datatypes.StringBuilderNode(token.value.string, new_tokens)
            case Datatypes.FUNCTION_KEYWORD:
                return self.declare_function()
            case Datatypes.ANONYMOUS_FUNCTION_KEYWORD:
                return self.declare_anonymous_function()
            case Datatypes.RETURN:
                if self.current_token_type == Datatypes.LINEBREAK:
                    return Datatypes.ReturnNode(statement=None)
                else:
                    return Datatypes.ReturnNode(statement=self.compound_statement())
            case Datatypes.BREAK:
                return Datatypes.AssignNode(Datatypes.VariableNode("__break__"), None)
            case Datatypes.CONTINUE:
                return Datatypes.AssignNode(Datatypes.VariableNode("__return__"), None)
            case Datatypes.REP:
                return self.gen_rep()
            case Datatypes.FOR:
                return self.gen_for()
            case Datatypes.IF:
                return self.gen_if()
            case Datatypes.ITERATE:
                return self.gen_iterate()
            case Datatypes.WHILE:
                return self.gen_while()
            case Datatypes.LBRACKET:
                arr = self.gen_arr()
                self.next_token()
                return arr
            case Datatypes.LCURLY:
                new_dict = self.gen_dict()
                self.next_token()
                return new_dict
            case Datatypes.TRUE:
                return Datatypes.Bool(True)
            case Datatypes.FALSE:
                return Datatypes.Bool(False)
            case Datatypes.NOT:
                return Datatypes.BooleanNegationNode(value=self.statement())
            case Datatypes.PLUS_SIGN:
                return self.exponential()
            case Datatypes.MINUS_SIGN:
                return Datatypes.MultNode(a=-1.0, b=self.factor())
            case Datatypes.LPAREN:
                if self.current_token_type == Datatypes.RPAREN:
                    raise SyntaxError("Empty parentheses cannot be evaluated.")
                result = self.compound_statement()
                if self.current_token is None or self.current_token_type != Datatypes.RPAREN:
                    raise SyntaxError("Expected a closing parenthesis")
                else:
                    self.next_token()
                    return result
            case Datatypes.DOUBLE_MINUS:
                fct = self.factor()
                return Datatypes.AssignNode(fct, Datatypes.AddNode(fct, -1.0))
            case Datatypes.DOUBLE_PLUS:
                fct = self.factor()
                return Datatypes.AssignNode(fct, Datatypes.AddNode(fct, 1.0))
            case Datatypes.IDENTIFIER:
                identifier = token.value
                if self.current_token_type == Datatypes.LPAREN:
                    return self.gen_funccall(identifier)
                else:
                    return Datatypes.VariableNode(identifier=identifier)
            case Datatypes.DEL:
                if self.current_token_type == Datatypes.LPAREN:
                    return self.gen_funccall("del")
                return token
            case Datatypes.LET:
                identifier = self.current_token.value
                self.next_token()
                return Datatypes.AssignNode(variable=Datatypes.VariableNode(identifier), value=self.compound_statement())
            case Datatypes.BLOCK_END:
                return
            case None:
                raise SyntaxError("Expected number or identifier")
            case _:
                msg = f"Expected any factor, got {Datatypes.type_dict.get(token_type)}"
                if token.value is not None:
                    msg += token.value
                raise SyntaxError(msg)

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
            return Datatypes.AssignNode(variable=Datatypes.VariableNode(identifier),
                                        value=Datatypes.Function(
                                            arglist=arguments,
                                            identifier=identifier,
                                            body=self.statement_block(func_block=True)
                                        ))
    
    def declare_anonymous_function(self):
        arguments = []
        while self.current_token_type == Datatypes.IDENTIFIER:
            arguments.append(self.current_token.value)
            self.next_token()
        return Datatypes.Function(
                    arglist=arguments,
                    body=self.statement_block(func_block=True)
                )

    def gen_funccall(self, identifier):
        arguments = []
        self.next_token()
        while self.current_token_type not in (None, Datatypes.RPAREN):
            arguments.append(self.compound_statement())
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RPAREN:
                raise SyntaxError("Expected comma or closing parenthesis")
        if self.current_token_type != Datatypes.RPAREN:
            raise SyntaxError("Expected closing parenthesis")
        self.next_token()
        return Datatypes.FuncCallNode(variable=Datatypes.VariableNode(identifier), arguments=arguments)

    def gen_rep(self):
        items = []
        loop_reps = self.compound_statement()
        if self.current_token_type == Datatypes.AS:
            self.next_token()
            if self.current_token_type != Datatypes.IDENTIFIER:
                raise SyntaxError("Expected identifier after 'as' keyword")
            items.append(self.current_token.value)
            self.next_token()
        return Datatypes.IterateNode(iterable = Datatypes.RangeNode(start=0, stop=loop_reps, step=1),
                                    items = items,
                                     statements=self.statement_block())

    def gen_for(self):
        assignment = self.compound_statement()
        if self.current_token_type == Datatypes.COMMA:
            self.next_token()
            condition = self.compound_statement()
            if self.current_token_type != Datatypes.COMMA:
                raise SyntaxError("Expected comma after condition")
            self.next_token()
            increment = self.compound_statement()
            return Datatypes.ForNode(assignment=assignment, condition=condition, increment=increment,
                                     statements=self.statement_block())
        elif type(assignment).__name__ == "ComparisonNode" and assignment.operator == Datatypes.IN:
            return Datatypes.IterateNode(iterable=assignment.b, items=[assignment.a.identifier],
                                         statements=self.statement_block())
        else:
            raise SyntaxError("Expected comma or \"in\" after statement")

    def gen_iterate(self):
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
        condition = self.compound_statement()
        return Datatypes.ForNode(assignment=None, condition=condition, increment=None, statements=self.statement_block())

    def gen_if(self):
        if_node = Datatypes.IfNode()
        condition = self.compound_statement()
        block = self.statement_block()
        if_node.add_block(Datatypes.IF, block, condition)
        self.next_token()
        self.skip_linebreaks()
        while self.current_token_type in (Datatypes.OR, Datatypes.ELSE):
            keyword = self.current_token_type
            self.next_token()
            condition = None if keyword == Datatypes.ELSE else self.compound_statement()
            block = self.statement_block()
            if_node.add_block(keyword, block, condition)
            self.next_token()
            self.skip_linebreaks()
        self.previous_token()
        return if_node

    def gen_arr(self):
        contents = []
        while self.current_token is not None and self.current_token_type != Datatypes.RBRACKET:
            contents.append(self.compound_statement())
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RBRACKET:
                raise SyntaxError("Expected comma or closing parenthesis")
            self.skip_linebreaks()
        if self.current_token_type != Datatypes.RBRACKET:
            raise SyntaxError("Expected closing bracket")
        return Datatypes.ArrayCreateNode(items=contents)

    def gen_dict(self):
        contents = []
        while self.current_token is not None and self.current_token_type != Datatypes.RCURLY:
            key = self.exponential()
            if self.current_token_type != Datatypes.BIND:
                raise SyntaxError("Expected bind keyword between key and value.")
            self.next_token()
            value = self.compound_statement()
            contents.append([key, value])
            if self.current_token_type == Datatypes.COMMA:
                self.next_token()
            elif self.current_token_type != Datatypes.RCURLY:
                raise SyntaxError("Expected comma or closing parenthesis")
            self.skip_linebreaks()
        if self.current_token_type != Datatypes.RCURLY:
            raise SyntaxError("Expected closing parenthesis")
        return Datatypes.DictCreateNode(items=contents)

    def gen_bracketcall(self, identifier):
        indexes = []
        while self.current_token_type == Datatypes.LBRACKET:
            self.next_token()
            index = self.compound_statement()
            if self.current_token_type != Datatypes.RBRACKET:
                raise SyntaxError("Expected ]")
            self.next_token()
            indexes.append(index)
        return Datatypes.BracketCallNode(identifier=identifier, index=indexes)
