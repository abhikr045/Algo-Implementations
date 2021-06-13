##### REFERENCE #####
# https://cp-algorithms.com/string/suffix-array.html


# All the chars in the alphabet in sorted order
# NOTE - '$' is a dummy char (which is smallest of all chars in the alphabet)
ALPHA = '$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def sortCyclicShifts(S):
    alphaID = {}    # Store index of each char in the alphabet
    for c in range(len(ALPHA)):
        alphaID[ALPHA[c]] = c

    rank2shift = [-1] * len(S)    # rank2shift[r] = i  ==>  cyclic shift 'i' is present at rank 'r' in sorted cyclic shifts (NOTE - equal cyclic shifts in sorted order can be assigned any suitable rank)
    eqCls = [-1] * len(S)            # eqCls[i] = c  ==>  equivalence class of cyclic shift 'i' = c (NOTE - cyclic shift A appearing before B in sorted order has c_A < c_B)
    cumFreq = [0] * max(len(ALPHA), len(S))        # Note that initially, there can be upto len(ALPHA) elements to calculate cumFreq across, but at last, there will be len(S) elemets to calculate the cumFreq across. So, len(cumFreq) = max(len(ALPHA), len(S))

    # Algo iterates through k = 0, 1, 2, ..., ceil(log(n)); where, n = len(S)
    # For k'th iteration, cyclic shifts are sorted according to first 2^k chars of cyclic shifts

    ##### Calculating rank2shift[] & eqCls[] for k=0 iteration #####
    # Step-1: Calculate cumFreq[] from freq of each char in alphabet
    for ch in S:
        cumFreq[alphaID[ch]] += 1
    for c in range(1, len(ALPHA)):
        cumFreq[c] += cumFreq[c-1]

    # Step-2: Calculate rank2shift[] (i.e., which cyclic shift, when in sorted order, is present at rank 'r') in O(n) time --> basically Counting Sort
    for i in range(len(S)):
        rank2shift[cumFreq[alphaID[S[i]]]-1] = i
        cumFreq[alphaID[S[i]]] -= 1

    # Step-3: Calculate eqCls[] of each char in alphabet
    eqCls[rank2shift[0]] = 0
    numCls = 1
    for r in range(1, len(S)):        # r = rank of cyclic shifts in sorted order
        if (S[rank2shift[r]] != S[rank2shift[r-1]]):
            numCls += 1
        eqCls[rank2shift[r]] = numCls - 1
    ##### Calculating rank2shift[] & eqCls[] for k=0 iteration #####

    ##### Calculating rank2shift[] & eqCls[] for k>0 iterations #####
    # A cyclic shift (of length 2^k) is divided into 2 halves (first & second) of length 2^(k-1) each
    # Each half has an eqCls value
    k = 0    # Loop invariant: k'th iteration has been completed
    while ((1<<k) < len(S)):
        # Step-0: Calculate sec_rank2shift[] from rank2shift[] of previous iteration
        sec_rank2shift = [-1] * len(S)        # sec_rank2shift[r] = i  ==>  When cyclic shifts (of length 2^k) sorted according to eqCls value of second half, cyclic shift 'i' is present at rank 'r'
        for r in range(len(S)):
            sec_rank2shift[r] = (rank2shift[r] - (1<<k)) % len(S)

        # Step-1: Calculate first_cumFreq[] from freq of each eqCls
        # Similar to Step-1 of k=0'th iteration (where "eqCls" in k>0'th iteration is equivalent to "char in alphabet" in k=0'th iteration)
        first_cumFreq = [0] * max(len(ALPHA), len(S))
        for ri in range(len(S)):
            # first_cumFreq[eqCls[sec_rank2shift[ri]]] += 1
            first_cumFreq[eqCls[ri]] += 1        # Short version of above commented line
        for cl in range(1, numCls):
            first_cumFreq[cl] += first_cumFreq[cl-1]

        # Step-2: Calculate rank2shift[] for (k+1)'th iteration from sec_rank2shift[] and first_cumFreq[]
        # Note that here, we must iterate from max. sec_rank to min. sec_rank. See examples below & check what happens if we iterate in opposite order of sec_rank -
        # Example-1:
        #    first_eqCls    =     0             1
        #                      <----->  <----------->
        #    sec_rank2shift = [3, 7, 0, 2, 6, 1, 5, 4]
        #    rank2shift     = [3, 7, 0, 2, 6, 1, 5, 4]    -->    Correct
        #    rank2shift     = [0, 7, 3, 4, 5, 1, 6, 2]    -->    WRONG
        #
        # # Example-2:
        #    first_eqCls    =     1             0
        #                      <----->  <----------->
        #    sec_rank2shift = [3, 7, 0, 2, 6, 1, 5, 4]
        #    rank2shift     = [2, 6, 1, 5, 4, 3, 7, 0]    -->    Correct
        #    rank2shift     = [4, 5, 1, 6, 2, 0, 7, 3]    -->    WRONG
        for r in range(len(S)-1, -1, -1):
            rank2shift[first_cumFreq[eqCls[sec_rank2shift[r]]]-1] = sec_rank2shift[r]
            first_cumFreq[eqCls[sec_rank2shift[r]]] -= 1

        # Step-3: Calculate new_eqCls[]
        new_eqCls = [-1] * len(S)
        new_eqCls[rank2shift[0]] = 0
        numCls = 1
        for r in range(1, len(S)):
            eqCls_cur = [eqCls[rank2shift[r]], eqCls[(rank2shift[r] + (1<<k)) % len(S)]]
            eqCls_prev = [eqCls[rank2shift[r-1]], eqCls[(rank2shift[r-1] + (1<<k)) % len(S)]]
            if (eqCls_cur != eqCls_prev):
                numCls += 1
            new_eqCls[rank2shift[r]] = numCls - 1
        eqCls = new_eqCls

        k += 1
    ##### Calculating rank2shift[] & eqCls[] for k>0 iterations #####

    return rank2shift


