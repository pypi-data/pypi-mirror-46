# coding:utf-8
"""
@author:ZouLingyun
@date:
@summary:
"""
import os
from difflib import SequenceMatcher
from itertools import chain

import pandas as pd


class HandleData(object):
    def __init__(self, cache_file=None):
        self.cache_file = cache_file or r"D:\tmp\password_infos.xlsx"
        if not os.path.exists(os.path.dirname(self.cache_file)):
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        self.cache_dict = None
        self.pre_mtime = None
        self.load_cache()

    def load_cache(self):
        self.cache_dict = {}
        if not os.path.exists(self.cache_file):
            cache_df = pd.DataFrame(columns=['key', 'value'])
            cache_df.to_excel(self.cache_file, index=False)
            self.cache_dict = {}
        else:
            cache_df = pd.read_excel(self.cache_file)
            cache_df = cache_df.astype(str)
            _tmp_dict = cache_df.to_dict(orient='records')
            for row_dict in _tmp_dict:
                key, value = row_dict['key'].strip(), row_dict['value']
                if key not in self.cache_dict:
                    self.cache_dict[key] = []
                if row_dict not in self.cache_dict[key]:
                    row_dict['show'] = key.ljust(20) + ':' + value
                    self.cache_dict[key].append(row_dict)
        self.pre_mtime = os.stat(self.cache_file).st_mtime

    def search(self, input_word=None, pre_count=10):
        if self.pre_mtime != os.stat(self.cache_file).st_mtime:
            self.load_cache()
        key_seq = self.cache_dict.keys()
        sim_seq = [(key, SequenceMatcher(a=input_word, b=key.lower()).quick_ratio()) for key in key_seq]
        sim_seq.sort(key=lambda x: x[1], reverse=True)
        sim_seq = list(filter(lambda x: x[1] > 0.1, sim_seq))
        targ_keys = [self.cache_dict[key] for key, _ in sim_seq[:pre_count]]
        return list(chain.from_iterable(targ_keys))


if __name__ == '__main__':
    a = HandleData().search('大战', 10)
    print(a)
