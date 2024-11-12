# pass-scrambler
Scrambles input string to use as password. Rates the output results by strength.

To use just do `python passgen.py` from the directory where you have it. 

For more help read `python passgen.py -h` (does anyone agree that it's annoying when only `--help` works despite `-h` not being used anywhere else (or the opposite, which is even worse)?)

## Installation
Either run `pip install -r requirements.txt` in the directory of the project (if you git pulled it or unzipped) or just `pip install passwordstrength zxcvbn` (I suggest downloading just the .py file and putting it in some directory with other tools).

---

## TODO

- [ ] Move to function, take arguments
- [x] Add option to only input string in interactive mode, the rest in command
- [ ] Add "interactive by default" instead of requiring an argument to go interactive.
- [ ] MAYBE rewrite the legacy method or think of some simplifications
