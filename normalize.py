import re
import unidecode

"""
This script processes a .txt file containing the transcription of an audio track, generating another
.txt file containing the same transcription split into sentences and parsed to contain only 
allowed characters.
Sentences are 'guessed' every time a char in 'stop_chars' is met, and only if longer than SENTENCE_MIN_LEN
words.

USAGE.

python3 normalize.py --in_file <transcription.txt> --sentence_min_len <?> --remove_lines <line1;line2;>

--in_file -> raw transcription in txt file
--remove_lines -> list of lines, separated by ';' that should be removed from transcription (example name of peoples spaking)
--sentence_min_len -> minimum words for generated sentences
"""

# Minimum words that a sentence must be composed of.
SENTENCE_MIN_LEN = 5

# Allowed chars.
allowed_chars =  [" ", "'", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'è', 'é', 'ì', 'ò', 'ù']

# Two lists of chars that must be removed.
chars_to_remove = [ ",", "?", ".", "!", "-", ";", ":", "’", '""', "%", '"', "�",'ʿ','“','”','(','=','`','_','+','«','<','>','~','…','«','»','–','\[','\]','°','´','ʾ','„','¡'] # ,'̇','̇','̇','̇',
apostrophe_to_remove =  ['’', '̇', '̇', '̇', '̇', '`']

# When one of this chars is met, an attempt to create a new sentence is made, if the currently 
# created sentence is longer than SENTENCE_MIN_LEN.
stop_chars = ['.', ',', '?', '!', ';', ':', '-']


class TextPreprocessor:
    """
    Class to preprocess transcripts of audio by removing unallowed chars and normalizing text.
    Allowed chars and chars to remove are defined in config yaml file in corresponding fields.
    For all chars which are not in the vocabulary we transform them in ASCII characters corresponding more or less
    to their sound (this is based on the unidecode_expect_ascii() function from 'unidecode' package).

    """

    def __init__(self):
        # self.chars_to_remove_regex = f'[{"".join(cfg.text_preprocessing.chars_to_remove)}]'
        self.chars_to_remove_regex = f"[{re.escape(''.join(chars_to_remove))}]"
        self.allowed_chars = set(allowed_chars)
        self.apostrophe_regex = f"[{re.escape(''.join(apostrophe_to_remove))}]"

    def normalize_char(self, char):
        # Normalize unallowed chars to ASCII or corresponding sound.
        if char in self.allowed_chars:
            return char
        else:
            return unidecode.unidecode_expect_ascii(char)

    def normalize_text(self, sentence):
        # Remove unwanted characters and normalize chars one by one
        # print(self.chars_to_remove_regex)
        allowed_sentence = re.sub(self.apostrophe_regex, "' ", sentence).lower()
        allowed_sentence = re.sub(self.chars_to_remove_regex, '', allowed_sentence).lower()
        new_sentence = ''
        for char in allowed_sentence:
            new_sentence += self.normalize_char(char)
        return new_sentence

    def __call__(self, sentence):
        return self.normalize_text(sentence)


def do_normalize(in_file, sentence_min_len, remove_lines):
    
    with open(in_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    if remove_lines is not None:
        remove_lines = remove_lines.lower().split(';')
    else:
        remove_lines = []

    for line in lines:
        if line.lower() not in remove_lines: 
            new_lines.append(line)

    text = ' '.join(new_lines)

    # print(text)

    new_file = ''
    sentence = ''
    sentence_len = 0
    splitted = text.split()

    for word in splitted:
        # print('Analyzing word:', word)
        sentence += word + ' '
        sentence_len += 1
        if any(x in word for x in stop_chars):
            # print('Word contains stop char!')
            if sentence_len >= sentence_min_len:
                # print(f'Current sentence is: {sentence} -> so long enough')
                sentence += '\n'
                new_file += sentence
                sentence = ''
                sentence_len = 0

    processor = TextPreprocessor()
    out_file = in_file.split('.')[-2]+'_out.'+in_file.split('.')[-1]
    with open(out_file, 'w') as f:
        f.write(processor.normalize_text(new_file))
            

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--in_file", type=str)
parser.add_argument("--remove_lines", nargs='?', type=str)
parser.add_argument("--sentence_min_len", nargs='?', const=1, default=SENTENCE_MIN_LEN, type=int)
args = parser.parse_args()
print(args)
do_normalize(args.in_file, args.sentence_min_len, args.remove_lines)
