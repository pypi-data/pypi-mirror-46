import math
import random

SYMBOLS = '!@$%^&*='


with open('/usr/share/dict/words') as f:
    WORDS = {
        x.strip().lower().replace("'s", '')
        for x in f
    }
    WORDS = sorted({
        x for x in WORDS
        if 3 < len(x) < 12
    })


def get_word():
    return random.choice(WORDS)


def gen_password(num_words=2, num_digits=3, add_symbol=False):
    words = [get_word() for i in range(num_words)]
    if num_digits > 0:
        digits_fmt = '{{:0{}}}'.format(num_digits)
        digits = digits_fmt.format(random.randint(0, 10**num_digits - 1))
    else:
        digits = ''
    i = random.randint(0, num_words - 1)
    words[i] = words[i].upper()
    if add_symbol:
        symbol = random.choice(SYMBOLS)
    else:
        symbol = ''
    entropy = len(WORDS)**num_words
    entropy *= 10**num_digits
    if add_symbol:
        entropy *= len(SYMBOLS)
    entropy = math.log(entropy, 2)
    pw = ''.join(words + [digits] + [symbol])
    return pw, entropy
