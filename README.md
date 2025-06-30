# Swedishelf

## Installation

### Linux

#### Download dictionary

Download the JSON dictionary `folkets_sv_en_public.json` from [here](https://github.com/celestialli/convert-dict/releases).

Store the file in one of the following locations:
- **Global installation** (recommended): `/home/<YOUR_USERNAME>/.config/swedishelf/` - This makes the dictionary available system-wide for all your swedishelf sessions. (You may need to create the `.config` and `swedishelf` directories if they don't exist)
- **Local installation**: Place the file in the directory where you plan to run `swedishelf` - The dictionary will only be available when running swedishelf from that specific directory.

#### Install audio dependency

Install ffplay (part of the FFmpeg package). The following example uses Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg -y
```

Verify that ffplay is installed correctly:

```bash
ffplay -version
```

#### Install swedishelf

Install swedishelf:

```bash
pip install swedishelf
```

Enjoy!

### Windows

#### Download dictionary

Download the JSON dictionary `folkets_sv_en_public.json` from [here](https://github.com/celestialli/convert-dict/releases).

Store the file in one of the following locations:
- **Global installation** (recommended): `C:\Users\<YOUR_USERNAME>\AppData\Roaming\swedishelf\` - This makes the dictionary available system-wide for all your swedishelf sessions. (You may need to enable viewing of hidden folders to access `AppData`, and create the `swedishelf` directory if it doesn't exist)
- **Local installation**: Place the file in the directory where you plan to run `swedishelf` - The dictionary will only be available when running swedishelf from that specific directory.

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

Enjoy!

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

#### Q: In what order does swedishelf search for the dictionary file?

Swedishelf searches for the dictionary file in the following priority order:

1. **Custom dictionary path** (specified with `-d` or `--dict` option)
2. **Current working directory** (the directory where you run the `swedishelf` command)
3. **System-wide user config directory** (varies by operating system):
   - Linux: `/home/<YOUR_USERNAME>/.config/swedishelf/`
   - Windows: `C:\Users\<YOUR_USERNAME>\AppData\Roaming\swedishelf\`

#### Q: Why doesn't the program show the next question immediately after I have answered one?
A: The audio of the question you just answered is playing, and swedishelf is downloading the audio for the next question at this time without blocking. The download duration depends on the network conditions. If you run the program with the `-m` or `--mute` option, this delay will not occur.

## Contributing

If you'd like to contribute to swedishelf, please fork the repository and submit a pull request with your changes. You can also report issues or suggest new features on the issue tracker.

## Licensing

Swedishelf is licensed under the MIT License. See the LICENSE file for more information.
