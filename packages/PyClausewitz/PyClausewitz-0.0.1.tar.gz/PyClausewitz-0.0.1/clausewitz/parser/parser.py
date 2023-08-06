import logging

from antlr4 import *

from clausewitz.antlr.ClausewitzLexer import ClausewitzLexer
from clausewitz.antlr.ClausewitzParser import ClausewitzParser
from clausewitz.antlr.ClausewitzVisitor import ClausewitzVisitor

logging.basicConfig(format='%(levelname)s: %(funcName)s %(message)s')


class ConfigVisitor(ClausewitzVisitor):
    # Visit a parse tree produced by ClausewitzParser#config.
    def visitConfig(self, ctx: ClausewitzParser.ConfigContext):
        logging.debug(ctx.getText())
        i = {}
        visitor = ValueVisitor()
        for x in ctx.assignment():
            i.update(x.accept(visitor))
        logging.debug(i)
        return i


class ValueVisitor(ClausewitzVisitor):

    # Visit a parse tree produced by ClausewitzParser#assignment.
    def visitAssignment(self, ctx: ClausewitzParser.AssignmentContext):
        logging.debug(ctx.getText())
        field = ctx.field().getText().strip("\"")
        value = self.visitChildren(ctx.value())
        return {field: value}

    # Visit a parse tree produced by ClausewitzParser#field.
    def visitField(self, ctx: ClausewitzParser.FieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#value.
    def visitValue(self, ctx: ClausewitzParser.ValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#symbol.
    def visitSymbol(self, ctx: ClausewitzParser.SymbolContext):
        logging.debug(ctx.getText())
        switcher = {
            "yes": True,
            "no": False,
        }
        str(ctx.getText())
        return switcher.get(str(ctx.getText()), str(ctx.getText()))

    # Visit a parse tree produced by ClausewitzParser#string.
    def visitString(self, ctx: ClausewitzParser.StringContext):
        logging.debug(ctx.getText())
        return str(ctx.getText()).strip("\"")

    # Visit a parse tree produced by ClausewitzParser#integer.
    def visitInteger(self, ctx: ClausewitzParser.IntegerContext):
        logging.debug(ctx.getText())
        return int(ctx.getText())

    # Visit a parse tree produced by ClausewitzParser#real.
    def visitReal(self, ctx: ClausewitzParser.RealContext):
        logging.debug(ctx.getText())
        return float(ctx.getText())

    # Visit a parse tree produced by ClausewitzParser#date.
    def visitDate(self, ctx: ClausewitzParser.DateContext):
        logging.debug(ctx.getText())
        return str(ctx.getText()).strip("\"")

    # Visit a parse tree produced by ClausewitzParser#percent.
    def visitPercent(self, ctx: ClausewitzParser.PercentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#map.
    def visitMap(self, ctx: ClausewitzParser.MapContext):
        logging.debug(ctx.getText())
        i = {}
        for x in ctx.assignment():
            i.update(x.accept(self))
        logging.debug(i)
        return i

    # Visit a parse tree produced by ClausewitzParser#array.
    def visitArray(self, ctx: ClausewitzParser.ArrayContext):
        logging.debug(ctx.getText())
        i = []
        for x in ctx.value():
            i.append(x.accept(self))
        logging.debug(i)
        return i


def parserFile(file_path):
    input_stream = FileStream(file_path)
    lexer = ClausewitzLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ClausewitzParser(stream)
    tree = parser.config()
    return tree.accept(ConfigVisitor())


def parserString(string):
    lexer = ClausewitzLexer(InputStream(string))
    stream = CommonTokenStream(lexer)
    parser = ClausewitzParser(stream)
    tree = parser.config()
    return tree.accept(ConfigVisitor())
