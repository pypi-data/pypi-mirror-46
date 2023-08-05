
 #  Copyright 2019  Dialect Software LLC or its affiliates. All Rights Reserved.
 #
 #  Licensed under the MIT License (the "License").
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.
 
import sys
from antlr4 import *
from pylingo.pylingoParser import pylingoParser
from pylingo.pylingoVisitor import pylingoVisitor

class pyVisitor(pylingoVisitor):
    def __init__(self):
        self.memory = {}

    # Visit a parse tree produced by pylingoParser#protolingo.
    def visitLexee(self, ctx:pylingoParser.LexeeContext):
        return super().visitChildren(ctx)
    
    def visitPreamble(self, ctx:pylingoParser.PreambleContext):
        result = self.visitChildren(ctx)
        print(" ".join([child.getText() for child in ctx.getChildren()] [1::]))
        return result

    # Visit a parse tree produced by pylingoParser#ident.
    def visitIdent(self, ctx:pylingoParser.IdentContext):
        print(ctx.getText(), end =' ')
        return self.visitChildren(ctx)