import os

import click

from swedishelf.fileop import get_app_dir
from swedishelf.sven import Sven

DIC_FILENAME = "folkets_sv_en_public.json"


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
    """swedishelf - An interactive command-line tool for learning Swedish through quizzes and exercises."""
    if version:
        print("swedishelf v0.1.1")
        exit(0)
    # If -d or --dic option passed, will use specified dict.
    if dic is None:
        cwd_dic_path = os.path.join(os.getcwd(), DIC_FILENAME)
        app_dir = get_app_dir()
        app_dir_dic_path = os.path.join(app_dir, DIC_FILENAME)

        if os.path.exists(os.path.join(os.getcwd(), DIC_FILENAME)):
            dic = cwd_dic_path
        elif os.path.exists(app_dir_dic_path):
            dic = app_dir_dic_path
        else:
            print("Run failed, no dictionary file found.")
            exit(1)
        print("Using dictionary file:", dic)

    sven = Sven(dic)
    sven.play(num, mute, choices)


if __name__ == "__main__":
    main()
