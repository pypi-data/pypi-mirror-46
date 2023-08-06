# Generated from C:/Users/LokiSharp/PycharmProjects/hoi4py/antlr\Clausewitz.g4 by ANTLR 4.7.2
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *
from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\r")
        buf.write("Q\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\7\2")
        buf.write("\34\n\2\f\2\16\2\37\13\2\3\3\3\3\3\3\3\3\3\4\3\4\3\4\5")
        buf.write("\4(\n\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5\62\n\5\3\6")
        buf.write("\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f")
        buf.write("\7\fB\n\f\f\f\16\fE\13\f\3\f\3\f\3\r\3\r\6\rK\n\r\r\r")
        buf.write("\16\rL\3\r\3\r\3\r\2\2\16\2\4\6\b\n\f\16\20\22\24\26\30")
        buf.write("\2\3\4\2\6\6\n\13\2P\2\35\3\2\2\2\4 \3\2\2\2\6\'\3\2\2")
        buf.write("\2\b\61\3\2\2\2\n\63\3\2\2\2\f\65\3\2\2\2\16\67\3\2\2")
        buf.write("\2\209\3\2\2\2\22;\3\2\2\2\24=\3\2\2\2\26?\3\2\2\2\30")
        buf.write("H\3\2\2\2\32\34\5\4\3\2\33\32\3\2\2\2\34\37\3\2\2\2\35")
        buf.write("\33\3\2\2\2\35\36\3\2\2\2\36\3\3\2\2\2\37\35\3\2\2\2 ")
        buf.write("!\5\6\4\2!\"\7\3\2\2\"#\5\b\5\2#\5\3\2\2\2$(\5\f\7\2%")
        buf.write("(\5\n\6\2&(\5\22\n\2\'$\3\2\2\2\'%\3\2\2\2\'&\3\2\2\2")
        buf.write("(\7\3\2\2\2)\62\5\16\b\2*\62\5\24\13\2+\62\5\20\t\2,\62")
        buf.write("\5\22\n\2-\62\5\f\7\2.\62\5\n\6\2/\62\5\26\f\2\60\62\5")
        buf.write("\30\r\2\61)\3\2\2\2\61*\3\2\2\2\61+\3\2\2\2\61,\3\2\2")
        buf.write("\2\61-\3\2\2\2\61.\3\2\2\2\61/\3\2\2\2\61\60\3\2\2\2\62")
        buf.write("\t\3\2\2\2\63\64\t\2\2\2\64\13\3\2\2\2\65\66\7\n\2\2\66")
        buf.write("\r\3\2\2\2\678\7\6\2\28\17\3\2\2\29:\7\b\2\2:\21\3\2\2")
        buf.write("\2;<\7\t\2\2<\23\3\2\2\2=>\7\7\2\2>\25\3\2\2\2?C\7\4\2")
        buf.write("\2@B\5\4\3\2A@\3\2\2\2BE\3\2\2\2CA\3\2\2\2CD\3\2\2\2D")
        buf.write("F\3\2\2\2EC\3\2\2\2FG\7\5\2\2G\27\3\2\2\2HJ\7\4\2\2IK")
        buf.write("\5\b\5\2JI\3\2\2\2KL\3\2\2\2LJ\3\2\2\2LM\3\2\2\2MN\3\2")
        buf.write("\2\2NO\7\5\2\2O\31\3\2\2\2\7\35\'\61CL")
        return buf.getvalue()


