# クラスタリング手法K-meansのTDDによる実装
## K-means法の概要
データ群Sを受け取り、それをk個のクラスタに分割するというクラスタリング手法である。
以下の処理によって行われる。
1. 各クラスタC<sub>i</sub>に代表点m<sub>i</sub>を割り振る
2. データ群Sの各点を代表点が最も近いクラスタに割り当てる
3. 各クラスタに割り当てられた点から、代表点を更新する
4. クラスタリング結果が安定するまで、2～3を繰り返す

## 作成した関数
### 仕様
`k_means` 関数の仕様を示す。
- 入力: 数直線上の点のリスト `data` , 分割数 `k`
- 出力: `data` を `k` 個に分割した結果

また、実装は次の方式を採用した。
- 初期代表点: ~~`data` の最小値から最大値の範囲を `k` 個に分割した時の、 `i` 番目の範囲の中心~~パーセンタイルの考え方を利用
- 代表点: 所属する点の座標の平均 (重心)
- 結果の安定性の判定: 前回の割り当て結果と同一であるかどうか

### 使用例
```python
from kmeans import k_means
data = [1, 2, 4, 10, 12]
clusters = k_means(data, k=2)
print(clusters) # [[1, 2, 4], [10, 12]]
```

## TDDによる開発の流れ
### `k_means`の仮実装
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

### 初期化とクラスター構築ロジック
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

### 順番でないデータに対応
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

Green: データの最小値・最大値を得るときに`min`関数や`max`関数を使用するように変更、及び返り値を結果を昇順にしたものに変更

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

### 外れ値があるデータに対応
Red: 外れ値がある場合のデータのテストケース

```diff
 class TestKMeans(unittest.TestCase):
+    def test_kmeans_multiple_iteration(self): # この時点では複数サイクルの実装で解決できると想定していた
+        self.assertEqual(k_means([1, 4, 6, 13], 3), [[1], [4, 6], [13]])
```

Green: クラスターの重心の初期化をパーセンタイル方式に変更

```diff
 def k_means(data, k):
-    d = (max(data) - min(data)) / k
-    centers = [min(data) + (i + 0.5) * d for i in range(k)]
+    sorted_data = sorted(data)
+    d = (len(data) - 1) / (k - 1)
+    centers = [sorted_data[int(d * i)] for i in range(k)]
	 # ---この後は変更なし---
```

Refactor: テストメソッド名を実際の解決方法に合わせて変更

```diff
 class TestKMeans(unittest.TestCase):
-    def test_kmeans_multiple_iteration(self):
+    def test_kmeans_outlier(self):
        self.assertEqual(k_means([1, 4, 6, 13], 3), [[1], [4, 6], [13]])
```

Refactor: 重心の初期化メソッドを別の関数として分割

```diff
def k_means(data, k):
-    sorted_data = sorted(data)
-    d = (len(data) - 1) / (k - 1)
-    centers = [sorted_data[int(d * i)] for i in range(k)]
+    centers = _init_centers(data, k)
	 # ---この後は変更なし---

+def _init_centers(data, k):
+    sorted_data = sorted(data)
+    d = (len(data) - 1) / (k - 1)
+    centers = [sorted_data[int(d * i)] for i in range(k)]
+    return centers
```

### ループ処理の実装
Red: 複数サイクルが必要になる場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_kmeans_multiple_iteration(self):
+        self.assertEqual(k_means([1, 6, 10, 11, 12], 3), [[1], [6], [10, 11, 12]])
```

Green: 重心の更新ロジックとループ処理を追加

```diff
def k_means(data, k):
    centers = _init_centers(data, k)

-    clusters = [[] for _ in range(k)]
-    for point in data:
-        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
-        clusters[cluster_index].append(point)
    
+    old_clusters = [[] for _ in range(k)]
+    while True:
+        clusters = [[] for _ in range(k)]
+        for point in data:
+            cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
+            clusters[cluster_index].append(point)
+        if(clusters == old_clusters):
+            break
+
+       for i in range(k):
+            centers[i] = sum(clusters[i]) / len(clusters[i])
+        old_clusters = clusters

    result = [sorted(cluster) for cluster in clusters]
    return result
```

Refactor: クラスター構築ロジックを別の関数として分離

```diff
def k_means(data, k):
	# ---ここは変更なし---
	while True:
-        clusters = [[] for _ in range(k)]
-        for point in data:
-            cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
-            clusters[cluster_index].append(point)
+        clusters = _form_clusters(data, k, centers)
        if(clusters == old_clusters):
            break
	# ---この後は変更なし--

+def _form_clusters(data, k, centers):
+    clusters = [[] for _ in range(k)]
+    for point in data:
+        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
+        clusters[cluster_index].append(point)
+    return clusters
```

### 所属する点が無いクラスターが発生する場合に対応
Red: 所属する点が無いクラスターが発生する場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_kmeans_empty_cluster(self):
+        self.assertEqual(k_means([10, 10], 2), [[10, 10], []])
```

Green: 所属する点が無い場合は重心をそのままにするように変更

```diff
def k_means(data, k):
	# ---変更のない部分は省略---
	while True:
		for i in range(k):
-            centers[i] = sum(clusters[i]) / len(clusters[i])
+            if(clusters[i] != []):
+                centers[i] = sum(clusters[i]) / len(clusters[i])
        old_clusters = clusters
		# ...
```

