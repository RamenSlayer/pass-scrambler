#!/bin/python

from passwordstrength.passwordmeter import PasswordStrength
from zxcvbn import zxcvbn

from random import random
from random import choice

from argparse import ArgumentParser as argparser

from warnings import warn

help_text = """
Generates a number of passwords from input by randomly switching characters to visually similar characters
"""

parser = argparser(description=help_text)
parser.add_argument("-e",
                    "--explicit",
                    dest="exp",
                    action="store_true",
                    help="Calls a menu to fill in options.")
parser.add_argument("-n",
                    "--number",
                    dest="num",
                    type=int,
                    default=128,
                    help="Number of generations")
parser.add_argument("-l",
                    "--lines",
                    dest="lines",
                    type=int,
                    help="Number of best password to print (all by default)")
parser.add_argument("-f",
                    "--friendly",
                    dest="friendly",
                    action="store_true",
                    help="Don't use symbols")
parser.add_argument("--not-recursive",
                    dest="recursive",
                    action="store_false",
                    help="Randomize non recursively. Less safe.")
parser.add_argument("-s",
                    "--strip",
                    dest="strip",
                    action="store_true",
                    help="Only prints passwords without strength measure")
parser.add_argument("password", nargs="*")
args = parser.parse_args()


def messtrength(s: str)->float:
    return PasswordStrength(s).strength()

def mesentropy(s: str)->float:
    # global entropy
    # return math.log2(entropy.entropy(s))
    return zxcvbn(s)['score']

l2n = {
       'a' : '4',
       'b' : '6',
       'e' : '3',
       'g' : '6',
       'h' : '4',
       'i' : '1',
       't' : '7',
       'l' : '1',
       'o' : '0',
       's' : '5',
       'z' : '2',
      }

n2l = {
      '1' : ('i', 'l', 'I', 'L'),
      '2' : ('z', 'Z'),
      '3' : ('e', 'E'),
      '4' : ('H', 'h', 'a', 'A'),
      '5' : ('s', 'S'),
      '6' : ('g', 'G'),
      '7' : ('t', 'T'),
      '0' : ('o', 'O'),
      }

smatch = {
          'a' : ('4', '@', 'A', 'a'),
          'b' : ('6', '8', 'b', 'B'),
          'c' : ('<', 'c', 'C'),
          'd' : ('0', 'd', 'D'),
          'e' : ('3', 'e', 'E'),
          'g' : ('6', '9', 'g', 'G'),
          'h' : ('4', '#', 'h', 'H'),
          'i' : ('1', '!', '|', 'i', 'I'),
          't' : ('7', 't', 'T',),
          'l' : ('1', '|', 'l', 'L'),
          'o' : ('0', 'o', 'O'),
          's' : ('5', 's', 'S', '$'),
          'z' : ('2', 'z', 'Z'),
          '1' : ('i', 'l', 'I', 'L', '!', '|', '1'),
          '2' : ('z', 'Z', '2'),
          '3' : ('e', 'E', '3'),
          '4' : ('H', 'h', 'a', 'A', '4'),
          '5' : ('s', 'S', '5'),
          '6' : ('g', 'G', 'b', 'B', '6'),
          '7' : ('t', 'T', '7'),
          '8' : ('&', 'b', 'B', '8'),
          '9' : ('g', 'G', '9'),
          '0' : ('o', 'O', '0', 'D'),
          '$' : ('s', 'S', '$'),
          '#' : ('h', 'H', '#'),
          '<' : ('c', 'C', '<'),
          '&' : ('8', 'b', 'B', '&'),
          '!' : ('i', 'I', '!', '|', '1'),
          '|' : ('i', 'I', '!', '|', '1', 'l', 'L'),
          '@' : ('a', 'A')
         }

# l2s = {
#       'q' : ('o|', '0|', 'O|', '*|'),
#       'w' : ('VV', 'vv'),
#       'e' :
#       }

def l2n_f(l: str)->str:
    l = l.lower()
    if l in l2n.keys():
        return l2n[l]
    return l

