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
    int numChild = 0;   // No. of children of 'v' in DFS Tree
    int numAPs_u = 0;
    bool isAP_v = false;
    visit[v] = true;
    time[v] = timer.t;
    low[v] = timer.t;
    timer.t++;

    for (int u: adj[v])
    {
        if (u == par)
            continue;

        if (visit[u])
        {
            low[v] = min(low[v], time[u]);
        }
        else
        {
            numChild++;
            numAPs_u += numAPs_DFS(adj, visit, time, low, timer, u, v);
            low[v] = min(low[v], low[u]);
            if ((par != -1) && (low[u] >= time[v]))
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
