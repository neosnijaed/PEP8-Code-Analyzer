import ast
import re

from PEP8_class import (PEP8LineLimitError, PEP8IndentationError, PEP8SemicolonError, PEP8InlineCommentSpaceError,
                        PEP8TodoFoundError, PEP8TwoBlackLinesError, PEP8ConstructionNameSpaceError,
                        PEP8ClassNameCamelCaseError, PEP8FunctionNameSnakeCaseError,
                        PEP8FunctionArgumentNameSnakeCaseError, PEP8FunctionVariableNameSnakeCaseError,
                        PEP8FunctionDefaultArgumentMutableError)


class CodeAnalyzer:
    """Create CodeAnalyser object."""
    code_lines = None

    def __init__(self, file_path: str):
        """
        Initialize CodeAnalyzer object.

        Parameters:
            file_path - a string with the path of the file,
            max_length_line - an integer with the maximum code line length,
            indent - an integer with the indentation of the code,
            blank_lines - an integer with the count of blank lines,
            max_blank_lines - an integer with the maximum number of blank lines
        """
        self.file_path = file_path
        self.max_length_line = 79
        self.indent = 4
        self.blank_lines = 0
        self.max_blank_lines = 2

    @staticmethod
    def get_code_lines_from_file(file_path: str):
        """Get list of lines read from a file.
        args:
            file_path - a string with the path of the file
        """
        with open(file_path, 'r') as file:
            CodeAnalyzer.code_lines = file.readlines()

    def check_length_code_lines(self, line_num: int, line: str):
        """Check code line for its length.
        If length exceeds maximum code line length, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        try:
            if len(line.strip()) > self.max_length_line:
                raise PEP8LineLimitError(self.file_path, line_num)
        except PEP8LineLimitError as err:
            print(err)

    def check_indentation(self, line_num: int, line: str):
        """Check code line for its indentation.
        If the indentation is not a multiple of 4 whitespaces, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if line[0] == ' ':
            line_indent = len(line) - len(line.lstrip())
            try:
                if line_indent % self.indent != 0:
                    raise PEP8IndentationError(self.file_path, line_num)
            except PEP8IndentationError as err:
                print(err)

    def check_semicolon(self, line_num: int, line: str):
        """Check code line for a semicolon at the end of an expression.
        If semicolon exists, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if not self.symbol_in_string(';', line) and not bool(re.match('.*#.*;.*', line)):
            try:
                if bool(re.match('.*;', line)):
                    raise PEP8SemicolonError(self.file_path, line_num)
            except PEP8SemicolonError as err:
                print(err)

    def check_inline_comments_space(self, line_num: int, line: str):
        """Check code line for an inline comment.
        If the space between the inline comment and code is less than 2 whitespaces, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if not self.symbol_in_string('#', line) and bool(re.match('.+#.*', line)):
            try:
                if not bool(re.match(r'.+\s{2,}#.*', line)):
                    raise PEP8InlineCommentSpaceError(self.file_path, line_num)
            except PEP8InlineCommentSpaceError as err:
                print(err)

    def check_todos(self, line_num: int, line: str):
        """Raise PEP8 error if a todos exist in a comment.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if (bool(re.search('.*todo.*', line, re.IGNORECASE))
                and not self.symbol_in_string('todo', line, re.IGNORECASE)):
            try:
                if bool(re.match('.*#.*todo.*', line, re.IGNORECASE)):
                    raise PEP8TodoFoundError(self.file_path, line_num)
            except PEP8TodoFoundError as err:
                print(err)

    def check_blank_lines(self, line_num: int, line: str):
        """Check for number of blank lines.
        If number of blank lines exceeds maximum number of blank lines, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if line == '\n':
            self.blank_lines += 1
            return
        try:
            if self.blank_lines > self.max_blank_lines:
                self.blank_lines = 0
                raise PEP8TwoBlackLinesError(self.file_path, line_num)
            else:
                self.blank_lines = 0
        except PEP8TwoBlackLinesError as err:
            print(err)

    def check_construction_name_spacing(self, line_num: int, line: str):
        """Check for correct spacing between construction name and class/func name.
        If it is not one whitespace between them, raise PEP8 Error.
        args:
            line_num - an integer with the line number,
            line - a string with the line content
        """
        if (line.strip().startswith('class') or line.strip().startswith('def')) and line.strip().endswith(':'):
            construction_name = line.strip().split()[0]
            if not self.symbol_in_string(construction_name, line):
                pattern = r'^class [^\s]' if construction_name.lower() == 'class' else r'^def [^\s]'
                try:
                    if not re.match(pattern, line.strip()):
                        raise PEP8ConstructionNameSpaceError(self.file_path, line_num, construction_name)
                except PEP8ConstructionNameSpaceError as err:
                    print(err)

    @staticmethod
    def symbol_in_string(symbol: str, line: str, ignore_case=0) -> bool:
        """Check if the given symbol is in a string.
        args:
            symbol - a string with the symbol,
            line - a string with the code line,
            ignore_case - re.IGNORECASE flag for case-insensitive matching
        return:
            True if the symbol is in a string, False otherwise
        """
        return (bool(re.match(f'.*".*{symbol}.*".*', line, ignore_case)) or
                bool(re.match(f".*'.*{symbol}.*'.*", line, ignore_case)) or
                bool(re.match(f'.*""".*{symbol}.*""".*', line, ignore_case)) or
                bool(re.match(f".*'''.*{symbol}.*'''.*", line, ignore_case)))


