import json
import os
import random
import sys
import time
from functools import cmp_to_key
from typing import List, Optional, Tuple

import click
from playsound3 import playsound

from swedishelf.fileop import download_file, get_app_dir


def compare_synonyms(syn1, syn2):
    if "l" in syn1 and "l" in syn2:
        # Larger level comes first
        if syn1["l"] > syn2["l"]:
            return -1
        elif syn1["l"] < syn2["l"]:
            return 1
        else:
            # If levels are the same, we do not want to change the order
            return 0
    elif "l" not in syn1 and "l" not in syn2:
        # Level not present for both, we do not want to change the order
        return 0
    elif "l" in syn1 and "l" not in syn2:
        # If syn1 has a level, but syn2 does not, syn1 comes first
        return -1
    else:
        # If syn2 has a level, but syn1 does not, syn2 comes first
        return 1


class Sven:
    def __init__(self, filepath: str) -> None:
        """
        Initialize Sven with a given filepath of a dictionary.

        Parameters
        ----------
        filepath : str
            Filepath of the dictionary file.
        """
        with open(filepath, "r") as f:
            self.dic = json.load(f)
            self.keys = list(self.dic.keys())
        self.right_cnt = 0

    def check_translation_similarity_high(
        self, translation1: List[str], translation2: List[str]
    ) -> bool:
        """Check if two translations are similar in a high level.

        This function takes two translations, and checks if they contain any
        identical strings. If they do, it returns True, meaning they are
        similar. Otherwise, it returns False.

        Parameters
        ----------
        translation1 : List[str]
            The first translation.
        translation2 : List[str]
            The second translation.
        Returns
        -------
        bool
            Whether the two translations are similar.
        """
        # Iterate over each translation in both translations
        for t1 in translation1:
            for t2 in translation2:
                # If any of the translations are equal, return True
                if t1 == t2:
                    return True
        # If no equal translations are found, return False
        return False

    def get_random_wrong_choices(self, translation: List[str], n: int) -> List[str]:
        """
        Get a list of n random wrong choices given a translation.

        Parameters
        ----------
        translation : List[str]
            The given translation.
        n : int
            The number of wrong choices to be returned.

        Returns
        -------
        List[str]
            A list of n random wrong choices.
        """
        wrong_choices = []
        while len(wrong_choices) < n:
            wrong_key = random.choice(self.keys)
            wrong_translation = self.dic[wrong_key]["t"]
            if not self.check_translation_similarity_high(
                translation, wrong_translation
            ):
                wrong_choices.append(wrong_key)
        return wrong_choices

    def get_choice_question(self, choices: int = 3) -> Tuple[str, List[str]]:
        """
        Get a choice question with the correct answer and wrong choices.

        Parameters
        ----------
        choices : int
            The number of total choices to present, including the correct answer.

        Returns
        -------
        tuple[str, list[str]]
            A tuple containing the answer key and a list of wrong keys.

        Raises
        ------
        AssertionError
            If the number of choices is not greater than 1.
        """
        assert choices > 1, "Choices must be greater than 1"
        while True:
            answer_key = random.choice(self.keys)
            # Check if the answer key has an example and an audio url
            if "t" in self.dic[answer_key] and (
                "e" in self.dic[answer_key] or "id" in self.dic[answer_key]
            ):
                break
        translation = self.dic[answer_key]["t"]
        wrong_keys = self.get_random_wrong_choices(translation, choices - 1)

        return answer_key, wrong_keys

    def display_entry(self, key: str) -> None:
        """
        Display a single entry from the dictionary.

        Parameters
        ----------
        key : str
            The key of the entry to be displayed.

        Returns
        -------
        None
        """
        click.secho(f"{key}", bold=True, fg="yellow", nl=False)
        if "c" in self.dic[key]:
            click.secho(f" {self.dic[key]['c']}", fg="bright_black", nl=False)
        if "p" in self.dic[key]:
            click.secho(f" [{self.dic[key]['p']}]", fg="bright_black", nl=False)
        click.secho(f" {', '.join(self.dic[key]['t'])}", fg="yellow")
        if "i" in self.dic[key]:
            click.secho(f"Inflections: {', '.join(self.dic[key]['i'])}")
        if "s" in self.dic[key]:
            sorted_synonyms = sorted(
                self.dic[key]["s"], key=cmp_to_key(compare_synonyms)
            )
            click.secho(f"Synonyms: ", nl=False)
            for idx, synonym in enumerate(sorted_synonyms):
                click.secho(f"{synonym['v']}", nl=False)
                if "l" in synonym:
                    click.secho(f"({synonym['l']})", fg="bright_black", nl=False)
                if idx < len(sorted_synonyms) - 1:
                    click.secho(f", ", nl=False)
            click.echo()
        if "d" in self.dic[key]:
            click.secho(f"Definition: {', '.join(self.dic[key]['d'])}")
        if "e" in self.dic[key]:
            click.secho("Example: ", nl=False)
            for item in self.dic[key]["e"]:
                click.secho(f"{item['v']}", nl=False)
                if "t" in item:
                    click.secho(f" ({item['t']})")
                else:
                    click.echo()
        if "id" in self.dic[key]:
            click.secho("Idiom: ", nl=False)
            for item in self.dic[key]["id"]:
                click.secho(f"{item['v']}", nl=False)
                if "t" in item:
                    click.secho(f" ({item['t']})")
                else:
                    click.echo()

    def display_question(
        self, answer_key: str, wrong_keys: List[str], mute: bool, is_last: bool
    ) -> None:
        """
        Display a question to the user.

        Parameters
        ----------
        answer_key : str
            The key of the dictionary entry for the correct answer.
        wrong_keys : List[str]
            The keys of the dictionary entries for the wrong answers.
        mute : bool
            If True, will not play the audio associated with the answer.
        is_last : bool
            If True, will set soundplay to block to finish the sound.
        Returns
        -------
        None
        """
        audio_path = None
        if not mute and "a" in self.dic[answer_key]:
            audio_path = download_file(self.dic[answer_key]["a"], category="audio")

        click.secho("=" * 120, fg="bright_black")
        click.secho(f"{', '.join(self.dic[answer_key]['t'])}", bold=True)
        choices = wrong_keys + [answer_key]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            click.secho(f"{i + 1}. {choice} | ", nl=False)

        input_char = click.getchar()

        try:
            input_num = int(input_char)
        except ValueError:
            input_num = 0

        click.secho(f"**{input_num}** ", fg="cyan", bold=True, nl=False)
        if input_num > len(choices):
            click.secho("Your choice is out of range!", fg="red")
        else:
            if input_num > 0 and answer_key == choices[input_num - 1]:
                click.secho("✅ Right!", fg="green")
                self.right_cnt += 1
            else:
                click.secho("❌ Wrong!", fg="red")

        click.echo()
        self.display_entry(answer_key)

        if not mute and audio_path is not None and os.path.exists(audio_path):
            if sys.platform.startswith("win"):
                playsound(audio_path, block=is_last)
            else:
                playsound(audio_path, block=is_last, backend="ffplay")

    def play(self, num: int, mute: bool, choices: int) -> None:
        """
        Play a round of questions.

        Parameters
        ----------
        num : int
            Number of questions for this round.
        mute : bool
            If True, will not play audio.
        choices : int
            Number of choices for each question.

        Returns
        -------
        None
        """
        self.right_cnt = 0
        questions = []
        for _ in range(num):
            answer_key, wrong_keys = self.get_choice_question(choices=choices)
            questions.append((answer_key, wrong_keys))

        for idx, (answer_key, wrong_keys) in enumerate(questions):
            if idx == num - 1:
                self.display_question(answer_key, wrong_keys, mute, is_last=True)
            else:
                self.display_question(answer_key, wrong_keys, mute, is_last=False)

        click.secho("=" * 120, fg="bright_black")
        click.secho(
            f"You've finished this round! Your score is {self.right_cnt}/{num}.",
            fg="green",
        )
