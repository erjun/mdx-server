#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# 代码来自 https://github.com/skywind3000/ECDICT
# 词形衍生：查找动词的各种时态，名词的复数等，或反向查找
# 格式为每行一条数据：根词汇 -> 衍生1,衍生2,衍生3
# 可以用 Hunspell数据生成，下面有个日本人做的简版（1.8万组数据）：
# http://www.lexically.net/downloads/version4/downloading%20BNC.htm
# ----------------------------------------------------------------------
import sys


class LemmaDB(object):

    def __init__(self):
        self._stems = {}
        self._words = {}
        self._frqs = {}

    # 读取数据
    def load(self, filename, encoding=None):
        content = open(filename, 'rb').read()
        if content[:3] == b'\xef\xbb\xbf':
            content = content[3:].decode('utf-8', 'ignore')
        elif encoding is not None:
            text = content.decode(encoding, 'ignore')
        else:
            text = None
            match = ['utf-8', sys.getdefaultencoding(), 'ascii']
            for encoding in match + ['gbk', 'latin1']:
                try:
                    text = content.decode(encoding)
                    break
                except:
                    pass
            if text is None:
                text = content.decode('utf-8', 'ignore')
        number = 0
        for line in text.split('\n'):
            number += 1
            line = line.strip('\r\n ')
            if (not line) or (line[:1] == ';'):
                continue
            pos = line.find('->')
            if not pos:
                continue
            stem = line[:pos].strip()
            p1 = stem.find('/')
            frq = 0
            if p1 >= 0:
                frq = int(stem[p1 + 1:].strip())
                stem = stem[:p1].strip()
            if not stem:
                continue
            if frq > 0:
                self._frqs[stem] = frq
            for word in line[pos + 2:].strip().split(','):
                p1 = word.find('/')
                if p1 >= 0:
                    word = word[:p1].strip()
                if not word:
                    continue
                self.add(stem, word.strip())
        return True

    # 保存数据文件
    def save(self, filename, encoding='utf-8'):
        stems = list(self._stems.keys())
        stems.sort(key=lambda x: x.lower())
        import codecs
        fp = codecs.open(filename, 'w', encoding)
        output = []
        for stem in stems:
            words = self.get(stem)
            if not words:
                continue
            frq = self._frqs.get(stem, 0)
            if frq > 0:
                stem = '%s/%d' % (stem, frq)
            output.append((-frq, u'%s -> %s' % (stem, ','.join(words))))
        output.sort()
        for _, text in output:
            fp.write(text + '\n')
        fp.close()
        return True

    # 添加一个词根的一个衍生词
    def add(self, stem, word):
        if stem not in self._stems:
            self._stems[stem] = {}
        if word not in self._stems[stem]:
            self._stems[stem][word] = len(self._stems[stem])
        if word not in self._words:
            self._words[word] = {}
        if stem not in self._words[word]:
            self._words[word][stem] = len(self._words[word])
        return True

    # 删除一个词根的一个衍生词
    def remove(self, stem, word):
        count = 0
        if stem in self._stems:
            if word in self._stems[stem]:
                del self._stems[stem][word]
                count += 1
            if not self._stems[stem]:
                del self._stems[stem]
        if word in self._words:
            if stem in self._words[word]:
                del self._words[word][stem]
                count += 1
            if not self._words[word]:
                del self._words[word]
        return (count > 0) and True or False

    # 清空数据库
    def reset(self):
        self._stems = {}
        self._words = {}
        return True

    # 根据词根找衍生，或者根据衍生反向找词根
    def get(self, word, reverse=False):
        if not reverse:
            if word not in self._stems:
                if word in self._words:
                    return [word]
                return None
            words = [(v, k) for (k, v) in self._stems[word].items()]
        else:
            if word not in self._words:
                if word in self._stems:
                    return [word]
                return None
            words = [(v, k) for (k, v) in self._words[word].items()]
        words.sort()
        return [k for (v, k) in words]

    # 知道一个单词求它的词根
    def word_stem(self, word):
        return self.get(word, reverse=True)

    # 总共多少条词根数据
    def stem_size(self):
        return len(self._stems)

    # 总共多少条衍生数据
    def word_size(self):
        return len(self._words)

    def dump(self, what='ALL'):
        words = {}
        what = what.lower()
        if what in ('all', 'stem'):
            for word in self._stems:
                words[word] = 1
        if what in ('all', 'word'):
            for word in self._words:
                words[word] = 1
        return words

    def __len__(self):
        return len(self._stems)

    def __getitem__(self, stem):
        return self.get(stem)

    def __contains__(self, stem):
        return (stem in self._stems)

    def __iter__(self):
        return self._stems.__iter__()
