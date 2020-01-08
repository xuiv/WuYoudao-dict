# -*- coding: utf-8 -*-
import zlib
import json
from io import BytesIO

class JsonReader:
    def __init__(self):
        self.__main_dict = {}
        self.FILE_NAME = './dict/en.z'
        self.INDEX_FILE_NAME = './dict/en.ind'
        self.ZH_FILE_NAME = './dict/zh.z'
        self.ZH_INDEX_FILE_NAME = './dict/zh.ind'
        self.__index_dict = {}
        self.__zh_index_dict = {}
        self.__mem_dict = {}
        self.__zh_mem_dict = {}
        with open(self.INDEX_FILE_NAME, 'r') as f:
            lines = f.readlines()
            prev_word, prev_no = lines[0].split('|')
            for v in lines[1:]:
                word, no = v.split('|')
                self.__index_dict[prev_word] = (int(prev_no), int(no) - int(prev_no))
                prev_word, prev_no = word, no
            self.__index_dict[word] = (int(no), f.tell() - int(no))
        with open(self.ZH_INDEX_FILE_NAME, 'r') as f:
            lines = f.readlines()
            prev_word, prev_no = lines[0].split('|')
            for v in lines[1:]:
                word, no = v.split('|')
                self.__zh_index_dict[prev_word] = (int(prev_no), int(no) - int(prev_no))
                prev_word, prev_no = word, no
            self.__zh_index_dict[word] = (int(no), f.tell() - int(no))
        with open(self.FILE_NAME, 'rb') as f:
            self.__mem_dict = BytesIO(f.read())
        with open(self.ZH_FILE_NAME, 'rb') as f:
            self.__zh_mem_dict = BytesIO(f.read())

    # return strings of word info
    def get_word_info(self, query_word):
        if query_word in self.__index_dict:
            word_offset = self.__index_dict[query_word]
            self.__mem_dict.seek(word_offset[0])
            bytes_obj = self.__mem_dict.read(word_offset[1])
            str_obj = zlib.decompress(bytes_obj).decode('utf8')
            list_obj = str_obj.split('|')
            word = {}
            word['word'] = list_obj[0]
            word['id'] = list_obj[1]
            word['pronunciation'] = {}
            if list_obj[2]:
                word['pronunciation']['美'] = list_obj[2]
            if list_obj[3]:
                word['pronunciation']['英'] = list_obj[3]
            if list_obj[4]:
                word['pronunciation'][''] = list_obj[4]
            try:
                word['paraphrase'] = json.loads(list_obj[5])
            except:
                word['paraphrase'] = {}
            word['rank'] = list_obj[6]
            word['pattern'] = list_obj[7]
            try:
                word['sentence'] = json.loads(list_obj[8])
            except:
                word['sentence'] = {}
            return json.dumps(word)
        else:
            return None

    def get_zh_word_info(self, query_word):
        if query_word in self.__zh_index_dict:
            word_offset = self.__zh_index_dict[query_word]
            self.__zh_mem_dict.seek(word_offset[0])
            bytes_obj = self.__zh_mem_dict.read(word_offset[1])
            str_obj = zlib.decompress(bytes_obj).decode('utf8')
            list_obj = str_obj.split('|')
            word = {}
            word['word'] = list_obj[0]
            word['id'] = list_obj[1]
            word['pronunciation'] = ''
            if list_obj[2]:
                word['pronunciation'] = list_obj[2]
            try:
                word['paraphrase'] = json.loads(list_obj[3])
            except:
                word['paraphrase'] = {}
            word['desc'] = []
            if list_obj[4]:
                try:
                    word['desc'] = json.loads(list_obj[4])
                except:
                    word['desc'] = {}
            word['sentence'] = []
            if list_obj[5]:
                try:
                    word['sentence'] = json.loads(list_obj[5])
                except:
                    word['sentence'] = {}
            return json.dumps(word)
        else:
             return None

