# mdtable

Command line tool to generate formatted markdown tables easy to read, even without markdown rendering.

It converts CSV to markdown table, or markdown table to CSV.

## Arguments

| Argument  | Description                              | Values (default in bold)                                      | Example        |
|-----------|------------------------------------------|---------------------------------------------------------------|----------------|
| in        | Type of input                            | **csv**, md                                                   | `-in:md`       |
| out       | Type of output                           | csv, **md**                                                   | `-out:csv`     |
| separator | Column separator for csv input or output | *character* (default = **semicolon**, **tab** for tabulation) | `-separator:,` |
| mini      | Minified markdown table output           |                                                               | `-mini`        |
| escape    | Escape characters in markdown output     |                                                               | `-escape`      |

## Examples

### CSV to markdown table

```bash
cat samples/sample.csv | python mdtable.py
cat samples/sample.csv | python mdtable.py -separator:;
cat samples/sample.csv | python mdtable.py -mini
```

### Markdown table to formatted markdown table

```bash
cat samples/sample.md | python mdtable.py -in:md
```

### Markdown table to CSV

```bash
cat samples/sample.md | python mdtable.py -in:md -out:csv
cat samples/sample.md | python mdtable.py -in:md -out:csv -separator:,
```
