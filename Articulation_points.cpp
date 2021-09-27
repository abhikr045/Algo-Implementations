#include <iostream>
#include <vector>

using namespace std;

class Timer
{
    public:
    int t = 0;
};


int numAPs_DFS(vector<vector<int>> &adj, vector<bool> &visit, vector<int> &time, vector<int> &low, Timer &timer, int v, int par)
{
    int numChild = 0;   // No. of children of 'v' in DFS Tree. Only required for checking if root vertex is AP or not (i.e., root is AP if numChild > 1)
    int numAPs_u = 0;   // Total no. of APs in all sub-trees rooted at children of 'v'
    bool isAP_v = false;    // v can be an AP if a sub-tree rooted at any of its child u has back-edge to ancestor of v
    visit[v] = true;
    time[v] = timer.t;
    low[v] = timer.t;
    timer.t++;

    for (int u: adj[v])
    {
        if (u == par)
            continue;

        if (visit[u])   // This means 'u' is an ancestor of 'v' but not a parent. So, 'v' must be connected to 'u' via back-edge
        {
            low[v] = min(low[v], time[u]);  // So, low[v] = min(low[v], discovery time of 'u')
        }
        else
        {
            numChild++;
            numAPs_u += numAPs_DFS(adj, visit, time, low, timer, u, v);
            low[v] = min(low[v], low[u]);   // 'u' is child of 'v' in DFS tree. So, low[v] = min(low[v], min. discovery time of any vertex reachable from sub-tree rooted at 'u') = min(low[v], low[u])

            if ((par != -1) && (low[u] >= time[v]))
                // Equality is required in "low[u] >= time[v]" above because of a case like:
                // . . . ---v---u---x---y---z
                //           \             /
                //            \___________/
                // Here, low[v] = low[u] = t
                // Removing vertex 'v' also disconnects the graph. So 'v' is an AP
                isAP_v = true;
        }
    }

    if (par == -1)
    {
        if (numChild > 1)
            return 1 + numAPs_u;
        else
            return numAPs_u;
    }
    else if (isAP_v)
        return 1 + numAPs_u;
    else
        return numAPs_u;
}


int articulationPoints(vector<vector<int>> &adj, Timer &timer)
{
    int V = adj.size();
    // time[v] = time of discovery of vertex 'v'
    // low[v] = min. discovery time of a vertex reachable from sub-tree rooted at 'v' via back-edge
    vector<int> time(V, -1), low(V, -1);
    vector<bool> visit(V, false);

    return numAPs_DFS(adj, visit, time, low, timer, 0, -1);
}


int main()
{
    int V, v, u, E, e;
    while (true)
    {
        cin >> V >> E;
        if ((V == 0) && (E == 0))
            break;

        vector<vector<int>> adj(V, vector<int>(0));
        for (e=0 ; e<E ; e++)
        {
            cin >> v >> u;
            // Input vertices are 1-indexed. So, converting them to 0-indexed
            v--;
            u--;
            adj[v].push_back(u);
            adj[u].push_back(v);
        }

        Timer timer = Timer();
        cout << articulationPoints(adj, timer) << endl;
    }

    return 0;
}
