import numpy
from interval import *
from math import *
class IntervalSets:
    #m为子序列长度，可以自行设置，默认为100
    def __init__(self,m=100):
        self.m=m
    '''
    功能：利用IntervalSets方法计算出每个序列的异常结构分数
    输入：data-从CSV文件读取的数据信息，不含标签，一维
    输出：每个序列的异常结构分数以及排序后的下标
    运行示例：
        import numpy as np
        import matplotlib.pyplot as plt
        from IntervalSets import *
        
        m=400  #设置子序列长度，ECG为400，chfdb为250时效果最佳
        #创建对象
        IS=IntervalSets(m)
        #从CSV文件读取数据
        data= np.genfromtxt('ECG108_2.csv',delimiter=',')
        #调用IntervalSets方法来查找异常
        SAS,SAS_index=IS.intervalsets(data)
        print(SAS)  #输出异常结构分数SAS
        print("最可能的异常序列标号为：",SAS_index[len(SAS_index)-1])
        
        #可视化标注异常
        x0=range(0,data.__len__())
        plt.plot(x0,data)
        t=SAS_index[len(SAS_index)-1]
        x1=range(t*m,t*m+m-1)
        plt.plot(x1,data[t*m:t*m+m-1],color="red")
        plt.text(100, 1,"m=400", size = 15, alpha = 0.8)
        plt.show()
        
    '''
    def intervalsets(self,data):
        data_matrix=self.split_data(data)   #对数据进行划分，形成多个子序列
        n=len(data_matrix) #子序列的个数
        m=self.m    #子序列长度
        Sp=self.cal_Sp(data_matrix)
        SA=self.cal_SA(data_matrix)
        #计算每个子序列的异常结构分数
        S=list()    #二维
        SAS=list()  #存储分数，一维
        for i in range(n):
            S_i=0
            for j in range(n):
                S_i=S_i+(0.5*SA[i][j]+0.5*Sp[i][j])
            S.append(S_i)
        for i in range(n):
            SAS_i =0
            for j in range(n):
                SAS_i=SAS_i+(S[i]-S[j])**2
            SAS.append(SAS_i/n)
        #排序
        SAS_index = numpy.argsort(SAS)

        return SAS,SAS_index

    '''
       输入：data_matrix，二维数据
       功能：类的私有方法，计算子序列之间的概率相似性Sp,boundary为区间边界参数
       输出：Sp，二维矩阵，每行为一个子序列与其他子序列的Spij值
    '''
    def cal_Sp(self,data_matrix,boundary=0.2):
        Sp=list()
        Amin = list()  # 每一行存储一个子序列的最小值
        Amax = list()  # 每一行存储一个子序列的最大值
        Pmin = list()  # 每一行存储一个子序列的概率最小值
        Pmax = list()  # 每一行存储一个子序列的概率最大值
        n = len(data_matrix)  # 子序列数量

        widths=self.find_best_w(data_matrix)
        #求子序列的取值区间
        for i in range(n):
            Amin.append(min(data_matrix[i]))  # 子序列最小值
            Amax.append(max(data_matrix[i]))  # 子序列最大值
        #求点分布在边界区间的概率
        for i in range(n):
            count_min=0
            count_max = 0
            for item in data_matrix[i]:
                if item>=Amin[i] and item<=Amin[i]+boundary*(Amax[i]-Amin[i]):
                    count_min=count_min+1
                if item>=Amax[i]-boundary*(Amax[i]-Amin[i]) and item<=Amax[i]:
                    count_max = count_max + 1

            Pmin.append(count_min/self.m)
            Pmax.append(count_max/self.m)

        #利用边界的点分布概率计算Sp
        for i in range(n):
            Sp_i=list()
            for j in range(n):
                if i==j:
                    Sp_i.append(1)
                else:
                    p=exp(-((Pmin[i]-Pmin[j])**2+(Pmax[i]-Pmax[j])**2)/widths[i]**2)
                    #p=numpy.exp(-1.0 * numpy.linalg.norm(one - two, ord=2) / numpy.power(w, 2))
                    Sp_i.append(p)
            Sp.append(Sp_i)
        return Sp



    '''
       输入：data_matrix，二维数据
       功能：类的私有方法，计算子序列之间的概率相似性SA
       输出：SA，二维矩阵，每行为一个子序列与其他子序列的SAij值
    '''

    def cal_SA(self, data_matrix):
        Amin=list()    #每一行存储一个子序列的最小值
        Amax = list()  # 每一行存储一个子序列的最大值
        SA=list()   #存储区相似度
        n=len(data_matrix) #子序列数量

        for i in range(n):
            Amin.append(min(data_matrix[i]))  # 子序列最小值
            Amax.append(max(data_matrix[i]))  # 子序列最大值

        for i in range(n):
            SA_i=list()
            A_i=Interval(Amin[i],Amax[i])
            #print(A_i)
            for j in range(n):
                A_j=Interval(Amin[j],Amax[j])
                if A_i.overlaps(A_j)==False:    #情况1，没有交集
                    SA_i.append(0)
                else:   #情况2，有交集
                    A_ij=A_i.join(A_j)  #合并
                    a=((A_i.upper_bound-A_i.lower_bound)+(A_j.upper_bound-A_j.lower_bound)-(A_ij.upper_bound-A_ij.lower_bound))/(A_ij.upper_bound-A_ij.lower_bound)
                    SA_i.append(a)
            SA.append(SA_i)

        return SA

    '''
       输入：data，一维数据
       功能：将读取到的一维数据按照传入的子序列长度进行划分
       输出：data_matrix，二维矩阵，每行为一个子序列
    '''
    def split_data(self, data):
        index = self.m
        length = data.__len__()
        data_matix = list()
        sequence = list()
        i = 0
        while i < length:
            sequence = data[i:i + index]
            # print(sequence)
            i = i + index
            data_matix.append(sequence)
        return data_matix

    '''
    函数功能：计算数据集的δ，高斯径向基函数的半径，通过信息熵的方法计算
    返回一个与子序列长度相等的数组
    '''
    def find_best_w(self, data_matrix):

        alist, blist = numpy.zeros(data_matrix.__len__()), numpy.zeros(data_matrix.__len__())
        r_index = range(data_matrix.__len__())
        gama = (5 ** 0.5 - 1) / 2
        coe = (2 ** 0.5) / 3
        for i in r_index:
            min_dist, max_dist = float('inf'), -float('inf')
            for j in r_index:
                if i == j:
                    continue
                dist = numpy.linalg.norm(data_matrix[i] - data_matrix[j], ord=2)  # 求二范数
                min_dist = min(dist, min_dist)
                max_dist = max(dist, max_dist)
            alist[i], blist[i] = coe * min_dist, coe * max_dist
        left, right = cal_sig(alist, blist, gama)
        ent_left = cal_entropy(left)
        ent_right = cal_entropy(right)
        epison = 1
        times = 0
        while numpy.linalg.norm(alist - blist) < 1 and times < 20:
            if ent_left < ent_right:
                blist, right = right.copy(), left.copy()
                ent_right = ent_left
                left = alist + (1 - gama) * (blist - alist)
                ent_left = cal_entropy(left)
            else:
                alist, left = left.copy(), right.copy()
                ent_left = ent_right
                right = alist + gama * (blist - alist)
                ent_right = cal_entropy(right)

            times += 1

        if ent_left < ent_right:
            return left
        else:
            return right


def cal_sig(alist, blist, gama):
    length = len(alist)
    index = range(length)
    left, right = numpy.zeros(length), numpy.zeros(length)
    for i in index:
        left[i] = alist[i] + (1 - gama) * (blist[i] - alist[i])
        right[i] = alist[i] + gama * (blist[i] - alist[i])
    return left, right

'''
计算信信息熵
'''
def cal_entropy(list):
    total = sum(list)
    list /= total
    log_list = numpy.log(list)
    return -numpy.dot(list, log_list)


