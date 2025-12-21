# クラスタリング手法K-meansのTDDによる実装
## K-means法の概要
データ群Sを受け取り、それをk個のクラスタに分割するというクラスタリング手法である。
以下の処理によって行われる。
1. 各クラスタC<sub>i</sub>に代表点m<sub>i</sub>を割り振る
2. データ群Sの各点を代表点が最も近いクラスタに割り当てる
3. 各クラスタに割り当てられた点から、代表点を更新する
4. クラスタリング結果が安定するまで、2～3を繰り返す

## 作成した関数
`k_means` 関数の仕様を示す。
- 入力: 数直線上の点のリスト `data` , 分割数 `k`
- 出力: `data` を `k` 個に分割した結果

また、実装は次の方式を採用した。
- 初期代表点: `data` の最小値から最大値の範囲を `k` 個に分割した時の、 `i` 番目の範囲の中心
- 代表点: 所属する点の座標の平均

## TDDによる開発の流れ
Red: 昇順に並んだ、1サイクルで終わるデータのテストケース

```python
class TestKMeans(unittest.TestCase):
    def test_kmeans_basic(self):
        self.assertEqual(k_means([1, 2, 4], 2), [[1, 2], [4]])
```

Green: 関数 `k_means` の仮実装

```python
def k_means(data, k):
    return [[1, 2], [4]]
```

Red: テストケースを追加

```diff
 class TestKMeans(unittest.TestCase):
     def test_kmeans_basic(self):
         self.assertEqual(k_means([1, 2, 4], 2), [[1, 2], [4]])
+        self.assertEqual(k_means([1, 5, 6, 10], 3), [[1], [5, 6], [10]])
```

Green: 重心の初期化ロジックとクラスタリングを1サイクル行うロジックを追加

```diff
 def k_means(data, k):
-    return [[1, 2], [4]]
+    d = (data[-1] - data[0]) / k
+    centers = [data[0] + (i + 0.5) * d for i in range(k)]
+    clusters = [[] for _ in range(k)]
+    for point in data:
+        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
+        clusters[cluster_index].append(point)
+    return clusters
```

Refactor: テストコードに`subTest`を適用

```diff
 class TestKMeans(unittest.TestCase):
     def test_kmeans_basic(self):
-        self.assertEqual(k_means([1, 2, 4], 2), [[1, 2], [4]])
-        self.assertEqual(k_means([1, 5, 6, 10], 3), [[1], [5, 6], [10]])
+        params = [
+            ([1, 2, 4], 2, [[1, 2], [4]]),
+            ([1, 5, 6, 10], 3, [[1], [5, 6], [10]])
+        ]
+        for data, k, expected in params:
+            with self.subTest(data=data, k=k, expected=expected):
+                self.assertEqual(k_means(data, k), expected)
```

Refactor: テストコードを別ファイルに移動

`kmeans.py`の変更
```diff
-import unittest

-class TestKMeans(unittest.TestCase):
-    def test_kmeans_basic(self):
-        params = [
-            ([1, 2, 4], 2, [[1, 2], [4]]),
-            ([1, 5, 6, 10], 3, [[1], [5, 6], [10]])
-        ]
-        for data, k, expected in params:
-            with self.subTest(data=data, k=k, expected=expected):
-                self.assertEqual(k_means(data, k), expected)

-if __name__ == "__main__":
-    unittest.main()
```

`testKMeans.py`の新規作成
```diff
+import unittest
+from kmeans import k_means

+class TestKMeans(unittest.TestCase):
+    def test_kmeans_basic(self):
+        # ---コード自体は変更なし---

+if __name__ == "__main__":
+    unittest.main()
```

Red: 順番に並んでいない、1サイクルで終わるデータのテストケース

```diff
 class TestKMeans(unittest.TestCase):
+    def test_kmeans_unsorted(self):
+        params = [
+            ([2, 1, 4], 2, [[1, 2], [4]]),
+            ([10, 5, 6, 1], 3, [[1], [5, 6], [10]])
+        ]
+        for data, k, expected in params:
+            with self.subTest(data=data, k=k, expected=expected):
+                self.assertEqual(k_means(data, k), expected)
```

Green: データの最小値・最大値を得るときにmin関数やmax関数を使用するように変更、及び返り値を結果を昇順にしたものに変更

```diff
def k_means(data, k):
-    d = (data[-1] - data[0]) / k
-    centers = [data[0] + (i + 0.5) * d for i in range(k)]
+    d = (max(data) - min(data)) / k
+    centers = [min(data) + (i + 0.5) * d for i in range(k)]
    clusters = [[] for _ in range(k)]
    for point in data:
        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
        clusters[cluster_index].append(point)
-    return clusters
+    result = [sorted(cluster) for cluster in clusters]
+    return result
```