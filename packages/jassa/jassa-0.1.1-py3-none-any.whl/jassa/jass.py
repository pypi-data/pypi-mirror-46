#jass: Just A Simple Sentiment analysis tool
#Version: 0.1
#Author: Hsin-Min Lu; luim@ntu.edu.tw
#Users Beware: This project was created for pedagogical purpose, and is not suitable for production use.

import os
import jieba
from datetime import datetime
import pandas as pd
import pkg_resources

class jass:
    def __init__(self, debug = False, basedir = "jass_v1/jass"):
        self.pos_words = []
        self.neg_words = []
        self.all_words = []
        self.stopwords = []
        self.sent_threshold = 0.1 #Threshold for postive or negative words
        self.jieba = jieba
        self.jieba.setLogLevel(60)

        #filename = pkg_resources.resource_filename('jass', "data/negation.txt")
        #print("the filename", filename)
        self.basedir = basedir
        #self.basedir = "jass_v1/jass/"
        #self.basedir = "./"

        # negation
        self.negation = []
        #self.negation_fn = os.path.join(self.basedir, "data/negation.txt")
        self.negation_fn = pkg_resources.resource_filename('jass', "data/negation.txt")
        if debug: print("negation_fn = ", self.negation_fn)
        with open(self.negation_fn, 'r', encoding='UTF-8') as file:
            for data in file:
                data = data.strip()
                self.negation.append(data)

        #self.posfn = os.path.join(self.basedir, "data/NTUSD_positive_unicode.txt")
        self.posfn = pkg_resources.resource_filename('jass', "data/NTUSD_positive_unicode.txt")
        if debug: print("posfn = ", self.posfn)
        with open(self.posfn, 'r', encoding='utf16') as file:
            for aphrase in file:
                aphrase = aphrase.strip()
                self.pos_words.append(aphrase)

        #self.negfn = os.path.join(self.basedir, "data/NTUSD_negative_unicode.txt")
        self.negfn = pkg_resources.resource_filename('jass', "data/NTUSD_negative_unicode.txt")
        exclude_neg = ['無法', '不大', '不是', '不會', '不能', '不要', '停止', '沒有', '絕不', '缺乏', '缺少', '難以']
        if debug: print("negfn = ", self.negfn)
        with open(self.negfn, 'r', encoding='utf16') as file:
            for aphrase in file:
                aphrase = aphrase.strip()
                if aphrase not in exclude_neg:
                    self.neg_words.append(aphrase)

        #self.cvawfn = os.path.join(self.basedir, "data/cvaw3.csv")
        self.cvawfn = pkg_resources.resource_filename('jass', "data/cvaw3.csv")
        self.cvaw = pd.read_csv(self.cvawfn, encoding='utf-8')
        self.cvaw.columns = ['no', 'word', 'valence', 'valence_sd', 'arousal', 'arousal_sd', 'freq']

        self.cvaw = self.cvaw.loc[:, ['word', 'valence', 'arousal', 'freq']].copy()
        self.cvaw['valence'] = (self.cvaw['valence'] - 5) / 4
        self.cvaw['arousal'] = (self.cvaw['arousal'] - 1) / 8

        self.cvaw_dict = dict()
        for arow in self.cvaw.iterrows():
            if arow[1]['word'] not in self.negation:
                self.cvaw_dict[arow[1]['word']] = arow[1]['valence']


        #self.antusdfn = os.path.join(self.basedir, "data/ANTUSD_unicode/opinion_word.csv")
        self.antusdfn = pkg_resources.resource_filename('jass', "data/ANTUSD_unicode/opinion_word.csv")
        antusd = pd.read_csv(self.antusdfn, encoding='utf-16', header=None)
        # 1. Score: the CopeOpi numerical sentiment score
        # 2. Pos: the number of positive annotations
        # 3. Neu: the number of neutral annotations
        # 4. Neg: the number of negative annotations
        # 5. Non: non-opinionated annotations
        # 6. Not: not-a-word annotations (which is collected from real online segmented data)
        antusd.columns = ['word', 'score', 'pos', 'neu', 'neg', 'non', 'not']

        self.antusd_dict = dict()
        for arow in antusd.iterrows():
            self.antusd_dict[arow[1]['word']] = arow[1]['score']


        #self.word_dictfn = os.path.join(self.basedir, "data/dict.txt")
        self.word_dictfn = pkg_resources.resource_filename('jass', "data/dict.txt")
        if debug: print("word_dictfn = ", self.word_dictfn)
        with open(self.word_dictfn, 'r', encoding='utf-8') as file:
            for aline in file:
                aline = aline.strip()
                aword = aline.split(" ")[0]
                self.all_words.append(aword)

        #self.stopword_fn = os.path.join(self.basedir, "data/stopwords_chn.txt")
        self.stopword_fn = pkg_resources.resource_filename('jass', "data/stopwords_chn.txt")
        if debug: print("stopword_fn = ", self.stopword_fn)
        with open(self.stopword_fn, 'r', encoding='UTF-8') as file:
            for data in file:
                data = data.strip()
                self.stopwords.append(data)

        self.stopwords.append(".")
        self.stopwords.append("丶")
        self.stopwords.append("(")  # 半形括號
        self.stopwords.append(")")  # 半形括號
        self.stopwords.append("[")
        self.stopwords.append("]")
        self.stopwords.append(";")
        self.stopwords.append("-")
        self.stopwords.append(",")
        self.stopwords.append("!")
        self.stopwords.append("=")
        self.stopwords.append("＝")
        self.stopwords.append("～")
        self.stopwords.append("】")
        self.stopwords.append("【")
        self.stopwords.append("'")
        self.stopwords.append("...")
        self.stopwords.append("....")
        self.stopwords.append(".....")
        self.stopwords.append("......")
        self.stopwords.append("*")
        self.stopwords.append("+")
        self.stopwords.append("^")
        self.stopwords.append("/")
        self.stopwords.append("\"")
        self.stopwords.append("\\\\")
        self.stopwords.append("\\")
        self.stopwords.append("~")
        self.stopwords.append("&")
        self.stopwords.append("．")

        self.stopwords.append("會")
        self.stopwords.append("說")
        self.stopwords.append("…")
        self.stopwords.append("喔")
        self.stopwords.append(":")
        self.stopwords.append("dot")

        self.stopwords.append("‧")
        self.stopwords.append("%")
        self.stopwords.append("@")

        self.stopwords.append("』")
        self.stopwords.append("『")


        tmpstr = 'abcdefghijklmnopqrstuvwxyz'
        for achar in tmpstr:
            self.stopwords.append(achar)
        tmpstr = tmpstr.upper()
        for achar in tmpstr:
            self.stopwords.append(achar)


        self.jieba.set_dictionary(self.word_dictfn)
        #print(self.jieba.get_dict_file())





        #now, we need to arrange the keywords.
        #need to add pos_words and neg_words to the dictionary if the word in not listed.
        #need to remove stop words if the term is in the positive or negative word list.

        self.pos_extra = list(set(self.pos_words) - set(self.all_words))
        if debug: print("Add %d words to dictionary from the positive words" % len(self.pos_extra))
        for aword in self.pos_extra:
            jieba.add_word(aword, freq=None, tag=None)

        self.neg_extra = list(set(self.neg_words) - set(self.all_words))
        if debug: print("Add %d words to dictionary from the negative words" % len(self.neg_extra))
        for aword in self.neg_extra:
            jieba.add_word(aword, freq=None, tag=None)

        self.stopword_toremove1 = set(self.stopwords).intersection(set(self.pos_words))
        self.stopword_toremove2 = set(self.stopwords).intersection(set(self.neg_words))
        self.stopwords = list(set(self.stopwords) - self.stopword_toremove1 - self.stopword_toremove2)

        if debug:
            print("Remove the following stopwords because they are also sentiment words")
            print(self.stopword_toremove1)
            print(self.stopword_toremove2)

    def process(self, text, negation = "remove"):
        """negation  = {"remove" | "ignore" | "inverse"}
                                         remove: remove the term following the negation word
                                         ignore: do nothing
                                         inverse: inverse the  polarity
               """
        #segment, tag, count pos and neg
        pos_count = 0
        pos_count_cvaw = 0
        pos_count_antu = 0
        neg_count = 0
        neg_count_cvaw = 0
        neg_count_antu = 0
        nega_count = 0

        tokens = self.jieba.cut(text, cut_all=False)
        token_len = 0
        token_len_ns = 0
        tokens_list = []
        pos_token_pos = []
        pos_token_pos_cvaw = []
        pos_token_pos_antu = []

        pos_tokens = []
        pos_tokens_cvaw = []
        pos_tokens_antu = []

        neg_token_pos = []
        neg_token_pos_cvaw = []
        neg_token_pos_antu = []

        neg_tokens = []
        neg_tokens_cvaw = []
        neg_tokens_antu = []

        nega_token_pos = []
        nega_tokens = []

        stop_words = []
        for key, value in enumerate(tokens):
            token_len += 1
            tokens_list.append(value)
            if value in self.pos_words:
                pos_count += 1
                pos_token_pos.append(key)
                pos_tokens.append(value)
            if value in self.neg_words:
                neg_count += 1
                neg_token_pos.append(key)
                neg_tokens.append(value)

            if value in self.cvaw_dict:
                if self.cvaw_dict[value] >= self.sent_threshold:
                    pos_count_cvaw += self.cvaw_dict[value]
                    pos_token_pos_cvaw.append(key)
                    pos_tokens_cvaw.append(value)
                if self.cvaw_dict[value] < -self.sent_threshold:
                    neg_count_cvaw += self.cvaw_dict[value]
                    neg_token_pos_cvaw.append(key)
                    neg_tokens_cvaw.append(value)

            if value in self.antusd_dict:
                if self.antusd_dict[value] >= self.sent_threshold:
                    pos_count_antu += self.antusd_dict[value]
                    pos_token_pos_antu.append(key)
                    pos_tokens_antu.append(value)
                if self.antusd_dict[value] < -self.sent_threshold:
                    neg_count_antu += self.antusd_dict[value]
                    neg_token_pos_antu.append(key)
                    neg_tokens_antu.append(value)

            if value not in self.stopwords:
                token_len_ns += 1
            else:
                stop_words.append(value)
            if value in self.negation:
                nega_count += 1
                nega_token_pos.append(key)
                nega_tokens.append(value)

        if negation in ["remove", "inverse"]:
            for aidx in nega_token_pos:
                target = aidx + 1
                try:
                    foundidx = pos_token_pos.index(target)
                    pop_pos = pos_token_pos.pop(foundidx)
                    pop_token = pos_tokens.pop(foundidx)
                    if negation == "inverse":
                        neg_token_pos.append(pop_pos)
                        neg_tokens.append(pop_token)
                    continue
                except:
                    pass

                try:
                    foundidx = neg_token_pos.index(target)
                    pop_pos = neg_token_pos.pop(foundidx)
                    pop_token = neg_tokens.pop(foundidx)
                    if negation == "inverse":
                        pos_token_pos.append(pop_pos)
                        pos_tokens.append(pop_token)
                    continue
                except:
                    pass

            #deal with cvaw
            for aidx in nega_token_pos:
                target = aidx + 1
                try:
                    foundidx = pos_token_pos_cvaw.index(target)
                    pop_pos = pos_token_pos_cvaw.pop(foundidx)
                    pop_token = pos_tokens_cvaw.pop(foundidx)
                    pos_count_cvaw -= self.cvaw_dict[pop_token]
                    if negation == "inverse":
                        neg_token_pos_cvaw.append(pop_pos)
                        neg_tokens_cvaw.append(pop_token)
                        neg_count_cvaw += self.cvaw_dict[pop_token]
                    continue
                except:
                    pass

                try:
                    foundidx = neg_token_pos_cvaw.index(target)
                    pop_pos = neg_token_pos_cvaw.pop(foundidx)
                    pop_token = neg_tokens_cvaw.pop(foundidx)
                    neg_count_cvaw -= self.cvaw_dict[pop_token]
                    if negation == "inverse":
                        pos_token_pos_cvaw.append(pop_pos)
                        pos_tokens_cvaw.append(pop_token)
                        pos_count_cvaw += self.cvaw_dict[pop_token]
                    continue
                except:
                    pass

        if token_len_ns == 0:
            token_len_ns = 1

        pos_count = len(pos_token_pos)
        neg_count = len(neg_token_pos)
        nega_count = len(nega_token_pos)
        pos_score = (pos_count / token_len_ns) ** 0.5
        neg_score = (neg_count / token_len_ns) ** 0.5

        pos_score_cvaw = (pos_count_cvaw / token_len_ns) ** 0.5
        neg_score_cvaw = - abs(neg_count_cvaw / token_len_ns) ** 0.5

        pos_score_antu = (pos_count_antu / token_len_ns) ** 0.5
        neg_score_antu = - abs(neg_count_antu / token_len_ns) ** 0.5

        retdict = {'pos_count': pos_count, 'neg_count': neg_count,
                   'nega_count': nega_count,
                   'pos_count_cvaw': pos_count_cvaw, 'neg_count_cvaw': neg_count_cvaw,
                   'pos_score_cvaw': pos_score_cvaw, 'neg_score_cvaw': neg_score_cvaw,
                   'pos_score_antu': pos_score_antu, 'neg_score_antu': neg_score_antu,
                   'token_len': token_len, 'token_len_ns': token_len_ns,
                   'pos_score': pos_score, 'neg_score': neg_score,
                   'text': text, 'tokens': tokens_list,
                   'pos_token_pos': pos_token_pos,
                   'neg_token_pos': neg_token_pos,
                   'pos_tokens': pos_tokens,
                   'neg_tokens': neg_tokens,
                   'pos_tokens_cvaw': pos_tokens_cvaw,
                   'neg_tokens_cvaw': neg_tokens_cvaw,
                   'pos_token_pos_cvaw': pos_token_pos_cvaw,
                   'neg_token_pos_cvaw': neg_token_pos_cvaw,
                   'pos_tokens_antu': pos_tokens_antu,
                   'neg_tokens_antu': neg_tokens_antu,
                   'nega_token_pos': nega_token_pos,
                   'nega_tokens':nega_tokens,
                   'stop_words': list(set(stop_words))}
        return(retdict)

    def add_word(self, word, sentiment = 0.0):
        if word not in self.all_words:
            self.jieba.add_word(word)
        if abs(sentiment) != 0.0:
            self.cvaw_dict[word] = sentiment

    def show_seg_sent(self, retdict, sep = '/'):
        return(sep.join(retdict["tokens"]))

    def show_sent_tag_ntusd(self, retdict, sep = '/', postag = '[P]', negtag = '[N]', negatag = '[U]'):
        tmptokens = retdict['tokens'].copy()
        for idx in retdict['pos_token_pos']:
            tmptokens[idx] = tmptokens[idx] + postag
        for idx in retdict['neg_token_pos']:
            tmptokens[idx] = tmptokens[idx] + negtag
        for idx in retdict['nega_token_pos']:
            tmptokens[idx] = tmptokens[idx] + negatag
        return(sep.join(tmptokens))

    def show_sent_tag_cvaw(self, retdict, sep = '/', postag = '[P]', negtag = '[N]', negatag = '[U]'):
        tmptokens = retdict['tokens'].copy()
        for idx in retdict['pos_token_pos_cvaw']:
            tmptokens[idx] = tmptokens[idx] + postag
        for idx in retdict['neg_token_pos_cvaw']:
            tmptokens[idx] = tmptokens[idx] + negtag
        for idx in retdict['nega_token_pos']:
            tmptokens[idx] = tmptokens[idx] + negatag
        print(sep.join(tmptokens))

    def show_short_summary_ntusd(self, retdict):
        print("Number of tokens: ", retdict['token_len'])
        print("Number of non-stopword tokens:", retdict['token_len_ns'])
        print("Number of positive tokens:", retdict['pos_count'])
        print("Number of negative tokens:", retdict['neg_count'])
        print("Positive score: %0.4f" % retdict['pos_score'])
        print("Negative score: %0.4f" % retdict['neg_score'])

    def show_short_summary_cvaw(self, retdict):
        print("Number of tokens: ", retdict['token_len'])
        print("Number of non-stopword tokens:", retdict['token_len_ns'])
        print("Sum of positive word scores: %0.4f" % retdict['pos_count_cvaw'])
        print("Sum of negative word scores: %0.4f" % retdict['neg_count_cvaw'])
        print("Overall positive score: %0.4f" % retdict['pos_score_cvaw'])
        print("Overall negative score: %0.4f" % retdict['neg_score_cvaw'])


