#!/usr/bin/python

"""
Generates Java code for Lox expressions and statement classes and subclasses. I
wrote this in Python instead of Java because why not.

You can run this script by entering `./tools/generate_ast.py <output-directory>`
in your terminal :3
"""

import sys
import os
from typing import List


def main(argv: str):
    if len(argv) != 2:
        print(f'Usage: {argv[0]} <output-directory>')
        sys.exit(1);

    output_path = argv[1]

    define_ast(output_path, 'Expr', [
        'Assign   : Token name, Expr value',
        'Binary   : Expr left, Token operator, Expr right',
        'Call     : Expr callee, Token paren, List<Expr> arguments',
        'Get      : Expr object, Token name',
        'Grouping : Expr expression',
        'Literal  : Object value',
        'Logical  : Expr left, Token operator, Expr right',
        'Set      : Expr object, Token name, Expr value',
        'Super    : Token keyword, Token method',
        'This     : Token keyword',
        'Unary    : Token operator, Expr right',
        'Variable : Token name'
    ])

    define_ast(output_path, 'Stmt', [
        'Block      : List<Stmt> statements',
        'Class      : Token name, Expr.Variable superclass, List<Stmt.Function> methods',
        'Expression : Expr expression',
        'Function   : Token name, List<Token> params, List<Stmt> body',
        'If         : Expr condition, Stmt thenBranch, Stmt elseBranch',
        'Print      : Expr expression',
        'Return     : Token keyword, Expr value',
        'Var        : Token name, Expr initializer',
        'While      : Expr condition, Stmt body'
    ])


def define_ast(output_dir: str, base_name: str, types: List[str]):
    with open(f'{output_dir}/{base_name}.java', 'w+') as file:
        file.write(
            'package com.craftinginterpreters.lox;\n'
            '\n'
            'import java.util.List;\n'
            '\n'
            f'abstract class {base_name} {{\n')

        file.write(define_visitor(base_name, types))

        for i, typename in enumerate(types):
            class_name = typename.split(':')[0].strip()
            fields = typename.split(':')[1].strip()
            file.write(define_types(base_name, class_name, fields, i == len(types)-1))

        file.write(
            '    abstract <R> R accept(Visitor<R> visitor);\n'
            '}\n'
        )


def define_visitor(base_name: str, types: str):
    source = '    interface Visitor<R> {\n'
    types = [t.split(':')[0].strip() for t in types]
    
    for typename in types:
        source += f'        R visit{typename}{base_name} ({typename} {base_name.lower()});\n'
    
    source += '    }\n\n'
    return source


def define_types(base_name: str, class_name: str, fields: List[str], last: bool) -> str:
    source = (
        f'    static class {class_name} extends {base_name} {{\n'
        f'        {class_name}({fields}) {{\n'
    )

    fields = [f.strip() for f in fields.split(',')]
    field_names = [f.split(' ')[1] for f in fields]
    for field in field_names:
        source += (
            f'            this.{field} = {field};\n'
        )

    source += (
        '        }\n\n'
        '        @Override\n'
        '        <R> R accept(Visitor<R> visitor) {\n'
        f'            return visitor.visit{class_name}{base_name}(this);\n'
        '        }\n\n'
    )

    for field in fields:
        source += f'        final {field};\n'

    source += '    }\n'
    if not last:
        source += '\n'

    return source


if __name__ == '__main__':
    main(sys.argv)