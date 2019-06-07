import multiprocessing as mp
import time
import random
import collections
import sys
from itertools import permutations

class ComputePath:
    def __init__(self, distance, ID2Index):
        self.distance = distance
        self.ID2Index = ID2Index
        self.crossRate = 0.7  # cross rate
        self.mutationRate = 0.02  # mutation rate
        self.num_of_life = 0 # population number, number of series
        self.geneLength = 0  # number of items
        self.lives = []  # population
        self.best = []  # optimal individuals
        self.generation = 1
        self.crossCount = 0  # cross time
        self.mutationCount = 0  # mutation time
        self.order=[]


    def run(self, orderList, algo):
        #print(orderList)
        if algo == 'BR':
            return self.bruteForce(orderList)
        if algo == 'GA':
            return self.parallel(orderList)
        elif algo == 'GREEDY':
            return self.greedy(orderList)
        else:
            raise ValueError('The method computePath.run(algo) must have ' +
                             'parameter \'BRUTEFORCE\', \'DP\' or \'GREEDY\'')

    def evaluation(self):
        best_score=self.Fitness(self.best)
        for life in self.lives:
            score = self.Fitness(life)
            if score > best_score:
                self.best = life
                best_score = score

    def crossover(self, parent1, parent2):
        left = random.randint(1, len(parent1) - 2)
        right = random.randint(left, len(parent1) - 2)
        newgene = collections.deque()
        newgene.extend(parent1[left:right])
        point = 0
        for g in parent2[1:-1]:
            if g not in parent1[left:right]:
                if point<left:
                    newgene.appendleft(g)
                    point += 1
                else:
                    newgene.append(g)
        newgene.appendleft(0)
        newgene.append(len(parent1)-1)
        self.crossCount += 1
        return list(newgene)

    def Mutation(self, gene):
        newg = gene
        left = random.randint(1, len(gene) - 2)
        right = random.randint(1, len(gene) - 2)
        newg[left], newg[right] = newg[right], newg[left]
        self.mutationCount += 1
        #print(gene)
        return list(newg)

    def select(self):
        index = random.randint(0, len(self.lives)-1)
        life = self.lives[index]
        return life

    def Child(self):
        parent1 = self.select()
        rate = random.random()
        if rate < self.crossRate:
            parent2 = self.select()
            gene = self.crossover(parent1, parent2)
        else:
            gene = parent1
        # ra = random.random()
        # if ra < self.mutationRate:
        #     gene = self.Mutation(gene)
        return gene

    def next_generation(self):
        self.evaluation()
        newLives = []
        newLives.append(self.best)
        while len(newLives) < self.num_of_life:
            newLives.append(self.Child())
        self.lives[:] = newLives
        self.generation += 1

    def New_distance(self,lifes):
        new_distance = 0.0
        for i in range(0, self.geneLength - 1):
            index1, index2 = self.ID2Index[self.order[lifes[i]]], self.ID2Index[self.order[lifes[i + 1]]]
            new_distance+=self.distance[index1][index2]
        return new_distance

    def Fitness(self, life):
        return 1.0/self.New_distance(life)

    def GA(self,order_list,q):
        dis=0
        n=1500
        self.order = ['000'] + order_list + ['-1']
        self.geneLength=len(self.order)
        while n > 0:
            self.next_generation()
            dis = self.New_distance(self.best)
            n -= 1
        res=[]
        for i in self.best:
            res.append(self.order[i])
        q.put(res[1:-1])
        q.put(dis)

    def RGA(self,oder_list,L,NUM,q):
        self.lives=L
        self.num_of_life=NUM
        self.best=L[-1]
        self.GA(oder_list,q)

    def initialpopulation(self,num, geneLength, q):
        lives = []
        while len(lives) < num:
            temp = [x for x in range(1, geneLength + 1)]
            random.shuffle(temp)
            gene = [0] + temp + [geneLength + 1]
            if gene not in lives:
                lives.append(gene)
        q.put(lives)

    def gre(self, orderlist, q):
        new_dis = self.convert(orderlist)
        N = len(new_dis)
        path_distance = 0  # least distance of current path
        s = []  # items has been picked up
        s.append(0)  # 0 is the starting location
        i, j = 1, 0
        for i in range(1, N - 1):  # N-1 because we don't care about end point
            k = 1
            shortest = sys.maxsize  # shortest distance of current point
            for k in range(1, N - 1):  # Greedy algo doesnt care about end
                picked = 0  # whether the item is picked or not
                if k in s:
                    picked = 1
                if (picked == 0) and (new_dis[k][s[i - 1]] < shortest):
                    j = k
                    shortest = new_dis[k][s[i - 1]]
            s.append(j)
            path_distance += shortest
        path_distance += new_dis[-1][j]  # Distance to the end point
        res = []
        for item in s[1:]:
            res.append(orderlist[item - 1])
        # print(path_distance)
        # print res
        q.put(s + [len(orderlist) + 1])


    def bruteForce(self, orderlist):
        '''
            Gets the order list and returns the shortest path
            Input: list with product IDs of the orders
            Output: The shortest sequence of pick ups
        '''
        result = []
        possible_sequences = self.getCombinations(orderlist)
        min_distance = -1
        for sequence in possible_sequences:
            prev_id = '000'  # Start point
            end_id = '-1'  # Force to end in the end point
            seq_inc_end = list(sequence) + [end_id]
            accu = 0
            for ID in seq_inc_end:
                str_ind = self.ID2Index[prev_id]
                end_ind = self.ID2Index[ID]
                dist = self.distance[str_ind][end_ind]
                accu += dist
                prev_id = ID
            if min_distance == -1:
                min_distance = accu
                result = sequence
            else:
                if accu < min_distance:
                    min_distance = accu
                    result = sequence[:]
        print(min_distance)
        return result

    def getCombinations(self, any_list):
        '''Gives all possible combinations of the list'''
        perm = permutations(any_list)
        return list(perm)

    def greedy(self, orderlist):
        new_dis = self.convert(orderlist)
        N = len(new_dis)
        path_distance = 0  # least distance of current path
        s = []  # items has been picked up
        s.append(0)  # 0 is the starting location
        i, j = 1, 0
        for i in range(1, N - 1):  # N-1 because we don't care about end point
            k = 1
            shortest = sys.maxsize  # shortest distance of current point
            for k in range(1, N - 1):  # Greedy algo doesnt care about end
                picked = 0  # whether the item is picked or not
                if k in s:
                    picked = 1
                if (picked == 0) and (new_dis[k][s[i - 1]] < shortest):
                    j = k
                    shortest = new_dis[k][s[i - 1]]
            s.append(j)
            path_distance += shortest
        path_distance += new_dis[-1][j]  # Distance to the end point
        res = []
        for item in s[1:]:
            res.append(orderlist[item - 1])
        print(path_distance)
        return res
        # print res

    def convert(self, orderlist):
        length = len(orderlist) + 2
        start_pt = '000'  # By convention start_pt id is '000'
        end_pt = '-1'  # Similarly end_pt id is '-1'
        new_list = [start_pt] + orderlist + [end_pt]
        fidistance = []
        for i in range(length):
            temp = [0] * length
            for j in range(length):
                sta = self.ID2Index[new_list[i]]
                end = self.ID2Index[new_list[j]]
                temp[j] = self.distance[sta][end]
            fidistance.append(temp)
        return fidistance

    def parallel(self, order_list):
        length = len(order_list)
        num = 1
        if len(order_list) <= 5:
            for i in range(1, len(order_list) + 1):
                num = num * i
        else:
            num = 500
        s1 = mp.Queue()
        s2 = mp.Queue()
        st1 = mp.Process(target=self.initialpopulation, args=(num, length, s1,))
        st2 = mp.Process(target=self.gre, args=(order_list, s2,))
        st1.start()
        st2.start()
        st1.join()
        st2.join()
        st1.terminate()
        st2.terminate()
        lives = list(s1.get())
        best_gre = list(s2.get())
        a = int(len(lives) / 2)
        l1 = lives[:a] + [best_gre]
        l2 = lives[a:] + [best_gre]
        q1 = mp.Queue()
        q2 = mp.Queue()
        p1 = mp.Process(target=self.RGA, args=(order_list, l1, num/2, q1,))
        p2 = mp.Process(target=self.RGA, args=(order_list, l2, num/2, q2,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        res1 = q1.get()
        dis_1 = q1.get()
        res2 = q2.get()
        dis_2 = q2.get()
        if dis_1 < dis_2:
            print(res1, dis_1)
            return res1
        else:
            print(res2, dis_2)
            return res2





# def main():
#     order_list = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
#     ID2Index = {}
#     ID2Index['000'] = 0
#     ID2Index['-1'] = 31
#     ID2Index['1'] = 1
#     ID2Index['2'] = 2
#     ID2Index['3'] = 3
#     ID2Index['4'] = 4
#     ID2Index['5'] = 5
#     ID2Index['6'] = 6
#     ID2Index['7'] = 7
#     ID2Index['8'] = 8
#     ID2Index['9'] = 9
#     ID2Index['10'] = 10
#     ID2Index['11'] = 11
#     ID2Index['12'] = 12
#     ID2Index['13'] = 13
#     ID2Index['14'] = 14
#     ID2Index['15'] = 15
#     ID2Index['16'] = 16
#     ID2Index['17'] = 17
#     ID2Index['18'] = 18
#     ID2Index['19'] = 19
#     ID2Index['20'] = 20
#     ID2Index['21'] = 21
#     ID2Index['22'] = 22
#     ID2Index['23'] = 23
#     ID2Index['24'] = 24
#     ID2Index['25'] = 25
#     ID2Index['26'] = 26
#     ID2Index['27'] = 27
#     ID2Index['28'] = 28
#     ID2Index['29'] = 29
#     ID2Index['30'] = 30
#
#     distance = [[11, 17, 5, 25, 13, 13, 13, 27, 9, 23, 4, 4, 16, 23, 17, 13, 18, 14, 4, 37, 37, 23, 19, 5, 12, 17, 17, 11, 12, 5, 37, 11],
#                        [17, 0, 9, 28, 16, 7, 21, 24, 16, 30, 8, 8, 13, 11, 12, 16, 26, 24, 8, 16, 16, 11, 14, 9, 13, 0, 0, 11, 16, 14, 16, 17],
#                        [5, 9, 0, 8, 6, 19, 13, 10, 6, 20, 8, 8, 12, 2, 13, 6, 10, 10, 8, 7, 7, 2, 13, 0, 8, 9, 9, 12, 7, 8, 7, 5],
#                        [25, 28, 8, 0, 10, 23, 18, 10, 6, 12, 16, 16, 20, 10, 19, 10, 18, 10, 16, 12, 12, 10, 18, 8, 16, 28, 28, 26, 15, 16, 12, 25],
#                        [13, 16, 6, 10, 0, 5, 14, 4, 6, 18, 12, 12, 12, 4, 9, 0, 18, 10, 12, 16, 16, 4, 8, 6, 16, 16, 16, 2, 7, 12, 16, 13],
#                        [13, 7, 19, 23, 5, 0, 12, 7, 6, 17, 17, 17, 15, 6, 8, 5, 12, 13, 17, 13, 13, 6, 7, 19, 11, 7, 7, 9, 11, 9, 13, 13],
#                        [13, 21, 13, 18, 14, 12, 0, 14, 26, 6, 22, 22, 10, 21, 13, 14, 1, 10, 22, 16, 16, 21, 10, 13, 6, 21, 21, 22, 26, 12, 16, 13],
#                        [27, 24, 10, 10, 4, 7, 14, 0, 4, 8, 16, 16, 14, 8, 7, 4, 16, 10, 16, 6, 6, 8, 4, 10, 12, 24, 24, 10, 9, 12, 6, 27],
#                        [9, 16, 6, 6, 6, 6, 26, 4, 0, 12, 12, 12, 6, 6, 11, 6, 14, 6, 12, 26, 26, 6, 24, 6, 4, 16, 16, 18, 11, 12, 26, 9],
#                        [23, 30, 20, 12, 18, 17, 6, 8, 12, 0, 13, 13, 24, 15, 17, 18, 6, 8, 13, 15, 15, 15, 20, 20, 20, 30, 30, 12, 20, 6, 15, 23],
#                        [4, 8, 8, 16, 12, 17, 22, 16, 12, 13, 0, 0, 20, 8, 1, 12, 10, 16, 0, 10, 10, 8, 13, 8, 16, 8, 8, 6, 11, 4, 10, 4],
#                        [4, 8, 8, 16, 12, 17, 22, 16, 12, 13, 0, 0, 20, 8, 1, 12, 10, 16, 0, 10, 10, 8, 13, 8, 16, 8, 8, 6, 11, 4, 10, 4],
#                        [16, 13, 12, 20, 12, 15, 10, 14, 6, 24, 20, 20, 0, 23, 3, 12, 8, 21, 20, 16, 16, 23, 22, 12, 4, 13, 13, 30, 28, 14, 16, 16],
#                        [23, 11, 2, 10, 4, 6, 21, 8, 6, 15, 8, 8, 23, 0, 2, 4, 9, 10, 8, 11, 11, 0, 14, 2, 19, 11, 11, 9, 5, 8, 11, 23],
#                        [17, 12, 13, 19, 9, 8, 13, 7, 11, 17, 1, 1, 3, 2, 0, 9, 18, 16, 1, 9, 9, 2, 18, 13, 7, 12, 12, 16, 11, 9, 9, 17],
#                        [13, 16, 6, 10, 0, 5, 14, 4, 6, 18, 12, 12, 12, 4, 9, 0, 18, 10, 12, 16, 16, 4, 8, 6, 16, 16, 16, 2, 7, 12, 16, 13],
#                        [18, 26, 10, 18, 18, 12, 1, 16, 14, 6, 10, 10, 8, 9, 18, 18, 0, 17, 10, 8, 8, 9, 8, 10, 6, 26, 26, 11, 12, 10, 8, 18],
#                        [14, 24, 10, 10, 10, 13, 10, 10, 6, 8, 16, 16, 21, 10, 16, 10, 17, 0, 16, 12, 12, 10, 9, 10, 25, 24, 24, 11, 13, 16, 12, 14],
#                        [4, 8, 8, 16, 12, 17, 22, 16, 12, 13, 0, 0, 20, 8, 1, 12, 10, 16, 0, 10, 10, 8, 13, 8, 16, 8, 8, 6, 11, 4, 10, 4],
#                        [37, 16, 7, 12, 16, 13, 16, 6, 26, 15, 10, 10, 16, 11, 9, 16, 8, 12, 10, 0, 0, 11, 10, 7, 12, 16, 16, 14, 18, 4, 0, 37],
#                        [37, 16, 7, 12, 16, 13, 16, 6, 26, 15, 10, 10, 16, 11, 9, 16, 8, 12, 10, 0, 0, 11, 10, 7, 12, 16, 16, 14, 18, 4, 0, 37],
#                        [23, 11, 2, 10, 4, 6, 21, 8, 6, 15, 8, 8, 23, 0, 2, 4, 9, 10, 8, 11, 11, 0, 14, 2, 19, 11, 11, 9, 5, 8, 11, 23],
#                        [19, 14, 13, 18, 8, 7, 10, 4, 24, 20, 13, 13, 22, 14, 18, 8, 8, 9, 13, 10, 10, 14, 0, 13, 26, 14, 14, 12, 2, 10, 10, 19],
#                        [5, 9, 0, 8, 6, 19, 13, 10, 6, 20, 8, 8, 12, 2, 13, 6, 10, 10, 8, 7, 7, 2, 13, 0, 8, 9, 9, 12, 7, 8, 7, 5],
#                        [12, 13, 8, 16, 16, 11, 6, 12, 4, 20, 16, 16, 4, 19, 7, 16, 6, 25, 16, 12, 12, 19, 26, 8, 0, 13, 13, 26, 24, 10, 12, 12],
#                        [17, 0, 9, 28, 16, 7, 21, 24, 16, 30, 8, 8, 13, 11, 12, 16, 26, 24, 8, 16, 16, 11, 14, 9, 13, 0, 0, 11, 16, 14, 16, 17],
#                        [17, 0, 9, 28, 16, 7, 21, 24, 16, 30, 8, 8, 13, 11, 12, 16, 26, 24, 8, 16, 16, 11, 14, 9, 13, 0, 0, 11, 16, 14, 16, 17],
#                        [11, 11, 12, 26, 2, 9, 22, 10, 18, 12, 6, 6, 30, 9, 16, 2, 11, 11, 6, 14, 14, 9, 12, 12, 26, 11, 11, 0, 14, 12, 14, 11],
#                        [12, 16, 7, 15, 7, 11, 26, 9, 11, 20, 11, 11, 28, 5, 11, 7, 12, 13, 11, 18, 18, 5, 2, 7, 24, 16, 16, 14, 0, 7, 18, 12],
#                        [5, 14, 8, 16, 12, 9, 12, 12, 12, 6, 4, 4, 14, 8, 9, 12, 10, 16, 4, 4, 4, 8, 10, 8, 10, 14, 14, 12, 7, 0, 4, 5],
#                        [37, 16, 7, 12, 16, 13, 16, 6, 26, 15, 10, 10, 16, 11, 9, 16, 8, 12, 10, 0, 0, 11, 10, 7, 12, 16, 16, 14, 18, 4, 0, 37],
#                        [11, 17, 5, 25, 13, 13, 13, 27, 9, 23, 4, 4, 16, 23, 17, 13, 18, 14, 4, 37, 37, 23, 19, 5, 12, 17, 17, 11, 12, 5, 37, 11]]
#     start = time.time()
#     com=ComputePath(distance,ID2Index)
#     com.run(order_list,'GA')
#     end = time.time()
#     print(end - start)
#
#
# if __name__ == '__main__':
#     main()
