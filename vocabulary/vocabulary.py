# -*- coding: utf-8 -*-
'''
分词，提词的主程序
先词形还原，再词频统计
去掉简单的单词后，生成单词本
'''
import requests,re,threading,traceback,os,sys,time
from bs4 import BeautifulSoup
from tqdm import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
lemmatizer = WordNetLemmatizer()
Max_lookup_connections = 5
Max_download_audio_connections = 10
class vocabulary(object):
    def __init__(self,file,learned_words_file = 'learned_words.txt',save_path='',download_audio=False):
        '''
        :param: file: 待处理的文本
        :param: learned_words_file: 已学会的简单的单词本
        :param: save_path: 要保存的路径，默认程序文件下
        :param: download_autio:是否下载音频，默认为false
        '''
        #生成保存路径
        self.file = file
        if save_path:
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
        else:
            save_path = './'
        self.learned_words_file = learned_words_file 
        self.save_path=save_path
        self.name = os.path.basename(file).split('.')[0]
        self.save_filename = self.save_path + os.sep + self.name + '_vocabulary.txt'
        self.download_audio_flag = download_audio

    def run(self):
        try:
            raw_text,text = self.get_content(self.file)#获取文本，原始文本用以提供例句
            words = self.lemmatizing(text)#单词变体还原，词形还原
            self.word_counts = self.counts(words)#计数
            words = self.remove_words(words)#去除简单的，已熟知的单词
            look_up_result = self.get_look_up_result(words,raw_text)#查词
            self.write_words(look_up_result)
            if self.download_audio_flag:
                self.download_audio(look_up_result)
            return look_up_result
        except:
            traceback.print_exc()
            return None
    def get_content(self,file):
        '''
        获取文本内容，输入文件名，返回字符串。
        '''
        with open(file,'r',encoding='utf-8') as f:
            raw_text = f.read()
        text = raw_text.lower()
        for ch in '''`~!@#$%^&*()_+-={}|[]\\:"?>”<;'“—‘’.…/,''':
            text = text.replace(ch,' ')
        return raw_text,text
    def lemmatizing(self,text):
        '''
        词形还原，输入字符串，返回单词列表
        '''
        words = text.split()
        print('words:',len(words))
        lemm_words = []
        with tqdm(total = len(words),desc='lemmatizing') as fbar:
            for i in range(len(words)):
                j = i+1
                self.get_lemmed_one(words[i],lemm_words)
                if j%1000==0:
                    fbar.update(1000)
        #print('lemm_words: ',len(lemm_words))
        return lemm_words
    def get_lemmed_one(self,word,lemm_words):
        try:
            tag = pos_tag([word])#标注单词在文本中的成分 
            #需要用nltk.download('averaged_perceptron_tagger')下载资源
            pos = self.get_pos(tag[0][1])#转为词性
            if pos:
                lemm_word = lemmatizer.lemmatize(word,pos)#词形还原，还原词根
                lemm_words.append(lemm_word)
            else:
                lemm_words.append(word)
        except:
            print(word, '<-- fail')
    def get_pos(self,tag):
        #需要用nltk.download('wordnet')下载资源
        try:
            if tag.startswith('J'):
                return wordnet.ADJ
            if tag.startswith('V'):
                return wordnet.VERB
            if tag.startswith('N'):
                return wordnet.NOUN
            if tag.startswith('R'):
                return wordnet.ADV
            else:
                return ''
        except:
            return ''
    def counts(self,words):
        '''
        词频统计，输入单词列表，输出词频,返回字典{单词:词频}
        '''
        #print(len(words))
        counts = {}
        for word in words:
            counts[word] = counts.get(word,0) +1
        items = list(counts.items())
        items.sort(key=lambda x:x[1],reverse=True)
        print('set words:',len(counts))
        #for i in range(20):
        #    word,count = items[i]
        #    print('{0:<10}{1:>5}'.format(word,count))
        return counts
    def remove_words(self,words):
        learned_words=[]
        try:
            with open(self.learned_words_file,'r',encoding='utf-8') as f:
                for line in f:
                    line = line.replace('\n','')
                    learned_words.append(line)
        except:
            learned_words=[]
        finally:
            words = list(set(words) - (set(learned_words)))
            print('removed_words:',len(words))
            return words
    def look_up_one(self,word):
        #查询单个单词，返回：key(单词),ps（音标）,pron（音频url）,pos（词性）,acceptation（释义）
        #调用金山词霸开放平台API
        #http://dict-co.iciba.com/api/dictionary.php?w=moose&key=4EE27DDF668AD6501DCC2DC75B46851B
        url = 'http://dict-co.iciba.com/api/dictionary.php?w={}&key=4EE27DDF668AD6501DCC2DC75B46851B'.format(word)
        match =re.search('[a-z]',word)
        if not match:
            return
        beats = 0
        blankbeats = 0
        while True:
            try:
                resp = requests.get(url,timeout=12)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text,'html.parser')
                key = soup.key.string
                if key == '':
                    if blankbeats >= 20:
                        print('requests blank')
                        break
                    time.sleep(0.2)
                    blankbeats += 1
                    continue
                ps = '[{}]'.format(soup.ps.string)
                pron = soup.pron.string
                pos_list = soup.select('pos')
                pos = pos_list[0].string
                acceptation_list = soup.select('acceptation')
                acceptation = pos_list[0].string + ' ' + acceptation_list[0].string.replace('\n','').replace('\r','')
                for i in range(1,len(pos_list)):
                    #acceptation = acceptation + '<div>' + pos_list[i].string + ' '  + acceptation_list[i].string.replace('\n','').replace('\r','') + '</div>'
                    acceptation = acceptation + ' ' + pos_list[i].string + ' '  + acceptation_list[i].string.replace('\n','').replace('\r','') + ' '
                return (key,ps,pron,pos,acceptation)
            except:
                if beats >= 20:
                    print('Error: requests data error --> ',word)
                    break
                time.sleep(0.2)
                beats += 1
    def get_sen(self,word,text):
        #获取原文例句：
        pattern= '\\..*?{}.*?\\.'.format(word) #问题：大单词包含该小单词
        match =re.search(pattern,text)
        if match:
            return match.group(0)[2:]
        else:
            return ' '

    def get_look_up_result(self,words,text):
        '''
        查词，返回字典列表，key(单词),ps（音标）,pron（音频url）,pos（词性）,acceptation（释义）
        key: 单词，count: 词频，ps: 音标，pron: 音频url，pos:词性，sen:原文例句，
        '''
        data = []
        threads=[]
        semaphore = threading.Semaphore(Max_lookup_connections)
        with tqdm(total = len(words),desc='Looking Up') as fbar:
            for i in range(len(words)):
                j = i+1
                word = words[i]
                #self.look_up(word,text,data,semaphore)
                semaphore.acquire()
                t = threading.Thread(target=self.look_up,args=(word,text,data,semaphore))
                threads.append(t)
                t.start()
                if j%100==0:
                    fbar.update(100)
            for t in threads:
                t.join()
        print('vocabulary:',len(data))
        #print(data[:10])
        return data
    def look_up(self,word,text,data,semaphore):
        '''
        查词，返回字典列表，key(单词),ps（音标）,pron（音频url）,pos（词性）,acceptation（释义）
        key: 单词，count: 词频，ps: 音标，pron: 音频url，pos:词性，sen:原文例句，
        '''
        if self.look_up_one(word):
            datum = {}
            key,ps,pron,pos,acceptation=self.look_up_one(word)
            sen = self.get_sen(word,text)
            count = self.word_counts.get(key,0)
            datum['key'] = key
            datum['count'] = count
            datum['ps'] = ps
            datum['pron'] = pron
            datum['pos'] = pos
            datum['acceptation'] = acceptation
            datum['sen'] = sen
            data.append(datum)
        semaphore.release()
    def write_words(self,data):
        with open(self.save_filename,'w',encoding='utf-8') as f:
            for datum in data:
                pron = '[sound:{}.mp3]'.format(datum['key']) 
                #text = '{}\t{}\t{}\t{}\t{}\n'.format(datum['key'],datum['ps'],pron,datum['acceptation'],datum['sen'])
                text = '{}\t{}\n  {}\n\n'.format(datum['key'],datum['ps'],datum['acceptation'])
                f.write(text)

    def download_audio_one(self,key,url):
        '''下载单词发音音频'''
        resp = requests.get(url)
        filepath = self.save_path + os.path.sep + 'audio'
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        filename = filepath + os.sep + key + '.mp3'
        if not os.path.isfile(filename):
            with open(filename,'wb') as f:
                f.write(resp.content)
    def download_audio_one_thread(self,key,url,semaphore):
        '''下载单词发音音频'''
        resp = requests.get(url)
        filepath = self.save_path + os.path.sep + 'audio'
        filename = filepath + os.sep + key + '.mp3'
        if not os.path.isfile(filename):
            with open(filename,'wb') as f:
                f.write(resp.content)
        semaphore.release()
    def download_audio(self,data):
        filepath = self.save_path + os.path.sep + 'audio'
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        threads = []
        semaphore = threading.Semaphore(Max_download_audio_connections)
        len_words = len(data)
        with tqdm(total = len_words,desc='Downloading sudio') as fbar:
            for i in range(len_words):
                j = i+1
                key = data[i]['key']
                url = data[i]['pron']
                semaphore.acquire()
                t = threading.Thread(target=self.download_audio_one_thread,args=(key,url,semaphore))
                threads.append(t)
                t.start()
                if j%100==0:
                    fbar.update(100)
            for t in threads:
                t.join()
if __name__=='__main__':
    #from pandas import DataFrame
    if len(sys.argv) == 1:
        file = 'wordlist.txt'
    else:
        file = sys.argv[1]
    work =  vocabulary(file,save_path = '')
    data = work.run()
    #pf = DataFrame(data)
    #print(pf)
