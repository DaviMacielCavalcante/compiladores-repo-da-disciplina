# Generated from PythonParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,45,238,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,3,1,59,8,1,1,2,1,2,1,2,1,2,1,2,5,2,66,8,2,10,2,12,2,
        69,9,2,1,2,1,2,1,2,3,2,74,8,2,1,3,1,3,1,3,1,3,1,3,5,3,81,8,3,10,
        3,12,3,84,9,3,1,3,1,3,3,3,88,8,3,1,4,1,4,1,4,1,4,1,4,3,4,95,8,4,
        1,4,1,4,3,4,99,8,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,108,8,5,1,6,1,
        6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,125,8,
        7,3,7,127,8,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,3,8,139,8,
        8,1,9,1,9,3,9,143,8,9,1,10,1,10,3,10,147,8,10,1,11,1,11,3,11,151,
        8,11,1,12,1,12,5,12,155,8,12,10,12,12,12,158,9,12,1,12,1,12,3,12,
        162,8,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,4,13,
        174,8,13,11,13,12,13,175,1,13,1,13,1,13,1,13,5,13,182,8,13,10,13,
        12,13,185,9,13,3,13,187,8,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,
        195,8,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,
        1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,
        5,13,221,8,13,10,13,12,13,224,9,13,1,14,1,14,1,15,1,15,1,16,1,16,
        1,17,1,17,1,18,1,18,1,19,1,19,1,19,0,1,26,20,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,28,30,32,34,36,38,0,5,1,0,15,16,1,0,17,19,1,0,
        21,26,1,0,27,29,1,0,30,31,258,0,43,1,0,0,0,2,58,1,0,0,0,4,60,1,0,
        0,0,6,75,1,0,0,0,8,89,1,0,0,0,10,100,1,0,0,0,12,109,1,0,0,0,14,114,
        1,0,0,0,16,132,1,0,0,0,18,140,1,0,0,0,20,144,1,0,0,0,22,148,1,0,
        0,0,24,161,1,0,0,0,26,194,1,0,0,0,28,225,1,0,0,0,30,227,1,0,0,0,
        32,229,1,0,0,0,34,231,1,0,0,0,36,233,1,0,0,0,38,235,1,0,0,0,40,42,
        3,2,1,0,41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,
        44,46,1,0,0,0,45,43,1,0,0,0,46,47,5,0,0,1,47,1,1,0,0,0,48,59,3,4,
        2,0,49,59,3,6,3,0,50,59,3,8,4,0,51,59,3,10,5,0,52,59,3,12,6,0,53,
        59,3,14,7,0,54,59,3,22,11,0,55,59,3,16,8,0,56,59,3,18,9,0,57,59,
        3,20,10,0,58,48,1,0,0,0,58,49,1,0,0,0,58,50,1,0,0,0,58,51,1,0,0,
        0,58,52,1,0,0,0,58,53,1,0,0,0,58,54,1,0,0,0,58,55,1,0,0,0,58,56,
        1,0,0,0,58,57,1,0,0,0,59,3,1,0,0,0,60,67,5,41,0,0,61,62,5,36,0,0,
        62,63,3,26,13,0,63,64,5,37,0,0,64,66,1,0,0,0,65,61,1,0,0,0,66,69,
        1,0,0,0,67,65,1,0,0,0,67,68,1,0,0,0,68,70,1,0,0,0,69,67,1,0,0,0,
        70,71,5,14,0,0,71,73,3,26,13,0,72,74,5,39,0,0,73,72,1,0,0,0,73,74,
        1,0,0,0,74,5,1,0,0,0,75,76,5,1,0,0,76,77,5,32,0,0,77,82,3,26,13,
        0,78,79,5,40,0,0,79,81,3,26,13,0,80,78,1,0,0,0,81,84,1,0,0,0,82,
        80,1,0,0,0,82,83,1,0,0,0,83,85,1,0,0,0,84,82,1,0,0,0,85,87,5,33,
        0,0,86,88,5,39,0,0,87,86,1,0,0,0,87,88,1,0,0,0,88,7,1,0,0,0,89,90,
        5,41,0,0,90,91,5,14,0,0,91,92,5,2,0,0,92,94,5,32,0,0,93,95,5,43,
        0,0,94,93,1,0,0,0,94,95,1,0,0,0,95,96,1,0,0,0,96,98,5,33,0,0,97,
        99,5,39,0,0,98,97,1,0,0,0,98,99,1,0,0,0,99,9,1,0,0,0,100,101,5,3,
        0,0,101,102,3,26,13,0,102,103,5,38,0,0,103,107,3,24,12,0,104,105,
        5,4,0,0,105,106,5,38,0,0,106,108,3,24,12,0,107,104,1,0,0,0,107,108,
        1,0,0,0,108,11,1,0,0,0,109,110,5,5,0,0,110,111,3,26,13,0,111,112,
        5,38,0,0,112,113,3,24,12,0,113,13,1,0,0,0,114,115,5,6,0,0,115,116,
        5,41,0,0,116,117,5,7,0,0,117,118,5,8,0,0,118,119,5,32,0,0,119,126,
        3,26,13,0,120,121,5,40,0,0,121,124,3,26,13,0,122,123,5,40,0,0,123,
        125,3,26,13,0,124,122,1,0,0,0,124,125,1,0,0,0,125,127,1,0,0,0,126,
        120,1,0,0,0,126,127,1,0,0,0,127,128,1,0,0,0,128,129,5,33,0,0,129,
        130,5,38,0,0,130,131,3,24,12,0,131,15,1,0,0,0,132,133,5,9,0,0,133,
        134,5,38,0,0,134,135,3,24,12,0,135,136,5,5,0,0,136,138,3,26,13,0,
        137,139,5,39,0,0,138,137,1,0,0,0,138,139,1,0,0,0,139,17,1,0,0,0,
        140,142,5,10,0,0,141,143,5,39,0,0,142,141,1,0,0,0,142,143,1,0,0,
        0,143,19,1,0,0,0,144,146,5,11,0,0,145,147,5,39,0,0,146,145,1,0,0,
        0,146,147,1,0,0,0,147,21,1,0,0,0,148,150,3,26,13,0,149,151,5,39,
        0,0,150,149,1,0,0,0,150,151,1,0,0,0,151,23,1,0,0,0,152,156,5,34,
        0,0,153,155,3,2,1,0,154,153,1,0,0,0,155,158,1,0,0,0,156,154,1,0,
        0,0,156,157,1,0,0,0,157,159,1,0,0,0,158,156,1,0,0,0,159,162,5,35,
        0,0,160,162,3,2,1,0,161,152,1,0,0,0,161,160,1,0,0,0,162,25,1,0,0,
        0,163,164,6,13,-1,0,164,165,5,32,0,0,165,166,3,26,13,0,166,167,5,
        33,0,0,167,195,1,0,0,0,168,173,5,41,0,0,169,170,5,36,0,0,170,171,
        3,26,13,0,171,172,5,37,0,0,172,174,1,0,0,0,173,169,1,0,0,0,174,175,
        1,0,0,0,175,173,1,0,0,0,175,176,1,0,0,0,176,195,1,0,0,0,177,186,
        5,36,0,0,178,183,3,26,13,0,179,180,5,40,0,0,180,182,3,26,13,0,181,
        179,1,0,0,0,182,185,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,
        187,1,0,0,0,185,183,1,0,0,0,186,178,1,0,0,0,186,187,1,0,0,0,187,
        188,1,0,0,0,188,195,5,37,0,0,189,195,5,41,0,0,190,195,5,42,0,0,191,
        195,5,43,0,0,192,195,5,12,0,0,193,195,5,13,0,0,194,163,1,0,0,0,194,
        168,1,0,0,0,194,177,1,0,0,0,194,189,1,0,0,0,194,190,1,0,0,0,194,
        191,1,0,0,0,194,192,1,0,0,0,194,193,1,0,0,0,195,222,1,0,0,0,196,
        197,10,14,0,0,197,198,3,32,16,0,198,199,3,26,13,15,199,221,1,0,0,
        0,200,201,10,13,0,0,201,202,3,30,15,0,202,203,3,26,13,14,203,221,
        1,0,0,0,204,205,10,12,0,0,205,206,3,28,14,0,206,207,3,26,13,13,207,
        221,1,0,0,0,208,209,10,11,0,0,209,210,3,34,17,0,210,211,3,26,13,
        12,211,221,1,0,0,0,212,213,10,10,0,0,213,214,3,38,19,0,214,215,3,
        26,13,11,215,221,1,0,0,0,216,217,10,9,0,0,217,218,3,36,18,0,218,
        219,3,26,13,10,219,221,1,0,0,0,220,196,1,0,0,0,220,200,1,0,0,0,220,
        204,1,0,0,0,220,208,1,0,0,0,220,212,1,0,0,0,220,216,1,0,0,0,221,
        224,1,0,0,0,222,220,1,0,0,0,222,223,1,0,0,0,223,27,1,0,0,0,224,222,
        1,0,0,0,225,226,7,0,0,0,226,29,1,0,0,0,227,228,7,1,0,0,228,31,1,
        0,0,0,229,230,5,20,0,0,230,33,1,0,0,0,231,232,7,2,0,0,232,35,1,0,
        0,0,233,234,7,3,0,0,234,37,1,0,0,0,235,236,7,4,0,0,236,39,1,0,0,
        0,23,43,58,67,73,82,87,94,98,107,124,126,138,142,146,150,156,161,
        175,183,186,194,220,222
    ]

