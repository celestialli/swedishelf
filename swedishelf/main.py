import click

from swedishelf.fileop import download_file
from swedishelf.sven import Sven

DIC_URL = "https://cdn.jsdelivr.net/gh/celestialli/convert-dict@main/folkets_sv_en_public.json"


@click.command()
@click.option(
    "-d",
    "--dic",
    type=str,
    help="Specify dict file, will use default dict if not specified.",
)
@click.option(
    "-n", "--num", type=int, default=20, help="Number of questions for this round."
)
@click.option("-m", "--mute", is_flag=True, help="If mute, will not play audio.")
@click.option(
    "-c",
    "--choices",
    type=int,
    default=3,
    help="Number of choices for each question, the bigger, the harder.",
)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    help="Show version and exit.",
)
def main(dic, num, mute, choices, version):
    """swedishelf - A command line tool that helps you learn swedish"""
    if version:
        print("swedishelf v0.1.0")
        exit(0)
    # If -d or --dic option passed, will use specified dict.
    if dic is None:
        dic = download_file(DIC_URL)

    sven = Sven(dic)
    sven.play(num, mute, choices)


if __name__ == "__main__":
    main()
