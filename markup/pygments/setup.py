from setuptools import setup

setup(
    name='pyre-journal-lexer',
    version='0.1.0',
    description='Pygments lexer and style for Pyre journal channels',
    py_modules=['pyrejournal_lexer', 'pyrejournal_style'],
    install_requires=['Pygments>=2.0'],
    entry_points={
        'pygments.lexers': [
            'pyre_journal = pyrejournal_lexer:PyreJournalLexer',
        ],
        'pygments.styles': [
            'pyre_journal_style = pyrejournal_style:PyreJournalStyle',
        ],
    },
)
