import re


class Rules():

    def __init__(self):
        pass

    def exceptions(self, given):  # must be first!!
        # сюда можно записать все исключения (и ханчу и риыль тоже)

        # 덕분에
        given = given.replace('tʌk-pun-e', 't͈ʌk-pun-e')
        return given

    def palatalization(self, given):  # must be second!!
        to_pal = ['k', 'g', 'l', 'ɾ', 'm', 'p', 's', 'ŋ', 'cʰ', 'kʰ', 'tʰ', 'pʰ',
                  't', 'n', 'h', 'k͈', 't͈', 'p͈', 's͈', 'c͈', 'ɦ']

        front_row = ['i', 'e']

        for tp in to_pal:
            # гласные переднего ряда
            for fr in front_row:
                given = given.replace(tp + '-' + fr, tp + 'ʲ-' + fr)
                given = given.replace(tp + fr, tp + 'ʲ' + fr)

            # йотированные гласные
            given = given.replace(tp + '-j', tp + 'ʲ-')

        return given

    def yi(self, given):
        # читает ый
        res = ''
        for i in range(len(given)):
            if given[i] == 'ы':
                if given[i - 1] == '/':
                    res += 'ɰi'
                else:
                    res += 'i'
            else:
                res += given[i]
        return res

    def liquids(self, given):
        vowels = ['ɐ', 'ʌ', 'o', 'ɨ', 'u', 'i', 'ɛ', 'e', 'ɰi']
        given = given.replace('ɾ', 'l')
        for v in vowels:
            given = given.replace('l' + v, 'ɾ' + v)
            given = given.replace('l-' + v, 'ɾ-' + v)
            # нечитаемое ㅎ
            given = given.replace('lh-' + v, 'ɾ-' + v)
            given = given.replace('l-h' + v, 'ɾ-' + v)
        return given

    def aspiration(self, given):

        to_fix_k = ['k-h', 'k͈-h', 'kʰ-h', 'h-k', 'h-k͈', 'h-kʰ']
        to_fix_t = ['t-h', 't͈-h', 'tʰ-h', 'h-t', 'h-t͈', 'h-tʰ']
        to_fix_c = ['c-h', 'c͈-h', 'cʰ-h', 'h-c', 'h-c͈', 'h-cʰ']
        to_fix_p = ['p-h', 'p͈-h', 'pʰ-h', 'h-p', 'h-p͈', 'h-pʰ']

        for k in to_fix_k:
            given = given.replace(k, '-kʰ')
        for t in to_fix_t:
            given = given.replace(t, '-tʰ')
        for c in to_fix_c:
            given = given.replace(c, '-cʰ')
        for p in to_fix_p:
            given = given.replace(p, '-pʰ')

        # нечитаемый ㅎ (с ㄹ разобрались в liquids)
        h_silent = ['m-h', 'n-h', 's-h', 's͈-h',
                    'h-m', 'h-n', 'h-s', 'h-s͈', 'ŋ-h']
        for h in h_silent:
            hh = h.replace('h', '')
            given = given.replace(h, hh)

        return given

    def stop_assim(self, given):
        # ассимиляция взрывных перед сонорными
        seps = ['-', '#']
        sonors = ['m', 'n']
        stops_to_sonors = {'m': ['p', 'pʰ', 'p͈', 'lb', 'ps'],
                           'n': ['t', 'tʰ', 't͈', 'c', 'cʰ', 'c͈', 's', 's͈'],
                           'ŋ': ['k', 'kʰ', 'k͈', 'lg', 'ks'],
                           }
        for s in seps:
            chunks = given.split(s)
            for i in range(len(chunks) - 1):
                for k, v in stops_to_sonors.items():
                    bgram = re.search(r'(lg|ps|ks|lb|cʰ|kʰ|tʰ|pʰ|t͈|k͈|p͈|c͈)', chunks[i][-2:])
                    if bgram is None:
                        if chunks[i][-1] in v and chunks[i + 1][0] == 'ɾ':
                            chunks[i] = chunks[i][:-1] + k
                            chunks[i + 1] = 'n' + chunks[i + 1][1:]

                        elif chunks[i][-1] in v and chunks[i + 1][0] in sonors:
                            chunks[i] = chunks[i][:-1] + k
                    else:
                        if bgram.group(1) in v and chunks[i + 1][0] == 'ɾ':
                            chunks[i] = chunks[i][:-2] + k
                            chunks[i + 1] = 'n' + chunks[i + 1][1:]

                        elif bgram.group(1) in v and chunks[i + 1][0] in sonors:
                            chunks[i] = chunks[i][:-2] + k
            given = s.join(chunks)

        return given

    def spirantization(self, given):
        seps = ['-', '#']
        for s in seps:
            chunks = given.split(s)
            for i in range(len(chunks) - 1):
                if chunks[i][-1] in ['t', 'tʰ', 't͈'] and chunks[i + 1][0] in ['s', 's͈']:
                    chunks[i] = chunks[i][:-1] + 's'

            given = s.join(chunks)

        return given

    def sonor_assim(self, given):
        # после stop_assim
        # ассимиляция сонорных ㄹ-ㄴ, ㅁ/ㄴ-ㄹ
        seps = ['-', '#']
        final_sonor = ['m', 'ŋ']
        for s in seps:
            chunks = given.split(s)
            for i in range(len(chunks) - 1):
                if chunks[i][-1] == 'ɾ' and chunks[i + 1][0] == 'n':
                    chunks[i] = chunks[i][:-1] + 'l'
                    chunks[i + 1] = 'l' + chunks[i + 1][1:]

                elif chunks[i][-1] == 'n' and chunks[i + 1][0] == 'ɾ':
                    chunks[i] = chunks[i][:-1] + 'l'
                    chunks[i + 1] = 'l' + chunks[i + 1][1:]

                elif chunks[i][-1] in final_sonor and chunks[i + 1][0] == 'ɾ':
                    chunks[i + 1] = 'n' + chunks[i + 1][1:]
            given = s.join(chunks)

        return given

    def coronal_assim(self, given):
        # ассимиляция переднеязычных

        seps = ['-', '#']
        coronals = ['t', 't͈', 'tʰ', 's', 's͈']

        labial = ['m', 'p', 'pʰ', 'p͈']
        post_alveolar = ['cʰ', 'c', 'c͈']
        velars = ['k', 'kʰ', 'k͈', 'g']
        for s in seps:
            chunks = given.split(s)
            for i in range(len(chunks) - 1):
                # before labial
                if chunks[i][-1] in coronals and chunks[i + 1][0] in labial and chunks[i + 1][0] != 'm':
                    chunks[i] = chunks[i][:-1] + 'p'

                elif chunks[i][-1] == 'n' and chunks[i + 1][0] in labial and chunks[i + 1][0] != 'm':
                    chunks[i] = chunks[i][:-1] + 'm'

                # before velars
                elif chunks[i][-1] in coronals and chunks[i + 1][0] in velars:
                    chunks[i] = chunks[i][:-1] + 'k'

                elif chunks[i][-1] == 'n' and chunks[i + 1][0] in velars:
                    chunks[i] = chunks[i][:-1] + 'ŋ'

                # before post_alveolar
                elif chunks[i][-1] in coronals and chunks[i + 1][0] in post_alveolar:
                    chunks[i] = chunks[i][:-1] + 'c'

                # labials and post alveolars assimilate to velars
                elif chunks[i][-1] in labial and chunks[i + 1][0] in velars and chunks[i][-1] != 'm':
                    chunks[i] = chunks[i][:-1] + 'k'

                elif chunks[i][-1] in labial and chunks[i + 1][0] in velars and chunks[i][-1] == 'm':
                    chunks[i] = chunks[i][:-1] + 'ŋ'

                elif chunks[i][-1] in post_alveolar and chunks[i + 1][0] in velars:
                    chunks[i] = chunks[i][:-1] + 'k'
            given = s.join(chunks)

        return given
      
      
    def patchims(given):
        # чтение патчимов
        seps = ['-', '#']
        vowels = ['ɐ', 'ʌ', 'o', 'ɨ', 'u', 'i', 'ɛ', 'e', 'ɰi']
        excepted = {'nʌlb': 'nʌp', 'pɐlb': 'pɐp'}
        first = {'ks': 'k', 'lg': 'k', 'nɟ': 'n', 'nh': 'n', 'lm': 'm', 
                 'lb': 'l', 'ls': 'l', 'ltʰ': 'l', 'lh': 'l',
                 'lpʰ': 'p', 'ps': 'p'}
        second = {'t͈': 't', 'tʰ': 't', 's': 't', 's͈': 't', 'cʰ': 't', 'c': 't', 'c͈': 't', 'h': 't'}
        # конец слога перед согласной
        for s in seps:
            chunks = given.split(s)
            for i in range(len(chunks) - 1):
      
                if chunks[i + 1][0] not in vowels:
                    for root in excepted.keys():  # проверка на исключения
                        if root in chunks[i]:
                            chunks[i] = excepted[root]
                    for patchim in first.keys():
                        if chunks[i].endswith(patchim):
                            chunks[i] = chunks[i].replace(patchim, first[patchim])
                    for patchim in second.keys():
                        if chunks[i].endswith(patchim):
                            chunks[i] = chunks[i].replace(patchim, second[patchim])
            given = s.join(chunks)
        # абсолютный конец
        for root in excepted.keys():
            given = given.replace(root + ' / ', excepted[root] + ' / ')
        for patchim in first.keys():
            given = given.replace(patchim + ' / ', first[patchim] + ' / ')
        for patchim in second.keys():
            given = given.replace(patchim + ' / ', second[patchim] + ' / ')
        return given


    def voicing_and_h(self, given):  # должно быть после патчимов
     # фонетические переходы в позиции между гласными
        vowels = ['ɐ', 'ʌ', 'o', 'ɨ', 'u', 'i', 'ɛ', 'e', 'ɰi']
        to_voice = {'c': 'ɟ', 'k': 'g', 't': 'd', 'p': 'b', 'h': 'ɦ',
                    'cʲ': 'ɟʲ', 'kʲ': 'gʲ', 'tʲ': 'dʲ', 'pʲ': 'bʲ'}
        for tv in to_voice.keys():
            voiced = to_voice[tv]
            for v1 in vowels:
                for v2 in vowels:
                    given = given.replace(v1 + tv + '-' + v2, v1 + voiced + '-' + v2)
                    given = given.replace(v1 + '-' + tv + v2, v1 + '-' + voiced + v2)
                
                sonors = ['l', 'm', 'n', 'ŋ']         
                if tv != 'h':
                    for son in sonors:
                        given = given.replace(son + '-' + tv + v1, son + '-' + voiced + v1)
                        given = given.replace(son + '#' + tv + v1, son + '#' + voiced + v1)

        return given

    def pot(self, given):  # должно быть в самом конце
        obstr = ['k', 'p', 'c', 'cʰ', 'kʰ', 'tʰ',
                 'pʰ', 't', 'k͈', 't͈', 'p͈', 'c͈']
        for obs in obstr:
            given = given.replace(obs + '-k', obs + '-k͈')
            given = given.replace(obs + '-t', obs + '-t͈')
            given = given.replace(obs + '-p', obs + '-p͈')
            given = given.replace(obs + '-c', obs + '-c͈')

        return given
