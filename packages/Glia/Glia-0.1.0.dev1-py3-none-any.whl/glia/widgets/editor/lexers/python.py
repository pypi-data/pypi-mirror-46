import builtins

from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QFontMetrics

from glia.widgets.editor.lexers import LexerBase


class PythonLexer(LexerBase):
    """
    Customized from QsciLexerPython to provide basic auto-completion.
    """
    def lock(self):
        """
        Sets the default properties for the Python lexer.
        """
        # Lexer Initialization
        lexer = QsciLexerPython(self.code_editor)
        lexer.setDefaultFont(self.font)
        self.code_editor.setLexer(lexer)

        # Auto Completion
        api = QsciAPIs(lexer)
        for var in dir(builtins):
            if not (var[0] == "_"):
                api.add(var)
        api.prepare()

        self.code_editor.setAutoCompletionThreshold(1)
        self.code_editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)

        # Indentation
        self.code_editor.setIndentationWidth(4)

        # Font Settings
        font_metrics = QFontMetrics(self.font)
        self.code_editor.setMinimumSize(
            int(font_metrics.width("0" * 80)),
            0
        )
