import click
import sys
import json
from subprocess import check_output
from pytijo import parser


@click.command(
    name="tijo",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
)
@click.option("--tijo-template", type=click.File())
@click.option("--tijo-output-beauty", is_flag=True, default=False)
@click.pass_context
def tijo(ctx, tijo_template, tijo_output_beauty):
    if len(ctx.args) <= 0 and tijo_template is None:
        print("--tijo-template is required if a command is not provided")
        raise click.Abort()

    template = None
    if tijo_template:
        template = json.load(tijo_template)
    else:
        # TODO: find the template from tijo repository
        print("pending to implement discover the template")
        raise click.Abort()
        pass

    output = None
    if len(ctx.args) <= 0:
        output = "".join(sys.stdin)
    else:
        output = check_output(ctx.args)

    result = parser.parse(output, template)
    output = json.dumps(result, indent=4) if tijo_output_beauty else result
    click.echo(output)


def main():
    tijo()


if __name__ == "__main__":
    tijo()
