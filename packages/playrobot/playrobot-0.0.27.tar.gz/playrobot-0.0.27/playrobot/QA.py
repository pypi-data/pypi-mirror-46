import jieba
import re
import wikipedia
import os
from playrobot import QA

path = os.path.dirname(os.path.abspath(QA.__file__))
jieba.set_dictionary(path + '/dict.txt')

class wikiQA():
    
    def __init__(self,target):
        self.target = target
        self.head = ''
        wikipedia.set_lang("zh-tw")
    
    def headFinding(self):
        words = jieba.lcut(self.target)
        for word in words:
            if(word != u'是' and word != u'在'):
                self.head += word
            else:
                break
            
    def result(self):
        self.headFinding()
        message = wikipedia.summary(self.head,sentences=1)
        message2 = re.sub(u'[a-zA-Z(),（）「」]','',message)
        print(message)
        return message2