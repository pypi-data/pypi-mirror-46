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
import warnings
import random
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.stats import f, chi2


# 生成迭代器
def data_iter(data, label, batch_size):
    # data:样本数据
    # label：样本标签
    # batch_size：批大小
    data, label = np.array(data), np.array(label)
    n_samples = data.shape[0]
    idx = list(range(n_samples))
    random.shuffle(idx)
    for i in range(0, n_samples, batch_size):
        j = np.array(idx[i:min(i + batch_size, n_samples)])
        yield np.take(data, j, 0), np.take(label, j, 0)


# label转one-hot
def to_categorical(label, num_classes=None):
    # label：样本标签
    # num_calsses：总共的类别数
    label = np.array(label, dtype='int')
    if num_classes is not None:
        assert num_classes > label.max()  # 类别数量错误
    else:
        num_classes = label.max() + 1
    if len(label.shape) == 1:
        y = np.eye(num_classes, dtype='int64')[label]
        return y
    elif len(label.shape) == 2 and label.shape[1] == 1:
        y = np.eye(num_classes, dtype='int64')[label.squeeze()]
        return y
    else:
        warnings.warn('Warning: one_hot_to_label do not work')
        return label


# one-hot转label
def one_hot_to_label(y):
    # y：one-hot编码
    y = np.array(y)
    if len(y.shape) == 2 and y.max() == 1 and y.sum(1).mean() == 1:
        return y.argmax(1)
    else:
        warnings.warn('Warning: one_hot_to_label do not work')
        return y


# 画出样本数据示意图
def plot(x, y, method='t-SNE'):
    # x：数据
    # y：标签
    # method：可视化方法
    x, y = check_data_target(x, y)
    if method == 't-SNE':
        x = TSNE(n_components=2).fit_transform(x)
    elif method == 'PCA' or method == 'pca':
        x = PCA(n_components=2).fit_transform(x)
    elif method == 'MDS' or method == 'mds':
        x = MDS(n_components=2).fit_transform(x)
    else:
        warnings.warn('Wrong method!')
        return
    for i in range(y.max() + 1):
        plt.scatter(x[y == i][:, 0], x[y == i][:, 1], label='class %d' % i)
    plt.legend()
    plt.show()


# 画出分类边界图
def plot_classifier(classifier, x, y):
    # classifier：分类器
    # x：数据
    # y：标签
    x, y = check_data_target(x, y)
    x1_min, x1_max = np.min(x[:, 0]) - 1, np.max(x[:, 0]) + 1
    x2_min, x2_max = np.min(x[:, 1]) - 1, np.max(x[:, 1]) + 1
    step_size = 0.01
    x1_values, x2_values = np.meshgrid(np.arange(x1_min, x1_max, step_size), np.arange(x2_min, x2_max, step_size))
    mesh_output = classifier.predict(np.c_[x1_values.ravel(), x2_values.ravel()])
    mesh_output = mesh_output.reshape(x1_values.shape)
    plt.figure()
    plt.pcolormesh(x1_values, x2_values, mesh_output, cmap=plt.cm.gray)
    plt.scatter(x[:, 0], x[:, 1], c=y, s=80, linewidths=1, cmap=plt.cm.Paired)
    plt.xlim(x1_values.min(), x1_values.max())
    plt.ylim(x2_values.min(), x2_values.max())
    plt.xticks((np.arange(int(np.min(x[:, 0]) - 1), int(np.max(x[:, 0]) + 1), 1)))
    plt.yticks((np.arange(int(np.min(x[:, 1]) - 1), int(np.max(x[:, 1]) + 1), 1)))
    plt.show()


# 检查数据和标签的形状
def check_data_target(x, y):
    # x：数据
    # y：标签
    x, y = np.array(x), np.array(y)
    assert x.ndim == 2  # 数据形状错误
    assert y.ndim == 1 or (y.ndim == 2 and y.shape[1] == 1)  # 标签形状错误
    if y.ndim == 2 and y.shape[1] == 1:
        y = y.squeeze()
    return x, y


# Friedman检测
def Friedman_test(x, alpha=0.025, ranked=False, use_f_distribution=False, verbose=False):
    # x：各个算法在不同数据集上的得分或排序，形状为[数据集个数,算法个数]
    # alpha：显著性水平
    # ranked：输入的数据是否为排序
    # use_f_distribution：是否使用改进的Friedman检测
    # verbose：当输入数据为得分时，是否打印排序结果
    x = np.array(x) + 0.
    n_datasets, n_algorithms = x.shape[0], x.shape[1]
    if not ranked:  # 输入为得分
        for i in range(n_datasets):  # 对于第i个数据集
            rank_list = np.zeros([n_algorithms])  # 不同算法的排名
            score = x[i].copy()
            chuli = 0
            while chuli != n_algorithms:
                M = np.max(score)
                score_equal = []
                for j in range(n_algorithms):
                    if score[j] == M:
                        score_equal.append(j)
                rank_list[score_equal] = np.sum(np.arange(chuli + 1, chuli + 1 + len(score_equal))) / len(score_equal)
                score[score_equal] = -np.inf
                x[i] = rank_list.copy()
                chuli += len(score_equal)
        if verbose:
            print('输入得分排名为：')
            print(x)
    R = np.mean(x, axis=0)
    Tao = 12 * n_datasets / n_algorithms / (n_algorithms + 1) * np.sum(np.square(R - (n_algorithms + 1) / 2))
    if use_f_distribution:  # 使用改进的Friedman检测
        F = f.isf(q=alpha, dfn=(n_algorithms - 1), dfd=int(n_algorithms - 1) * (n_datasets - 1))
        Tao = (n_datasets - 1) * Tao / (n_datasets * (n_algorithms - 1) - Tao)
        if Tao > F:
            print('Tao值为%.4f，显著性水平为%.4f的F分布值为%.4f，有显著区别' % (Tao, alpha, F))
        else:
            print('Tao值为%.4f，显著性水平为%.4f的F分布值为%.4f，无显著区别' % (Tao, alpha, F))
    else:  # 使用传统的Friedman检测
        Chi2 = chi2.isf(q=alpha, df=n_algorithms - 1)
        if Tao > Chi2:
            print('Tao值为%.4f，显著性水平为%.4f的卡方分布值为%.4f，有显著区别' % (Tao, alpha, Chi2))
        else:
            print('Tao值为%.4f，显著性水平为%.4f的卡方分布值为%.4f，无显著区别' % (Tao, alpha, Chi2))


# 计算Gram矩阵
def Gram(x):
    # x：输入数据/向量
    x = np.array(x).squeeze()
    assert len(x.shape) == 1  # 样本维度不符
    return x.reshape(-1, 1) * x