import nltk
import re


def clean(txt):
    txt = txt.lower()
    txt = re.sub(r"[^a-zA-Z|'\s]", ' ', txt)  # To eliminate punctuation and whitespace.
    txt = re.sub(r"[']", '-', txt)  # naive approach to avoid errors words like bird's in string call
    return txt


def bigram_clean(txtb):
    txtb = " ".join(txtb.split())  # for eliminate whitespace.
    txtb = txtb.lower()
    txtb = re.sub(r'[0-9|,;"]', " ", txtb)  # To eliminate numbers and point marks.
    txtb = re.sub(r"[']", '-', txtb)  # naive approach to avoid errors words like bird's in string call
    return txtb


def add_stop_symbol(word_list):  # to add stop signs - please read the readme file.
    for index, word in enumerate(word_list):
        if re.match(r"[.!?]+(\")*", word):
            word_list[index] = '<s>'
            word_list.insert(index, '</s>')
    word_list.insert(0, word_list.pop())
    return word_list


file_path = input('Enter File Name (Without File Extension):')
file_path = file_path + '.txt'  # Include file extension - no control

# Reading file
hw1 = open(file_path, 'r')
txt = hw1.read()

# finding sentence numbers
cumleler = nltk.sent_tokenize(txt, language='English')
cumle_sayısı = len(cumleler)
print('Number of Sentences in Test File ', cumle_sayısı)

# Finding word counts
clean_txt = clean(txt)
kelimeler = nltk.word_tokenize(clean_txt)
kelime_sayısı = len(kelimeler)
print('Number of Total Tokens: ', kelime_sayısı)

# find the frequency of  words
kelime_frekans = {}
for i in kelimeler:
    if isinstance(i, str):  # Is the word made up of letters?
        if i in kelime_frekans:
            kelime_frekans[i] += 1
        else:
            kelime_frekans[i] = 1

# Unique word counts
unique_sayısı = len(kelime_frekans.keys())
print('Number of Unique Words (Vocabulary Size):', unique_sayısı)

# unigrams with highest frequencies
sorted_words = sorted(kelime_frekans.items(), key=lambda x: x[1], reverse=True)  # sorting dictionary
print("""\nTop 10 Unigrams with Highest Frequencies:
Unigram1 - ItsCount - ItsProbabibility""")

if len(sorted_words) >= 10:  # to avoid out of range.
    z = 0
    for i, j in sorted_words:
        if z < 10:
            print(i, '-', j, '-', j / kelime_sayısı)
            z += 1
else:

    for i, j in sorted_words:
        print(i, '-', j, '-', j / kelime_sayısı)

# bigram
txtb = bigram_clean(txt)
word_list = nltk.word_tokenize(txtb)  # separation into words. There is point mark.
word_list = add_stop_symbol(word_list)  # for  add stop signs.

bigram_list = (nltk.ngrams(word_list, 2))  # bigram list
bigram = {}

for i in bigram_list:
    if i in bigram:
        bigram[i] += 1
    else:
        bigram[i] = 1

bigram.pop(('</s>', '<s>'))  # Deleting the meaningless bigram from the list.

sorted_bigram = sorted(bigram.items(), key=lambda x: x[1], reverse=True)  # Sorting Bigrams

print("""\nTop 10 Bigrams with Highest Frequencies:
Bigram1 - ItsCount - ItsProbabibility""")

z = 0
for i, j in sorted_bigram:
    if z < 10:
        if i[0] == '</s>' or i[0] == '<s>':
            print(i, '-', j, '-', j / cumle_sayısı)
            z += 1
        else:
            ilk_kelime = i[0]
            print(i, '-', j, '-', j / kelime_frekans[ilk_kelime])
            z += 1

# smoothing section

#  finding  three lowest frequency words
en_az_gecen = []
for i in range(len(sorted_words) - 1, len(sorted_words) - 4, -1):
    en_az_gecen.append(sorted_words[i][0])

txts = txt

for i in en_az_gecen:  # for replace three lowest frequency words
    txts = txts.replace(i, 'UNK')

txtsb = txts  # backed up the modified text so that the dot marks do not disappear when tokenize.

txts = clean(txts)  # clear before new word count. Point marks disappeared

smooth_words = nltk.word_tokenize(txts)
# how often words occur after smooth
smooth_frekans = {}
for i in smooth_words:
    if isinstance(i, str):  # Is the word made up of letters?
        if i in smooth_frekans:
            smooth_frekans[i] += 1
        else:
            smooth_frekans[i] = 1

yeni_unique_sayısı = len(smooth_frekans.keys())

txtsb = bigram_clean(txtsb)
smooth_word_list = nltk.word_tokenize(txtsb)  # separation into words. There is point mark.
smooth_word_list = add_stop_symbol(smooth_word_list)  # for add stop signs.

smooth_bigram_list = (nltk.ngrams(smooth_word_list, 2))  # bigram list
smooth_bigram = {}

for i in smooth_bigram_list:
    if i in smooth_bigram:
        smooth_bigram[i] += 1
    else:
        smooth_bigram[i] = 1

smooth_bigram.pop(('</s>', '<s>'))  # Deleting the meaningless bigram from the list.

smooth_sorted_bigram = sorted(smooth_bigram.items(), key=lambda x: x[1],
                              reverse=True)  # sortin bigram's list

print("""\nAfter UNK addition and Smoothing Operations Top 10 Bigrams with Highest Frequencies:
Bigram - ItsCount - ItsProbabibility
""")

k = 0.5  # k smooth

smooth_prob = {}  # to store probability values in the dictionary.

for i, j in smooth_sorted_bigram:

    if i[0] == '</s>' or i[0] == '<s>':
        smooth_prob[i] = (j + k) / (cumle_sayısı + (yeni_unique_sayısı * k))

    else:
        ilk_kelime = i[0]
        smooth_prob[i] = (j + k) / (smooth_frekans[ilk_kelime] + (yeni_unique_sayısı * k))

z = 0  # for not to lose the frequency of the bigrams.
for i, j in smooth_sorted_bigram:
    if z < 10:
        if i[0] == '</s>' or i[0] == '<s>':
            print(i, '-', j, '-', (j + k) / (cumle_sayısı + (yeni_unique_sayısı * k)))
            z += 1
        else:
            ilk_kelime = i[0]
            print(i, '-', j, '-', (j + k) / (smooth_frekans[ilk_kelime] + yeni_unique_sayısı * k))
            z += 1

# Sample sentence..
r = 1
while r <= 2:
    c = input("""


    SampleSentence1 : """)

    cb = bigram_clean(c)  # cleaning
    cb_word_list = nltk.word_tokenize(cb)
    cb_word_list = add_stop_symbol(cb_word_list)

    # Replacing words not in the word list with 'unk'.
    for i in range(len(cb_word_list)):
        if cb_word_list[i] == '<s>' or cb_word_list[i] == '</s>':
            pass
        else:
            if cb_word_list[i] not in smooth_frekans:
                cb_word_list[i] = 'unk'

    cumle_bigram_list = (nltk.ngrams(cb_word_list, 2))  # bigram's list

    p = 1  # prob

    for i in cumle_bigram_list:
        if i in smooth_prob:  # Are there any calculated bigrams in the text?
            p *= smooth_prob[i]

        elif i[0] == '</s>' or i[0] == '<s>':
            p *= k / (cumle_sayısı + (yeni_unique_sayısı * k))
        else:
            ilk_kelime = i[0]
            p *= k / (smooth_frekans[ilk_kelime] + (yeni_unique_sayısı * k))

    print(f'\t{r}. ItsComputeProbability= ', p)

    r += 1
