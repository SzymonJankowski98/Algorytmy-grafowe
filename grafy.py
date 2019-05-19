import random
import copy
import time
import sys
sys.setrecursionlimit(10000000)

def generate(n):
    tab = []
    for i in range(n):
        tab.append([])
        for j in range(int(n)):
            tab[i].append(0)
    x = 0
    while x < n * (n - 1) / 4:
        a = random.randint(0, n-2)
        b = random.randint(a+1, n-1)
        while tab[a][b] == 1:
            a = random.randint(0, n-2)
            b = random.randint(a+1, n-1)
        tab[a][b] = 1
        x += 1
    return tab

consistentTab = []
def isConsistent(tab):
    for i in range(len(tab)):
        for j in range(i+1,len(tab)):
            tab[j][i]=tab[i][j]
    isConsistentRec(tab)
    if not list(set(list(range(len(tab)))) - set(consistentTab)):
        return True
    else:
        return False

def isConsistentRec(tab,i=0):
    consistentTab.append(i)
    for j in range(len(tab[i])):
        if tab[i][j] == 1 and j not in consistentTab:
            isConsistentRec(tab,j)
    return

def consequent_list(tab):
    c_list = []
    for i in range(len(tab)):
        c_list.append([])
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[i][j] == 1:
                c_list[i].append(j)
    return c_list

def incident_matrix(tab):
    x = 0
    for i in tab:
        x += i.count(1)
    i_matrix=[]
    for i in range(x):
        i_matrix += [[]]
        for j in range(len(tab)):
            i_matrix[i].append(0)
    counter=0
    for i in range(len(tab)):
        for j in  range(len(tab)):
            if tab[i][j] == 1:
                i_matrix[counter][i] = -1
                i_matrix[counter][j] = 1
                counter+=1
    return i_matrix

def edge_table(tab):
    e_tab = []
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if tab[i][j] == 1:
                e_tab.append([i,j])
    return e_tab

def generator(n):
    tab = generate(n)
    consistentTab = []
    while not isConsistent(copy.deepcopy(tab)):
        tab = generate(n)
    return tab, consequent_list(tab), edge_table(tab)


class AdjacencyMatrix:
    def __init__(self,tab):
        self.tab = tab
        self.dfsResult = []
        self.rvResult = []

    def findNext(self,i,j):
        for k in range(j,len(self.tab)):
            if self.tab[i][k] == 1 and k not in self.dfsResult:
                return True, k
        return False, j

    def dfs(self):
        y = list(set(list(range(len(self.tab))))-set(self.dfsResult))
        while y:
            self.dfs_path(y[0],0)
            y = list(set(list(range(len(self.tab)))) - set(self.dfsResult))

    def dfs_path(self,i=0,j=0):
        x = True
        while x:
            x, j = self.findNext(i, j)
            if x and j not in self.dfsResult:
                self.dfs_path(j, 0)
        self.dfsResult = [i] + self.dfsResult

    def findAll(self, i):
        tab = []
        for k in range(0,len(self.tab)):
            if self.tab[i][k] == 1:
                tab.append(k)
        return tab

    def remove_vertex(self):
        temp = []
        for i in range(len(self.tab)):
            temp.append(0)
            for j in range(len(self.tab)):
                if self.tab[j][i] == 1:
                    temp[i] += 1
        y = list(set(list(range(len(self.tab)))) - set(self.rvResult))
        while y:
            for i in range(len(temp)):
                if temp[i] == 0:
                    self.rvResult.append(i)
                    temp[i] -= 1
                    for j in self.findAll(i):
                        temp[j] -= 1
                    y = list(set(list(range(len(self.tab)))) - set(self.rvResult))
                    break


class ConsequentList:
    def __init__(self,tab):
        self.tab = tab
        self.dfsResult = []
        self.rvResult = []

    def dfs(self):
        y = list(set(list(range(len(self.tab)))) - set(self.dfsResult))
        while y:
            self.dfs_path(y[0])
            y = list(set(list(range(len(self.tab)))) - set(self.dfsResult))

    def dfs_path(self, i=0):
        for k in self.tab[i]:
            if k not in self.dfsResult:
                self.dfs_path(k)
        self.dfsResult = [i] + self.dfsResult

    def remove_vertex(self):
        temp = []
        for i in range(len(self.tab)):
            temp.append(0)
        for j in range(len(self.tab)):
            for k in self.tab[j]:
                temp[k] += 1
        y = list(set(list(range(len(self.tab)))) - set(self.rvResult))
        while y:
            for i in range(len(temp)):
                if temp[i] == 0:
                    self.rvResult.append(i)
                    temp[i] -= 1
                    for j in self.tab[i]:
                        temp[j] -= 1
                    y = list(set(list(range(len(self.tab)))) - set(self.rvResult))
                    break