class ClausewitzParser(Parser):
    grammarFileName = "Clausewitz.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "<INVALID>", "'{'", "'}'"]

    symbolicNames = ["<INVALID>", "OPERATOR", "BLOCK_START", "BLOCK_END",
                     "INT", "PCT", "REAL", "DATE", "STRING", "SYMBOL",
                     "WHITESPACE", "LINE_COMMENT"]

    RULE_config = 0
    RULE_assignment = 1
    RULE_field = 2
    RULE_value = 3
    RULE_symbol = 4
    RULE_string = 5
    RULE_integer = 6
    RULE_real = 7
    RULE_date = 8
    RULE_percent = 9
    RULE_map = 10
    RULE_array = 11

    ruleNames = ["config", "assignment", "field", "value", "symbol", "string",
                 "integer", "real", "date", "percent", "map", "array"]

    EOF = Token.EOF
    OPERATOR = 1
    BLOCK_START = 2
    BLOCK_END = 3
    INT = 4
    PCT = 5
    REAL = 6
    DATE = 7
    STRING = 8
    SYMBOL = 9
    WHITESPACE = 10
    LINE_COMMENT = 11

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ConfigContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ClausewitzParser.AssignmentContext)
            else:
                return self.getTypedRuleContext(ClausewitzParser.AssignmentContext, i)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_config

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterConfig"):
                listener.enterConfig(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitConfig"):
                listener.exitConfig(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitConfig"):
                return visitor.visitConfig(self)
            else:
                return visitor.visitChildren(self)

    def config(self):

        localctx = ClausewitzParser.ConfigContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_config)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << ClausewitzParser.INT) | (1 << ClausewitzParser.DATE) | (1 << ClausewitzParser.STRING) | (
                    1 << ClausewitzParser.SYMBOL))) != 0):
                self.state = 24
                self.assignment()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AssignmentContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self):
            return self.getTypedRuleContext(ClausewitzParser.FieldContext, 0)

        def OPERATOR(self):
            return self.getToken(ClausewitzParser.OPERATOR, 0)

        def value(self):
            return self.getTypedRuleContext(ClausewitzParser.ValueContext, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_assignment

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAssignment"):
                listener.enterAssignment(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAssignment"):
                listener.exitAssignment(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAssignment"):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)

    def assignment(self):

        localctx = ClausewitzParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.field()
            self.state = 31
            self.match(ClausewitzParser.OPERATOR)
            self.state = 32
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(ClausewitzParser.StringContext, 0)

        def symbol(self):
            return self.getTypedRuleContext(ClausewitzParser.SymbolContext, 0)

        def date(self):
            return self.getTypedRuleContext(ClausewitzParser.DateContext, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_field

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterField"):
                listener.enterField(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitField"):
                listener.exitField(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitField"):
                return visitor.visitField(self)
            else:
                return visitor.visitChildren(self)

    def field(self):

        localctx = ClausewitzParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_field)
        try:
            self.state = 37
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.string()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.symbol()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 36
                self.date()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def integer(self):
            return self.getTypedRuleContext(ClausewitzParser.IntegerContext, 0)

        def percent(self):
            return self.getTypedRuleContext(ClausewitzParser.PercentContext, 0)

        def real(self):
            return self.getTypedRuleContext(ClausewitzParser.RealContext, 0)

        def date(self):
            return self.getTypedRuleContext(ClausewitzParser.DateContext, 0)

        def string(self):
            return self.getTypedRuleContext(ClausewitzParser.StringContext, 0)

        def symbol(self):
            return self.getTypedRuleContext(ClausewitzParser.SymbolContext, 0)

        def map(self):
            return self.getTypedRuleContext(ClausewitzParser.MapContext, 0)

        def array(self):
            return self.getTypedRuleContext(ClausewitzParser.ArrayContext, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_value

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterValue"):
                listener.enterValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitValue"):
                listener.exitValue(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitValue"):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)

    def value(self):

        localctx = ClausewitzParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_value)
        try:
            self.state = 47
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 2, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 39
                self.integer()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 40
                self.percent()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 41
                self.real()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 42
                self.date()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 43
                self.string()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 44
                self.symbol()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 45
                self.map()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 46
                self.array()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SymbolContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ClausewitzParser.STRING, 0)

        def INT(self):
            return self.getToken(ClausewitzParser.INT, 0)

        def SYMBOL(self):
            return self.getToken(ClausewitzParser.SYMBOL, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_symbol

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSymbol"):
                listener.enterSymbol(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSymbol"):
                listener.exitSymbol(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSymbol"):
                return visitor.visitSymbol(self)
            else:
                return visitor.visitChildren(self)

    def symbol(self):

        localctx = ClausewitzParser.SymbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_symbol)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << ClausewitzParser.INT) | (1 << ClausewitzParser.STRING) | (
                    1 << ClausewitzParser.SYMBOL))) != 0)):
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

    class StringContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ClausewitzParser.STRING, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_string

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterString"):
                listener.enterString(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitString"):
                listener.exitString(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitString"):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)

    def string(self):

        localctx = ClausewitzParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(ClausewitzParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IntegerContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ClausewitzParser.INT, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_integer

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterInteger"):
                listener.enterInteger(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitInteger"):
                listener.exitInteger(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitInteger"):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)

    def integer(self):

        localctx = ClausewitzParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(ClausewitzParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RealContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REAL(self):
            return self.getToken(ClausewitzParser.REAL, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_real

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterReal"):
                listener.enterReal(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitReal"):
                listener.exitReal(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitReal"):
                return visitor.visitReal(self)
            else:
                return visitor.visitChildren(self)

    def real(self):

        localctx = ClausewitzParser.RealContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_real)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(ClausewitzParser.REAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DateContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATE(self):
            return self.getToken(ClausewitzParser.DATE, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_date

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterDate"):
                listener.enterDate(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitDate"):
                listener.exitDate(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDate"):
                return visitor.visitDate(self)
            else:
                return visitor.visitChildren(self)

    def date(self):

        localctx = ClausewitzParser.DateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_date)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.match(ClausewitzParser.DATE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PercentContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PCT(self):
            return self.getToken(ClausewitzParser.PCT, 0)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_percent

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPercent"):
                listener.enterPercent(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPercent"):
                listener.exitPercent(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPercent"):
                return visitor.visitPercent(self)
            else:
                return visitor.visitChildren(self)

    def percent(self):

        localctx = ClausewitzParser.PercentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_percent)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(ClausewitzParser.PCT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MapContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLOCK_START(self):
            return self.getToken(ClausewitzParser.BLOCK_START, 0)

        def BLOCK_END(self):
            return self.getToken(ClausewitzParser.BLOCK_END, 0)

        def assignment(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ClausewitzParser.AssignmentContext)
            else:
                return self.getTypedRuleContext(ClausewitzParser.AssignmentContext, i)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_map

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMap"):
                listener.enterMap(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMap"):
                listener.exitMap(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMap"):
                return visitor.visitMap(self)
            else:
                return visitor.visitChildren(self)

    def map(self):

        localctx = ClausewitzParser.MapContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_map)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(ClausewitzParser.BLOCK_START)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << ClausewitzParser.INT) | (1 << ClausewitzParser.DATE) | (1 << ClausewitzParser.STRING) | (
                    1 << ClausewitzParser.SYMBOL))) != 0):
                self.state = 62
                self.assignment()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 68
            self.match(ClausewitzParser.BLOCK_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArrayContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLOCK_START(self):
            return self.getToken(ClausewitzParser.BLOCK_START, 0)

        def BLOCK_END(self):
            return self.getToken(ClausewitzParser.BLOCK_END, 0)

        def value(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ClausewitzParser.ValueContext)
            else:
                return self.getTypedRuleContext(ClausewitzParser.ValueContext, i)

        def getRuleIndex(self):
            return ClausewitzParser.RULE_array

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArray"):
                listener.enterArray(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArray"):
                listener.exitArray(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArray"):
                return visitor.visitArray(self)
            else:
                return visitor.visitChildren(self)

    def array(self):

        localctx = ClausewitzParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_array)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(ClausewitzParser.BLOCK_START)
            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 71
                self.value()
                self.state = 74
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                        (1 << ClausewitzParser.BLOCK_START) | (1 << ClausewitzParser.INT) | (
                        1 << ClausewitzParser.PCT) | (1 << ClausewitzParser.REAL) | (1 << ClausewitzParser.DATE) | (
                                1 << ClausewitzParser.STRING) | (1 << ClausewitzParser.SYMBOL))) != 0)):
                    break

            self.state = 76
            self.match(ClausewitzParser.BLOCK_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
