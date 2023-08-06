# Generated from fortran.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .fortranParser import fortranParser
else:
    from fortranParser import fortranParser

# This class defines a complete generic visitor for a parse tree produced by fortranParser.

class fortranVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by fortranParser#root.
    def visitRoot(self, ctx:fortranParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#units.
    def visitUnits(self, ctx:fortranParser.UnitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#script_unit.
    def visitScript_unit(self, ctx:fortranParser.Script_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#module.
    def visitModule(self, ctx:fortranParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#module_decl.
    def visitModule_decl(self, ctx:fortranParser.Module_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#private_decl.
    def visitPrivate_decl(self, ctx:fortranParser.Private_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#public_decl.
    def visitPublic_decl(self, ctx:fortranParser.Public_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#interface_decl.
    def visitInterface_decl(self, ctx:fortranParser.Interface_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#program.
    def visitProgram(self, ctx:fortranParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#subroutine.
    def visitSubroutine(self, ctx:fortranParser.SubroutineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#function.
    def visitFunction(self, ctx:fortranParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#sub_block.
    def visitSub_block(self, ctx:fortranParser.Sub_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#contains_block.
    def visitContains_block(self, ctx:fortranParser.Contains_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#sub_or_func.
    def visitSub_or_func(self, ctx:fortranParser.Sub_or_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#implicit_statement.
    def visitImplicit_statement(self, ctx:fortranParser.Implicit_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#use_statement.
    def visitUse_statement(self, ctx:fortranParser.Use_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#use_symbol_list.
    def visitUse_symbol_list(self, ctx:fortranParser.Use_symbol_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#use_symbol.
    def visitUse_symbol(self, ctx:fortranParser.Use_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#id_list.
    def visitId_list(self, ctx:fortranParser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#var_decl.
    def visitVar_decl(self, ctx:fortranParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#var_type.
    def visitVar_type(self, ctx:fortranParser.Var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#var_modifier.
    def visitVar_modifier(self, ctx:fortranParser.Var_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#var_sym_decl.
    def visitVar_sym_decl(self, ctx:fortranParser.Var_sym_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#array_decl.
    def visitArray_decl(self, ctx:fortranParser.Array_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#array_comp_decl.
    def visitArray_comp_decl(self, ctx:fortranParser.Array_comp_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#statements.
    def visitStatements(self, ctx:fortranParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#statement.
    def visitStatement(self, ctx:fortranParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#assignment_statement.
    def visitAssignment_statement(self, ctx:fortranParser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#exit_statement.
    def visitExit_statement(self, ctx:fortranParser.Exit_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#cycle_statement.
    def visitCycle_statement(self, ctx:fortranParser.Cycle_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#return_statement.
    def visitReturn_statement(self, ctx:fortranParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#subroutine_call.
    def visitSubroutine_call(self, ctx:fortranParser.Subroutine_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#builtin_statement.
    def visitBuiltin_statement(self, ctx:fortranParser.Builtin_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#if_single_line.
    def visitIf_single_line(self, ctx:fortranParser.If_single_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#if_multi_line.
    def visitIf_multi_line(self, ctx:fortranParser.If_multi_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#if_cond.
    def visitIf_cond(self, ctx:fortranParser.If_condContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#if_block.
    def visitIf_block(self, ctx:fortranParser.If_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#if_else_block.
    def visitIf_else_block(self, ctx:fortranParser.If_else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#where_single_line.
    def visitWhere_single_line(self, ctx:fortranParser.Where_single_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#where_multi_line.
    def visitWhere_multi_line(self, ctx:fortranParser.Where_multi_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#where_cond.
    def visitWhere_cond(self, ctx:fortranParser.Where_condContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#where_block.
    def visitWhere_block(self, ctx:fortranParser.Where_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#where_else_block.
    def visitWhere_else_block(self, ctx:fortranParser.Where_else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#do_statement.
    def visitDo_statement(self, ctx:fortranParser.Do_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#while_statement.
    def visitWhile_statement(self, ctx:fortranParser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#select_statement.
    def visitSelect_statement(self, ctx:fortranParser.Select_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#case_statement.
    def visitCase_statement(self, ctx:fortranParser.Case_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#select_default_statement.
    def visitSelect_default_statement(self, ctx:fortranParser.Select_default_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#print_statement.
    def visitPrint_statement(self, ctx:fortranParser.Print_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#write_statement.
    def visitWrite_statement(self, ctx:fortranParser.Write_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#stop_statement.
    def visitStop_statement(self, ctx:fortranParser.Stop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#error_stop_statement.
    def visitError_stop_statement(self, ctx:fortranParser.Error_stop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_list.
    def visitExpr_list(self, ctx:fortranParser.Expr_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_or.
    def visitExpr_or(self, ctx:fortranParser.Expr_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_truefalse.
    def visitExpr_truefalse(self, ctx:fortranParser.Expr_truefalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_unary.
    def visitExpr_unary(self, ctx:fortranParser.Expr_unaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_array_call.
    def visitExpr_array_call(self, ctx:fortranParser.Expr_array_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_id.
    def visitExpr_id(self, ctx:fortranParser.Expr_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_not.
    def visitExpr_not(self, ctx:fortranParser.Expr_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_eqv.
    def visitExpr_eqv(self, ctx:fortranParser.Expr_eqvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_nest.
    def visitExpr_nest(self, ctx:fortranParser.Expr_nestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_pow.
    def visitExpr_pow(self, ctx:fortranParser.Expr_powContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_number.
    def visitExpr_number(self, ctx:fortranParser.Expr_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_and.
    def visitExpr_and(self, ctx:fortranParser.Expr_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_addsub.
    def visitExpr_addsub(self, ctx:fortranParser.Expr_addsubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_array_const.
    def visitExpr_array_const(self, ctx:fortranParser.Expr_array_constContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_rel.
    def visitExpr_rel(self, ctx:fortranParser.Expr_relContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_fn_call.
    def visitExpr_fn_call(self, ctx:fortranParser.Expr_fn_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_string_conc.
    def visitExpr_string_conc(self, ctx:fortranParser.Expr_string_concContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_muldiv.
    def visitExpr_muldiv(self, ctx:fortranParser.Expr_muldivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#expr_string.
    def visitExpr_string(self, ctx:fortranParser.Expr_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#arg_list.
    def visitArg_list(self, ctx:fortranParser.Arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#arg.
    def visitArg(self, ctx:fortranParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#array_index_list.
    def visitArray_index_list(self, ctx:fortranParser.Array_index_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#array_index_simple.
    def visitArray_index_simple(self, ctx:fortranParser.Array_index_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#array_index_slice.
    def visitArray_index_slice(self, ctx:fortranParser.Array_index_sliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#struct_member.
    def visitStruct_member(self, ctx:fortranParser.Struct_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#number_real.
    def visitNumber_real(self, ctx:fortranParser.Number_realContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#number_complex.
    def visitNumber_complex(self, ctx:fortranParser.Number_complexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by fortranParser#ident.
    def visitIdent(self, ctx:fortranParser.IdentContext):
        return self.visitChildren(ctx)



del fortranParser