Refactor: 重心の更新ロジックを別の関数として分離

```diff
def k_means(data, k):
	# ---変更のない部分は省略---
	while True:
-        for i in range(k):
-            if(clusters[i] != []):
-                centers[i] = sum(clusters[i]) / len(clusters[i])
+        centers = _update_centers(centers, clusters)
		old_clusters = clusters
		# ...

+def _update_centers(centers, clusters):
+    new_centers = []
+    for current_center, cluster in zip(centers, clusters):
+        if cluster != []:
+            new_centers.append(sum(cluster) / len(cluster))
+        else:
+            new_centers.append(current_center)
+    return new_centers
```

### `k`についてのバリデーション
Red: `k`が正整数でない場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_k_must_be_positive(self):
+        params = [-1, 0]
+        for k in params:
+            with self.subTest(k=k):
+                with self.assertRaisesRegex(ValueError, "k must be positive"):
+                    k_means([1, 2, 3], k)
```

Green: `k`が正でない場合に`ValueError`を出すように修正

```diff
def k_means(data, k):
+    if k <= 0:
+        raise ValueError("k must be positive")
	#...
```

Red: `k`が整数でない場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_k_must_be_integer(self):
+        params = ["1", 0.5, [1, 2]]
+        for k in params:
+            with self.subTest(k=k):
+                with self.assertRaisesRegex(TypeError, "k must be integer"):
+                    k_means([1, 2, 3], k)
```

Green: `k`が整数でない場合に`TypeError`を出すように修正

```diff
def k_means(data, k):
+    if not isinstance(k, int):
+        raise TypeError("k must be integer")
	#...
```

### `data`についてのバリデーション

Red: `data`に数値(`int`または`float`)でない値が混ざっている場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_data_must_be_numeric_list(self):
+        params = [
+            [1, 2, "a"],
+            [1, [2, 3], 4]
+        ]
+        for data in params:
+            with self.subTest(data=data):
+                with self.assertRaisesRegex(TypeError, "data must be numeric list"):
+                    k_means(data, 3)
```

Green: `data`に`int`でも`float`でもない値が混ざっている場合に`TypeError`を出すように修正

```diff
def k_means(data, k):
+    if not all(isinstance(x, (int, float)) for x in data):
+        raise TypeError("data must be numeric list")
```

### `k`が1の場合の特例処理

Red: `k=1`の場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_k_is_one(self):
+        self.assertEqual(k_means([1, 2, 3], 1), [[1, 2, 3]])
```

Green: `k=1`ならば特例として結果をすぐ返すように修正

```diff
def k_means(data, k):
    # ---変更のない部分は省略---
    if k <= 0:
        raise ValueError("k must be positive")

+    if k == 1:
+        return [sorted(data)]
    #...
```

### `k`が`data`のサイズより大きい場合の処理

Red: `k`が`data`のサイズより大きい場合のテストケース

```diff
class TestKMeans(unittest.TestCase):
+    def test_k_must_not_be_larger_than_datasize(self):
+        with self.assertRaisesRegex(ValueError, "k must not be larger than data size"):
+            k_means([1, 2, 3], 4)
```

Green: `k>len(data)`の場合に`ValueError`を出すよう修正

```diff
class TestKMeans(unittest.TestCase):
    # ---変更のない部分は省略---
    if k <= 0:
        raise ValueError("k must be positive")
+    if k > len(data):
+        raise ValueError("k must not be larger than data size")
    #...
```

## 課題
### 適切にクラスタリングできないデータの存在

今回のプログラムでは、最終的にパーセンタイルの考え方を利用し、外れ値に強くした。
しかしこの初期化ロジックでは、データが密集していると適切にクラスタリングできない場合が存在する。

例えば、`data = [1, 5, 10, 11, 12]`の場合である。
このデータを3つのクラスターにクラスタリングすると、`[[1], [5], [10, 11, 12]]`となるのが自然である。
しかし、今回のプログラムでは`[[1, 5], [10, 11], [12]]`という局所解に陥る。

この問題に対する改善案を2つ挙げる。
1. 初期のように、`data`の最小値から最大値までを均等に分割する初期化方式でも行い、良い方の結果を採用する。
    - 利点: 決定的アルゴリズムであり、テストが容易である。
    - 欠点: データの密集と外れ値が両方存在するデータの場合、適切なクラスタリングができない可能性がある。
2. k-means++のように、乱数を用いて重心を初期化する方式でも行い、良い方の結果を採用する。
    - 利点: 十分な回数を行えば、適切なクラスタリングが行われることが期待できる。
    - 欠点: 乱数を用いるため、シード固定などテストの際に一工夫必要になる。

クラスタリングの良し悪しは、クラスタ内の二乗和誤差 (SSE) によって判断可能である。
アルゴリズムとしては適切なクラスタリングが行われることが重要なため、案2が有力と考えられる。

### より複雑なデータタイプへの対応

今回は、数直線上の点、すなわち単なる数値をクラスタリングを行う対象とした。
しかし、実際には二次元平面上の点など、より複雑なデータに対するクラスタリングが一般に行われている。

このようなデータでは、各データ間に順序が定義できるとは限らないため、その意味でも現在の初期化方式ではなく、k-means++などの他のアルゴリズムが有力となる。
