import numpy as np

def editDistance(w1, w2, showAlignment=False):
        w1list = list(w1.lower())
        w2list = list(w2.lower())
        w1list.insert(0,'')
        w2list.insert(0,'')
        memo = np.zeros((len(w2list), len(w1list)))
        for i in range(memo.shape[1]):
            memo[0][i] = i
        for j in range(memo.shape[0]):
            memo[j][0] = j
        return editDistanceDP(w1, w2, memo, showAlignment)

def editDistanceDP(w1, w2, memo, showAlignment):
    w1list = list(w1.lower())
    w2list = list(w2.lower())
    w1list.insert(0,'')
    w2list.insert(0,'')
    backtrace = np.zeros(memo.shape, dtype=(int, 2))

    for i in range(1, memo.shape[1]):
        for j in range(1, memo.shape[0]):
            next = min(
                (memo[j][i-1] + getCost(w1list[i],''), (j,i-1)),
                (memo[j-1][i] + getCost('', w2list[j]), (j-1,i)),
                (memo[j-1][i-1] + getCost(w1list[i], w2list[j]), (j-1,i-1))
            )
            memo[j][i] = next[0]
            backtrace[j][i] = next[1]
    if (showAlignment):
        showAlignmentBacktrace(w1, w2, backtrace)
    return memo[memo.shape[0]-1][memo.shape[1]-1]

def showAlignmentBacktrace(w1, w2, backtrace):
    w1list = list(w1)
    w2list = list(w2)
    w1list.insert(0,'')
    w2list.insert(0,'')
    w1AlignString = []
    w2AlignString = []
    j, i = (backtrace.shape[0]-1, backtrace.shape[1]-1)
    j_, i_ = (0,0)
    while (i > 0 or j > 0):
        #find next cell
        j_, i_ = backtrace[j][i]
        #compare cells to determine insert, delete, or sub
        if (i == i_):
            #insert
            w1AlignString.insert(0,'-')
            w2AlignString.insert(0,w2list[j])
        elif (j == j_):
            #delete
            w1AlignString.insert(0,w1list[i])
            w2AlignString.insert(0,'-')
        else:
            #substitution
            w1AlignString.insert(0,w1list[i])
            w2AlignString.insert(0,w2list[j])

        i = i_
        j = j_

    print(w1AlignString)
    print(w2AlignString)
    return

def getCost(c1,c2):
    SUBSTITUTION = 1
    INSERTION = 2
    DELETION = 1
    if (c1 == ''):
        return INSERTION
    elif (c2 == ''):
        return DELETION
    elif (c1 != c2):
        return SUBSTITUTION
    return 0