if __name__ == "__main__":
    js1 = jass(debug = True)
    stopset = set(js1.stopwords)

    with open('jass_v1/jass/newword.txt', encoding = 'utf-8') as fh_new1:
        for aline in fh_new1:
            aline = aline.strip()
            if len(aline) > 1:
                print("add word", aline)
                js1.jieba.add_word(aline)


    text = "我今天很快樂。我今天很憤怒。"
    tsent1 = js1.process(text)
    #print(tsent1)
    print(js1.show_seg_sent(tsent1))
    print(js1.show_sent_tag(tsent1))

    text2 = "高雄市長韓國瑜昨天發表五點聲明，直言無法參加現有初選制度；鴻海董事長郭台銘宣布投入國民黨初選，不接受徵召；" \
            "國民黨基層又不斷力挺韓國瑜，面對各界聲浪，國民黨中央為了初選制度傷透腦筋；今天中常會中，中常委提案解套，" \
            "讓所有可能人選，納入初選；會中通過研擬特別辦法，納入所有可能人選，至於初選方式是否採用全民調，" \
            "常會中達成共識，也交由相關單位研議。預計6月後啟動民調。" \
            "國民黨中常會稍早出現挺韓粉絲與挺制度的年輕黨員雙方口角，" \
            "國民黨中央委員徐正文帶領挺韓粉絲高喊口號要求黨中央徵召韓國瑜，" \
            "一旁的國民黨青年中常委李成蔭率領的青年黨代表要求公正初選，使得挺韓粉絲不爽，" \
            "有超過30年的挺韓黨員拿出榮譽狀先嗆「郭台銘有榮譽狀，我也有榮譽狀」、「就是支持國民黨韓國瑜選總統」" \
            "，並連續質疑青年黨代表是「是民進黨還是國民黨」。但常會仍順利舉行。（政治中心／台北報導）"

    tsent2 = js1.process(text2)
    print(js1.show_sent_tag(tsent2))
    print(js1.show_short_summary(tsent2))
    print(js1.show_sent_tag_cvaw(tsent2))
    print(js1.show_short_summary_cvaw(tsent2))

    #set(js1.negation).intersection(js1.neg_words)
    #set(js1.negation).intersection(js1.pos_words)

    text3 = """這是我的第2支蘋果手機,11/4在嘉義市的耐斯松屋istore花了4萬多元買的
用了2個多月一直都沒問題,但在1/12晚上講完約40分鐘的LINE視訊電話後就當機了,
強迫關機後再強迫開機螢幕顯示需用電腦還原,結果還原後點入APP商店又死當了
這次連強迫開機也沒辦法,只好在1/13下班後立即送修
1/15下午維修完畢取件,維修單內容是軟體重灌+長時間測試,一切正常沒有元件壞掉
結果好景不常,1/21下午5點左右我要開LINE看訊息又當掉了
強迫開機後螢幕還是顯示需用電腦還原,但這次還原到一半就卡死了,電腦螢幕顯示發生未知的錯誤
當掉之前約14:30左右有撥了通10分鐘左右的LINE視訊電話之後就沒動到手機
因為2次當機剛好都是跟LINE有關,所以今天早上再送修就有跟小姐強調這情況
結果她竟然說LINE是第3方軟體,如果真的是LINE造成死當蘋果沒辦法負責這種話
說真的我聽了很生氣就回她說,請問LINE有多少人用?有人的X像我的一樣嗎?
我的APP只有簡單的幾樣,除了LINE,臉書,微信,淘寶,天貓,都是一些大家常用的
而且我不玩遊戲,都只看看臉書和LINE及上淘寶
這次工程師檢修也沒辦法開機了,告訴我要送新加坡原廠檢測需7~14天
我的天啊,怎麼會樣?請問有人跟我一樣的狀況嗎?
2次送修浪費我這麼多天,我可以要求延長保固嗎?還是要求什麼?"""
    tsent3 = js1.process(text3)
    print(js1.show_sent_tag_cvaw(tsent3))
    js1.show_short_summary_cvaw(tsent3)


    text4 = """手機故障，竟想把責任推到軟體身上，這神腦也真是⋯⋯
我256g太空灰，line有當過兩三次，推掉後台或重開機解決～
既然神腦打算閃躲維修職責，請你注意個重點，手機當機別再強調是因什麼app操作引起的，就說一般操作中死當便可，哪有這樣子的處理態度！"""

    tsent4 = js1.process(text4)
    print(js1.show_sent_tag(tsent4))
    print(tsent4['pos_tokens'])
    print(tsent4['neg_tokens'])
    js1.show_short_summary_cvaw(tsent4)

    text5 = '2016新年快樂 新的一年來了<BR>2015和閒聊版的各位經歷了不少事<BR>有些同伴因為個人的原因離了閒聊版<BR>也有些同伴因為版規<BR>因此要在推進城跨年<BR>總之新的一年開始了<BR>請大家新的一年也多多照顧<BR>過去一年的種種<BR>就請多包涵了 <BR>夜露死苦'

    text5 = text5.replace("<BR>", " ")
    tsent5 = js1.process(text5)
    print(js1.show_sent_tag(tsent5))
    print(tsent5['pos_tokens'])
    print(tsent5['neg_tokens'])
    js1.show_short_summary(tsent5)
    js1.show_short_summary_cvaw(tsent5)


    #compare with an existing dataset

    import pandas as pd
    import numpy as np
    import jieba

    #jieba.set_dictionary("data/dict.txt")

    # pd.get_option("display.max_columns")
    pd.options.display.max_columns = 20
    pd.options.display.width = 120

    df1 = pd.read_csv("K:/Users/hmlu/svn_drive3/research/sentiment analysis/senti_class_v1/data/流行性商品1-5(2016)_utf8.csv", encoding='utf-8')
    # df1 = df1.head(5000)

    # first, adjust scores so that all are between 0 and 1,
    # for type == "main" concate title and content. otherwise, use content only

    tmpind0 = df1.pos_score.values > 1.0
    tmpind1 = df1.neg_score.values > 1.0
    tmpind2 = np.logical_or(tmpind0, tmpind1)
    df1.loc[tmpind2, "pos_score"] = df1.loc[tmpind2, "pos_score"] / 100.0
    df1.loc[tmpind2, "neg_score"] = df1.loc[tmpind2, "neg_score"] / 100.0

    indmain = df1.type == "main"
    indreply = np.logical_not(indmain)

    df1["raw_text"] = df1["content"]
    df1.loc[indmain, "raw_text"] = df1.loc[indmain, "title"] + " " + df1.loc[indmain, "content"]
