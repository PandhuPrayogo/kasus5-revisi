# Jaringan Pipa Minimum & Latensi Terjauh

## Deskripsi Proyek

Implementasi algoritma untuk membangun jaringan pipa minimum (MST) dan menghitung latensi terjauh dari reservoir dalam jaringan tersebut.

**Tujuan:**
1. Bangun **Jaringan Pipa Minimum** (Minimum Spanning Tree) dengan biaya minimum
2. Dari reservoir di MST, hitung jalur dengan **latensi (jarak) terjauh**
3. (Opsional) Analisis kapasitas/max-flow ke lahan kritis

## Struktur Direktori
```
projek_network_pipe/
├── pipeline_network_mst.py      # Program utama
├── data/
│   └── network_edges.csv        # CSV input (edge list)
├── results/                     # Folder hasil (opsional)
└── README.md
```

## Instalasi dan Setup

### Prasyarat
- Python 3.x

### Install Dependensi
```bash
pip install -r requirements.txt
```

### Persiapan Dataset

Simpan file CSV berisi edge list di folder `data/`.

**Format edge list:**
- Setiap baris merepresentasikan satu pipa: `u, v, w`
  - `u`: Node awal
  - `v`: Node akhir
  - `w`: Bobot (biaya atau latensi)

## Format CSV

### Contoh Format
```csv
node_from,node_to,weight
A,B,10
A,C,15
B,C,5
B,D,20
C,D,8
D,E,12
```

Atau dengan nama kolom lain:
```csv
source,target,cost
0,1,10
0,2,15
1,2,5
1,3,20
2,3,8
3,4,12
```

**Catatan:**
- Program akan auto-detect nama kolom umum
- Node dapat berupa angka (index) atau label string
- Bobot merepresentasikan biaya pembangunan atau latensi pipa

## Konfigurasi

Edit file `pipeline_network_mst.py` untuk menyesuaikan input:
```python
# Path ke file CSV
csv_path = "data/network_edges.csv"

# Label reservoir (None = auto-detect node pertama atau index 0)
reservoir_label = None  # atau "A", 0, dsb.
```

## Cara Menjalankan
```bash
python pipeline_network_mst.py
```

### Output Terminal

Program akan menampilkan:
1. **Informasi Graf**
   - Jumlah node
   - Jumlah edge
   - Reservoir yang digunakan

2. **Hasil MST**
   - Total biaya MST
   - Edge list yang terpilih (opsional)

3. **Analisis Latensi**
   - Node terjauh dari reservoir
   - Latensi maksimum
   - Jalur lengkap dari reservoir ke node terjauh

## Algoritma yang Digunakan

### 1. Kruskal's Algorithm (MST)

**Cara kerja:**
1. Urutkan semua edge berdasarkan bobot (ascending)
2. Iterasi setiap edge, tambahkan ke MST jika tidak membentuk cycle
3. Gunakan Disjoint Set Union (DSU/Union-Find) untuk deteksi cycle
4. Berhenti saat MST memiliki (V-1) edge

**Karakteristik:**
- Menghasilkan **MST dengan biaya minimum**
- Menjamin tidak ada siklus
- Optimal untuk graf sparse

**Kompleksitas:**
- Sorting: O(E log E)
- Union-Find: O(E · α(V)) ≈ O(E)
- **Total: O(E log E) ≈ O(E log V)**

**Alternatif:** Prim's Algorithm (lebih efisien untuk graf dense)

### 2. Dijkstra's Algorithm (SSSP pada MST)

**Cara kerja:**
1. Inisialisasi jarak dari reservoir = 0, node lain = ∞
2. Gunakan priority queue untuk memilih node dengan jarak minimum
3. Update jarak neighbor yang belum dikunjungi
4. Lacak predecessor untuk rekonstruksi jalur

**Karakteristik:**
- Mencari **shortest path** dari reservoir ke semua node
- Dalam konteks MST: mencari node dengan **latensi terjauh**
- Hanya bekerja untuk graf dengan bobot non-negatif

**Kompleksitas:**
- Dengan binary heap: O((V + E) log V)
- Dalam MST: E = V - 1, sehingga O(V log V)

## Analisis Teoretis

### Properti MST

1. **Cut Property**
   - Edge dengan bobot minimum yang crossing cut harus ada di MST

2. **Cycle Property**
   - Edge dengan bobot maksimum dalam cycle tidak ada di MST

3. **Uniqueness**
   - Jika semua bobot berbeda, MST unik
   - Jika ada bobot sama, bisa ada multiple MST dengan total biaya sama

### Disjoint Set Union (DSU)

Struktur data untuk efisiensi Kruskal:
- **Union**: Gabungkan dua set
- **Find**: Cari root/representative set
- **Path Compression**: Optimasi untuk O(α(n)) ≈ O(1) amortized

### Kompleksitas Total

| Fase | Algoritma | Kompleksitas |
|------|-----------|--------------|
| MST Construction | Kruskal | O(E log E) |
| SSSP on MST | Dijkstra | O(V log V) |
| **Total** | | **O(E log E + V log V)** |

Untuk graf terhubung: E ≥ V - 1, sehingga didominasi oleh O(E log E).

## Interpretasi Hasil

### Total Biaya MST
- **Minimum cost** untuk menghubungkan semua node
- Tidak ada subset edge lain yang lebih murah untuk menghubungkan graf

