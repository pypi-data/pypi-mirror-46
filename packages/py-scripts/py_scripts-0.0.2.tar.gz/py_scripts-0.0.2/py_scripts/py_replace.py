import click

_opt = dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
)


def entry(filename, output="", symbol="$", **params):
    if not params:
        return click.echo("[EXIT]: params not found.")
    with open(filename, "r") as f:
        content = f.read()
        for k, v in params.items():
            if len(symbol) <= 1:
                key = "{}{}".format(symbol, k)
            elif symbol == "{}":
                key = '{%s}' % (k)
            elif symbol == "{{}}":
                key = '{%s}' % (k)
            else:
                return click.echo("[Fail]: symbol '{}' is not supported ".format(symbol))

            click.echo("[REPLACE] %s => %s" % (key, v))
            content = content.replace(key, v)

    output = output or "{}.out".format(filename)
    with open(output, 'w') as f:
        f.write(content)
    click.echo("[SUCCESS] >>> {}".format(output))


@click.command(name="py_replace", context_settings=_opt)
@click.help_option("--help", "-h")
@click.argument('filename', type=str)
@click.option('--output', '-o', default="", help='output file, default: $FILENAME.out')
@click.option('--symbol', '-s', default="$",
              help="symbol of parameter variable, default: '$', specific support: ['{}', '{{}}']")
@click.pass_context
def cli(ctx, filename, output="", symbol="$"):
    '''
    py_replace [OPTIONS] file key1=val1 [key2=val2 ... kn=vn]

    desc: output file with replace content of `$key1` to `val1` and so on.
    '''
    kws = {}
    for arg in ctx.args:
        kws.update([arg.split("=", 1)])
    entry(filename, output, symbol, **kws)


if __name__ == '__main__':
    cli()
