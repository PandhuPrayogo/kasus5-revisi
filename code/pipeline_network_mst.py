#!/usr/bin/env python3
"""
pipeline_network_mst.py

Studi Kasus 5 — Bangun jaringan pipa minimum + ukur latensi terjauh dari reservoir.

Input:
  - CSV edge list: tiap baris (node_u, node_v, weight)
  - nama kolom bisa 'u','v','w' atau sejenis
  - parameter: sumber reservoir node (reservoir_id)

Tugas:
  1. Hitung MST (minimum total weight) dari graf tak berarah berbobot
  2. Dari MST, jalankan Dijkstra dari reservoir → hitung jarak maksimum dan jalur ke node terjauh
Output:
  - Total biaya MST
  - Node yang paling jauh dari reservoir, jarak (latensi) dan jalurnya
  - (Opsional bisa juga menyimpan MST edge list ke file)

Referensi:
- Kruskal’s algorithm (heaps + DSU) — GeeksforGeeks. :contentReference[oaicite:4]{index=4}
- Dijkstra’s algorithm (non-negatif berat) — Wikipedia. :contentReference[oaicite:5]{index=5}
"""

import csv
import os
import sys
import heapq

# ---------------- Disjoint Set Union (Union-Find) untuk Kruskal ----------------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0]*n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[yr] < self.rank[xr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

# ---------------- Membaca CSV graf ----------------
def load_graph_edge_list(csv_path, u_col=None, v_col=None, w_col=None):
    """
    Baca CSV dan kembalikan (edges, node_map) dimana
    edges = list of (u,v,w)
    node_map = dict mapping node_label -> integer id 0..N-1
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File tidak ditemukan: {csv_path}")
    edges = []
    node_map = {}
    next_id = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        # deteksi kolom otomatis jika belum diberikan
        if u_col is None or v_col is None or w_col is None:
            lower = {c.lower():c for c in cols}
            if u_col is None:
                for c in ('u','node_u','from','src'):
                    if c in lower:
                        u_col = lower[c]
                        break
            if v_col is None:
                for c in ('v','node_v','to','dst'):
                    if c in lower:
                        v_col = lower[c]
                        break
            if w_col is None:
                for c in ('w','weight','cost','latency'):
                    if c in lower:
                        w_col = lower[c]
                        break
        # fallback: first three columns
        if u_col is None or v_col is None or w_col is None:
            u_col = u_col or cols[0]
            v_col = v_col or cols[1]
            w_col = w_col or cols[2]

        for row in reader:
            u_lbl = row[u_col]
            v_lbl = row[v_col]
            try:
                w = float(row[w_col])
            except:
                w = float(row[w_col].strip())
            if u_lbl not in node_map:
                node_map[u_lbl] = next_id; next_id += 1
            if v_lbl not in node_map:
                node_map[v_lbl] = next_id; next_id += 1
            u = node_map[u_lbl]
            v = node_map[v_lbl]
            edges.append((u, v, w))
    return edges, node_map

# ---------------- Hitung MST (Kruskal) ----------------
def compute_mst(n_nodes, edges):
    """
    edges: list of (u,v,w)
    return: mst_edges (list of (u,v,w)), total_weight
    """
    # sort edges by weight ascending
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n_nodes)
    mst_edges = []
    total_w = 0.0
    for u,v,w in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u,v,w))
            total_w += w
        if len(mst_edges) == n_nodes-1:
            break
    return mst_edges, total_w

# ---------------- Build adjacency list dari MST ----------------
def build_adj_from_edges(n, edges):
    adj = [[] for _ in range(n)]
    for u,v,w in edges:
        adj[u].append((v,w))
        adj[v].append((u,w))
    return adj

# ---------------- Dijkstra (untuk MST) ----------------
def dijkstra(adj, src):
    """
    adj: adjacency list of graph (u -> list of (v, w))
    src: source id
    return: dist[], prev[] untuk reconstruct path
    """
    n = len(adj)
    dist = [float('inf')]*n
    prev = [-1]*n
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d,u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v,w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

# ---------------- Path reconstruct ----------------
def reconstruct_path(prev, target):
    path = []
    u = target
    while u != -1:
        path.append(u)
        u = prev[u]
    path.reverse()
    return path

# ---------------- Main ----------------
def main():
    # Ubah path di sini jika perlu (atau bisa diteruskan sebagai argumen)
    csv_path = "studikasus5/data/flight_data_2024_sample20.csv"
    reservoir_label = None    # jika label string, nanti convert lewat node_map
    # reservoir_label = "Reservoir1"

    edges, node_map = load_graph_edge_list(csv_path)
    n = len(node_map)
    print(f"Jumlah node = {n}, jumlah edge = {len(edges)}")

    mst_edges, total_weight = compute_mst(n, edges)
    print(f"Total biaya MST = {total_weight:.3f}")

    adj_mst = build_adj_from_edges(n, mst_edges)

    # tentukan reservoir id
    if reservoir_label is None:
        # anggap node id 0 sebagai reservoir
        src = 0
    else:
        src = node_map.get(reservoir_label, None)
        if src is None:
            print(f"Reservoir label {reservoir_label} tidak ditemukan, pakai id 0.")
            src = 0

    dist, prev = dijkstra(adj_mst, src)
    # temukan node dengan jarak maksimum
    max_d = -1.0
    max_node = -1
    for u,d in enumerate(dist):
        if d < float('inf') and d > max_d:
            max_d = d
            max_node = u

    path = reconstruct_path(prev, max_node)
    # konversi back ke label (reverse mapping)
    rev_map = {v:k for k,v in node_map.items()}
    path_labels = [rev_map[u] for u in path]

    print(f"Reservoir id = {src} (label {rev_map.get(src,'?')})")
    print(f"Node terjauh dari reservoir = {max_node} (label {rev_map.get(max_node,'?')})")
    print(f"Latensi terjauh = {max_d:.3f}")
    print("Jalur terjauh:", " -> ".join(path_labels))

if __name__ == "__main__":
    main()
