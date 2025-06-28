# Swedishelf

## Installation

### Linux

First, install ffplay (part of the FFmpeg package). The following example uses Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg -y
```

Verify that ffplay is installed correctly:

```bash
ffplay -version
```

Install swedishelf:

```bash
pip install swedishelf
```

### Windows

#### Configure UTF-8 Support

Before installing swedishelf, you need to enable UTF-8 support on Windows:

1. Open **Control Panel** → **Clock and Region** → **Region**
2. Click the **Administrative** tab → **Change system locale**
3. Check the box for **"Beta: Use Unicode UTF-8 for worldwide language support"**
4. Restart your system

#### Install swedishelf

After restarting your system, install swedishelf:

```bash
pip install swedishelf
```

## Usage

To use swedishelf, simply run the command `swedishelf` in your terminal. This will start an interactive session where you can practice your Swedish language skills.

### Options

You can customize your experience with the following options:

* `-d` or `--dic`: Specify dict file, will use default dict if not specified.
* `-n` or `--num`: Number of questions for this round.
* `-m` or `--mute`: If mute, will not play audio.
* `-c` or `--choices`: Number of choices for each question, the bigger, the harder.
* `-v` or `--version`: Show version and exit.
* `--help`: Show CLI help and exit.

### Example

Here's an example of how to use swedishelf with the default settings, open a terminal and run:
```bash
$ swedishelf
```
This will start a session with 20 questions, using the default dictionary file.

### FAQs

#### Q: Why does the program take a long time on first start?
A: When you run swedishelf for the first time, it may take 10 seconds or more to start. This is because the program is downloading the dictionary file. This download only occurs on the first run.

You can download the JSON dictionary from [here](https://github.com/celestialli/convert-dict/releases/tag/v1.0.4488). Then run the program with
```bash
$ swedishelf -d <your_local_path_to_json_dictionary>
```

#### Q: Why doesn't the program show the next question immediately after I have answered one?
A: The audio of the question you just answered is playing, and swedishelf is downloading the audio for the next question at this time without blocking. The downloading duration depends on the network conditions. If you run the program with the `-m` or `--mute` option, this delay will not occur.

## Contributing

If you'd like to contribute to swedishelf, please fork the repository and submit a pull request with your changes. You can also report issues or suggest new features on the issue tracker.

## Licensing

swedishelf is licensed under the MIT License. See the LICENSE file for more information.
