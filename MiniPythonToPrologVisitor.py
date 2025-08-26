#!/usr/bin/env python
# coding: utf-8

# In[1]:


from MiniPythonGramatikaVisitor import MiniPythonGramatikaVisitor
from MiniPythonGramatikaParser import MiniPythonGramatikaParser


# In[2]:


class MiniPythonToPrologVisitor(MiniPythonGramatikaVisitor):

    def visitProgram(self, ctx: MiniPythonGramatikaParser.ProgramContext):
        statements = [self.visit(s) for s in ctx.statement()]
        return "\n".join([s for s in statements if s])

    def visitStatement(self, ctx: MiniPythonGramatikaParser.StatementContext):
        code = ""

        if ctx.simple_stmt():
            simple = ctx.simple_stmt()
            if simple.return_stmt():
                code = self.visit(simple.return_stmt())
            elif simple.assignment():
                code = self.visit(simple.assignment())
            elif simple.print_stmt():
                code = self.visit(simple.print_stmt())
            elif simple.function_call():
                code = self.visit(simple.function_call())
        elif ctx.compound_stmt():
            code = self.visit(ctx.compound_stmt())
       
        if code and not code.endswith('.'):
            code += '.'
       
        return code


    # --------------------------------------------------------------------------
    # Simple_stmt
    # --------------------------------------------------------------------------
    def visitAssignment(self, ctx: MiniPythonGramatikaParser.AssignmentContext):
        var = ctx.ID().getText()
        val = self.visit(ctx.expr())
        if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
            val = "'" + val[1:-1] + "'"
            return f"{var} = {val}."
        else: 
            return f"{var} is {val}"

    def visitPrint_stmt(self, ctx: MiniPythonGramatikaParser.Print_stmtContext):
    
        values = [self.visit(e).strip('.') for e in ctx.expr()]
   
        results = []
        for v in values:
            if v.startswith('"') and v.endswith('"'):
                v = "'" + v[1:-1] + "'"

            # 1) string literal
            if v.startswith("'") and v.endswith("'"):
                results.append(f"R = {v}, writeln(R)")
            # 2) čisti broj ili aritmetički izraz
            elif any(op in v for op in ['+', '-', '*', '/']):
                results.append(f"R is {v}, writeln(R)")
            elif v.isnumeric():
                results.append(f"R is {v}, writeln(R)")
            # 3) varijabla 
            else:
                results.append(f"writeln({v})")

        return ", ".join(results)
        

    def visitReturn_stmt(self, ctx: MiniPythonGramatikaParser.Return_stmtContext):
        v = self.visit(ctx.expr()).strip('.')
        if v.startswith('"') and v.endswith('"'):
            v = "'" + v[1:-1] + "'"
        # 1) string literal
        if v.startswith("'") and v.endswith("'"):
            return f"R = {v}"
        # 2) aritmetički izraz
        elif any(op in v for op in ['+', '-', '*', '/']):
            return f"R is {v}"
        elif v.isnumeric():
            return f"R is {v}"
        # 3) varijabla 
        else:
            return f"R = {v}"

    def visitFunction_call(self, ctx: MiniPythonGramatikaParser.Function_callContext):
        fname = ctx.ID().getText()
        args = [self.visit(e) for e in ctx.expr()]
        return f"{fname}({', '.join(args)}, R)"

    # --------------------------------------------------------------------------
    # Compound_stmt
    # --------------------------------------------------------------------------
    def visitIf_stmt(self, ctx: MiniPythonGramatikaParser.If_stmtContext):
        cond = self.visit(ctx.expr())
        then_body = [self.visit(s).strip('.') for s in ctx.block(0).statement()]
        then_body = ", ".join([b for b in then_body if b])
        if ctx.ELSE():
            else_body = [self.visit(s).strip('.') for s in ctx.block(1).statement()]
            else_body = ", ".join([b for b in else_body if b])
            return f"({cond} -> {then_body}; {else_body})"
        return f"({cond} -> {then_body}; true)"

    def visitWhile_loop(self, ctx: MiniPythonGramatikaParser.While_loopContext):
        cond = self.visit(ctx.expr())
        body_stmts = [self.visit(s).strip('.') for s in ctx.block().statement() if s]
        var_updates = ["X1 is X + 1"]  # tu treba promijeniti update ako treba nesto drugo
        body_str = ", ".join(body_stmts)
        updates_str = ", ".join(var_updates)

        return f"""
    while_loop(X) :-
        {cond},
        {body_str},
        {updates_str},
        while_loop(X1).
    while_loop(X) :-
        \\+ ({cond}).
    """.strip()



    def visitFor_loop(self, ctx: MiniPythonGramatikaParser.For_loopContext):
        var = ctx.ID().getText()
        start, end = self.visit(ctx.range_expr())
        body_stmts = [self.visit(s).strip('.') for s in ctx.block().statement() if s]
        body_str = ", ".join(body_stmts) if body_stmts else "true"
       
        return f"""
    for_loop({var}, {end}) :-
        {var} =< {end},
        {body_str},
        Next{var} is {var} + 1,
        for_loop(Next{var}, {end}).
    for_loop({var}, {end}) :-
        {var} > {end}.
    """.strip()
        
    def visitRange_expr(self, ctx: MiniPythonGramatikaParser.Range_exprContext):
        args = [self.visit(e) for e in ctx.expr()]
        if len(args) == 1:
            start = "0"
            end = f"{args[0]} - 1"
        elif len(args) == 2:
            start = args[0]
            end = f"{args[1]} - 1"
        elif len(args) == 3:
            start = args[0]
            end = f"{args[1]} - 1"   
        else:
            start = "0"
            end = "0"
        return start, end

    def visitFunction_def(self, ctx: MiniPythonGramatikaParser.Function_defContext):
        fname = ctx.ID().getText()
        params = []
        if ctx.param_list():
            params = [p.getText() for p in ctx.param_list().ID()]

        body_stmts = ctx.block().statement()
        if len(body_stmts) == 1:
            stmt = body_stmts[0]
            # ako je return
            if stmt.simple_stmt().return_stmt():
                ret_expr = self.visit(stmt.simple_stmt().return_stmt())
                return f"{fname}({', '.join(params)}, R) :- {ret_expr}."
            # ako je print
            elif stmt.simple_stmt() and stmt.simple_stmt().print_stmt():
                expr = self.visit(stmt.simple_stmt().print_stmt())
                return f"{fname}({', '.join(params)}) :- {expr}"
       
        # za slučaj više linija ili složenije funkcije
        statements_code = [self.visit(s) for s in body_stmts]
        statements_code = [s for s in statements_code if s]
        return f"{fname}({', '.join(params)}) :- {', '.join(statements_code)}."

    def visitBlock(self, ctx: MiniPythonGramatikaParser.BlockContext):
        stmts = [self.visit(s).strip('.') for s in ctx.statement()]
        return ",\n   ".join([s for s in stmts if s])

    # --------------------------------------------------------------------------
    # Expressions
    # --------------------------------------------------------------------------
    def visitExpr(self, ctx: MiniPythonGramatikaParser.ExprContext):
        if ctx.op:  # binarne operacije
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.op.text
            if op == "==":
                op = "="
            elif op == "!=":
                op = "\\="
            elif op == "%":
                op = "mod"
            return f"({left} {op} {right})"
        elif ctx.LPAREN() and ctx.RPAREN():
            return f"({self.visit(ctx.expr(0))})"
        elif ctx.ID():
            return ctx.ID().getText()
        elif ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.STRING():
            return ctx.STRING().getText()
        elif ctx.function_call():
            return self.visit(ctx.function_call())
        elif ctx.expr(0):
            return f"({self.visit(ctx.expr(0))})"
        return ""



# In[ ]:




