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


def kor_to_ipa(text, transcr) -> str:
    """
    Turns Korean alphabet into IPA

    Args:
        text: str
            Korean text
        transcr:
            Transcription class

    Returns:
        Transcription with rules in IPA tradition

    """

    text = transcr.transcribe(text)
    text = re.sub(r'[-/\s#\.,]', '', text)

    return text


def remove_non_ascii(text):
    """
    Removes non ascii elements.
    Necessary for string that contain both English and Korean symbols.

    Args:
        text: str
           Text from the English part of dataset.

    Returns:
        Clean version (if a string previously included Korean symbols)
    """

    return re.sub(r'[^\x00-\x7F]', ' ', text)


def eng_to_ipa(text) -> str:
    """
    Converts English to IPA

    Args:
        text: str
            String in English

    Returns:
        IPA string
    """

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
    """
            Finds last syllable in the string&

            Args:
                string: str
                    transcribed string in Unicode

            Returns: IPAString
                last syllable -- CV(C*)
    """

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
    s_ipa = IPAString(unicode_string=text)
    return s_ipa.vowels


def get_vowel_type(vowel):
    vowel = vowel[0]
    vowel = ' '.join(vowel.name.split()[:3])
    return vowel

if __name__ == '__main__':
    df = pd.read_csv('kor_eng.csv')
    transcr = IPAkor.Transcription()
    df['kor_transcribed'] = df.korean.apply(lambda x: kor_to_ipa(x, transcr))
    df['eng_transcribed'] = df.english.apply(eng_to_ipa)
    df['kor_rhyme_syll'] = df.kor_transcribed.apply(get_last_syll)
    df['eng_rhyme_syll'] = df.eng_transcribed.apply(get_last_syll)
    df['rhyme_type_kor'] = df.kor_rhyme_syll.apply(get_stats)
    df['rhyme_type_eng'] = df.eng_rhyme_syll.apply(get_stats)
    df['vowel_type_kor'] = df.rhyme_type_kor.apply(get_vowel_type)
    df['vowel_type_eng'] = df.rhyme_type_eng.apply(get_vowel_type)
    df[['rise_kor', 'placement_kor', 'roundness_kor']] = df.vowel_type_kor.str.split(expand=True)
    df[['rise_eng', 'placement_eng', 'roundness_eng']] = df.vowel_type_eng.str.split(expand=True)
    df.to_csv('processed_new.csv')
