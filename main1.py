import math
import sys


def char_frequency(text):
    length = len(text)
    cf = {}
    for ch in alphabet:
        cf[ch] = text.count(ch) / length
    return cf


def char_entropy(cf):
    ce = {}
    allce = 0
    for ch in cf.items():
        ce[ch[0]] = ch[1] * (-(math.log(ch[1], 2)))
        allce += ce[ch[0]]
    print('\nH1 = {}'.format(allce))
    return ce


def bigram_frequency_intersection(text):
    bif = {}
    bil = 0
    for ch1 in alphabet:
        for ch2 in alphabet:
            bil += text.count(ch1 + ch2)
    for ch1 in alphabet:
        for ch2 in alphabet:
            bif[ch1 + ch2] = text.count(ch1 + ch2) / bil
            if bif[ch1 + ch2] == 0:
                bif[ch1 + ch2] += sys.float_info.min
    return bif


def bigram_entropy_intersection(bif):
    bie = {}
    allbie = 0
    for ch in bif.items():
        bie[ch[0]] = ch[1] * (-(math.log(ch[1], 2)))
        allbie += bie[ch[0]]
    allbie = allbie / 2
    print('\nintersection H2 = {}'.format(allbie))
    return bie


def bigram_frequency_nintersection(text):
    bif = {}
    bil = 0
    for i in range(0, len(text) - 1, 2):
        bil += 1
    for ch1 in alphabet:
        for ch2 in alphabet:
            bif[ch1 + ch2] = sys.float_info.min
    for i in range(0, len(text) - 1, 2):
        bif[text[i:i + 2]] += 1
    for ch1 in alphabet:
        for ch2 in alphabet:
            bif[ch1 + ch2] /= bil
    return bif


def bigram_entropy_nintersection(bif):
    bie = {}
    allbie = 0
    for ch in bif.items():
        bie[ch[0]] = ch[1] * (-(math.log(ch[1], 2)))
        allbie += bie[ch[0]]
    allbie = allbie / 2
    print('\nnon intersection H2 = {}'.format(allbie))
    return bie


def bigram_frequency_with_space(text):
    bif = {}
    bil = 0
    for ch1 in alphabet_space:
        for ch2 in alphabet_space:
            bil += text.count(ch1 + ch2)
    for ch1 in alphabet_space:
        for ch2 in alphabet_space:
            bif[ch1 + ch2] = text.count(ch1 + ch2) / bil
            if bif[ch1 + ch2] == 0:
                bif[ch1 + ch2] += sys.float_info.min
    return bif


def bigram_entropy_with_space(bif):
    bie = {}
    allbie = 0
    for ch in bif.items():
        bie[ch[0]] = ch[1] * (-(math.log(ch[1], 2)))
        allbie += bie[ch[0]]
    allbie = allbie / 2
    print('\nwith space H2 = {}'.format(allbie))
    return bie


def print_char_info(char_frequency, char_entropy):
    print('\n{} {:^10}\t{:^15}'.format('Char', 'Frequency', 'Entropy'))
    for item in sorted(char_frequency.items(), key=lambda fr: fr[1], reverse=True):
        print('{:^4} {:7f}\t{:.15f}'.format(item[0], item[1], char_entropy[item[0]]))


def print_bigram_frequency(bigram_frequency, alphabet_of):
    for ch in alphabet_of:
        print('{:^9s}'.format(ch), end='')
    print()
    for c1 in alphabet_of:
        print('{:s} '.format(c1), end='')
        for c2 in alphabet_of:
            s = '{:.5f}'.format(bigram_frequency[c1 + c2])
            print('{:^9s}'.format(s), end='')
        print()


def print_bigram_entropy(bigram_entropy, alphabet_of):
    for ch in alphabet_of:
        print('{:^9s}'.format(ch), end='')
    print()
    for c1 in alphabet_of:
        print('{:s} '.format(c1), end='')
        for c2 in alphabet_of:
            s = '{:.5f}'.format(bigram_entropy[c1 + c2])
            print('{:>9s}'.format(s), end='')
        print()


def encrypt_by_key(text, key):
    k, m, l = len(key), len(alphabet), len(text)
    encrypt = ''
    for i in range(0, l):
        encrypt += alphabet[(alphabet.index(text[i]) + alphabet.index(key[i % k])) % m]
    return encrypt


def decrypt_by_key(text, key):
    k, m, l = len(key), len(alphabet), len(text)
    decrypt = ''
    for i in range(0, l):
        decrypt += alphabet[(alphabet.index(text[i]) - alphabet.index(key[i % k])) % m]
    return decrypt


def lenght_key_short(text):
    key_len = 5
    index = {}
    tmp_index = []
    for ch in alphabet:
        for i in range(0, len(text), key_len):
            tmp_index.append(
                (text[i:i + key_len].count(ch) * (text[i:i + key_len].count(ch) - 1)) / (key_len * (key_len - 1)))
        index[ch] = sum(tmp_index) / len(tmp_index)
    return alphabet.index(max(index.items(), key=lambda kv: kv[1])[0])


