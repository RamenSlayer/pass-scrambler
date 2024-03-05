from passwordstrength.passwordmeter import PasswordStrength
from passwordstrength.entropy import Entropy

from zxcvbn import zxcvbn

from random import random
from random import choice


entropy = Entropy()

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

def letter(l: str)->str:
    r = random()
    if r <= 1/2:
        return switch_cap(l)
    elif r <= 2/2:
        return l2n_f(l)

def number(n: str)->str:
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
                newpwd += number(sym)
            elif sym.lower() in letters:
                newpwd += letter(sym)
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


inpwd = input("Password to randomize:\n> ")
iterations = input("How many times to iterate (default = 128):\n> ")
method = input("Method 0 or 1 (default 0)\n> ")

if iterations is None or iterations == '':
    iterations = 128
else:
    try:
        iterations = int(iterations) - 1
    except:
        print(" ! Failed input, defaulting to 128")
        iterations = 128

passwords = []
if method != '1':
    newpwd = Swchr(inpwd)
    passwords.append(newpwd)
    for i in range(iterations):
        newpwd = Swchr(newpwd)
        passwords.append(newpwd)
else:
    newpwd = randomizer(inpwd)
    passwords.append(newpwd)
    for i in range(iterations - 1):
        newpwd = randomizer(newpwd)
        passwords.append(newpwd)
ranked_pwds = []

try:
    for pwd in passwords:
        ranked_pwds.append((mesentropy(pwd), messtrength(pwd), pwd))
except:
    print(" ! Entropy measure failed for whatever reason beyond my control or comprehension\n",
          " ! Falling back to strength measure")
    for pwd in passwords:
        ranked_pwds.append((messtrength(pwd), pwd))
print(*sorted(ranked_pwds), sep='\n')