#
    df1 = df1.fillna("")

    import re
    def word_seg(t1):
        # t1 = df1.loc[i, "raw_text"]
        t1 = t1.replace("<BR>", " ")

        re_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        t1 = re_url.sub(' URL ', t1)

        re_int = re.compile(r'\d+')
        t1 = re_int.sub(' NUMBER ', t1)

        re_dot = re.compile(r'\.+')
        t1 = re_dot.sub(' DOT ', t1)

        re_xd = re.compile('xd+', re.IGNORECASE)
        t1 = re_xd.sub(' XD ', t1)

        re_space = re.compile('\s+')
        t1 = re_space.sub(' ', t1)
        # t1 = t1.replace("  ", " ")
        tmp1 = js1.jieba.cut(t1, cut_all=False)
        tmp2 = []
        for aelem in tmp1:
            if aelem.strip() != "":
                tmp2.append(aelem)
        return " ".join(tmp2)
    df1["text_sp"] = df1.raw_text.transform(word_seg)
#
    #from sklearn.feature_extraction.text import CountVectorizer
#
    #count_vect = CountVectorizer(min_df=100)
    #X_train_counts = count_vect.fit_transform(df1.text_sp)
    #X_train_counts.shape
    #word_freq = X_train_counts.sum(axis=0)
    ## sind = np.argsort(word_freq)[::-1]
    #vocab0 = [x[0] for x in count_vect.vocabulary_.items()]
    ## vocab0 = np.array(vocab0)
