
# Py-Scripts

 python scripts for any platforms

 please feel comfort to pull request for your scripts. 

## Depends

```bash
pip install py-scripts
```

## Install

```bash
pip install py-scripts
```

### Includes

#### py_replace

```
Usage: py_replace.py [OPTIONS] FILENAME

  py_replace [OPTIONS] file key1=val1 [key2=val2 ... kn=vn]

  desc: output file with replace content of `$key1` to `val1` and so on.

Options:
  -h, --help         Show this message and exit.
  -o, --output TEXT  output file, default: $FILENAME.out
  -s, --symbol TEXT  symbol of parameter variable, default: '$', specific
                     support: ['{}', '{{}}']

```