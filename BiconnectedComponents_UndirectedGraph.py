class Global:
    def __init__(self):
        self.t = 0          # Timer
        self.allBCC = []    # Store all Biconnected Components (i.e., set of edges forming a BCC)


def biconnComp(adj, disc, low, stck, v, par, g):
    disc[v] = low[v] = timer.t
    g.t += 1
    childs = 0
    
    for u in adj[v]:
        if disc[u]:
            if (u != par) and (disc[u] < disc[v]):
                # 'u' is already visited & 'u' is not the parent of 'v' --> 2 cases arise when the graph is Undirected -
                # Case-1: Edge v--u is a back-edge in the DFS tree (this case can be captured by the condition "disc[u] < disc[v]")
                #   In this case, we would want to update low[v] & push this back-edge in the stack (since this edge will be a part of current Biconnected component)
                # Case-2: Edge v--u is a forward-edge in the DFS tree (this case can be captured by the condition "disc[u] > disc[v]")
                #   In this case, we wouldn't want to update low[v]. Also, we wouldn't want to push this forward-edge "v--u" in stack (since the corresponding back-edge "u--v" would have already been pushed in stack earlier during DFS)
                
                # NOTE-1: "disc[v] = disc[u]" is not possible
                low[v] = min(low[v], disc[u])
                stck.append([v,u])
            continue
        
        childs += 1
        stck.append([v,u])
        biconnComp(adj, disc, low, stck, u, v, timer)
        low[v] = min(low[v], low[u])
        if ((not par) and (childs > 1)) or (par and (low[u] >= disc[v])):
            # NOTE-2: Unlike Tarjan's algo (where for finding SCC, the stack is popped out after DFS of 'v' is finished), here we need to check whether 'v' is an AP due to each DFS tree edge "v--u".
            # This is because for each DFS tree edge v--u1, v--u2, ..., v--u_i, if 'v' is an AP due to DFS tree edge v--u_i, then we found a Biconnected component which contains v--u_i. So, we need to pop out edges from stack till we get edge v--u_i out of stack.
            bcc = []
            while (stck[-1] != [v,u]):
                bcc.append(stck.pop())
            bcc.append(stck.pop())
            g.allBCC.append(bcc)
        

def allBiconnectedComponents(adj):
    V = len(adj)
    disc = [None] * V
    low = [None] * V
    stck = []   # To push visited edges in stack (NOTE-3: Unlike Tarjan's SCC algo for Directed graphs (where visited "vertices" are pushed in stack), here we need to push visited "edges" in stack, since 2 Biconnected components are gauranteed to be edge-disjoint but not vertex-disjoint)
    g = Global()
    
    for v in range(V):
        if (not disc[v]):
            biconnComp(adj, disc, low, stck, v, None, g)
            
            # A Biconnected component may still remain in stack (see an example below). So, we need to pop out that BCC too
            # Ex - Let's say 'v' has edges u1, u2, ..., u_i in DFS tree. Also, let's say that 'v' is an AP due to u1, u2, ..., u_k and 'v' is not an AP due to u_k+1, ..., u_i.
            # Since we check for BCC after every DFS tree edge is processed (see NOTE-2), each BCC containing edge v--u1, v--u2, ..., v--u_k is already popped out of stack & stored as answer,
            # but because v is not an AP due to v--u_k+1, ..., v--u_i, these edges (along with some other edges) will still remain in the stack, which form a BCC.
            # So, we need to pop these edges out of stack & add this remaining BCC in the answer.
            if stck:
                bcc = []
            while stck:
                bcc.append(stck.pop())
            g.allBCC.append(bcc)


def main():
    V, E = map(int, input().split())
    adj = [[] for v in range(V)]
    for e in range(E):
        v, u = map(int, input().split())    # Vertices in 0-indexed format
        adj[v].append(u)
        adj[u].append(v)
        
    return allBiconnectedComponents(adj)


if __name__ == '__main__':
    main()
