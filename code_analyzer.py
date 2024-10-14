import argparse
import ast
import os

from code_analyzer_classes import (CodeAnalyzer, FunctionNameAnalyzer, FunctionArgumentsAnalyzer,
                                   FunctionVariableNameAnalyser, ClassNameAnalyzer)


def get_command_line_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    return:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_or_file', help='Path of directory or file')
    return parser.parse_args()


def get_file_paths(dir_or_file: str) -> list:
    """Search for a file or files in a directory.
    args:
        dir_or_file - file or directory name
    return:
        list of a file name(s)
    """
    file_paths = []
    if os.path.isfile(dir_or_file) and dir_or_file.endswith('.py'):
        return [dir_or_file]
    else:
        for root, dirs, files in os.walk(dir_or_file, topdown=False):
            for name in dirs:
                if name.endswith('.py'):
                    file_paths.append(os.path.join(root, name))
            for name in files:
                if name.endswith('.py'):
                    file_paths.append(os.path.join(root, name))
        return sorted(file_paths)


def get_tree_from_file_content(file_path: str) -> ast:
    """Read file in file path, parse file content into AST and return the AST tree."""
    with open(file_path, 'r') as file:
        return ast.parse(file.read())


def main():
    """Analyze codes in files and print out PEP8 errors."""
    args = get_command_line_arguments()
    file_paths = get_file_paths(args.dir_or_file)
    for file_path in file_paths:
        code_analyzer = CodeAnalyzer(file_path)
        code_analyzer.get_code_lines_from_file(file_path)
        generate_code_line = (line for line in code_analyzer.code_lines)
        for line_num, line in enumerate(generate_code_line, start=1):
            code_analyzer.check_length_code_lines(line_num, line)
            code_analyzer.check_indentation(line_num, line)
            code_analyzer.check_semicolon(line_num, line)
            code_analyzer.check_inline_comments_space(line_num, line)
            code_analyzer.check_todos(line_num, line)
            code_analyzer.check_blank_lines(line_num, line)
            code_analyzer.check_construction_name_spacing(line_num, line)
        tree = get_tree_from_file_content(file_path)
        ClassNameAnalyzer(file_path).visit(tree)
        FunctionNameAnalyzer(file_path).visit(tree)
        FunctionArgumentsAnalyzer(file_path).visit(tree)
        FunctionVariableNameAnalyser(file_path).visit(tree)


if __name__ == '__main__':
    main()