class ClassNameAnalyzer(ast.NodeVisitor):
    """Create ClassNameAnalyzer object."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    """Check camel-case for class names."""
    def visit_ClassDef(self, node: ast.ClassDef):
        try:
            if not re.match(r'^([A-Z][a-z]+)+(\(([A-Z][a-z]+)+\))?$', node.name):
                raise PEP8ClassNameCamelCaseError(self.file_path, node.lineno, node.name)
        except PEP8ClassNameCamelCaseError as err:
            print(err)


class FunctionNameAnalyzer(ast.NodeVisitor):
    """Create FunctionNameAnalyzer object."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    """Check snake-case for function names."""
    def visit_FunctionDef(self, node: ast.FunctionDef):
        try:
            if not re.match(r'^(_*[a-z\d]+)+_*$', node.name):
                raise PEP8FunctionNameSnakeCaseError(self.file_path, node.lineno, node.name)
        except PEP8FunctionNameSnakeCaseError as err:
            print(err)
        self.generic_visit(node)


class FunctionArgumentsAnalyzer(ast.NodeVisitor):
    """Create FunctionArgumentsAnalyzer object."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    """Check snake-case for function arguments and no mutable for function default arguments."""
    def visit_arguments(self, node: ast.arguments):
        for arg in node.args:
            try:
                if not re.match(r'^(_*[a-z\d]+)+_*$', arg.arg):
                    raise PEP8FunctionArgumentNameSnakeCaseError(self.file_path, arg.lineno, arg.arg)
            except PEP8FunctionArgumentNameSnakeCaseError as err:
                print(err)
        for default in node.defaults:
            try:
                if isinstance(default, ast.List) or isinstance(default, ast.Dict) or isinstance(default, ast.Set):
                    raise PEP8FunctionDefaultArgumentMutableError(self.file_path, default.lineno)
            except PEP8FunctionDefaultArgumentMutableError as err:
                print(err)
        self.generic_visit(node)


class FunctionVariableNameAnalyser(ast.NodeVisitor):
    """Create FunctionVariableNameAnalyzer object."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    """Check snake-case for local variable names inside functions."""
    def visit_FunctionDef(self, node: ast.FunctionDef):
        for assign in node.body:
            if isinstance(assign, ast.Assign):
                for target in assign.targets:
                    if isinstance(target, ast.Name):
                        try:
                            if not re.match(r'^(_*[a-z\d]+)+_*$', target.id):
                                raise PEP8FunctionVariableNameSnakeCaseError(self.file_path, target.lineno, target.id)
                        except PEP8FunctionVariableNameSnakeCaseError as err:
                            print(err)
        self.generic_visit(node)