### Node Terjauh & Latensi
- **Critical Path**: Jalur dengan latensi terbesar dari reservoir
- Menunjukkan bottleneck/titik terlemah dalam jaringan
- Berguna untuk:
  - Prioritas upgrade infrastruktur
  - Perencanaan kapasitas tambahan
  - Analisis risiko supply chain

### Perbandingan dengan Graf Asli
- MST menghilangkan edge redundan
- Total biaya MST << Total biaya semua edge
- Beberapa jalur alternatif mungkin hilang

## Pengembangan Lanjutan

### Max-Flow ke Lahan Kritis

Setelah mendapat MST dan node kritis:

1. **Identifikasi Bottleneck**
   - Edge dengan kapasitas minimum di critical path

2. **Ford-Fulkerson / Edmonds-Karp**
   - Hitung maximum flow dari reservoir ke node kritis
   - Identifikasi min-cut untuk upgrade

3. **Capacity Augmentation**
   - Tentukan edge mana yang perlu ditingkatkan kapasitasnya
   - Optimasi biaya upgrade vs peningkatan flow

### Reliability Analysis

- **Edge Failure Probability**: Simulasi reliability jaringan
- **Redundant Paths**: Tambahkan edge backup untuk critical nodes
- **k-MST**: Bangun multiple spanning trees untuk redundancy

## Contoh Kasus

### Input
```csv
node_from,node_to,weight
Reservoir,A,10
Reservoir,B,15
A,C,20
B,C,8
C,D,12
B,D,25
```

### Output MST (Kruskal)
```
Selected edges:
- Reservoir → B (cost: 15)
- B → C (cost: 8)
- Reservoir → A (cost: 10)
- C → D (cost: 12)

Total MST cost: 45
```

### Latensi Terjauh (Dijkstra)
```
Reservoir: Reservoir
Farthest node: D
Maximum latency: 35 (Reservoir → B → C → D)
Path: Reservoir → B → C → D
```

**Interpretasi:**
- Node D memiliki latensi tertinggi (35 unit)
- Jika terjadi masalah di edge B→C atau C→D, supply ke D terganggu total
- Pertimbangkan backup path atau capacity upgrade

## Catatan Debugging

### Graf Tidak Terhubung
Jika MST tidak dapat dibentuk:
- Periksa apakah semua node terhubung dalam graf input
- Program akan memberikan warning jika graf disconnected

### Reservoir Tidak Valid
- Pastikan reservoir_label ada dalam node list
- Jika None, program akan gunakan node pertama/index 0

### Bobot Negatif
- Kruskal tetap bekerja dengan bobot negatif
- Dijkstra **tidak** bekerja dengan bobot negatif (gunakan Bellman-Ford)

## Pernyataan Keaslian (Untuk Laporan UTS)

> **Pernyataan Keaslian**
> 
> Kami menyatakan bahwa kode dan laporan ini adalah hasil kerja kelompok kami. Ide algoritma yang digunakan adalah materi umum yang dipelajari (Kruskal's Algorithm untuk MST, Dijkstra's Algorithm untuk SSSP); implementasi, eksperimen, dan analisis dilakukan oleh anggota tim: [Nama1, Nama2, Nama3]. Jika ada penggunaan sumber eksternal (paper, blog, AI), kami mencantumkan referensi dan menjelaskan bagian yang diadaptasi.

**Jika menggunakan bantuan AI:**
> Bagian kode X dihasilkan atau dibantu oleh AI (ChatGPT) dan telah saya modifikasi, verifikasi, dan pahami sepenuhnya.

## Referensi

Wajib dicantumkan dalam bibliografi laporan UTS:

1. Kruskal, J. B. (1956). On the shortest spanning subtree of a graph and the traveling salesman problem. *Proceedings of the American Mathematical Society*, 7(1), 48-50.

2. Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1(1), 269-271.

3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. — Chapter 23 (MST) & Chapter 24 (Single-Source Shortest Paths).

4. Tarjan, R. E. (1975). Efficiency of a good but not linear set union algorithm. *Journal of the ACM*, 22(2), 215-225. — Disjoint Set Union.

5. GeeksforGeeks — Kruskal's Minimum Spanning Tree Algorithm. https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/

6. Wikipedia — Minimum spanning tree. https://en.wikipedia.org/wiki/Minimum_spanning_tree

7. Wikipedia — Dijkstra's algorithm. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

8. Scaler Topics — Time Complexity of Kruskal's Algorithm. https://www.scaler.com/topics/data-structures/kruskal-algorithm/

---

**Catatan:** Pastikan semua referensi di atas dicantumkan dalam laporan UTS Anda, tidak hanya di README.

## Lisensi

Proyek ini dibuat untuk keperluan akademik (UTS). Penggunaan di luar konteks akademik harus seizin pembuat.

## FAQ

**Q: Apa perbedaan Kruskal vs Prim?**
- Kruskal: Sort edges, pilih edge minimum yang tidak cycle (bagus untuk sparse graph)
- Prim: Grow tree dari satu node, selalu pilih edge minimum connected (bagus untuk dense graph)

**Q: Kenapa pakai Dijkstra di MST, bukan di graf asli?**
- MST sudah optimal untuk biaya pembangunan
- Dijkstra di MST menunjukkan worst-case latency **setelah** jaringan dibangun dengan biaya minimum

**Q: Bagaimana jika ada multiple MST?**
- Semua MST memiliki total biaya sama
- Pilihan edge spesifik bisa berbeda
- Analisis latensi bisa berbeda tergantung MST yang dipilih
