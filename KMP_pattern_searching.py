# Returns lps[] array, where,
# lps[i] = Longest Prefix which is a proper Suffix of pat[0 to i]
def calcLPS(pat):
    n = len(pat)
    lps = [0] * n

    # Note - lps[0] = 0, since LPS of 1 char can't have a proper suffix of len > 0
    for i in range(1,n):
        j = i-1
        while (j >= 0):
            if (pat[lps[j]] == pat[i]):
                lps[i] = lps[j] + 1
                break
            j = lps[j] - 1
            
    return lps


def KMP_pat_search(pat, txt):
    lps_pat = calcLPS(pat)

    patLen = len(pat)
    txtLen = len(txt)
    p = 0
    t = 0
    occurID = []
    while (t < txtLen):
        if (p < patLen):
            if (pat[p] == txt[t]):
                p += 1
                t += 1
            elif (p == 0):
                t += 1
            else:
                p = lps_pat[p-1]
        else:
            occurID.append(t-p)
            p = lps_pat[p-1]
    
    # Note - below check is required to include the occurrence of pat at the end of txt
    if (p == patLen):
        occurID.append(t-p)
    
    return occurID


if __name__ == '__main__':
    pat = input()
    txt = input()
    print('Pattern occurs in text at following indices -')
    print(KMP_pat_search(pat, txt))
