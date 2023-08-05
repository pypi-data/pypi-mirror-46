# Generated from pylingo/pylingo.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pylingoParser import pylingoParser
else:
    from pylingoParser import pylingoParser

# This class defines a complete listener for a parse tree produced by pylingoParser.
class pylingoListener(ParseTreeListener):

    # Enter a parse tree produced by pylingoParser#lexee.
    def enterLexee(self, ctx:pylingoParser.LexeeContext):
        pass

    # Exit a parse tree produced by pylingoParser#lexee.
    def exitLexee(self, ctx:pylingoParser.LexeeContext):
        pass


    # Enter a parse tree produced by pylingoParser#decl.
    def enterDecl(self, ctx:pylingoParser.DeclContext):
        pass

    # Exit a parse tree produced by pylingoParser#decl.
    def exitDecl(self, ctx:pylingoParser.DeclContext):
        pass


    # Enter a parse tree produced by pylingoParser#comment.
    def enterComment(self, ctx:pylingoParser.CommentContext):
        pass

    # Exit a parse tree produced by pylingoParser#comment.
    def exitComment(self, ctx:pylingoParser.CommentContext):
        pass


    # Enter a parse tree produced by pylingoParser#code.
    def enterCode(self, ctx:pylingoParser.CodeContext):
        pass

    # Exit a parse tree produced by pylingoParser#code.
    def exitCode(self, ctx:pylingoParser.CodeContext):
        pass


    # Enter a parse tree produced by pylingoParser#preamble.
    def enterPreamble(self, ctx:pylingoParser.PreambleContext):
        pass

    # Exit a parse tree produced by pylingoParser#preamble.
    def exitPreamble(self, ctx:pylingoParser.PreambleContext):
        pass


    # Enter a parse tree produced by pylingoParser#obj.
    def enterObj(self, ctx:pylingoParser.ObjContext):
        pass

    # Exit a parse tree produced by pylingoParser#obj.
    def exitObj(self, ctx:pylingoParser.ObjContext):
        pass


    # Enter a parse tree produced by pylingoParser#body.
    def enterBody(self, ctx:pylingoParser.BodyContext):
        pass

    # Exit a parse tree produced by pylingoParser#body.
    def exitBody(self, ctx:pylingoParser.BodyContext):
        pass


    # Enter a parse tree produced by pylingoParser#variable.
    def enterVariable(self, ctx:pylingoParser.VariableContext):
        pass

    # Exit a parse tree produced by pylingoParser#variable.
    def exitVariable(self, ctx:pylingoParser.VariableContext):
        pass


    # Enter a parse tree produced by pylingoParser#assignment.
    def enterAssignment(self, ctx:pylingoParser.AssignmentContext):
        pass

    # Exit a parse tree produced by pylingoParser#assignment.
    def exitAssignment(self, ctx:pylingoParser.AssignmentContext):
        pass


    # Enter a parse tree produced by pylingoParser#array.
    def enterArray(self, ctx:pylingoParser.ArrayContext):
        pass

    # Exit a parse tree produced by pylingoParser#array.
    def exitArray(self, ctx:pylingoParser.ArrayContext):
        pass


    # Enter a parse tree produced by pylingoParser#doc.
    def enterDoc(self, ctx:pylingoParser.DocContext):
        pass

    # Exit a parse tree produced by pylingoParser#doc.
    def exitDoc(self, ctx:pylingoParser.DocContext):
        pass


    # Enter a parse tree produced by pylingoParser#json.
    def enterJson(self, ctx:pylingoParser.JsonContext):
        pass

    # Exit a parse tree produced by pylingoParser#json.
    def exitJson(self, ctx:pylingoParser.JsonContext):
        pass


    # Enter a parse tree produced by pylingoParser#ident.
    def enterIdent(self, ctx:pylingoParser.IdentContext):
        pass

    # Exit a parse tree produced by pylingoParser#ident.
    def exitIdent(self, ctx:pylingoParser.IdentContext):
        pass


    # Enter a parse tree produced by pylingoParser#value.
    def enterValue(self, ctx:pylingoParser.ValueContext):
        pass

    # Exit a parse tree produced by pylingoParser#value.
    def exitValue(self, ctx:pylingoParser.ValueContext):
        pass


