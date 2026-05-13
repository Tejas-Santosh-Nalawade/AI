#include <bits/stdc++.h>
using namespace std;

int prim(int n, vector<vector<pair<int,int>>> &adj) {
    vector<bool> vis(n, false);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;

    pq.push({0, 0});
    int mst = 0;

    while(!pq.empty()) {
        auto [w, u] = pq.top();
        pq.pop();

        if(vis[u]) continue;

        vis[u] = true;
        mst += w;

        for(auto [v, wt] : adj[u]) {
            if(!vis[v])
                pq.push({wt, v});
        }
    }

    return mst;
}

int main() {
    int n = 4;
    vector<vector<pair<int,int>>> adj(n);

    adj[0] = {{1,10},{2,6},{3,5}};
    adj[1] = {{0,10},{3,15}};
    adj[2] = {{0,6},{3,4}};
    adj[3] = {{0,5},{1,15},{2,4}};

    cout << prim(n, adj);
}