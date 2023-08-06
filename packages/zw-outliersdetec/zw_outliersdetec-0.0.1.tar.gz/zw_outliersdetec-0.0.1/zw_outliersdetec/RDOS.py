import numpy as np
from sklearn.neighbors import NearestNeighbors
from math import *

'''
说明：RDOS算法，根据K近邻集合、逆近邻集合以及共享近邻集合进行对象的核密度估计，从而得出异常分数
传入参数：k-近邻的个数，h-高斯核的宽度参数
'''
class RDOS:
    #初始化，传入参数并设置默认值
    def __init__(self,n_outliers=1,n_neighbors=5,h=2):
        self.n_outliers=n_outliers
        self.n_neighbors=n_neighbors
        self.h=h

    '''
    RDOS
    输入：data-数据集，n-返回的异常个数(默认为1)，n_neighbors-近邻个数，h-高斯核函数的宽度参数
    输出：返回异常的分数以及按异常分数排序好的下标，同时会根据预设的异常个数输出其下标及得分
    运行示例：
        import pandas as pd
        from RDOS import *
        
        #如果是带有Lable的数据集则需要先去除Label列
        data=pd.read_csv("hbk.csv",sep=',')
        #data=data.drop('Label', axis=1)
        data=np.array(data)
        print(data.shape)
        #调用RDOS算法，传入预设的异常个数
        rdos=RDOS(n_outliers=10)
        RDOS_index,RDOS_score=rdos.rdos(data)
    '''
    def rdos(self,data):
        n_outliers = self.n_outliers
        n_neighbors=self.n_neighbors
        h=self.h
        n=data.shape[0] #n是数据集的样例数量
        d=data.shape[1] #d是数据集的维度，即属性个数

        #规范输入的参数
        if n_neighbors>=n or n_neighbors<1:
            print('n_neighbors input must be less than number of observations and greater than 0')
            exit()

        outliers=list()
        #存储每个数据对象的近邻下标
        Sknn= list()
        Srnn= list()
        Ssnn = list()
        S= list()
        P= list()
        #计算Sknn
        for X in data:
            Sknn_temp = self.KNN(data, [X], return_distance=False)
            Sknn_temp = np.squeeze(Sknn_temp)
            Sknn.append(Sknn_temp[1:])
            S.append(list(Sknn_temp[1:]))  # X的所有近邻集合
        #计算Srnn
        for i in range(n):
            Srnn_temp = list()  # 记录每个数据对象的rnn
            for item in Sknn[i]:
                item_neighbors = Sknn[item]
                # 如果X的近邻的k近邻集合中也包含X，说明该近邻是X的逆近邻
                if i in item_neighbors:
                    Srnn_temp.append(item)
            Srnn.append(Srnn_temp)
            S[i].extend(Srnn_temp)  # X的所有近邻集合
        #计算Ssnn
        for i in range(n):
            Ssnn_temp = list()
            for j in Sknn[i]:
                kneighbor_rnn = Srnn[j]  # k近邻的逆近邻集合
                Ssnn_temp.extend(kneighbor_rnn)
            Ssnn_temp = list(set(Ssnn_temp))  # 去重
            if i in Ssnn_temp:
                Ssnn_temp.remove(i)  # 删除X本身下标
            Ssnn.append(Ssnn_temp)  # X的共享近邻集合
            S[i].extend(Ssnn_temp)  # X的所有近邻集合
            S[i] = list(set(S[i]))  # 去重

            P.append(self.getKelnelDensity(data, i, S[i]))#计算论文中的P值

        '''
        #计算每个数据对象的近邻集合
        for i in range(n):
            Sknn_temp=self.KNN(data,[data[i]],return_distance=False)
            Sknn_temp = np.squeeze(Sknn_temp)
            print("Sknn:",Sknn_temp[1:])
            Sknn.append(Sknn_temp[1:]) #需要除去其本身,例：[[11 29  7 26 24]]→[29  7 26 24]
            Srnn.append(self.RNN(data,[data[i]],return_distance=False)) #例：[29 24]
            Ssnn_temp=list()
            for j in Sknn[i]:
                kneighbor_rnn = self.RNN(data, [data[j]], return_distance=False) #k近邻的逆近邻集合
                Ssnn_temp.extend(kneighbor_rnn)
            Ssnn_temp = list(set(Ssnn_temp))  # 去重
            if i in Ssnn_temp:
                Ssnn_temp.remove(i)  # 删除X本身下标
            Ssnn.append(Ssnn_temp) #X的共享近邻集合
            S.append(list(set(Ssnn_temp)))  #X的所有近邻集合
            '''

            #print("S:",S[i]) #打印


        #计算异常得分RDOS
        RDOS_score=list()

        for i in range(n):
            S_RDOS=0
            for j in S[i]:  #计算近邻集合的RDOS总分数
                S_RDOS=S_RDOS+P[j]

            RDOS_score.append(S_RDOS/(len(S[i])*P[i]))

        RDOS_index= np.argsort(RDOS_score) #对异常分数进行排序，从低到高,返回的是数组的索引


        return RDOS_score,RDOS_index[::-1]  #返回异常的得分及其下标（下标由得分从高到低排序）



    '''
    找出数据集X中每个对象的的k近邻并返回序号(当k>1时，会包括其本身)
    X可以是一个点或者一组数据,data是所有数据
    return_distance=True时会同时返回距离
    '''
    def KNN(self,data,X,return_distance=False):
        neigh = NearestNeighbors(self.n_neighbors)
        neigh.fit(data)
        return neigh.kneighbors(X, return_distance=return_distance)

    '''
    找出X的k逆近邻集合并返回序号
    X是一个数据对象,data是所有数据
    return_distance=True时会同时返回距离
    
    def RNN(self, data, X, return_distance=False):
        neigh = NearestNeighbors(self.n_neighbors)
        neigh.fit(data)
        X_neighbors=neigh.kneighbors(X, return_distance=return_distance)
        X_Srnn=list()   #存储逆近邻的下标集合
        # 遍历X的近邻集合寻找其逆近邻集合，item为近邻的序号
        index = X_neighbors[0, 1:]
        X_index = X_neighbors[0, 0] #X的下标
        #近邻的下标
        for item in index:
            item_neighbors = neigh.kneighbors([data[item]], return_distance=False)  #寻找近邻的k近邻集合
            # 如果X的近邻的k近邻集合中也包含X，说明该近邻是X的逆近邻
            if X_index in item_neighbors:
                X_Srnn.append(item)
        return np.array(X_Srnn)
    '''

    '''
    计算核密度
    输入：data-数据集，X_index-数据对象的下标，S近邻集合
    输出：论文中的P
    '''
    def getKelnelDensity(self,data,X_index,S):
        h=self.h    #高斯核函数参数
        d=data.shape[1] #数据的属性个数
        S_X=list(S)
        S_X.append(X_index)
        X_guassian =0
        for i in S_X:
            X_guassian+=(1/((2*pi)**(d/2)))*exp(-(np.linalg.norm(data[i]-data[X_index]))/(2*h**2))

        S_len=S.__len__()
        P=1/(S_len+1)*(1/h**d)*X_guassian
        return P









