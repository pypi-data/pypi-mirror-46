import numpy as np
import math
from operator import add
from zw_outliersdetec import __dimension_reduction as dim_red

class FastVOA:
    #t是随机超平面投影时的参数
    def __init__(self,t):
        self.t=t

    #Algorithm 3 FirstMomentEstimator(L; t; n)
    def __first_moment_estimator(self,projected, t, n):
        f1 = [0] * n
        for i in range(0, t):
            cl = [0] * n
            cr = [0] * n
            li = projected[i]
            for j in range(0, n):
                idx = li[j][0]
                cl[idx] = j     #原：cl[idx] = j - 1
                cr[idx] = n - 1 - cl[idx]
            for j in range(0, n):
                f1[j] += cl[j] * cr[j]
        return list(map(lambda x: x * ((2 * math.pi) / (t * (n - 1) * (n - 2))), f1))

    #Algorithm 4 FrobeniusNorm(L; t; n)
    def __frobenius_norm(self,projected, t, n):
        f2 = [0] * n
        sl = np.random.choice([-1, 1], size=(n,), p=None)
        sr = np.random.choice([-1, 1], size=(n,), p=None)
        for i in range(0, t):
            amsl = [0] * n
            amsr = [0] * n
            li = projected[i]
            for j in range(1, n):
                idx1 = li[j][0]
                idx2 = li[j - 1][0]
                amsl[idx1] = amsl[idx2] + sl[idx2]
            for j in range(n - 2, -1, -1):
                idx1 = li[j][0]
                idx2 = li[j + 1][0]
                amsr[idx1] = amsr[idx2] + sr[idx2]
            for j in range(0, n):
                f2[j] += amsl[j] * amsr[j]
        return f2

    #Algorithm 1 FastVOA(S; t; s1; s2)
    '''
    功能：计算每个数据对象的角度值
    输入：train-不带标签的数据，n-数据对象的个数，t-随机超平面投影参数，s1,s2
    输出：每个数据对象的角度值分数scores以及按分数排序后的下标scores_index
    调用示例：
    
        import pandas as pd
        from FastVOA import *
        
        #读取数据,不需要标签
        data=pd.read_csv('isolet.csv',sep=',')
        ytrain = data.iloc[:, -1]
        train=data.drop('Label',axis=1)
        #对数据进行随机超平面投影
        DIMENSION = 600
        t = DIMENSION
        n = train.shape[0]
        print(n)
        #调用FatsVOA进行角度值计算
        fv=FastVOA(t)
        scores,scores_index=fv.fastvoa(train, n, t, 1, 1)
    '''
    def fastvoa(self,train, n, t, s1, s2):
        projected = dim_red.random_projection(train, t)
        f1 = self.__first_moment_estimator(projected, t, n)
        y = []
        for i in range(0, s2):
            s = [0] * n
            for j in range(0, s1):
                result = list(map(lambda x: x ** 2, self.__frobenius_norm(projected, t, n)))
                s = list(map(add, s, result))
            s = list(map(lambda x: x / s1, s))  #s的长度为n（由于result的长度为n）
            y.append(s)     #yi的长度为n，y的长度为s2，y有s2行，n列
        y = list(map(list, zip(*y))) #拆分y
        f2 = []
        for i in range(0, n):
            f2.append(np.average(y[i])) #求均值
        var = [0] * n
        for i in range(0, n):
            f2[i] = (4 * (math.pi ** 2) / (t * (t - 1) * (n - 1) * (n - 2))) * f2[i] - (2 * math.pi * f1[i]) / (t - 1)
            var[i] = f2[i] - (f1[i] ** 2)
        # 排序
        scores=var
        scores_index = np.argsort(scores)  # 按角度值从低到高排序
        return scores,scores_index[::-1]  #返回异常得分及下标
