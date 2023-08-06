# -*- coding: utf-8 -*-
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
import numpy as np
import warnings


# 核方法（A:[m1,n],B:[m2,n],K:[m1,m2]）
def Kernel(A, B=None, kernel='linear', gamma=0.1, q=0.1, degree=3):
    A = np.array(A, np.float)
    if B is None:
        B = A.copy()
    B = np.array(B, np.float)
    if kernel == 'linear':  # 线性核
        my_kernel = A.dot(B.T)
    elif kernel == 'polynomial' or kernel == 'poly':  # 多项式核
        my_kernel = (gamma * A.dot(B.T) + q) ** degree
    elif kernel == 'sigmoid':  # Sigmoid核
        my_kernel = np.tanh(gamma * A.dot(B.T) - q)
    elif kernel == 'rbf':  # 高斯核
        rA = np.sum(np.square(A), 1, keepdims=True)
        rB = np.sum(np.square(B), 1, keepdims=True)
        sq_dists = rA - 2 * A.dot(B.T) + np.transpose(rB)  # x^2-2*x*y+y^2
        my_kernel = np.exp(-gamma * np.abs(sq_dists))
    elif kernel == 'laplace':  # 拉普拉斯核
        A, B = np.array(A), np.array(B)
        rA, rB = np.expand_dims(A, 1), np.expand_dims(B, 0)
        my_kernel = np.exp(-gamma * np.sum(np.abs(rA - rB), axis=2))
    else:
        print('kernel error!')
        return
    return my_kernel


# 主成分分析
def PCA(x, feature_num=None, svd=False):
    # x：样本
    # feature_num：保留的特征数
    x = np.array(x, np.float)
    if len(x.shape) != 1 and len(x.shape) != 2:
        warnings.warn('数据维度不正确，不执行操作！')
        return None
    if len(x.shape) == 1:
        x = np.expand_dims(x, 0)
    if feature_num is None:
        feature_num = x.shape[1]
    x -= x.mean(0, keepdims=True)
    if svd:
        U, S, VT = np.linalg.svd(x)
        index_sort = np.argsort(S)  # 对奇异值进行排序
        index = index_sort[-1:-(feature_num + 1):-1]
        return x.dot(VT[index])  # 乘上最大的feature_num个奇异值组成的特征向量
    else:
        eigval, eigvec = np.linalg.eig(x.transpose().dot(x) / x.shape[0])
        index_sort = np.argsort(eigval)  # 对特征值进行排序
        index = index_sort[-1:-(feature_num + 1):-1]
        return x.dot(eigvec[:, index])  # 乘上最大的feature_num个特征组成的特征向量


# 核化主成分分析
def KernelPCA(x, feature_num=None, kernel='rbf', gamma=0.1, q=0.1, degree=3):
    # x：样本
    # feature_num：保留的特征数
    x = np.array(x, np.float)
    if len(x.shape) != 1 and len(x.shape) != 2:
        warnings.warn('数据维度不正确，不执行操作！')
        return None
    if len(x.shape) == 1:
        x = np.expand_dims(x, 0)
    if feature_num is None:
        feature_num = x.shape[1]
    K = Kernel(x, kernel=kernel, gamma=gamma, q=q, degree=degree)
    one_m = np.ones([x.shape[0], x.shape[0]]) / x.shape[0]
    K = K - one_m.dot(K) - K.dot(one_m) + one_m.dot(K).dot(one_m)
    eigval, eigvec = np.linalg.eig(K)
    index_sort = np.argsort(eigval)  # 对特征值进行排序
    index = index_sort[-1:-(feature_num + 1):-1]
    lambdas = eigval[index]
    alphas = eigvec[:, index]  # 乘上最大的feature_num个特征组成的特征向量
    return K.dot(alphas / np.sqrt(lambdas))
