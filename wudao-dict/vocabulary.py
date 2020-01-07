# -*- coding: utf-8 -*-
'''
分词，提词的主程序
先词形还原，再词频统计
去掉简单的单词后，生成单词本
'''
import traceback,os,sys,json,socket
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag

lemmatizer = WordNetLemmatizer()
Max_lookup_connections = 5
class vocabulary(object):
    def __init__(self,file,learned_words_file = 'learned_words.txt',save_path=''):
        '''
        :param: file: 待处理的文本
        :param: learned_words_file: 已学会的简单的单词本
        :param: save_path: 要保存的路径，默认程序文件下
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
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            raw_text,text = self.get_content(self.file)#获取文本，原始文本用以提供例句
            words = self.lemmatizing(text)#单词变体还原，词形还原
            self.word_counts = self.counts(words)#计数
            words = self.remove_words(words)#去除简单的，已熟知的单词
            look_up_result = self.get_look_up_result(words,raw_text)#查词
            self.write_words(look_up_result)
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
        for i in range(len(words)):
            j = i+1
            self.get_lemmed_one(words[i],lemm_words)
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
        #查询单个单词，返回：key(单词),ps（音标）,pattern（时态）,acceptation（释义）
        key = ''
        ps = ''
        pattern = ''
        acceptation = []
        word_info = {}
        word_info = None
        word = word.lower()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        beats = 0
        while True:
            try:
                self.client.connect(("0.0.0.0", 23764))
                break
            except ConnectionRefusedError:
                if beats >= 60:
                    print('Error: Connection out of time')
                    return (key,ps,pattern,acceptation)
                time.sleep(0.2)
                beats += 1
        self.client.sendall(word.encode('utf-8'))
        server_context = b''
        while True:
            rec = self.client.recv(512)
            if not rec:
                break
            server_context += rec
        self.client.sendall('---shutdown keyword---'.encode('utf-8'))
        self.client.close()
        server_context = server_context.decode('utf-8')
        server_context = server_context.strip()
        #print(server_context)
        if server_context != 'None':
            word_info = json.loads(server_context)
            #print(word_info)
            if word_info['word']:
                key = word_info['word']
            if word_info['pronunciation']:
                if '英' in word_info['pronunciation']:
                    ps += u'英 ' + word_info['pronunciation']['英'] + ' '
                if '美' in word_info['pronunciation']:
                    ps += u'美 ' + word_info['pronunciation']['美']
                if '' in word_info['pronunciation']:
                    ps = u'英/美 ' + word_info['pronunciation']['']
            if word_info['pattern']:
                pattern = word_info['pattern']
            if word_info['paraphrase']:
                acceptation = word_info['paraphrase']
            return (key,ps,pattern,acceptation)
        else:
            return (key,ps,pattern,acceptation)

    def get_look_up_result(self,words,text):
        '''
        查词，返回字典列表，key(单词),ps（音标）,pattern（时态）,acceptation（释义）
        key: 单词，ps: 音标，pattern:时态
        '''
        data = []
        for i in range(len(words)):
            j = i+1
            word = words[i]
            self.look_up(word,text,data)
        print('vocabulary:',len(data))
        return data
    def look_up(self,word,text,data):
        '''
        查词，返回字典列表，key(单词),ps（音标）,pattern（时态）,acceptation（释义）
        key: 单词，ps: 音标，pattern:时态
        '''
        if self.look_up_one(word):
            datum = {}
            key,ps,pattern,acceptation=self.look_up_one(word)
            count = self.word_counts.get(key,0)
            datum['key'] = key
            datum['ps'] = ps
            datum['pattern'] = pattern
            datum['acceptation'] = acceptation
            data.append(datum)
    def write_words(self,data):
        with open(self.save_filename,'w',encoding='utf-8') as f:
            for datum in data:
                text = '{}\t{}\t{}'.format(datum['key'],datum['ps'],datum['pattern'])
                for paraphrase in datum['acceptation']:
                    text += '\n  ' + paraphrase
                text += '\n\n'
                f.write(text)

if __name__=='__main__':
    if len(sys.argv) == 1:
        file = 'wordlist.txt'
        work =  vocabulary(file,save_path = '')
    if len(sys.argv) == 2:
        file = sys.argv[1]
        work =  vocabulary(file,save_path = '')
    if len(sys.argv) > 2:
        file = sys.argv[1]
        learned_words_file = sys.argv[2]
        work =  vocabulary(file,learned_words_file,save_path = '')
    data = work.run()
