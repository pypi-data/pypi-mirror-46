import numpy as np
from zw_outliersdetec.__sax_via_window import *

'''
函数功能：计算欧式距离
'''
def euclidean(a, b):
    """Compute a Euclidean distance value."""
    return np.sqrt(np.sum((a-b)**2))

'''
类功能：实现HOT_SAX算法，找出异常时间序列
'''
class HOTSAX:
    #初始化，num_discords-预设输出异常的数量
    def __init__(self,num_discords=2):
        self.num_discords=num_discords

    '''
    功能：利用HOT-SAX算法找出异常时间序列的位置信息
    输入：series-数据集，win-size-自行设置的窗口大小（可理解为序列长度，默认为100），其他参数默认
    输出：根据设定的异常个数输出异常的开始位置以及对应的分数，表示从该位置开始的长度为win-size的序列被认为是异常
    运行示例：
        import numpy as np
        from HOTSAX import *
        #ECG数据，不带标签，只有一列值
        data = np.genfromtxt("ECG0606_1.csv", delimiter=',')
        
        hs=HOTSAX(2)
        discords,win_size =hs.find_discords_hotsax(data)
        print(discords,win_size)
    '''
    def hotsax(self,series, win_size=100, a_size=3,
                             paa_size=3, z_threshold=0.01):
        """HOT-SAX-driven discords discovery."""
        discords = list()

        globalRegistry = set()

        while (len(discords) < self.num_discords):

            bestDiscord =self.find_best_discord_hotsax(series, win_size, a_size,
                                                   paa_size, z_threshold,
                                                   globalRegistry)

            if -1 == bestDiscord[0]:
                break

            discords.append(bestDiscord)

            mark_start = bestDiscord[0] - win_size
            if 0 > mark_start:
                mark_start = 0

            mark_end = bestDiscord[0] + win_size
            '''if len(series) < mark_end:
                mark_end = len(series)'''

            for i in range(mark_start, mark_end):
                globalRegistry.add(i)

        return discords,win_size #返回设定异常个数的异常开始位置和窗口大小


    def find_best_discord_hotsax(self,series, win_size, a_size, paa_size,
                                 znorm_threshold, globalRegistry): # noqa: C901
        """Find the best discord with hotsax."""
        """[1.0] get the sax data first"""
        sax_none = sax_via_window(series, win_size, a_size, paa_size, "none", 0.01)

        """[2.0] build the 'magic' array"""
        magic_array = list()
        for k, v in sax_none.items():
            magic_array.append((k, len(v)))

        """[2.1] sort it desc by the key"""
        m_arr = sorted(magic_array, key=lambda tup: tup[1])

        """[3.0] define the key vars"""
        bestSoFarPosition = -1
        bestSoFarDistance = 0.

        distanceCalls = 0

        visit_array = np.zeros(len(series), dtype=np.int)

        """[4.0] and we are off iterating over the magic array entries"""
        for entry in m_arr:

            """[5.0] some moar of teh vars"""
            curr_word = entry[0]
            occurrences = sax_none[curr_word]

            """[6.0] jumping around by the same word occurrences makes it easier to
            nail down the possibly small distance value -- so we can be efficient
            and all that..."""
            for curr_pos in occurrences:

                if curr_pos in globalRegistry:
                    continue

                """[7.0] we don't want an overlapping subsequence"""
                mark_start = curr_pos - win_size
                mark_end = curr_pos + win_size
                visit_set = set(range(mark_start, mark_end))

                """[8.0] here is our subsequence in question"""
                cur_seq = znorm(series[curr_pos:(curr_pos + win_size)],
                                znorm_threshold)

                """[9.0] let's see what is NN distance"""
                nn_dist = np.inf
                do_random_search = 1

                """[10.0] ordered by occurrences search first"""
                for next_pos in occurrences:

                    """[11.0] skip bad pos"""
                    if next_pos in visit_set:
                        continue
                    else:
                        visit_set.add(next_pos)

                    """[12.0] distance we compute"""
                    dist = euclidean(cur_seq, znorm(series[next_pos:(
                                     next_pos+win_size)], znorm_threshold))
                    distanceCalls += 1

                    """[13.0] keep the books up-to-date"""
                    if dist < nn_dist:
                        nn_dist = dist
                    if dist < bestSoFarDistance:
                        do_random_search = 0
                        break

                """[13.0] if not broken above,
                we shall proceed with random search"""
                if do_random_search:
                    """[14.0] build that random visit order array"""
                    curr_idx = 0
                    for i in range(0, (len(series) - win_size)):
                        if not(i in visit_set):
                            visit_array[curr_idx] = i
                            curr_idx += 1
                    it_order = np.random.permutation(visit_array[0:curr_idx])
                    curr_idx -= 1

                    """[15.0] and go random"""
                    while curr_idx >= 0:
                        rand_pos = it_order[curr_idx]
                        curr_idx -= 1

                        dist = euclidean(cur_seq, znorm(series[rand_pos:(
                                         rand_pos + win_size)], znorm_threshold))
                        distanceCalls += 1

                        """[16.0] keep the books up-to-date again"""
                        if dist < nn_dist:
                            nn_dist = dist
                        if dist < bestSoFarDistance:
                            nn_dist = dist
                            break

                """[17.0] and BIGGER books"""
                if (nn_dist > bestSoFarDistance) and (nn_dist < np.inf):
                    bestSoFarDistance = nn_dist
                    bestSoFarPosition = curr_pos

        return (bestSoFarPosition, bestSoFarDistance)