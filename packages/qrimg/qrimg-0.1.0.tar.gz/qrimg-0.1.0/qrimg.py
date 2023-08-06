import click
import qrcode


def gen(output, message):
    img = qrcode.make(message)
    img.save(output)
    return img

@click.command()
@click.option("-o", "--output", help="Output file name.", required=True)
@click.argument("message", nargs=1, required=True)
def main(output, message):
    gen(output, message)


if __name__ == "__main__":
    main()