#
    #vocab_df = pd.DataFrame({'word': vocab0, 'freq': word_freq.tolist()[0]})
    #vocab_df.sort_values(by=['freq'], ascending=False, inplace=True)
    #print(vocab_df.head(10))
    #print(vocab_df.tail(10))
#
    #
#
    #from sklearn.feature_extraction.text import TfidfVectorizer
#
    #vectorizer = TfidfVectorizer(max_df=0.5, max_features=5000,
    #                             min_df=10, stop_words = js1.stopwords,
    #                             use_idf=True)
    #X_tfidf = vectorizer.fit_transform(df1.text_sp)
#
    #from sklearn.decomposition import TruncatedSVD
#
    #svd = TruncatedSVD(n_components=200, n_iter=20, random_state=42)
    #svd.fit(X_tfidf)
#
    #from sklearn.preprocessing import Normalizer
    #from sklearn.pipeline import make_pipeline
    #normalizer = Normalizer(copy=False)
    #lsa = make_pipeline(svd, normalizer)
#
    #X_lsa = lsa.fit_transform(X_tfidf)
#
#
    #explained_variance = svd.explained_variance_ratio_.sum()
#
    #
    #from sklearn.cluster import KMeans, MiniBatchKMeans
    #true_k = 30
    #km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
    #            verbose=True)
    #km.fit(X_lsa)
