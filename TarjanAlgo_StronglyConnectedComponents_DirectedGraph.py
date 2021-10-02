##### Tarjan's algorithm to find all Strongly Connected Components (SCCs) in a Directed Graph
##### This is a solution for https://www.hackerearth.com/practice/algorithms/graphs/strongly-connected-components/practice-problems/algorithm/components-of-graph-2b95e067/

import sys
sys.setrecursionlimit(500000)
 
 
class Timer:
    def __init__(self):
        self.t = 0
 
 
def anySCC_sizeGTEk_DFS(adj, inStck, stck, time, low, timer, v, air, thresh, K):
    inStck[v] = True
    stck.append(v)
 
    time[v] = timer.t
    low[v] = timer.t
    timer.t += 1
 
    if (air[v] >= thresh):
        for u in adj[v]:
            if (air[u] < thresh):
                continue
 
            if time[u]:
                if (not inStck[u]):
                    continue
                low[v] = min(low[v], time[u])
                continue
 
            if anySCC_sizeGTEk_DFS(adj, inStck, stck, time, low, timer, u, air, thresh, K):
                return True
            low[v] = min(low[v], low[u])

    # Note that since 'stck' is not a DFS callstack, a node 'v' is not popped out immediately after its DFS call is finished
    if (low[v] == time[v]):
        scc = []
        while (stck[-1] != v):
            scc.append(stck[-1])
            inStck[stck[-1]] = False
            stck.pop()
        scc.append(stck[-1])
        inStck[stck[-1]] = False
        stck.pop()

        if (len(scc) >= K):
            return True

    return False
 
 
def anySCC_sizeGTEk(adj, air, thresh, K):
    V = len(adj)
    inStck = [False] * V
    stck = []
    ##### IMPORTANT #####
    # Saying that "cross edges are not considered for updating low values" is WRONG..!! What actually is not considered
    # is an "SCC bridge" (if we define an "SCC bridge" as a "cross edge going from one SCC to an already visited SCC").
    # The reason for above is - the stack used in the algorithm is not a "DFS callstack" (i.e., it does not store the nodes
    # of a "single" branch of DFS tree); it is an "SCC stack" to store the entire sub-tree rooted at head of SCC.
    # Therefore, when we check if an already visited node (say, X) is present in the stack or not, we are actually
    # checking if X is present in an already visited SCC or not:
    #   1. X present in stack implies X is not a part of an already visited SCC. This implies that the edge to X is
    #      not an "SCC bridge". So, X is considered for updating low values.
    #   2. X not present in stack implies X is a part of an already visited SCC. This implies that the edge to X is
    #      an "SCC bridge". So, X is not considered for updating low values.
    # Thus, we see that the edge to X is like a 1-way bridge connecting an SCC to an already visited SCC.


    ##### Why back edges are considered but not SSC bridges? #####
    # Lets first understand why back edges are considered, & then we'll switch to the reason why SSC bridges are not.

    # Take a sheet of paper & draw a node 'U' & its ancestor 'V' in DFS tree (NOTE1 - V is not necessarily an immediate
    # ancestor of U; there can be 'k' no. of nodes between V & U in DFS tree, k>=0). Also draw a back edge from U to V.
    # That is, we are considering (k+2) nodes here.
    # Now, seeing this back edge, we know that if we select any 2 nodes from these (k+2) nodes, we'll be able to reach
    # from one to another. That is, back edges ensure that all these (k+2) nodes are in a single SCC. That's why, back
    # edges are considered in updating low values of U -
    #   low[u] = min(low[u], disc[v]);

    # Now, draw an SCC (called SCC2) which has some nodes, excluding those (k+2) nodes. (NOTE2 - SCC2 has already been
    # traversed in DFS, & during that traversal, there was found no path to reach U. That's why, we are considering U
    # as not a part of SCC2). Also, draw an edge from U to any node in SCC2. This is called a SCC bridge.
    # Now, we can go from U to SCC2 through this bridge, but can we come back from a node in SCC2 to U..??
    # The answer is no (because there is no edge from any node of SCC2 to U, as discussed in NOTE2).
    # That is, SCC bridges provide only one way path from one SCC to another SCC, & thus, it is assured that U will
    # never be in SCC2. Due to this assurance, low[u] is not updated when cross edges are encountered.

    # (NOTE3 - the sole purpose of updating low[u] value is to see - upto which ancestral node we can reach from
    # sub-tree rooted at U, & include it in the SCC of U.)
    
    time = [None] * V   # This is also used as visited array to check if a node is already visited by DFS
    low = [None] * V
    timer = Timer()
 
    for v in range(V):
        if (not time[v]):
            if anySCC_sizeGTEk_DFS(adj, inStck, stck, time, low, timer, v, air, thresh, K):
                return True
 
    return False
 
 
def airThresh(adj, air, K):
    low, high = 1, 10**9
    
    while (low < high):
        mid = (low + high)//2 + 1
        if anySCC_sizeGTEk(adj, air, mid, K):
            low = mid
        else:
            high = mid - 1
 
    return low
 
 
def main():
    N, M, K = map(int, input().split())
    air = list(map(int, input().split()))
    adj = [[] for n in range(N)]
    for m in range(M):
        u, v = map(int, input().split())
        # Converting vertices from 1-indexed to 0-indexed
        u -= 1
        v -= 1
        adj[u].append(v)
 
    print(airThresh(adj, air, K))
 
 
if __name__ == '__main__':
    main()
