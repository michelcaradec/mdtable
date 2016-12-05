#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys


def get_matrix_from_csv(stream, separator=";"):
    """Return a matrix of values from an input stream containing csv data."""
    for line in stream:
        yield [col.strip("\r\n") for col in line.split(separator)]


def get_matrix_from_md(stream):
    """Return a matrix of values from an input stream containing a markdown table."""
    for idx, line in enumerate(stream):
        if idx == 1:
            continue

        cols = line.split("|")
        yield [col.strip(" \r\n") for col in cols][1:len(cols) - 1]


def get_column_store_from_matrix(matrix):
    """Return input stream as a column-store."""
    columns = []

    for row in matrix:
        if not len(columns):
            columns = [[col] for col in row]
        else:
            for idx, col in enumerate(row):
                columns[idx].append(col)

    return columns


def get_formatted_string(text, width, formatted=True):
    """Return text with trailing spaces."""
    return " " + text + " " + (" " * (width - len(text))) if formatted else text


def get_md_table(column_store, formatted=True):
    """Return a formatted markdown table from a column-store."""
    widths = [max(len(value) for value in column) for column in column_store]
    md_table = ""

    for idx in range(len(column_store[0])):
        columns = (column[idx] for column in column_store)
        md_table += "|" + "|".join((get_formatted_string(column, width, formatted) for column, width in zip(columns, widths))) + "|\n"
        if idx == 0:
            md_table += "|" + "|".join(("-" * (width + 2 if formatted else 3) for width in widths)) + "|\n"

    return md_table


def get_csv_table(column_store, separator=";"):
    """Return a csv table from a column-store."""
    csv_table = ""

    for idx in range(len(column_store[0])):
        columns = (column[idx] for column in column_store)
        csv_table += separator.join(columns) + "\n"

    return csv_table


def main(args):
    """Main function."""
    formatted = True
    input_type = "csv"
    output_type = "md"
    separator = ";"

    for arg in args:
        if arg == "-mini":
            formatted = False
        elif arg.startswith("-in:"):
            input_type = arg[4:].lower()
        elif arg.startswith("-out:"):
            output_type = arg[5:].lower()
        elif arg.startswith("-separator:"):
            separator = arg[11:]

    if input_type == "csv":
        matrix = get_matrix_from_csv(sys.stdin, separator)
    elif input_type == "md":
        matrix = get_matrix_from_md(sys.stdin)
    else:
        raise Exception("Invalid input type: %s (csv or md expected)" % input_type)

    if output_type == "csv":
        table = get_csv_table(get_column_store_from_matrix(matrix), separator)
    elif output_type == "md":
        table = get_md_table(get_column_store_from_matrix(matrix), formatted)
    else:
        raise Exception("Invalid output type: %s (csv or md expected)" % input_type)

    sys.stdout.write(table)
    sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
