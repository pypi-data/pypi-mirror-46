# -*- coding: utf-8 -*-
"""
"Token.Keyword"
"Token.Keyword.Constant"
"Token.Keyword.Declaration"
"Token.Keyword.Namespace"
"Token.Keyword.Pseudo"
"Token.Keyword.Reserved"
"Token.Keyword.Type"

"Token.Operator.Word"

"Token.Name.Class"
"Token.Name.Exception"
"Token.Name.Function"
"Token.Name.Namespace"
"Token.Name.Builtin"
"Token.Name.Builtin.Pseudo"

"Token.Comment"
"Token.Comment.Single"
"Token.Comment.Hashbang"

"Token.Literal.String"
"Token.Literal.String.Double"
"Token.Literal.String.Single"
"Token.Literal.String.Doc"


"Bracket.Token.Punctuation.Bracket1", foreground="#ffffff", background="#000000")
"Bracket.Token.Punctuation.Bracket2", foreground="#ffffff", background="#555555")
"Bracket.Token.Punctuation.Bracket3", foreground="#000000", background="#999999")
"Bracket.Token.Punctuation.Bracket4", foreground="#000000", background="#cccccc")
"Bracket.Token.Punctuation.Bracket5", foreground="#ffffff", background="#000000")
"Bracket.Token.Punctuation.Bracket6", foreground="#ffffff", background="#555555")
"Bracket.Token.Punctuation.Bracket7", foreground="#000000", background="#999999")
"Bracket.Token.Punctuation.Bracket8", foreground="#000000", background="#cccccc")
"""

class Token(object):
    foreground = None
    background = None
    tokens = []
    def __init__(self):
        pass
    
    def configure_tags(self,text_instance):
        pass
        


class CommentToken(Token):
    """ Characters representing a comment in the code. """
    foreground = '#007F00'
    background = None
    tokens = ["Token.Comment","Token.Comment.Single","Token.Comment.Hashbang"]
    

class TodoCommentToken(CommentToken):
    """ Characters representing a comment in the code. """
    defaultStyle = 'fore:#E00,italic'

class StringToken(Token):
    """ Characters representing a textual string in the code. """'
    foreground = '#7F007F'
    background = None
    tokens = ["Token.Literal.String",
              "Token.Literal.String.Double", 
              "Token.Literal.String.Single",
              "Token.Literal.String.Doc"]

class UnterminatedStringToken(StringToken):
    """ Characters belonging to an unterminated string. """
    pass

class TextToken(Token):
    """ Anything that is not a string or comment. """
    foreground = '#000'
    background = None
    tokens = ["Token.Text"]

class WhitespaceToken(TextToken):
    """ Anything that is not a string or comment. """
    tokens = ["Token.Text.Whitespace.Leading0",
              "Token.Text.Whitespace.Leading1",
              "Token.Text.Whitespace.Leading2",
              "Token.Text.Whitespace.Newline",
              "Token.Text.Whitespace.Trailing"]

class IdentifierToken(TextToken):
    """ Characters representing normal text (i.e. words). """


class NonIdentifierToken(TextToken):
    """ Not a word (operators, whitespace, etc.). """


class KeywordToken(IdentifierToken):
    """ A keyword is a word with a special meaning to the language. """
    foreground = '#00007F'
    background = None
    tokens = []

class BuiltinsToken(IdentifierToken):
    """ Characters representing a builtins in the code. """
    foreground = '#00007F'
    background = None
    tokens = []

class InstanceToken(IdentifierToken):
    """ Characters representing a instance in the code. """
    foreground = '#00007F'
    background = None
    tokens = []

class NumberToken(IdentifierToken):
    """ Characters represening a number. """
    foreground = '#007F7F'
    background = None
    tokens = []

class FunctionNameToken(IdentifierToken):
    """ Characters represening the name of a function. """
    foreground = '#007F7F'
    background = None
    tokens = ["Token.Name.Function"]

class ClassNameToken(IdentifierToken):
    """ Characters represening the name of a class. """
    foreground = '#0000FF'
    background = None
    tokens = ["Token.Name.Class"]
    

class ParenthesisToken(TextToken) :
    """ Parenthesis (and square and curly brackets). """
    foreground = '#000'
    background = None
    tokens = []

class OpenParenToken(ParenthesisToken) :
    """ Opening parenthesis (and square and curly brackets). """
    foreground = '#000'
    background = None
    tokens = []

class CloseParenToken(ParenthesisToken) :
    """ Closing parenthesis (and square and curly brackets). """
    foreground = '#000'
    background = None
    tokens = []
