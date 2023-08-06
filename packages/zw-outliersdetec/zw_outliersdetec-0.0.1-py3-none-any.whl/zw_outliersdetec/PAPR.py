
import numpy
from sklearn.preprocessing import scale

class PAPR:
    splits = dict() #创建一个新的字典
    splits[2] = [0, float('inf')]   #float（‘inf’）正无穷
    splits[3] = [-0.43, 0.43, float('inf')]
    splits[4] = [-0.67, 0, 0.67, float('inf')]
    splits[5] = [-0.84, -0.25, 0.25, 0.84, float('inf')]
    splits[6] = [-0.97, -0.43, 0, 0.43, 0.97, float('inf')]
    splits[7] = [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07, float('inf')]
    splits[8] = [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, float('inf')]
    splits[9] = [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, float('inf')]
    splits[10] = [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28, float('inf')]

    def __init__(self,m):
        self.m=m

    '''
    功能：利用PAPR_RW算法进行异常分数的计算
    输入：data，从CSV文件读取的一维数据
    输出：data_matrix，二维矩阵，每行为一个子序列
    运行示例：
        from PAPR import *
        import numpy as np
        import matplotlib.pyplot as plt
        
        m=250  #设置子序列长度,每个数据集不一样
        P=PAPR(m)
        #从CSV文件读取数据，不带标签
        data = np.genfromtxt("chfdb_1.csv", delimiter=',')
        
        scores,scores_index=P.PAPR(data)
        
        #可视化标注异常
        t=scores_index[0]   #得分最低的序列的下标，该序列被认为是异常
        x0=range(0,data.__len__())
        plt.plot(x0,data)
        x1=range(t*m,t*m+m-1)
        plt.plot(x1,data[t*m:t*m+m-1],color="red")
        plt.show()
    
    '''
    def papr(self,data):
        m=self.m  #划分的序列长度
        # 将数据划分成多个子序列
        data_matrix = self.split_data(data)
        # 对子序列分别进行归一化处理
        data_matrix = scale(data_matrix, axis=1)
        # 计算子序列的高斯径向基函数的宽度参数
        widths = self.find_best_w(data_matrix)
        matrix = self.cal_matrix(data_matrix, 6)
        sim_matrix = self.cal_similarity(matrix=matrix, wc=0.3, wd=0.4, wr=0.3, length=widths.__len__(), widths=widths)
        scores = self.random_walk(sim_matrix, error=0.05)

        scores_index=numpy.argsort(scores) #异常分数从低到高排序

        return scores,scores_index


    '''
    输入：data，一维数据
    功能：将读取到的一维数据按照传入的子序列长度进行划分
    输出：data_matrix，二维矩阵，每行为一个子序列
    '''
    def split_data(self,data):
        index=self.m
        length=data.__len__()
        data_matix=list()
        sequence=list()
        i=0
        while i<length:
            sequence=data[i:i+index]
           # print(sequence)
            i=i+index
            data_matix.append(sequence)
        return data_matix

    '''
    值空间划分以及PAPR指标的计算
    '''
    def cal_matrix(self,data, k):
        points = self.splits[k]
        new_data = list()
        for item in data:
            tmp_points = list()
            for i in range(k):
                tmp_points.append(list())
            for p in item:
                for w in range(k):
                    if p < points[w]:
                        tmp_points[w].append(p)
                        break
            tmp_matrix = numpy.zeros((k, 3))    #生成一个K行3列的全0矩阵，用于记录PAPR方法得出的Mi = [di, ci, ri]
            for w in range(k):
                tmp_matrix[w, 0] = len(tmp_points[w])   #记录子值空间的点个数
                if tmp_matrix[w, 0] != 0:
                    tmp_matrix[w, 1] = numpy.mean(tmp_points[w])     #记录子值空间的点均值
                    tmp_matrix[w, 2] = numpy.var(tmp_points[w])     #记录子值空间的方差
            new_data.append(tmp_matrix)

        return numpy.array(new_data)

    '''
    计算相似度矩阵
    #length是子序列的数量，width是计算Scij和Srij使所用到的δ
    '''
    def cal_similarity(self,matrix, length, wd, wc, wr, widths):
        index = range(length)
        sim_matrix = numpy.zeros((length, length))   #生成一个length行length列的全0矩阵
        for r in index:
            for c in index:
                sd = self.cal_d_sim(matrix[r, :, 0], matrix[c, :, 0])
                sc = self.cal_rc_sim(matrix[r, :, 1], matrix[c, :, 1], widths[r])
                sr = self.cal_rc_sim(matrix[r, :, 2], matrix[c, :, 2], widths[r])
                sim_matrix[r, c] = wd*sd + wc*sc + wr*sr
        return sim_matrix

    '''
    函数功能：计算记录两点数量的向量di和dj的相似度Sdij
    '''
    def cal_d_sim(self,one, two):
        #m是子序列one的总长度，m=∑（k=1..q）dik
        m = numpy.sum(one)
        #length是记录子序列特征的Mi=[di,ci,ri]的长度,即子值空间的划分数目
        length = len(one)
        s = 0
        for l in range(length):
            s += min(one[l], two[l])
        return 1.0 * s / m

    '''
    函数功能：计算Scij和Srij，两个计算公式相同
    w即δ，高斯径向基函数的半径，通过信息熵的方法可以计算出每个数据集的该值
    '''
    def cal_rc_sim(self,one, two, w=0.005):
        return numpy.exp(-1.0 * numpy.linalg.norm(one - two, ord=2) / numpy.power(w, 2))

    '''
    RW模型,最终会得到一个概率分布矩阵，即异常得分
    '''
    def random_walk(self,sim_matrix, error=0.1):
        rows, cols = sim_matrix.shape
        s_matrix = numpy.zeros((rows, cols))
        for r in range(rows):
            totSim = 0.0
            for c in range(cols):
                totSim += sim_matrix[r, c]
            for c in range(cols):
                s_matrix[r, c] = 1.0*sim_matrix[r, c] / totSim

        damping_factor = 0.1
        ct = numpy.array([1.0/rows]*rows)
        recursive_err = error+1
        times = 0
        while recursive_err > error and times < 100:
            ct1 = damping_factor/rows + numpy.dot(s_matrix.T, ct)
            recursive_err = numpy.linalg.norm(ct-ct1, ord=1)
            times += 1
            ct = ct1[:]
        return ct

    '''
    函数功能：计算数据集的δ，高斯径向基函数的半径，通过信息熵的方法计算
    '''
    def find_best_w(self,data_matrix):

        alist, blist = numpy.zeros(data_matrix.__len__()), numpy.zeros(data_matrix.__len__())
        r_index = range(data_matrix.__len__())
        gama = (5**0.5-1)/2
        coe = (2**0.5)/3
        for i in r_index:
            min_dist, max_dist = float('inf'), -float('inf')
            for j in r_index:
                if i == j:
                    continue
                dist = numpy.linalg.norm(data_matrix[i]-data_matrix[j], ord=2)    #求二范数
                min_dist = min(dist, min_dist)
                max_dist = max(dist, max_dist)
            alist[i], blist[i] = coe*min_dist, coe*max_dist
        left, right = cal_sig(alist, blist, gama)
        ent_left = cal_entropy(left)
        ent_right = cal_entropy(right)
        epison = 1
        times = 0
        while numpy.linalg.norm(alist-blist) < 1 and times < 20:
            if ent_left < ent_right:
                blist, right = right.copy(), left.copy()
                ent_right = ent_left
                left = alist + (1-gama)*(blist-alist)
                ent_left = cal_entropy(left)
            else:
                alist, left = left.copy(), right.copy()
                ent_left = ent_right
                right = alist + gama*(blist-alist)
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
        left[i] = alist[i] + (1-gama)*(blist[i]-alist[i])
        right[i] = alist[i] + gama*(blist[i]-alist[i])
    return left, right

'''
计算信信息熵
'''
def cal_entropy(list):
    total = sum(list)
    list /= total
    log_list = numpy.log(list)
    return -numpy.dot(list, log_list)