def lenght_key_long(text):
    kl = {}
    for key_len in range(6, 33):
        counter = 0
        for i in range(key_len):
            tmp_text = text[i::key_len]
            for j in range(len(tmp_text) - 1):
                if tmp_text[j] == tmp_text[j + 1]:
                    counter += 1
                kl[key_len] = counter
    print('\n', kl, '\n')
    return max(kl.items(), key=lambda kv: kv[1])[0]


def decrypt_text(text, key_len):
    count, ck, key = {}, {}, {}
    m, l = len(alphabet), len(text)
    decrypt = ''
    for i in range(key_len):
        tmp_text = text[i::key_len]
        for ch in alphabet:
            count[ch] = tmp_text.count(ch)
        ck[i] = sorted(count.items(), key=lambda kv: kv[1], reverse=True)[0][0]
        key[i] = alphabet[(alphabet.index(ck[i]) - alphabet.index('о')) % m]
    print(key.items())
    for i in range(l):
        decrypt += alphabet[(alphabet.index(text[i]) - alphabet.index(key[i % key_len])) % m]
    print(decrypt)


def conformity_index(text):
    index = 0
    for ch in alphabet:
        index += (text.count(ch) * (text.count(ch) - 1)) / (len(text) * (len(text) - 1))
    return index


def redundancy_language(alphabet):
    Hinf = 0.70227
    H0 = math.log(len(alphabet), 2)
    redund_lang = 1 - Hinf / H0
    return redund_lang


alphabet = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з',
            'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
            'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
            'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я')
alphabet_space = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з',
                  'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
                  'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
                  'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' ')

with open("secret_text") as file:
    data = file.read().lower().replace('ё', 'е')
    for c in data:
        if c not in alphabet:
            data = data.replace(c, '')

# with open("solyaris.txt") as file:
#     data_temp = file.read().lower().replace('ё', 'е')
#     for c in data_temp:
#         if c not in alphabet:
#             data_temp = data_temp.replace(c, '')

# with open("solyaris.txt") as file:
#     data_temp = file.read().lower().replace('ё', 'е')
#     for c in data_temp:
#         if c not in alphabet_space:
#             data_temp = data_temp.replace(c, '').replace('  ', ' ')
#
with open("solyaris1.txt") as file: # text without any symbol accept alphabet
    data1 = file.read()

with open("solyaris2.txt") as file: # text without any symbol accept alphabet and space
    data2 = file.read()

with open("open_text") as file:
    data3 = file.read()
    for ch in data3:
        if ch not in alphabet:
            data3 = data3.replace(ch, '')

# print('\n', ' Table of char Frequency and Entropy', '\n')
# print_char_info(char_frequency(data1), char_entropy(char_frequency(data1)))
# print('\n', ' Table of bigramm Frequency Non Intersection ', '\n')
# print_bigram_frequency(bigram_frequency_nintersection(data1), alphabet)
# print('\n', ' Table of bigramm Entropy Non Intersection ', '\n')
# print_bigram_entropy(bigram_entropy_nintersection(bigram_frequency_nintersection(data1)), alphabet)
# print('\n', ' Table of bigramm Frequency Intersection ', '\n')
# print_bigram_frequency(bigram_frequency_intersection(data1), alphabet)
# print('\n',  'Table of bigramm Entropy Intersection', '\n')
# print_bigram_entropy(bigram_entropy_intersection(bigram_frequency_intersection(data1)), alphabet)
# print('\n', ' Table of bigramm Frequency With Space ', '\n')
# print_bigram_frequency(bigram_frequency_with_space(data2), alphabet_space)
# print('\n', 'Table of bigramm Entropy With Space ', '\n')
# print_bigram_entropy(bigram_entropy_with_space(bigram_frequency_with_space(data2)), alphabet_space)
# key = "делолисоборотней"
# encr_text = encrypt_by_key(data, key)
# print(decrypt_by_key(encrypt_by_key(data, key), key), '\n')
# print(lenght_key_short(encr_text))
# print(lenght_key_long(data))
# print(decrypt_by_key(data, key), '\n')
key_lenght = lenght_key_long(data)
decrypt_text(data, key_lenght)
key_temp1, key_temp2, key_temp3, key_temp4, key_temp5 = "ку", "хай", "пока", "привет", "какделанормально"
# print(' Conformity Index of not crypted text: = {}'.format(conformity_index(data3)))
# print(' Conformity Index of crypted text by key len {}: = {}'.format(len(key_temp1), conformity_index(encrypt_by_key(data3, key_temp1))))
# print(' Conformity Index of crypted text by key len {}: = {}'.format(len(key_temp2), conformity_index(encrypt_by_key(data3, key_temp2))))
# print(' Conformity Index of crypted text by key len {}: = {}'.format(len(key_temp3), conformity_index(encrypt_by_key(data3, key_temp3))))
# print(' Conformity Index of crypted text by key len {}: = {}'.format(len(key_temp4), conformity_index(encrypt_by_key(data3, key_temp4))))
# print(' Conformity Index of crypted text by key len {}: = {}'.format(len(key_temp5), conformity_index(encrypt_by_key(data3, key_temp5))))
# print(' Redundancy of language = {}'.format(redundancy_language(alphabet)))