def suffixArray(S):
    S += '$'    # Append dummy char (which is smallest of all chars in alphabet) at the end of S
    sortedCyclicShifts = sortCyclicShifts(S)
    return sortedCyclicShifts[1:]    # Sorted cyclic shifts of S+'$' contains |S| in the beginning. Suffix Array is the sorted cyclic shifts without the 1st element |S|


    # LCPArray() returns an array lcp[] of len=len(S)-1, where      
# lcp[i] = Longest Common Prefix between adjacent suffixes (in sorted order) 'i' and 'i+1'
def LCPArray(S, sfxArr):
    sfx2rank = [-1] * len(S)    # sfx2rank[i] = r  ==>  in sorted order, the suffix 'i' is present at rank 'r'
    for r in range(len(S)):
        sfx2rank[sfxArr[r]] = r     # Note: sfxArr[] is equivalent to rank2sfx[]

    lcp = [-1] * (len(S)-1)
    prevLcp = 0
    for i in range(len(S)):
        if (sfx2rank[i] == len(S)-1):
            prevLcp = 0
            continue

        j = sfxArr[sfx2rank[i]+1]
        while (i+prevLcp < len(S)) and (j+prevLcp < len(S)) and (S[i+prevLcp] == S[j+prevLcp]):
            prevLcp += 1

        lcp[sfx2rank[i]] = prevLcp
        if (prevLcp > 0):
            prevLcp -= 1

    return lcp


def calc_suffixArr_LCPArr(S):
    sfxArr = suffixArray(S)
    lcpArr = LCPArray(S, sfxArr)
    return sfxArr, lcpArr


if __name__ == '__main__':
    S = input()
    sfxArr, lcpArr = calc_suffixArr_LCPArr(S)

    print('Suffixes in sorted order & LCP (Longest Common Prefix) between current and next suffix in sorted order -')
    print('Suffix Array  ---  Suffix  ---  LCP')
    for rank in range(len(sfxArr)):
        if (rank == len(lcpArr)):
            print('%d  ---  %s' % (sfxArr[rank], S[sfxArr[rank]:]))
        else:
            print('%d  ---  %s  ---  %d' % (sfxArr[rank], S[sfxArr[rank]:], lcpArr[rank]))
