#include<bits/stdc++.h>
using namespace std;

struct Edge {
    int u,v , weight;
};

bool cmp(Edge a, Edge b){
    return a.weight < b.weight;
}

class DSU{
    public:
        vector<int>parent, rank;

        DSU(int n){
            parent.resize(n);
            rank.resize(n);
            for(int i=0; i<n; i++){
                parent[i] = i;
            }
        }
        int find(int x){
            if(parent[x] !=x){
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }
        void unite(int x, int y){
            int px = find(x);
            int py = find(y);
            if(px!=py){
                if(rank[px]< rank[py]){
                    parent[px] = py;
                }
                else if (rank[px] > rank[py]){
                    parent[py] = px;
                }
                else{
                    parent[py] = px;
                    rank[px]++;
                }
            }
        }
};

int kruskal(int n, vector<Edge>&edges){
    sort(edges.begin(), edges.end(), cmp);

    DSU dsu(n);

    int cost =0;

    for(auto edge:edges){
        if(dsu.find(edge.u) != dsu.find(edge.v)){
            cost+=edge.weight;
            dsu.unite(edge.u, edge.v);
        }
    }
    return cost;
}

int main(){

int n = 4;
    vector<Edge> edges = {
        {0, 1, 10},
        {0, 2, 6},
        {0, 3, 5},
        {1, 3, 15},
        {2, 3, 4}
    };
    cout << "MST Cost: " << kruskal(n, edges);


    return 0;
}