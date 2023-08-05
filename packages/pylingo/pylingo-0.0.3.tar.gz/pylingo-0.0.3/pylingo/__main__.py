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
from pylingo.pyVisitor import pyVisitor
from pylingo.pylingoLexer import pylingoLexer
from pylingo.pylingoParser import pylingoParser
from pylingo.pylingoVisitor import pylingoVisitor
 
def main(argv):
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())
    #print(input_stream)

    lexer = pylingoLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = pylingoParser(stream)
    tree = parser.lexee()

    #lisp_tree_str = tree.toStringTree(recog=parser)
    #print(lisp_tree_str)

    visitor = pyVisitor()
    visitor.visit(tree)
 
if __name__ == '__main__':
    main(sys.argv)