import sys
from typing import (
    List,
    TextIO,
)

MatrixRow = List[str]
Matrix = List[MatrixRow]
ColumnStore = List[List[str]]

__SEPARATOR_PIPE = '|'


def get_matrix_from_csv(
    stream: TextIO,
    separator: str = ';',
) -> Matrix:
    """Return a matrix of values from an input stream containing csv data."""
    matrix: Matrix = []

    for line in stream:
        matrix.append([col.strip('\r\n') for col in line.split(separator)])

    return matrix


def get_matrix_from_md(stream: TextIO) -> Matrix:
    """Return a matrix of values from an input stream containing a markdown table."""
    matrix: Matrix = []

    for idx, line in enumerate(stream):
        if idx == 1:
            continue

        cols = line.split(__SEPARATOR_PIPE)
        matrix.append([col.strip(' \r\n') for col in cols][1 : len(cols) - 1])

    return matrix


def get_column_store_from_matrix(
    matrix: Matrix,
    escape: bool = False,
) -> ColumnStore:
    """Return input stream as a column-store."""
    columns: ColumnStore = []

    for row in matrix:
        if not len(columns):
            columns = [[get_escaped_string(col, escape)] for col in row]
        else:
            for idx, col in enumerate(row):
                columns[idx].append(get_escaped_string(col, escape))

    return columns


__MARKDOWN_ESCAPE_CHAR = '\\`*_{}[]()#+-.!'


def get_escaped_string(
    text: str,
    escape: bool = True,
) -> str:
    """Return text with escaped characters for markdown."""
    if escape:
        for esc_chr in __MARKDOWN_ESCAPE_CHAR:
            text = text.replace(esc_chr, '\\' + esc_chr)

    return text


def get_formatted_string(
    text: str,
    width: int,
    formatted: bool = True,
) -> str:
    """Return text with trailing spaces."""
    return ' ' + text + ' ' + (' ' * (width - len(text))) if formatted else text


def get_md_table(
    column_store: ColumnStore,
    formatted: bool = True,
) -> str:
    """Return a formatted markdown table from a column-store."""
    widths: List[int] = [max(len(value) for value in column) for column in column_store]
    md_table: str = ''

    for idx in range(len(column_store[0])):
        columns = (column[idx] for column in column_store)
        md_table += (
            __SEPARATOR_PIPE
            + __SEPARATOR_PIPE.join(
                (get_formatted_string(column, width, formatted) for column, width in zip(columns, widths))
            )
            + __SEPARATOR_PIPE + '\n'
        )
        if idx == 0:
            md_table += (
                __SEPARATOR_PIPE
                + __SEPARATOR_PIPE.join(('-' * (width + 2 if formatted else 3) for width in widths))
                + __SEPARATOR_PIPE
                + '\n'
            )

    return md_table


def get_csv_table(
    column_store: ColumnStore,
    separator: str = ';',
) -> str:
    """Return a csv table from a column-store."""
    csv_table: str = ''

    for idx in range(len(column_store[0])):
        columns = (column[idx] for column in column_store)
        csv_table += separator.join(columns) + '\n'

    return csv_table


def main(args: List[str]) -> None:
    """Main function."""
    formatted = True
    escape = False
    input_type = 'csv'
    output_type = 'md'
    separator = ';'

    for arg in args:
        if arg == '-mini':
            formatted = False
        elif arg.startswith('-in:'):
            input_type = arg[4:].lower()
        elif arg.startswith('-out:'):
            output_type = arg[5:].lower()
        elif arg.startswith('-separator:'):
            separator = arg[11:]
        elif arg.startswith('-escape'):
            escape = True

    if separator == 'tab':
        separator = '\t'

    if input_type == 'csv':
        matrix = get_matrix_from_csv(sys.stdin, separator)
    elif input_type == 'md':
        matrix = get_matrix_from_md(sys.stdin)
    else:
        raise ValueError(f'Invalid input type: {input_type} (csv or md expected)')

    if output_type == 'csv':
        table = get_csv_table(get_column_store_from_matrix(matrix), separator)
    elif output_type == 'md':
        table = get_md_table(get_column_store_from_matrix(matrix, escape), formatted)
    else:
        raise ValueError(f'Invalid output type: {output_type} (csv or md expected)')

    sys.stdout.write(table)
    sys.stdout.flush()


if __name__ == '__main__':
    main(sys.argv[1:])
