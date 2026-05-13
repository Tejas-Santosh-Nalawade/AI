import java.util.*;

public class Prims{

    static int prim(int n, List<List<int[]>> adj) {
        boolean[] vis = new boolean[n];
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));

        pq.add(new int[]{0,0});
        int mst = 0;

        while(!pq.isEmpty()) {
            int[] cur = pq.poll();
            int w = cur[0], u = cur[1];

            if(vis[u]) continue;

            vis[u] = true;
            mst += w;

            for(int[] nei : adj.get(u)) {
                int v = nei[0], wt = nei[1];
                if(!vis[v])
                    pq.add(new int[]{wt, v});
            }
        }

        return mst;
    }

    public static void main(String[] args) {
        int n = 4;

        List<List<int[]>> adj = new ArrayList<>();
        for(int i=0;i<n;i++) adj.add(new ArrayList<>());

        adj.get(0).add(new int[]{1,10});
        adj.get(0).add(new int[]{2,6});
        adj.get(0).add(new int[]{3,5});
        adj.get(1).add(new int[]{0,10});
        adj.get(1).add(new int[]{3,15});
        adj.get(2).add(new int[]{0,6});
        adj.get(2).add(new int[]{3,4});
        adj.get(3).add(new int[]{0,5});
        adj.get(3).add(new int[]{1,15});
        adj.get(3).add(new int[]{2,4});

        System.out.println(prim(n, adj));
    }
}