#
    #from sklearn import metrics
#
    #print("Silhouette Coefficient: %0.3f"
    #      % metrics.silhouette_score(X_lsa, km.labels_, sample_size=1000))
    #print()
#
    #original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    #order_centroids = original_space_centroids.argsort()[:, ::-1]
#
    #terms = vectorizer.get_feature_names()
    #for i in range(true_k):
    #    print("Cluster %d:" % i, end='')
    #    for ind in order_centroids[i, :20]:
    #        print(' %s' % terms[ind], end='')
    #    print()
#
    #df1['km_label'] = km.labels_
#
    ##count by topics clusters.
    #df1.km_label.value_counts()
#

    #df1['pub_date'] = df1.pub_time.transform(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))
#
    #tmp1 = df1.loc[:, ['pub_date', 'km_label']].groupby(['pub_date'])['km_label'].value_counts()
    #count_by_date = tmp1.unstack()
    #count_by_date = count_by_date.fillna(0.0)
#
    #plt.scatter(count_by_date.index, count_by_date[0])
#
    #tmpind1 = df1.km_label.values == 10
    #df1_t10 = df1.loc[tmpind1, :]
    #df1_t10.raw_text.sample(30)
#
    #tmpind1 = df1.km_label.values == 7
    #df1_t7 = df1.loc[tmpind1, :]
    #df1_t7.raw_text.sample(30)
