import java.util.*;

class DSU {
    int[] p, r;

    DSU(int n) {
        p = new int[n];
        r = new int[n];
        for(int i=0;i<n;i++) p[i]=i;
    }

    int find(int x) {
        return p[x]==x ? x : (p[x]=find(p[x]));
    }

    boolean unite(int a, int b) {
        a = find(a);
        b = find(b);
        if(a == b) return false;

        if(r[a] < r[b]) { int t=a; a=b; b=t; }
        p[b] = a;
        if(r[a] == r[b]) r[a]++;
        return true;
    }
}

public class Kruskal {
    public static void main(String[] args) {
        int n = 4;
        int[][] edges = {
            {10,0,1}, {6,0,2}, {5,0,3},
            {15,1,3}, {4,2,3}
        };

        Arrays.sort(edges, Comparator.comparingInt(a -> a[0]));

        DSU dsu = new DSU(n);
        int mst = 0;

        for(int[] e : edges)
            if(dsu.unite(e[1], e[2]))
                mst += e[0];

        System.out.println(mst);
    }
}