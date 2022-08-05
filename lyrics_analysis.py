import urllib.request
from bs4 import BeautifulSoup
import re
import time
import codecs
import csv
import MeCab
import os

# test_url = 'http://j-lyric.net/artist/a0560d3/l04d4da.html'
test_url = 'https://j-lyric.net/artist/a0560d3/l05603c.html'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_nega_posi_dict() -> dict:
    with codecs.open(os.path.join(__location__, "./data_set/yougenList.csv"), 'r', 'utf-8') as fp:
        reader = csv.reader(fp, delimiter=',', lineterminator='\n')
        negaPosiDic = {}
        for i, x in enumerate(reader):
            y = x[0].split(' ')
            negaPosiDic[y[1]] = y[0]

    with codecs.open(os.path.join(__location__, "./data_set/nounList.csv"), 'r', 'utf-8') as fp:
        reader = csv.reader(fp, delimiter=',', lineterminator='\n')
        for _, x in enumerate(reader):
            y = x[0].split(' ')
            negaPosiDic[y[1]] = y[0]
    return negaPosiDic


def nlp(data: str) -> int:
    # NEologd辞書を用いる場合はコメントを外す
    # nm = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    nm = MeCab.Tagger()
    points = 0
    negaposi_dic = get_nega_posi_dict()
    sentenses = re.split("[。！!？?（）w]", data)
    try:
        for sentense in sentenses:
            negaposi = 0
            result_all = nm.parse(sentense)
            result_words = result_all.split('\n')[:-1]
            for word in result_words:
                try:
                    word_toarray = re.split('[\t,]', word)

                    if word_toarray[0] in ('\3000', 'EOS'):
                        continue

                    if word_toarray[7] in negaposi_dic:
                        negaposi += int(negaposi_dic[word_toarray[7]])
                        print(word_toarray[7], negaposi_dic[word_toarray[7]], flush=True)
                except Exception as e:
                    print('%r' % e, flush=True)
            points += negaposi
    except Exception as e:
        print('%r' % e, flush=True)
        print(data, flush=True)
    return points


if __name__ == '__main__':
    response = urllib.request.urlopen(test_url)
    # お作法
    time.sleep(3)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')
    select = soup.find("p", id="Lyric")
    lyric = re.sub('<p id="Lyric">', '', str(select)).replace('<br/>', '').replace('</p>', '')

    print(lyric)
    review = nlp(lyric)
    print(f'合計pt: {review}')
