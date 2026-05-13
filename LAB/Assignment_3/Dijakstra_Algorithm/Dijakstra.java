import java.util.*;

public class Dijakstra {
	public static void main(String[] args) {
		int[][] g = {
			{0, 10, 0, 5, 0},
			{0, 0, 1, 2, 0},
			{0, 0, 0, 0, 4},
			{0, 3, 9, 0, 2},
			{7, 0, 6, 0, 0}
		};
		int n = g.length;
		int s = 0;
		int[] d = new int[n];
		boolean[] used = new boolean[n];
		Arrays.fill(d, Integer.MAX_VALUE);
		d[s] = 0;

		for (int i = 0; i < n; i++) {
			int u = -1;
			for (int j = 0; j < n; j++)
				if (!used[j] && (u == -1 || d[j] < d[u])) u = j;
			if (u == -1 || d[u] == Integer.MAX_VALUE) break;
			used[u] = true;

			for (int v = 0; v < n; v++)
				if (g[u][v] > 0 && d[u] + g[u][v] < d[v]) d[v] = d[u] + g[u][v];
		}

		for (int x : d) System.out.print((x == Integer.MAX_VALUE ? -1 : x) + " ");
	}
}
