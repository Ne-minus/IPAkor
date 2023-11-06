# How to use IPAkor

Authors: Alina Lobanova, Ekaterina Neminova, Varvara Vasilyeva, Alyona Zenina.

This is how our Python library IPAkor works:

```
! pip install IPAkor
import IPAkor
transcr = IPAkor.Transcription()
print(transcr.transcribe('이해할수 있어요? 설악산의 높은 뭐예요?'))
```
You will get the following result: i-ɦɛ#hɐl-su / is͈-ʌ-jo / sʌɾ-ɐk-sɐn-ɛ#nopʰ-ɨn#mwʌ-je-jo / 

# Korean IPA automatic transcription
Our transcription is based on rules. You can see them in the way generative phonology would prescribe them below.

We believe the transcription to represent the South Korean standard language.

## Phonemes
Currently we took phonems from \[4\]. You can see how syllables correspond to transcription BEFORE any rules are applied in final_trans.csv.
However, we are aware that these might be not the best options, so we will work on it later.

## The rules

### Position rules
c → t / _ #, c͈ → t / _ #, cʰ → t / _ #

h → t / _ #, s → t /_ #, s͈ → t / _ #

h → ɦ / V _ V

We also handled position dependent readings of ㄹ and ㅢ.

### Assimilation
- by aspiration

k → kʰ/h_, t → tʰ/h_, p → pʰ/h_

k → kʰ/_h, t → tʰ/_h, p → pʰ/_h

- by way of articulation

t → s/_s

n → l / _ l, n → l / l _, t → l / _ l

p, pʰ, pp → m/_m; p, pʰ, pp → m/_n 

t, tʰ, tt → n/_m; t, tʰ, tt → n/_n 

k, kʰ, kk → ŋ/_m; k, kʰ, kk → ŋ/_n 

- by place of articulation

t → p/_p, t → c/_c

n → ŋ/_k, m → ŋ/_k

c → k/_k, t → k/_k, p → k/_k

n → m/_p

### Palatalization
All consonants become palatalized before \[i\] and \[e\].

### Post-Obstruent Tensification (POT)
After obstruents, other obstruents become tense (for example: t → t͈/p_). 
We won't be listing all rules due to big number of combinanions.

### Grammar-specific rules
Grammar analysis was made with Twitter morphological parser by https://konlpy.org .

Genitive is transcripted as \[ɛ\].

We prevent voicing in grammars:
- ㄹ게요, 
- ㄹ거(예요/야)
- ㅁ다 in predicates
- 덕분에

Please, let us know if any grammar that should have voicing by rules but in reality doesn't comes to your mind.

## Challenges


### Voicing
Voicing is not a phonological feature in Korean. "Weak" vowels are sometimes voiced and sometimes aren't. 
They (almost) always are between vowels or sonorants inside one words (남자, 오기). But between words it's not always the case.


According to \[3\], Korean sonority is a continuum with /k/, /t/, /p/ having ~0% chances of being voiced phrase initially and much higher between syllables of one word.
We took this idea to make the voicing rules.

We use https://konlpy.org Twitter morphological parser to predict (based on our own rules) where the phonetic word begins and ends. 
This part is quite sophisticated and we are yet to test and develop it. Probably a separate reaserch would be needed.

### Yet to be done
1. Spiritization of ㅅ(s) and ㅈ(c) classes before \[i\] and such.
2. Some rules work differently before plain vowels and diphthongs.
3. Merge several same class consonants into one.
4. Change some symbols to more IPA-appropriate.

### What we ignored
1. Words like 지하철역, 알약, 십육 which have ethymological ㄹ in place of written ㅇ, are read as if they don't have ethymological ㄹ.
2. Originally Chinese words that do not have voicing (like 길가) do have it in our transcription.

If you have a list of words of either group, feel free to share with us.
 

## Sources
We mainly used the following sources:
1. Yu Cho, Y.  Korean Phonetics and Phonology. Oxford Research Encyclopedia of Linguistics, 2022.
2. Касаткина И. Л., Чон Ин Сун, Пентюхова В. Е. Учебник корейского языка. М.: ООО НИЦ "Инженер", 2012.
3. Sun-Ah Jun. The Status of the Lenis Stop Voicing Rule in Korean. Theoretical Issues in Korean Linguistics, 1994.
4. Ho-Min Sohn. The Korean Language. Cambridge Language Surveys, Cambridge University Press, 1999.