#
    #tmpind1 = df1.km_label.values == 6
    #df1_t7 = df1.loc[tmpind1, :]
    #df1_t7.raw_text.sample(30)
#
    #=======================
    # sentiment analysis
    def compu_score(astr):
        tsent4 = js1.process(astr)
        return tsent4['pos_score_cvaw'], tsent4['neg_score_cvaw']

    df2 = df1.head(10000).copy()

    a1 = df2.raw_text.transform(compu_score)
    a1 = pd.DataFrame(a1.to_list(), columns=['pos', 'neg'])

    df2['pos'] = a1['pos']
    df2['neg'] = a1['neg']

    import matplotlib.pyplot as plt
    #plt.scatter(df2['pos'], df2['pos_score'])
    #plt.scatter(df2['neg'], df2['neg_score'])
    #plt.show()

    # how about trending topics...???
    dow_word = dict()
    word_count = dict()
    for aline in df1.iterrows():
        #print(aline)
        #aline[0]
        text = aline[1]['text_sp']
        rem1 = text.lower().split()
        # filter stop words
        rem1 = [word for word in rem1 if word not in stopset]

        thetime = datetime.strptime(aline[1]['pub_time'], '%Y-%m-%d %H:%M:%S')
        #weeknum = thetime.isocalendar()[1]
        weeknum = ((thetime - datetime(thetime.year, 1, 1)).days // 7)
        for aword in rem1:
            if aword not in dow_word:
                dow_word[aword] = np.zeros((53,))
                word_count[aword] = 0
            dow_word[aword][weeknum] += 1
            word_count[aword] += 1

    word_ts_std = dict()
    for aword in dow_word.keys():
        word_ts_std[aword] = dow_word[aword].std()

    word_std = pd.DataFrame(word_ts_std.items(), columns = ['word', 'std'])
    word_freq = pd.DataFrame(word_count.items(), columns = ['word', 'freq'])
    word_std.sort_values(by = ['std'], ascending= False, inplace= True)

    word_std2 = word_std.merge(word_freq)
    word_std2['std_norm'] = word_std2['std'] / word_std2['freq']

    word_std2.sort_values(by = "std_norm", ascending= False, inplace = True)

    nmsg = df1.shape[0]
    #threshold = nmsg * 0.005
    threshold = nmsg * 0.01
    word_std3 = word_std2.loc[word_std2['freq'] > threshold, :]

    #import matplotlib.pyplot as plt

    #plt.plot(dow_word['香港'])
    #plt.plot(dow_word['英文'])
    #plt.plot(dow_word['台灣人'])
    #plt.plot(dow_word['女兒'])
    #plt.figure(-1)
    #plt.plot(dow_word['電腦'])
    #plt.title('aaa')

    #plt.show()

    #fig, ax = plt.subplots()
    #ax.plot(dow_word['台灣人'], label='freq')
    #ax.plot(dow_word['電腦'], label='freq')
    #ax.plot(dow_word['香港'], label='freq')
    #ax.set_title('電腦', fontsize=12, color='r')
    #plt.show()

    #!!! todo, plot all words
    from matplotlib.font_manager import FontProperties
    ChineseFont2 = FontProperties(fname='C:\\Windows\\Fonts\\mingliu.ttc')
    for arow in word_std3.iterrows():
        fig, ax = plt.subplots()
        aword = arow[1]['word']
        ax.plot(dow_word[aword], label='freq')
        ax.set_title(aword, fontsize = 12, color = 'r', fontproperties = ChineseFont2 )
        plt.waitforbuttonpress()
        plt.close()

    #topic modeling
    import gensim
    import logging
    import pyLDAvis.gensim

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


    class my_corpus():
        def __init__(self, df_col, dict=None, s_size=10):
            import tempfile
            import csv
            import gensim

            #maxInt = 10000000
            #csv.field_size_limit(maxInt)
            #self.csvfn = csvfn
            self.df_col = df_col
            self.s_size = s_size

            self.dict = dict
            self.doclen = -1

        def len(self):
            if self.doclen < 0:
                #self.fh2 = open(self.csvfn, 'r', newline='')
                #self.csvreader = csv.DictReader(self.fh2)
                #n = sum(1 for line in self.csvreader)
                self.doclen = self.df_col.shape[0]
                return (self.doclen)
            else:
                return (self.doclen)

        def __len__(self):
            return self.len()

        def __iter__(self):
            #self.fh1 = open(self.csvfn, 'r', newline='')
            #self.csvreader = csv.DictReader(self.fh1)
            self.linecount = 0

            for arow in self.df_col.iteritems():
                self.linecount += 1
                if self.s_size > 0 and self.linecount > self.s_size:
                    break
                #text = arow['pure_text2']
                text = arow[1]
                # rem1 = self.reword.findall(text.lower())
                rem1 = text.lower().split()
                #filter stop words
                rem1 = [word for word in rem1 if word not in stopset]
                if self.dict == None:
                    yield rem1
                else:
                    yield self.dict.doc2bow(rem1)

    s_size = -1
    mycorp0 = my_corpus(df_col = df1.text_sp, s_size=s_size)


    #def mytext(itext):
    #    #nrow = textrow.shape[0]
    #    #itext = textrow.iteritems()
    #    for aitem in itext:
    #        text1 = aitem[1].replace('<BR>', ' ')
    #        yield text1

    #for arow in mytext(df1.raw_text.iteritems()):
    #    print(arow)

    no_below = 20
    print("Constructing dictionary...", flush=True)
    dct = gensim.corpora.Dictionary(mycorp0)
    print("Processed", dct.num_docs, "docs")
    print("Processed", dct.num_pos, "tokens")
    print(dct)
    print("filter lowe frequency tokens")
    dct.filter_extremes(no_below=no_below)
    print(dct)
    dct.save_as_text("lda_dict.txt")
    print("done with dictionary...", flush=True)

    t1 = datetime.now()
    print("Start running LDA model....", flush=True)
    mycorp = my_corpus(df_col=df1.text_sp, s_size=s_size, dict=dct)
    ntopic = 15
    npass = 20
    lda = gensim.models.ldamodel.LdaModel(corpus=mycorp, id2word=dct, num_topics=ntopic, \
                                          update_every=1, chunksize=40000, \
                                          alpha='auto', eta='auto', \
                                          passes=npass, random_state = 1001)
    lda.save("mobile_tm_k%d_p30.model" % ntopic)
    print("done with LDA model...", flush=True)

    t2 = datetime.now()
    lda_runtime = t2 - t1
    print("Lda runtime is", lda_runtime)

    b1 = lda.print_topics(50, 15)
    import pprint as pp

    pp.pprint(b1)

    print("preparing LDA visualization...", flush=True)
    vis1 = pyLDAvis.gensim.prepare(lda, mycorp, dct)
    tmp1 = pyLDAvis.display(vis1)
    str1 = tmp1.__html__()
    fh1 = open("lda_visualize_k%d.html" % ntopic, 'w')
    fh1.write(str1)
    fh1.close()

    t3 = datetime.now()
    ldav_runtime = t3 - t2
    print("Lda visual runtime is", ldav_runtime)




    #now, need to extract topic distribution for each post
    #some experiments
    #text_sp = df1.text_sp[1001]
    #rem1 = text_sp.lower().split()
    ## filter stop words
    #rem1 = [word for word in rem1 if word not in stopset]
    #adoc = dct.doc2bow(rem1)
    #adoctop = lda.get_document_topics(adoc, minimum_probability=1e-10)

    #sic_list = []
    topic_list = []

    def get_topic(text_sp):
        rem1 = text_sp.lower().split()
        # filter stop words
        rem1 = [word for word in rem1 if word not in stopset]
        adoc = dct.doc2bow(rem1)
        adoctop = lda.get_document_topics(adoc, minimum_probability=1e-10)
        #lda.num_topics
        if len(adoctop) != lda.num_topics:
            print("Error, number of topic does not match")
            raise Exception("num_topic error")
        adoctop2 = [x[1] for x in adoctop]
        return adoctop2

    #tmp2 = df1.head(100).copy()
    #tmp3 = tmp2.text_sp.transform(get_topic)
    #cname = [ "t_" + str(x) for x in list(range(lda.num_topics))]
    #tmp3 = pd.DataFrame(tmp3.to_list(), columns = cname)
    #tmp4 = pd.concat([tmp2, tmp3], axis=1, sort=False)


    tmp3 = df1.text_sp.transform(get_topic)
    cname = ["t_" + str(x) for x in list(range(lda.num_topics))]
    tmp3 = pd.DataFrame(tmp3.to_list(), columns=cname)
    df1a = pd.concat([df1, tmp3], axis=1, sort=False)

    df1a['pub_date'] = df1a.pub_time.transform(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))
    df1a['time'] = df1a.pub_time.transform(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').time())
    df1a['hour'] = df1a.time.transform(lambda x: x.hour)
    #

    targetcol2 = ['hour']
    targetcol2.extend(cname)
    topic_hour = df1a.loc[:, targetcol2].groupby(['hour']).sum()
    #topic_hour.plot.area()

    topic_hour_sum = topic_hour.sum(axis = 1)
    topic_hour2 = topic_hour.div(topic_hour_sum, axis = 0)
    #normalized area plot.
    #topic_hour2.plot.area()

    targetcol = ['pub_date']
    targetcol.extend(cname)
    #tmp1 = df1a.loc[:, ['pub_date', 't_0']].groupby(['pub_date'])['t_0'].sum()
    topic_date = df1a.loc[:, targetcol].groupby(['pub_date']).sum()

    #now, aggregate by dayofweek
    #weeknum = ((thetime - datetime(thetime.year, 1, 1)).days // 7)
    df1a['weeknum'] = df1a.pub_date.transform(lambda thetime: ((thetime - datetime(thetime.year, 1, 1)).days // 7))
    targetcol3 = ['weeknum']
    targetcol3.extend(cname)
    topic_weeknum = df1a.loc[:, targetcol3].groupby(['weeknum']).sum()




    daily_sum = topic_date.sum(axis = 1)
    #daily_sum.plot()
    topic_date2 = topic_date.div(daily_sum, axis = 0)
    #topic_date.plot()
    #topic_date.loc[topic_date.index >= '2016-11-01', :].plot()
    #topic_date2.loc[topic_date.index >= '2016-11-01', :].plot.area()
    #topic_date2.plot.area()

    topic_date_dow = topic_date.copy()
    #topic_date_dow = topic_date2.copy()
    topic_date_dow['dow'] = topic_date.index.dayofweek.to_list()

    topic_dow = topic_date_dow.groupby('dow').sum()
    #topic_dow.plot.area()
    #topic_dow_sum = topic_dow.sum(axis = 1)

    #topic_dow_prop = topic_dow.div(topic_dow_sum, axis = 0)
    #topic_dow_prop.plot.area()
    #topic_dow_prop.plot.bar()
#
    #topic_sum = topic_dow.sum(axis=0)
    #topic_dow_prop2 = topic_dow.div(topic_sum, axis = 1)
    #topic_dow_prop2.plot.bar()
#
    ##topic_dow.plot.area()
    #topic_dow.plot()
    #topic_dow.plot.bar()
#
    #from topic_date



    # count_by_date = tmp1.unstack()
    # count_by_date = count_by_date.fillna(0.0)
    #
    # plt.scatter(count_by_date.index, count_by_date[0])
    #
    # tmpind1 = df1.km_label.values == 10
    # df1_t10 = df1.loc[tmpind1, :]
    # df1_t10.raw_text.sample(30)

    df1a['neg_0'] = df1a['neg_score'] * df1a['t_0']
    df1a['pos_0'] = df1a['pos_score'] * df1a['t_0']

    neg_0_desc = df1a.groupby(['pub_date'])['neg_0'].describe()
    neg_0_desc['mean'].plot()

    pos_0_desc = df1a.groupby(['pub_date'])['pos_0'].describe()
    pos_0_desc['mean'].plot()

    pos_0_desc['net'] = pos_0_desc['mean'] - neg_0_desc['mean']
    pos_0_desc['net'].plot()

    df1a_pos = df1a.sort_values(['pos_score'], ascending=False)
    df1a_pos.loc[:, ['raw_text', 'text_len', 'pos_score', 'neg_score']].head(400)

    df1a_neg = df1a.sort_values(['neg_score'], ascending=False)
    df1a_neg.loc[:, ['raw_text', 'text_len', 'pos_score', 'neg_score']].head(100)

    js1.process('竟然沒圖... 真是太令人失望了...')
