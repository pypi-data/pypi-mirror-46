# Copyright 2018 Zhao Xingyu & An Yuexuan. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
import numpy as np


# 汉语nlp：句子转成字典与labels列表
def sentence_to_list(text, return_dict=False, Chinese=False):
    # text：输入的句子
    # return_dict：是否返回字典
    # Chinese：是否为中文
    if Chinese:
        idx_to_char = list(set(''.join(np.array(text, np.str).ravel().tolist())))  # 把句子里的每一个字转换成列表，并删除重复字。可以把索引转为字
        char_to_idx = dict([(char, i + 1) for i, char in enumerate(idx_to_char)])  # 一个字典，键为字，值是索引。可以把字转为标签
        text_list = []
        for sentence in text:
            text_list.append([char_to_idx[char] for char in sentence])
        if return_dict:
            return text_list, idx_to_char  # 返回转成的list与索引转成字的字典
        else:
            return text_list
    else:
        idx_to_char = list(
            set(''.join(np.array(text, np.str).ravel().tolist()).split()))  # 把句子里的每一个字转换成列表，并删除重复字。可以把索引转为字
        print(idx_to_char)
        char_to_idx = dict([(char, i + 1) for i, char in enumerate(idx_to_char)])  # 一个字典，键为字，值是索引。可以把字转为标签
        text_list = []
        for sentence in text:
            text_list.append([char_to_idx[char] for char in sentence.split()])
        if return_dict:
            return text_list, idx_to_char  # 返回转成的list与索引转成字的字典
        else:
            return text_list