# Praktikum 3

## Metode Integrasi Roomberg

### Pengertian
Metode integrasi roomberg adalah metode numerik untuk menghitung nilai integral tertentu dengan mengombinasikan aturan trapesium dan ekstrapolasi Richardson. Metode ini menambahkan ukuran langkah pada metode Tujuan utama dari metode ini adalah meningkatkan akurasi hasil integrasi tanpa menggunakan jumlah partisi yang sangat besar.


### Rumus
Secara umum, rumus yang digunakan untuk menggunakan integrasi roomber adalah sebagai berikut

- untuk menghitung kolom pertama dengan (m = 1)

$$
T_n =
\frac{h}{2}
\left[
f(a)
+
2\sum_{i=1}^{n-1}f(a+ih)
+
f(b)
\right]
$$


- untuk menghitung kolom berikutnya dengan (m>1)

$$
R_{k,m}=R_{k,m-1}+\frac{R_{k,m-1}-R_{k-1,m-1}}{4^{m-1}-1}
$$


## Keterangan:
- k : indeks baris
- m : indeks kolom (tingkat ekstrapolasi)



## Kode Program

```Python

```

### Penjelasan Kode
Kode program ini ditulis dengan menggunakan bahasa Python.

- Untuk `romberg.py` 
File ini berisi fungsi untuk melakukan integrasi dengan formula romberg

```Python
import math
```

digunakan untuk melakukan operasi matematika di Python

```Python
def romberg(f, a, b, n):
```
Deklarasi untuk fungsi `roomberg`

```Python
R = [[0.0] * n for _ in range(n)]
```
Digunakan untuk membuat matriks sesuai dengan indeks n

```Python
R[0][0] = (b - a) * (f(a) + f(b)) / 2
```

Rumus trapesium yang digunakan jika n = 1

```Python
for i in range(1, n):

        m = 2 ** i
        h = (b - a) / m
```

Kode ini berisi perulangan for() untuk menambah jumlah partisi dengan `m = 2 ** i`.


```Python

        sum = 0

        for k in range(1, m, 2):
            sum += f(a + k * h)

```

Digunakan untuk menambahkan titik-titik baru setelah jumlah interval digandakan

```Python
 R[i][0] = 0.5 * R[i - 1][0] + h * sum
```
Digunakan untuk memperbarui nilai trapesium

```Python
for j in range(1, i + 1):
```
Digunakan untuk mengisi kolom-kolom berikutnya 

```Python
R[i][j] = ( 4**j * R[i][j - 1] - R[i - 1][j - 1]) / (4**j - 1)
```
Perhitungan dengan menggunakan rumus romberg hingga dicapai hasil yang paling akurat

```Python
return R
```

Akan diambil nilai `R` terakhir

- Untuk `app.py`

```Python
from sympy import symbols
from sympy import sympify
from sympy import lambdify
```
> Sympy digunakan untuk membuat varibel simbolik, misalnya `x` menjadi variabel dalam matematika

```Python
import streamlit as st
```
Streamlit digunakan untuk membuat web app dan UI dari program Python yang dibuat

```Python
from romberg import romberg
```
Fungsi dari `romberg.py` yang telah dibuat sebelumnya diimport untuk `app.py`

```Python
import pandas as pd
```
`pandas` digunakan untuk mengolah data dalam bentuk tabel

```Python
import numpy as np
```
`numpy` digunakan untuk melakukan komputasi numerik

```Python
import matplotlib.pyplot as plt
```

`matplotlib` digunakan untuk membuat grafik dari fungsi



### Dokumentasi


