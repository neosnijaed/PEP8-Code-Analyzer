class PEP8Error(Exception):
    """Create PEP8Error object."""

    def __init__(self, file_path: str, line_num: int, issue_code: str, code_message: str):
        """
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            issue_type - a string with the issue type according to PEP8,
            issue_code - a string with the issue code according to PEP8,
            code_message - a string with the error message.
        """
        self.file_path = file_path
        self.line_num = line_num
        self.issue_type = 'S'
        self.issue_code = issue_code
        self.code_message = code_message

    def __str__(self):
        """Return string with full PEP8 error message."""
        return f'{self.file_path}: Line {self.line_num}: {self.issue_type}{self.issue_code} {self.code_message}'


class PEP8LineLimitError(PEP8Error):
    """Create PEP8LineLimitError object."""

    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '001', 'Too Long')
        """
        Initialize PEP8LineLimitError object.
        Initialize PEP8Error object.
        
        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8IndentationError(PEP8Error):
    """Create PEP8IndentationError object."""

    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '002', 'Indentation is not a multiple of four')
        """
        Initialize PEP8IndentationError object.
        Initialize PEP8Error object.
        
        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8SemicolonError(PEP8Error):
    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '003', 'Unnecessary semicolon')
        """
        Initialize PEP8SemicolonError object.
        Initialize PEP8Error object.
        
        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8InlineCommentSpaceError(PEP8Error):
    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '004',
                         'At least two spaces required before inline comments')
        """
        Initialize PEP8InlineCommentSpaceError object.
        Initialize PEP8Error object.
        
        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8TodoFoundError(PEP8Error):
    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '005', 'TODO found')
        """
        Initialize PEP8TodoFoundError object.
        Initialize PEP8Error object.
        
        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8TwoBlackLinesError(PEP8Error):
    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '006',
                         'More than two black lines used before this line')
        """
        Initialize PEP8TwoBlackLinesError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line
        """


class PEP8ConstructionNameSpaceError(PEP8Error):
    def __init__(self, file_path: str, line_num: int, construction_name: str):
        super().__init__(file_path, line_num, '007',
                         f'Too many spaces after \'{construction_name}\'')
        """
        Initialize PEP8ConstructionNameSpaceError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            construction_name - a string with the construction name (def, class)
        """


class PEP8ClassNameCamelCaseError(PEP8Error):
    def __init__(self, file_path: str, line_num: int, class_name: str):
        super().__init__(file_path, line_num, '008',
                         f'Class name \'{class_name}\' should use CamelCase')
        """
        Initialize PEP8ClassNameCamelCaseError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            class_name - a string with the class name
        """


class PEP8FunctionNameSnakeCaseError(PEP8Error):
    def __init__(self, file_path: str, line_num: int, func_name: str):
        super().__init__(file_path, line_num, '009',
                         f'Function name \'{func_name}\' should use snake_case')
        """
        Initialize PEP8FunctionNameSnakeCaseError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            func_name - a string with the function name
        """


class PEP8FunctionArgumentNameSnakeCaseError(PEP8Error):
    def __init__(self, file_path: str, line_num: int, arg_name: str):
        super().__init__(file_path, line_num, '010',
                         f'Argument name \'{arg_name}\' should be snake_case')
        """
        Initialize PEP8FunctionArgumentNameSnakeCaseError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            arg_name - a string with the argument name
        """


class PEP8FunctionVariableNameSnakeCaseError(PEP8Error):
    def __init__(self, file_path: str, line_num: int, var_name: str):
        super().__init__(file_path, line_num, '011',
                         f'Variable \'{var_name}\' in function should be snake_case')
        """
        Initialize PEP8FunctionVariableNameSnakeCaseError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
            var_name = a string with the local variable name
        """


class PEP8FunctionDefaultArgumentMutableError(PEP8Error):
    def __init__(self, file_path: str, line_num: int):
        super().__init__(file_path, line_num, '012',
                         f'Default argument value is mutable')
        """
        Initialize PEP8FunctionDefaultArgumentMutableError object.
        Initialize PEP8Error object.

        Parameters:
            file_path - a string with the path to the file,
            line_num - a string with the line number of the code line,
        """
