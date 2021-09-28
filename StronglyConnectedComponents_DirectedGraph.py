##### Solution for https://www.hackerearth.com/practice/algorithms/graphs/strongly-connected-components/practice-problems/algorithm/components-of-graph-2b95e067/

import sys
sys.setrecursionlimit(500000)

def fillStck_finishTimeV_DFS1(adj, visit, stck, v, air, thresh):
    visit[v] = True
    for u in adj[v]:
        if visit[u]:   # If air[u] < thresh, there is no path from v to u (since the flight got cancelled due to low air quality index)
            continue
        
        fillStck_finishTimeV_DFS1(adj, visit, stck, u, air, thresh)

    stck.append(v)


def getSCC_DFS2(adjTransp, visit, scc, v, air, thresh):
    visit[v] = True
    scc.append(v)

    for u in adjTransp[v]:
        if visit[u]:
            continue

        getSCC_DFS2(adjTransp, visit, scc, u, air, thresh)


def anySCC_sizeGTEk(origAdj, air, thresh, K):
    V = len(origAdj)
    stck = []

    adj = [[] for v in range(V)]
    adjTransp = [[] for v in range(V)]
    for v in range(V):
        for u in origAdj[v]:
            if (air[v] >= thresh) and (air[u] >= thresh):
                adj[v].append(u)
                adjTransp[u].append(v)
    
    # DFS1 - insert vertices in stack acc. to finish time of vertices during DFS
    visit = [False] * V
    for v in range(V):
        if (not visit[v]):
            fillStck_finishTimeV_DFS1(adj, visit, stck, v, air, thresh)

    # DFS2 - keep doing DFS from top-most vertex in stack to get an SCC
    visit = [False] * V
    while stck:
        v = stck.pop()
        if (not visit[v]):
            scc = []
            getSCC_DFS2(adjTransp, visit, scc, v, air, thresh)
            if (len(scc) >= K):
                return True
            
    return False


def airThresh(origAdj, air, K):
    low, high = 1, 10**9
    
    while (low < high):
        mid = (low + high)//2 + 1
        if anySCC_sizeGTEk(origAdj, air, mid, K):
            low = mid
        else:
            high = mid - 1

    return low


def main():
    N, M, K = map(int, input().split())
    air = list(map(int, input().split()))
    origAdj = [[] for n in range(N)]
    for m in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        origAdj[u].append(v)
    
    print(airThresh(origAdj, air, K))


if __name__ == '__main__':
    main()
