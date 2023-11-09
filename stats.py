import IPAkor
import pandas as pd
import re
import os

from ipapy import UNICODE_TO_IPA
from ipapy import is_valid_ipa
from ipapy.ipachar import IPAConsonant
from ipapy.ipachar import IPAVowel
from ipapy.ipastring import IPAString
from phonemizer import phonemize
from phonemizer.separator import Separator


def kor_to_ipa(text, transcr):
    text = transcr.transcribe(text)
    text = re.sub(r'[-/\s#\.,]', '', text)

    return text


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', ' ', text)

def eng_to_ipa(text):
    text = remove_non_ascii(text)
    # to add stress marks use
    # with_stress=True as a parameter of phomemize
    phn = phonemize(
        text,
        language='en-us',
        backend='espeak',
        separator=Separator(phone='', word='', syllable='|'),
        strip=True,
        preserve_punctuation=False,
        njobs=4)
    phn = re.sub(r'[-/\s#\.,]', '', phn)

    return phn


def get_last_syll(s_uni):
    desired = ['diacritic', 'suprasegmental']
    s_ipa = IPAString(unicode_string=s_uni)
    ending = IPAString()

    for i in reversed(s_ipa):

        if i.name.split()[-1] in desired:
            ending.insert(0, i)
        elif i.name.split()[-1] == 'vowel':
            ending.insert(0, i)
            # counter += 1
        elif i.name.split()[-1] == 'consonant':
            ending.insert(0, i)
            if len(ending.vowels) >= 1:
                break

    return str(ending)


def get_stats(text):
    rhyme = ''
    s_ipa = IPAString(unicode_string=text)
    # for i in s_ipa:
    #     if i.is_vowel:
    #         rhyme += f'{str(i)}_'
    #     elif i.is_consonant:
    #         rhyme += f'{str(i.name.split()[-2])}_'
        # else:
        #     rhyme += f'{str(i.name.split()[0])} '
    return s_ipa.vowels


if __name__ == '__main__':
    df = pd.read_csv('kor_eng.csv')
    transcr = IPAkor.Transcription()
    df['kor_transcribed'] = df.korean.apply(lambda x: kor_to_ipa(x, transcr))
    df['eng_transcribed'] = df.english.apply(eng_to_ipa)
    df['kor_rhyme_syll'] = df.kor_transcribed.apply(get_last_syll)
    df['eng_rhyme_syll'] = df.eng_transcribed.apply(get_last_syll)
    df['rhyme_type_kor'] = df.kor_rhyme_syll.apply(get_stats)
    df['rhyme_type_eng'] = df.eng_rhyme_syll.apply(get_stats)
    df.to_csv('processed.csv')