class PythonParser ( Parser ):

    grammarFileName = "PythonParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "'input'", "'if'", "'else'", 
                     "'while'", "'for'", "'in'", "'range'", "'do'", "'break'", 
                     "'continue'", "'True'", "'False'", "'='", "'+'", "'-'", 
                     "'*'", "'/'", "'%'", "'**'", "'=='", "'!='", "'<'", 
                     "'>'", "'<='", "'>='", "'and'", "'or'", "'not'", "'&'", 
                     "'|'", "'('", "')'", "'{'", "'}'", "'['", "']'", "':'", 
                     "';'", "','" ]

    symbolicNames = [ "<INVALID>", "PRINT", "INPUT", "IF", "ELSE", "WHILE", 
                      "FOR", "IN", "RANGE", "DO", "BREAK", "CONTINUE", "TRUE", 
                      "FALSE", "ASSIGN", "PLUS", "MINUS", "MULT", "DIV", 
                      "MOD", "POW", "EQ", "NEQ", "LT", "GT", "LTE", "GTE", 
                      "AND", "OR", "NOT", "BITAND", "BITOR", "LPAREN", "RPAREN", 
                      "LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", 
                      "SEMICOLON", "COMMA", "IDENTIFIER", "NUMBER", "STRING", 
                      "WS", "COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_assignmentStatement = 2
    RULE_printStatement = 3
    RULE_inputStatement = 4
    RULE_ifStatement = 5
    RULE_whileStatement = 6
    RULE_forStatement = 7
    RULE_doWhileStatement = 8
    RULE_breakStatement = 9
    RULE_continueStatement = 10
    RULE_expressionStatement = 11
    RULE_block = 12
    RULE_expression = 13
    RULE_add_sub = 14
    RULE_mul_div = 15
    RULE_pow_op = 16
    RULE_comparison_op = 17
    RULE_logical_op = 18
    RULE_bitwise_and_or = 19

    ruleNames =  [ "program", "statement", "assignmentStatement", "printStatement", 
                   "inputStatement", "ifStatement", "whileStatement", "forStatement", 
                   "doWhileStatement", "breakStatement", "continueStatement", 
                   "expressionStatement", "block", "expression", "add_sub", 
                   "mul_div", "pow_op", "comparison_op", "logical_op", "bitwise_and_or" ]

    EOF = Token.EOF
    PRINT=1
    INPUT=2
    IF=3
    ELSE=4
    WHILE=5
    FOR=6
    IN=7
    RANGE=8
    DO=9
    BREAK=10
    CONTINUE=11
    TRUE=12
    FALSE=13
    ASSIGN=14
    PLUS=15
    MINUS=16
    MULT=17
    DIV=18
    MOD=19
    POW=20
    EQ=21
    NEQ=22
    LT=23
    GT=24
    LTE=25
    GTE=26
    AND=27
    OR=28
    NOT=29
    BITAND=30
    BITOR=31
    LPAREN=32
    RPAREN=33
    LBRACE=34
    RBRACE=35
    LBRACKET=36
    RBRACKET=37
    COLON=38
    SEMICOLON=39
    COMMA=40
    IDENTIFIER=41
    NUMBER=42
    STRING=43
    WS=44
    COMMENT=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PythonParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.StatementContext)
            else:
                return self.getTypedRuleContext(PythonParser.StatementContext,i)


        def getRuleIndex(self):
            return PythonParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = PythonParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 15466177248874) != 0):
                self.state = 40
                self.statement()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
            self.match(PythonParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentStatement(self):
            return self.getTypedRuleContext(PythonParser.AssignmentStatementContext,0)


        def printStatement(self):
            return self.getTypedRuleContext(PythonParser.PrintStatementContext,0)


        def inputStatement(self):
            return self.getTypedRuleContext(PythonParser.InputStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(PythonParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(PythonParser.WhileStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(PythonParser.ForStatementContext,0)


        def expressionStatement(self):
            return self.getTypedRuleContext(PythonParser.ExpressionStatementContext,0)


        def doWhileStatement(self):
            return self.getTypedRuleContext(PythonParser.DoWhileStatementContext,0)


        def breakStatement(self):
            return self.getTypedRuleContext(PythonParser.BreakStatementContext,0)


        def continueStatement(self):
            return self.getTypedRuleContext(PythonParser.ContinueStatementContext,0)


        def getRuleIndex(self):
            return PythonParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = PythonParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.assignmentStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 49
                self.printStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 50
                self.inputStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 51
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 52
                self.whileStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 53
                self.forStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 54
                self.expressionStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 55
                self.doWhileStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 56
                self.breakStatement()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 57
                self.continueStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(PythonParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(PythonParser.ASSIGN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)


        def LBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.LBRACKET)
            else:
                return self.getToken(PythonParser.LBRACKET, i)

        def RBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.RBRACKET)
            else:
                return self.getToken(PythonParser.RBRACKET, i)

        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_assignmentStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentStatement" ):
                listener.enterAssignmentStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentStatement" ):
                listener.exitAssignmentStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentStatement" ):
                return visitor.visitAssignmentStatement(self)
            else:
                return visitor.visitChildren(self)




    def assignmentStatement(self):

        localctx = PythonParser.AssignmentStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assignmentStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(PythonParser.IDENTIFIER)
            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 61
                self.match(PythonParser.LBRACKET)
                self.state = 62
                self.expression(0)
                self.state = 63
                self.match(PythonParser.RBRACKET)
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 70
            self.match(PythonParser.ASSIGN)
            self.state = 71
            self.expression(0)
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 72
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(PythonParser.PRINT, 0)

        def LPAREN(self):
            return self.getToken(PythonParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)


        def RPAREN(self):
            return self.getToken(PythonParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.COMMA)
            else:
                return self.getToken(PythonParser.COMMA, i)

        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_printStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintStatement" ):
                listener.enterPrintStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintStatement" ):
                listener.exitPrintStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStatement" ):
                return visitor.visitPrintStatement(self)
            else:
                return visitor.visitChildren(self)




    def printStatement(self):

        localctx = PythonParser.PrintStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_printStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(PythonParser.PRINT)
            self.state = 76
            self.match(PythonParser.LPAREN)
            self.state = 77
            self.expression(0)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 78
                self.match(PythonParser.COMMA)
                self.state = 79
                self.expression(0)
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 85
            self.match(PythonParser.RPAREN)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 86
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InputStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(PythonParser.IDENTIFIER, 0)

        def ASSIGN(self):
            return self.getToken(PythonParser.ASSIGN, 0)

        def INPUT(self):
            return self.getToken(PythonParser.INPUT, 0)

        def LPAREN(self):
            return self.getToken(PythonParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PythonParser.RPAREN, 0)

        def STRING(self):
            return self.getToken(PythonParser.STRING, 0)

        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_inputStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInputStatement" ):
                listener.enterInputStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInputStatement" ):
                listener.exitInputStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInputStatement" ):
                return visitor.visitInputStatement(self)
            else:
                return visitor.visitChildren(self)




    def inputStatement(self):

        localctx = PythonParser.InputStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_inputStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(PythonParser.IDENTIFIER)
            self.state = 90
            self.match(PythonParser.ASSIGN)
            self.state = 91
            self.match(PythonParser.INPUT)
            self.state = 92
            self.match(PythonParser.LPAREN)
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 93
                self.match(PythonParser.STRING)


            self.state = 96
            self.match(PythonParser.RPAREN)
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 97
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(PythonParser.IF, 0)

        def expression(self):
            return self.getTypedRuleContext(PythonParser.ExpressionContext,0)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.COLON)
            else:
                return self.getToken(PythonParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.BlockContext)
            else:
                return self.getTypedRuleContext(PythonParser.BlockContext,i)


        def ELSE(self):
            return self.getToken(PythonParser.ELSE, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = PythonParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(PythonParser.IF)
            self.state = 101
            self.expression(0)
            self.state = 102
            self.match(PythonParser.COLON)
            self.state = 103
            self.block()
            self.state = 107
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 104
                self.match(PythonParser.ELSE)
                self.state = 105
                self.match(PythonParser.COLON)
                self.state = 106
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(PythonParser.WHILE, 0)

        def expression(self):
            return self.getTypedRuleContext(PythonParser.ExpressionContext,0)


        def COLON(self):
            return self.getToken(PythonParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PythonParser.BlockContext,0)


        def getRuleIndex(self):
            return PythonParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = PythonParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.match(PythonParser.WHILE)
            self.state = 110
            self.expression(0)
            self.state = 111
            self.match(PythonParser.COLON)
            self.state = 112
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(PythonParser.FOR, 0)

        def IDENTIFIER(self):
            return self.getToken(PythonParser.IDENTIFIER, 0)

        def IN(self):
            return self.getToken(PythonParser.IN, 0)

        def RANGE(self):
            return self.getToken(PythonParser.RANGE, 0)

        def LPAREN(self):
            return self.getToken(PythonParser.LPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)


        def RPAREN(self):
            return self.getToken(PythonParser.RPAREN, 0)

        def COLON(self):
            return self.getToken(PythonParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PythonParser.BlockContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.COMMA)
            else:
                return self.getToken(PythonParser.COMMA, i)

        def getRuleIndex(self):
            return PythonParser.RULE_forStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = PythonParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(PythonParser.FOR)
            self.state = 115
            self.match(PythonParser.IDENTIFIER)
            self.state = 116
            self.match(PythonParser.IN)
            self.state = 117
            self.match(PythonParser.RANGE)
            self.state = 118
            self.match(PythonParser.LPAREN)
            self.state = 119
            self.expression(0)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==40:
                self.state = 120
                self.match(PythonParser.COMMA)
                self.state = 121
                self.expression(0)
                self.state = 124
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==40:
                    self.state = 122
                    self.match(PythonParser.COMMA)
                    self.state = 123
                    self.expression(0)




            self.state = 128
            self.match(PythonParser.RPAREN)
            self.state = 129
            self.match(PythonParser.COLON)
            self.state = 130
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoWhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(PythonParser.DO, 0)

        def COLON(self):
            return self.getToken(PythonParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PythonParser.BlockContext,0)


        def WHILE(self):
            return self.getToken(PythonParser.WHILE, 0)

        def expression(self):
            return self.getTypedRuleContext(PythonParser.ExpressionContext,0)


        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_doWhileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoWhileStatement" ):
                listener.enterDoWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoWhileStatement" ):
                listener.exitDoWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhileStatement" ):
                return visitor.visitDoWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def doWhileStatement(self):

        localctx = PythonParser.DoWhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_doWhileStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.match(PythonParser.DO)
            self.state = 133
            self.match(PythonParser.COLON)
            self.state = 134
            self.block()
            self.state = 135
            self.match(PythonParser.WHILE)
            self.state = 136
            self.expression(0)
            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 137
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(PythonParser.BREAK, 0)

        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_breakStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStatement" ):
                listener.enterBreakStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStatement" ):
                listener.exitBreakStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)




    def breakStatement(self):

        localctx = PythonParser.BreakStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_breakStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(PythonParser.BREAK)
            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 141
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(PythonParser.CONTINUE, 0)

        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_continueStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStatement" ):
                listener.enterContinueStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStatement" ):
                listener.exitContinueStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)




    def continueStatement(self):

        localctx = PythonParser.ContinueStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_continueStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.match(PythonParser.CONTINUE)
            self.state = 146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 145
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(PythonParser.ExpressionContext,0)


        def SEMICOLON(self):
            return self.getToken(PythonParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_expressionStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionStatement" ):
                listener.enterExpressionStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionStatement" ):
                listener.exitExpressionStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionStatement" ):
                return visitor.visitExpressionStatement(self)
            else:
                return visitor.visitChildren(self)




    def expressionStatement(self):

        localctx = PythonParser.ExpressionStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_expressionStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.expression(0)
            self.state = 150
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 149
                self.match(PythonParser.SEMICOLON)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(PythonParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(PythonParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.StatementContext)
            else:
                return self.getTypedRuleContext(PythonParser.StatementContext,i)


        def getRuleIndex(self):
            return PythonParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = PythonParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.state = 161
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 152
                self.match(PythonParser.LBRACE)
                self.state = 156
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 15466177248874) != 0):
                    self.state = 153
                    self.statement()
                    self.state = 158
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 159
                self.match(PythonParser.RBRACE)
                pass
            elif token in [1, 3, 5, 6, 9, 10, 11, 12, 13, 32, 36, 41, 42, 43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 160
                self.statement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PythonParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ParentesesContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(PythonParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(PythonParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(PythonParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenteses" ):
                listener.enterParenteses(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenteses" ):
                listener.exitParenteses(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenteses" ):
                return visitor.visitParenteses(self)
            else:
                return visitor.visitChildren(self)


    class VariableContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(PythonParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def comparison_op(self):
            return self.getTypedRuleContext(PythonParser.Comparison_opContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)


    class MulDivContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def mul_div(self):
            return self.getTypedRuleContext(PythonParser.Mul_divContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDiv" ):
                listener.enterMulDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDiv" ):
                listener.exitMulDiv(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDiv" ):
                return visitor.visitMulDiv(self)
            else:
                return visitor.visitChildren(self)


    class AddSubContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def add_sub(self):
            return self.getTypedRuleContext(PythonParser.Add_subContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSub" ):
                listener.enterAddSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSub" ):
                listener.exitAddSub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSub" ):
                return visitor.visitAddSub(self)
            else:
                return visitor.visitChildren(self)


    class StringContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(PythonParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class ArrayLiteralContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACKET(self):
            return self.getToken(PythonParser.LBRACKET, 0)
        def RBRACKET(self):
            return self.getToken(PythonParser.RBRACKET, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.COMMA)
            else:
                return self.getToken(PythonParser.COMMA, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayLiteral" ):
                listener.enterArrayLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayLiteral" ):
                listener.exitArrayLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayLiteral" ):
                return visitor.visitArrayLiteral(self)
            else:
                return visitor.visitChildren(self)


    class LogicalContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def logical_op(self):
            return self.getTypedRuleContext(PythonParser.Logical_opContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogical" ):
                listener.enterLogical(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogical" ):
                listener.exitLogical(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)


    class ArrayAccessContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(PythonParser.IDENTIFIER, 0)
        def LBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.LBRACKET)
            else:
                return self.getToken(PythonParser.LBRACKET, i)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def RBRACKET(self, i:int=None):
            if i is None:
                return self.getTokens(PythonParser.RBRACKET)
            else:
                return self.getToken(PythonParser.RBRACKET, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayAccess" ):
                listener.enterArrayAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayAccess" ):
                listener.exitArrayAccess(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayAccess" ):
                return visitor.visitArrayAccess(self)
            else:
                return visitor.visitChildren(self)


    class NumberContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(PythonParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)


    class BoolFalseContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(PythonParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolFalse" ):
                listener.enterBoolFalse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolFalse" ):
                listener.exitBoolFalse(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolFalse" ):
                return visitor.visitBoolFalse(self)
            else:
                return visitor.visitChildren(self)


    class BitwiseContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def bitwise_and_or(self):
            return self.getTypedRuleContext(PythonParser.Bitwise_and_orContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBitwise" ):
                listener.enterBitwise(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBitwise" ):
                listener.exitBitwise(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitwise" ):
                return visitor.visitBitwise(self)
            else:
                return visitor.visitChildren(self)


    class PowContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PythonParser.ExpressionContext,i)

        def pow_op(self):
            return self.getTypedRuleContext(PythonParser.Pow_opContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPow" ):
                listener.enterPow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPow" ):
                listener.exitPow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPow" ):
                return visitor.visitPow(self)
            else:
                return visitor.visitChildren(self)


    class BoolTrueContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PythonParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(PythonParser.TRUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolTrue" ):
                listener.enterBoolTrue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolTrue" ):
                listener.exitBoolTrue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolTrue" ):
                return visitor.visitBoolTrue(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PythonParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 26
        self.enterRecursionRule(localctx, 26, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                localctx = PythonParser.ParentesesContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 164
                self.match(PythonParser.LPAREN)
                self.state = 165
                self.expression(0)
                self.state = 166
                self.match(PythonParser.RPAREN)
                pass

            elif la_ == 2:
                localctx = PythonParser.ArrayAccessContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 168
                self.match(PythonParser.IDENTIFIER)
                self.state = 173 
                self._errHandler.sync(self)
                _alt = 1
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 169
                        self.match(PythonParser.LBRACKET)
                        self.state = 170
                        self.expression(0)
                        self.state = 171
                        self.match(PythonParser.RBRACKET)

                    else:
                        raise NoViableAltException(self)
                    self.state = 175 
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

                pass

            elif la_ == 3:
                localctx = PythonParser.ArrayLiteralContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 177
                self.match(PythonParser.LBRACKET)
                self.state = 186
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 15466177245184) != 0):
                    self.state = 178
                    self.expression(0)
                    self.state = 183
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==40:
                        self.state = 179
                        self.match(PythonParser.COMMA)
                        self.state = 180
                        self.expression(0)
                        self.state = 185
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 188
                self.match(PythonParser.RBRACKET)
                pass

            elif la_ == 4:
                localctx = PythonParser.VariableContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 189
                self.match(PythonParser.IDENTIFIER)
                pass

            elif la_ == 5:
                localctx = PythonParser.NumberContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 190
                self.match(PythonParser.NUMBER)
                pass

            elif la_ == 6:
                localctx = PythonParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 191
                self.match(PythonParser.STRING)
                pass

            elif la_ == 7:
                localctx = PythonParser.BoolTrueContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 192
                self.match(PythonParser.TRUE)
                pass

            elif la_ == 8:
                localctx = PythonParser.BoolFalseContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 193
                self.match(PythonParser.FALSE)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 222
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,22,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 220
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
                    if la_ == 1:
                        localctx = PythonParser.PowContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 196
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 197
                        self.pow_op()
                        self.state = 198
                        self.expression(15)
                        pass

                    elif la_ == 2:
                        localctx = PythonParser.MulDivContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 200
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 201
                        self.mul_div()
                        self.state = 202
                        self.expression(14)
                        pass

                    elif la_ == 3:
                        localctx = PythonParser.AddSubContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 204
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 205
                        self.add_sub()
                        self.state = 206
                        self.expression(13)
                        pass

                    elif la_ == 4:
                        localctx = PythonParser.ComparisonContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 208
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 209
                        self.comparison_op()
                        self.state = 210
                        self.expression(12)
                        pass

                    elif la_ == 5:
                        localctx = PythonParser.BitwiseContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 212
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 213
                        self.bitwise_and_or()
                        self.state = 214
                        self.expression(11)
                        pass

                    elif la_ == 6:
                        localctx = PythonParser.LogicalContext(self, PythonParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 216
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 217
                        self.logical_op()
                        self.state = 218
                        self.expression(10)
                        pass

             
                self.state = 224
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,22,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Add_subContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(PythonParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(PythonParser.MINUS, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_add_sub

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd_sub" ):
                listener.enterAdd_sub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd_sub" ):
                listener.exitAdd_sub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdd_sub" ):
                return visitor.visitAdd_sub(self)
            else:
                return visitor.visitChildren(self)




    def add_sub(self):

        localctx = PythonParser.Add_subContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_add_sub)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 225
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mul_divContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MULT(self):
            return self.getToken(PythonParser.MULT, 0)

        def DIV(self):
            return self.getToken(PythonParser.DIV, 0)

        def MOD(self):
            return self.getToken(PythonParser.MOD, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_mul_div

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMul_div" ):
                listener.enterMul_div(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMul_div" ):
                listener.exitMul_div(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMul_div" ):
                return visitor.visitMul_div(self)
            else:
                return visitor.visitChildren(self)




    def mul_div(self):

        localctx = PythonParser.Mul_divContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_mul_div)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 917504) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pow_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POW(self):
            return self.getToken(PythonParser.POW, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_pow_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPow_op" ):
                listener.enterPow_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPow_op" ):
                listener.exitPow_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPow_op" ):
                return visitor.visitPow_op(self)
            else:
                return visitor.visitChildren(self)




    def pow_op(self):

        localctx = PythonParser.Pow_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_pow_op)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.match(PythonParser.POW)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Comparison_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(PythonParser.EQ, 0)

        def NEQ(self):
            return self.getToken(PythonParser.NEQ, 0)

        def LT(self):
            return self.getToken(PythonParser.LT, 0)

        def GT(self):
            return self.getToken(PythonParser.GT, 0)

        def LTE(self):
            return self.getToken(PythonParser.LTE, 0)

        def GTE(self):
            return self.getToken(PythonParser.GTE, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_comparison_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison_op" ):
                listener.enterComparison_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison_op" ):
                listener.exitComparison_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison_op" ):
                return visitor.visitComparison_op(self)
            else:
                return visitor.visitChildren(self)




    def comparison_op(self):

        localctx = PythonParser.Comparison_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_comparison_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 132120576) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Logical_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(PythonParser.AND, 0)

        def OR(self):
            return self.getToken(PythonParser.OR, 0)

        def NOT(self):
            return self.getToken(PythonParser.NOT, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_logical_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogical_op" ):
                listener.enterLogical_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogical_op" ):
                listener.exitLogical_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical_op" ):
                return visitor.visitLogical_op(self)
            else:
                return visitor.visitChildren(self)




    def logical_op(self):

        localctx = PythonParser.Logical_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_logical_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Bitwise_and_orContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BITAND(self):
            return self.getToken(PythonParser.BITAND, 0)

        def BITOR(self):
            return self.getToken(PythonParser.BITOR, 0)

        def getRuleIndex(self):
            return PythonParser.RULE_bitwise_and_or

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBitwise_and_or" ):
                listener.enterBitwise_and_or(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBitwise_and_or" ):
                listener.exitBitwise_and_or(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitwise_and_or" ):
                return visitor.visitBitwise_and_or(self)
            else:
                return visitor.visitChildren(self)




    def bitwise_and_or(self):

        localctx = PythonParser.Bitwise_and_orContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_bitwise_and_or)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 235
            _la = self._input.LA(1)
            if not(_la==30 or _la==31):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[13] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 9)
         