class IncidentMatrix:
    def __init__(self, tab):
        self.tab = tab
        self.dfsResult = []
        self.dfsResultTemp = []
        self.rvResult = []

    def findNext(self, i, j):
        for k in range(j, len(self.tab)):
            if self.tab[k][i] == -1:
                for l in range(0, len(self.tab[0])):
                    if self.tab[k][l] == 1 and l not in self.dfsResult and l not in self.dfsResultTemp:
                        return True, l
        return False, j

    def dfs(self):
        y = list(set(list(range(len(self.tab[0])))) - set(self.dfsResult))
        while y:
            self.dfs_path(y[0], 0)
            self.dfsResult = self.dfsResultTemp + self.dfsResult
            self.dfsResultTemp = []
            y = list(set(list(range(len(self.tab[0])))) - set(self.dfsResult))

    def dfs_path(self, i=0, j=0):
        x = True
        while x:
            x, j = self.findNext(i, j)
            if x and j not in self.dfsResult and j not in self.dfsResultTemp:
                self.dfs_path(j, 0)
        self.dfsResultTemp = [i] + self.dfsResultTemp

    def findAll(self, i):
        tab = []
        for k in range(0, len(self.tab)):
            if self.tab[k][i] == -1:
                for l in range(0, len(self.tab[0])):
                    if self.tab[k][l] == 1:
                        tab.append(l)
        return tab

    def remove_vertex(self):
        temp = []
        for i in range(len(self.tab[0])):
            temp.append(0)
        for i in range(len(self.tab)):
            for j in range(len(self.tab[0])):
                if self.tab[i][j] == 1:
                    temp[j] += 1
        y = list(set(list(range(len(self.tab[0])))) - set(self.rvResult))
        while y:
            for i in range(len(temp)):
                if temp[i] == 0:
                    self.rvResult.append(i)
                    temp[i] -= 1
                    for j in self.findAll(i):
                        temp[j] -= 1
                    y = list(set(list(range(len(self.tab[0])))) - set(self.rvResult))
                    break


class EdgeTable:
    def __init__(self,tab):
        self.tab = tab
        self.dfsResult = []
        self.rvResult = []

    def findNext(self,i,j):
        for k in range(j,len(self.tab)):
            if self.tab[k][0] == i and self.tab[k][1] not in self.dfsResult:
                return True, k
        return False, j

    def dfs(self):
        h=0
        for i in range(len(self.tab)):
           if max(self.tab[i][0],self.tab[i][1]) > h:
               h = max(self.tab[i][0],self.tab[i][1])
        y = list(set(list(range(h+1)))-set(self.dfsResult))
        while y:
            self.dfs_path(y[0],0)
            y = list(set(list(range(h+1))) - set(self.dfsResult))

    def dfs_path(self,i=0,j=0):
        x = True
        while x:
            x, j = self.findNext(i, j)
            if x and self.tab[j][1] not in self.dfsResult and self.tab[j][1]:
                self.dfs_path(self.tab[j][1], 0)
        self.dfsResult = [i] + self.dfsResult

    def findAll(self, i):
        tab = []
        for k in range(0,len(self.tab)):
            if self.tab[k][0] == i:
                tab.append(self.tab[k][1])
        return tab

    def remove_vertex(self):
        h = 0
        for i in range(len(self.tab)):
            if max(self.tab[i][0], self.tab[i][1]) > h:
                h = max(self.tab[i][0], self.tab[i][1])
        temp = []
        for i in range(h+1):
            temp.append(0)
            for j in range(len(self.tab)):
                if self.tab[j][1] == i:
                    temp[i] += 1
        y = list(set(list(range(h + 1))) - set(self.rvResult))
        while y:
            for i in range(len(temp)):
                if temp[i] == 0:
                    self.rvResult.append(i)
                    temp[i] -= 1
                    for j in self.findAll(i):
                        temp[j] -= 1
                    y = list(set(list(range(h + 1))) - set(self.rvResult))
                    break

n=500
w = [[],[],[],[],[],[]]
for i in range(n,n*11,n):
    x, y, z = generator(i)
    t1=time.time()
    a=AdjacencyMatrix(x)
    a.dfs()
    w[0].append(time.time()-t1)
    t2 = time.time()
    b = AdjacencyMatrix(x)
    b.remove_vertex()
    w[1].append(time.time() - t2)

    t3 = time.time()
    c = ConsequentList(y)
    c.dfs()
    w[2].append(time.time() - t3)
    t4 = time.time()
    d = ConsequentList(y)
    d.remove_vertex()
    w[3].append(time.time() - t4)

    t5 = time.time()
    e = EdgeTable(z)
    e.dfs()
    w[4].append(time.time() - t5)
    t6 = time.time()
    f = EdgeTable(z)
    f.remove_vertex()
    w[5].append(time.time() - t6)
f = open("wynik2.txt", "w")
l = ["AdjacencyMatrix - dfs:","AdjacencyMatrix - remove vertex:","ConsequentList - dfs:","ConsequentList - remove vertex:","EdgeTable - dfs:","EdgeTable - remove vertex:"]
for j, c in enumerate(w,0):
    f.write(l[j]+"\n")
    for k in range(len(c)):
        f.write(str(n*(k+1))+": "+str(w[j][k])+"\n")
    f.write("\n")