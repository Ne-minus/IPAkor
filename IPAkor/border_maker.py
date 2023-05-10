# ЭТОТ КОД ДЕЛАЕТ РАЗНЫЕ ВИДЫ ГРАНИЦ МЕЖДУ СЛОГАМИ, КЛИТИКАМИ, СЛОВАМИ И СИНТАГМАМИ
from konlpy.tag import Twitter
from konlpy.tag import Kkma
import csv
import os
import re
import wget


class BorderMaker:

    def __init__(self):
        self.twitter = Twitter()
        self.kkma = Kkma()

        self.final_trans = dict()
        self.path_to_module = os.path.dirname(__file__)
        self.weight_path = os.path.join(self.path_to_module, "static", "final_trans.csv")
        with open(self.weight_path, 'r') as ft_file:
            spamreader = csv.reader(ft_file)

            for row in spamreader:
                self.final_trans[row[0]] = row[2]

    def intruser(self, word: str) -> str:
        ready_word = ''
        for char in word:
            ready_word += '-' + self.final_trans[char]
        return ready_word.strip('-')

    def separator(self, text: str) -> str:
        syll_dict = dict()

        with open(self.weight_path, 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            sylls = list(spamreader)
            for s in sylls:
                syll_dict[s[0]] = s[2]

        good_text = ' '
        twit_morph = self.twitter.pos(text, norm=True)

        lil_morphs = ('Josa', 'Suffix', 'Eomi', 'PreEomi')
        end_morphs = ('Exclamation', 'Conjunction', 'Eomi', 'PreEomi')
        bad = ('Foreign', 'Alpha', 'Number', 'Unknown', 'KoreanParticle',
               'Hashtag', 'ScreenName', 'Email', 'URL')

        for entity in twit_morph:
            if entity[1] in lil_morphs:
                if entity[0] == '의':
                    good_text = good_text.strip(" /-#") + '-ɛ#'  # генитив
                else:
                    good_text = good_text.strip(" /-#") + '-' + self.intruser(entity[0]) + '#'

            elif entity[1] in end_morphs:
                if good_text.endswith('/ '):
                    good_text += self.intruser(entity[0]) + ' / '
                else:
                    good_text += self.intruser(entity[0]) + ' / '

            elif entity[1] == 'Adjective' or entity[1] == 'Verb':
                # отглагольные существительные должны вести себя как
                # существительные
                if entity[0].endswith('ki'):
                    good_text += self.intruser(entity[0]) + '#'
                else:
                    tr = self.intruser(entity[0])
                    if 'ɾ-ke-jo' in tr:
                        # ㄹ게요
                        rtr = ''.join(reversed(list(tr)))
                        rtr = rtr.replace('ek-ɾ', 'ek͈-ɾ', 1)
                        tr = ''.join(reversed(list(rtr)))

                    elif 'ɾ-kʌ-jɐ' in tr or 'ɾ-kʌ-je-jo' in tr:
                        # ㄹ거(예요 / 야)
                        rtr = ''.join(reversed(list(tr)))
                        rtr = rtr.replace('ʌk-ɾ', 'ʌk͈-ɾ', 1)
                        tr = ''.join(reversed(list(rtr)))

                    elif 'm-tɐ-ko' in tr or 'm-tɐ /' in tr:
                        # ㅁ다
                        rtr = ''.join(reversed(list(tr)))
                        rtr = rtr.replace('ɐt-m', 'ɐt͈-m', 1)
                        tr = ''.join(reversed(list(rtr)))

                    # проверяем, аттрибутивное или предикативное употребление
                    if 'ETD' in self.kkma.pos(entity[0])[-1][1]:
                        good_text += tr + '#'
                    else:
                        good_text += tr + ' / '
            elif entity[1] == 'Punctuation':
                good_text = good_text.strip(" /-#") + ' / '
            elif entity[1] in bad:
                pass

            else:
                good_text += self.intruser(entity[0]) + '#'

        return good_text.strip(' /#') + ' / '
