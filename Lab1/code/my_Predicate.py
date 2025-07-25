import re
from copy import deepcopy
from queue import Queue

class Sentences:
    def __init__(self, filename: str) -> None:
        # Initialize basic sections
        self.n = 0
        self.sel = list()
        
        # Read the file
        with open(filename, 'r') as file:
            content = file.read()
        
        # Split the content into two parts
        parts = content.split('QUERY:', 1)
        self.kb_part = parts[0].replace("KB:", "").strip()
        self.query_part = parts[1].strip()

        # Get and Store the information
        self.op(self.kb_part)
        self.op(self.query_part)

        # Initialize assignment and parent section
        self.asg = []
        self.prt = []
        for i in range(self.n):
            self.prt.append([])

        # Record all kinds of variables
        self.variable = ('u', 'v', 'w', 'x', 'y', 'z')
    
    # Get clauses and store in same type
    def op(self, part: str):
        for line in part.splitlines():
            line = line.strip()
            self.sel.append(re.findall(r'~?\w+\(\w+(?:,\s*\w+)*\)', line))
            for i in range(len(self.sel[self.n])):
                self.sel[self.n][i] = self.sel[self.n][i].replace('(', ',')
                self.sel[self.n][i] = self.sel[self.n][i].replace(')', '')
                self.sel[self.n][i] = self.sel[self.n][i].split(',')
            self.n = self.n + 1 
    
    # Make opposite
    def opposite(self, str):
        if str[0] == '~':
            return str[1:]
        else:
            return '~' + str
        
    # Reduce duplicate
    def unique(self, list_pre):
        list_new = set(map(tuple, list_pre))
        list_new = list(map(list, list_new))
        return list_new
    
    # Check if the predicate can be unified and return the assignment
    def judge(self, list1:list, list2:list):
        sub = []
        for i in range(1, len(list1)):
            if list1[i] not in self.variable and list2[i] not in self.variable and list1[i] == list2[i]:
                continue
            elif list1[i] not in self.variable and list2[i] in self.variable:
                sub.append((list1[i], list2[i]))
            else:
                return False
        return sub

    # The main function - resolution
    def resolution(self):
        for i, si in enumerate(self.sel):
            for j, sj in enumerate(self.sel):
                if i == j:
                    continue
                for ki, kii in enumerate(self.sel[i]):
                    for kj, kjj in enumerate(self.sel[j]):
                        if self.sel[i][ki][0] == self.opposite(self.sel[j][kj][0]) and len(self.sel[i][ki]) == len(self.sel[j][kj]):
                            # For the opposite predicate, delete them if their arguments are the same
                            if self.sel[i][ki][1:] == self.sel[j][kj][1:]:
                                tp1 = deepcopy(self.sel[i])
                                tp2 = deepcopy(self.sel[j])
                                del tp1[ki]
                                del tp2[kj]

                                # Record all the New clauses
                                sel_new = self.unique(tp1 + tp2)
                                self.prt.append([i, ki, j, kj])
                                self.asg.append([])
                                self.sel.append(sel_new)

                                # End resolution if empty clause is found
                                if sel_new == []:
                                    return
                                
                            # For the rest, try to make substitution and unify them
                            else:
                                sub = self.judge(self.sel[i][ki], self.sel[j][kj])
                                if sub == False:
                                    continue
                                else:
                                    # Copy and delete the complementary pair
                                    tp1 = deepcopy(self.sel[i])
                                    tp2 = deepcopy(self.sel[j])
                                    del tp1[ki]
                                    del tp2[kj]

                                    # Substitute variable in tp1 with constant
                                    for p in range(len(sub)):
                                        for q in range(len(tp2)):
                                            while sub[p][1] in tp2[q]:
                                                index = tp2[q].index(sub[p][1])
                                                tp2[q][index] = sub[p][0]
                                    
                                    # Record all the new clauses
                                    sel_new = self.unique(tp1 + tp2)
                                    self.prt.append([i, ki, j, kj])
                                    self.asg.append(sub)
                                    self.sel.append(sel_new)

                                    # Empty clause, end resolution
                                    if sel_new == []:
                                        return
    
    # Track the index of arguments
    def is_mul(self, pr:list, id:int):
        if len(pr) == 1:
            return ''
        else:
            return chr(id + 97)
    
    # Track the substituion of variables
    def is_var(self, lst:list):
        if lst == []:
            return ''
        elif(len(lst) == 1):
            return f"({lst[0][1]}={lst[0][0]})"
        else:
            s = list()
            for i, li in enumerate(lst):
                s.append(f"{li[1]}={li[0]}")
            s='(' + ','.join(s) + ')'
            return s
    
    # Output in standard
    def out_std(self, lst:list):
        return lst[0] + '(' + ','.join(lst[1:]) + ')'

    # The main function - reindex
    def reindex(self):
        # Recall start
        list_used = list()
        q = Queue()
        q.put(self.prt[-1])
        list_used.append([self.sel[-1], self.prt[-1], self.asg[-1]])

        # Level order for necessary steps
        while not q.empty():
            pre = q.get()
            if pre[0] >= self.n:
                list_used.append([self.sel[pre[0]], self.prt[pre[0]], self.asg[pre[0] - self.n]])
                q.put(self.prt[pre[0]])
            if pre[2] >= self.n:
                list_used.append([self.sel[pre[2]], self.prt[pre[2]], self.asg[pre[2] - self.n]])
                q.put(self.prt[pre[2]])
        list_used.reverse()

        # Reindex the clauses
        idx_r = dict()

        # Record the clauses
        for i in range(self.n):
            idx_r[i] = None
        for i, ui in enumerate(list_used):
            if ui[1][0] not in idx_r:
                idx_r[ui[1][0]] = None
            if ui[1][2] not in idx_r:
                idx_r[ui[1][2]] = None

        # Reorder and make new index
        idx_r = list(idx_r.keys())
        idx_r = {x:idx_r.index(x) + 1 for x in idx_r}

        # Print the existing clauses
        print(self.kb_part)
        print(self.query_part)
        
        # Print the operation steps
        for i, ui in enumerate(list_used):
            if i == len(list_used) - 1:
                print(f"R[{idx_r[ui[1][0]]},{idx_r[ui[1][2]]}] = []")
                break 
            else:
                print(f"R[{idx_r[ui[1][0]]}{self.is_mul(self.sel[ui[1][0]],ui[1][1])},{idx_r[ui[1][2]]}{self.is_mul(self.sel[ui[1][2]],ui[1][3])}]{self.is_var(ui[2])} = ", end = '')
            for j in range(len(ui[0])):
                if j is not len(ui[0]) - 1:
                    print(self.out_std(ui[0][j]), end = ',')
                else:
                    print(self.out_std(ui[0][j]))
    