def n2l_f(n: str)->str:
    if n in n2l.keys():
        return choice(n2l[n])
    return n

def switch_cap(l: str)->str:
    if l.lower() == l:
        return l.upper()
    return l.lower()

def letter_op(l: str)->str:
    r = random()
    if r <= 1/2:
        return switch_cap(l)
    elif r <= 2/2:
        return l2n_f(l)

def number_op(n: str)->str:
    r = random()
    if r <= 1/1:
        return n2l_f(n)

# def uni(str:u)->str:
#     r = random()
#     if r <= 1/2:
#         return u * 2
#     elif r <= 2/2

numbers = "1234567890"
letters = 'qwertyuiopasdfghjklzxcvbnm'

def randomizer(pwd: str)->str:
    newpwd = str()
    for sym in pwd:
        r = random()
        if r <= 1/2:
            newpwd += sym
        elif r <= 2/2:
            if sym in numbers:
                newpwd += number_op(sym)
            elif sym.lower() in letters:
                newpwd += letter_op(sym)
    return newpwd

def Swchr(pwd: str)->str:
    newpwd = ""
    for sym in pwd:
        if sym.lower() in smatch.keys():
            newpwd += choice(smatch[sym.lower()])
        elif sym.lower() in letters:
            if random() >= 0.5:
                if sym.upper() == sym:
                    newpwd += sym.lower()
                else:
                    newpwd += sym.upper()
            else:
                newpwd += sym
        else:
            newpwd += sym
    return newpwd


if args.exp:
    inpwd = input("Password to randomize:\n> ")
    if inpwd == "":
        raise Exception("A password is required")
    number = input("How many passwords to generate (default = 128):\n> ")
    if number == '':
        number = 128
    else:
        try:
            number = int(number)
        except:
            warn(" ! Failed input, defaulting to 128")
            number = 128
    lines = input("Number of best password to print (default = all)\n> ")
    if lines == "":
        lines = number
    else:
        try:
            lines = int(lines)
        except:
            warn(" ! Input wasn't an integer\n ! Defaulting to all")
            lines = number
    if lines > number:
        warn("Print more lines than passwords generated. Will break print")
    friendly = input("(y) for friendly\n> ")
    friendly = friendly.lower() == 'y'
    strip = input("(y) to strip additional data from passwords\n> ")
    strip = strip.lower() == 'y'
    recursive = input("(n) to generate non recursively\n> ")
    recursive = recursive.lower() != 'n'
else:
    inpwd = " ".join(args.password)
    if inpwd == "":
        raise Exception("A password is required")
    number = args.num
    friendly = args.friendly
    if args.lines is None:
        lines = number
    else:
        lines = args.lines
    if lines > number:
        warn(" ! Print more lines than passwords generated. Will break print")
    friendly = args.friendly
    strip = args.strip
    recursive = args.recursive


passwords = []
if not friendly:
    newpwd = Swchr(inpwd)
    passwords.append(newpwd)
    for i in range(number - 1):
        if recursive:
            newpwd = Swchr(newpwd)
        else:
            newpwd = Swchr(inpwd)
        passwords.append(newpwd)
else:
    newpwd = randomizer(inpwd)
    passwords.append(newpwd)
    for i in range(number - 1):
        if recursive:
            newpwd = randomizer(newpwd)
        else:
            newpwd = randomizer(inpwd)
        passwords.append(newpwd)

ranked_pwds = []

try:
    for pwd in passwords:
        ranked_pwds.append((messtrength(pwd), mesentropy(pwd), pwd))
except:
    warn(" ! Entropy measure failed\n ! Falling back to strength measure")
    ranked_pwds = []
    for pwd in passwords:
        ranked_pwds.append((messtrength(pwd), pwd))

if strip:
    for outpass in sorted(ranked_pwds)[len(ranked_pwds) - lines:]:
        print(outpass[-1])
else:
    for outpass in sorted(ranked_pwds)[len(ranked_pwds) - lines:]:
        print(outpass)
