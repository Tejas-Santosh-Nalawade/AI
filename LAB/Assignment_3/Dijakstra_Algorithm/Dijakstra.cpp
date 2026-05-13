#include<bits/stdc++.h>
using namespace std;

int main() {
	vector<vector<int>> g = {
		{0, 10, 0, 5, 0},
		{0, 0, 1, 2, 0},
		{0, 0, 0, 0, 4},
		{0, 3, 9, 0, 2},
		{7, 0, 6, 0, 0}
	};
	int n = g.size();
	int s = 0;
	vector<int> d(n, INT_MAX), used(n, 0);
	d[s] = 0;

	for (int i = 0; i < n; i++) {
		int u = -1;
		for (int j = 0; j < n; j++)
			if (!used[j] && (u == -1 || d[j] < d[u])) u = j;
		if (u == -1 || d[u] == INT_MAX) break;
		used[u] = 1;

		for (int v = 0; v < n; v++)
			if (g[u][v] > 0 && d[u] + g[u][v] < d[v]) d[v] = d[u] + g[u][v];
	}

	for (int x : d) cout << (x == INT_MAX ? -1 : x) << " ";
}
