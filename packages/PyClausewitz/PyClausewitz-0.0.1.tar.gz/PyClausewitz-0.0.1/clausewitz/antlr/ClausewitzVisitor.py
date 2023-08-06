# Generated from C:/Users/LokiSharp/PycharmProjects/hoi4py/antlr\Clausewitz.g4 by ANTLR 4.7.2
from antlr4 import *

from .ClausewitzParser import ClausewitzParser


# This class defines a complete generic visitor for a parse tree produced by ClausewitzParser.

class ClausewitzVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ClausewitzParser#config.
    def visitConfig(self, ctx: ClausewitzParser.ConfigContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#assignment.
    def visitAssignment(self, ctx: ClausewitzParser.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#field.
    def visitField(self, ctx: ClausewitzParser.FieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#value.
    def visitValue(self, ctx: ClausewitzParser.ValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#symbol.
    def visitSymbol(self, ctx: ClausewitzParser.SymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#string.
    def visitString(self, ctx: ClausewitzParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#integer.
    def visitInteger(self, ctx: ClausewitzParser.IntegerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#real.
    def visitReal(self, ctx: ClausewitzParser.RealContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#date.
    def visitDate(self, ctx: ClausewitzParser.DateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#percent.
    def visitPercent(self, ctx: ClausewitzParser.PercentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#map.
    def visitMap(self, ctx: ClausewitzParser.MapContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ClausewitzParser#array.
    def visitArray(self, ctx: ClausewitzParser.ArrayContext):
        return self.visitChildren(ctx)


del ClausewitzParser
