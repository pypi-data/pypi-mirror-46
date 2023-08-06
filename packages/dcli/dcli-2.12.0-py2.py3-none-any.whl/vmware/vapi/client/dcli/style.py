"""
module holding dcli styling related functionality
"""

from pygments.lexer import RegexLexer, using
from pygments.lexers.data import JsonLexer
from pygments.token import Text, Name, String


class DcliInputLexer(RegexLexer):
    """
    For HTML 4 and XHTML 1 markup. Nested JavaScript and CSS is highlighted
    by the appropriate lexer.
    """

    name = 'DcliInput'

    tokens = {
        'root': [
            (r'--[^\s]+', Name.Tag, 'param-val'),
            (r'\+[^\s]+', String.Doc),
            (r'[^\s]+', Text),
            (r'\s+', Text)
        ],
        'param-val': [
            (r'(?<=\').+?(?=\')', using(JsonLexer), '#pop'),
            (r'\s+', Text),
            (r'([^\s\'])', Text, '#pop')
        ]
    }
