# pass-scrambler
Scrambles input string to use as password. Rates the output results by strength.

To use just do `python passgen.py` from the directory where you have it. 

Default method is just better in my opinion and uses special symbols. Old method was the original that I was too lazy to rewrite and it doesn't use special symbols so I kept it.

## Installation
Either run `pip install -r requirements.txt` in the directory of the project (if you git pulled it or unzipped) or just `pip install passwordstrength zxcvbn` (I suggest downloading just the .py file and putting it in some directory with other tools).

---

## TODO:
1. Add an option for non recursive scrambling. Should be easy if I ever get to it.
2. Convert options into cli options for better usage.
3. Idk, make it not bad? Add options for randomizing how much of each kind of scramble you want to see? Add other methods of scrambling? But who's going to use that tbh?
