# Praktikum 2 - Metode Integrasi Romberg - Kelompok 4

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


### Keterangan:
- k : indeks baris
- m : indeks kolom (tingkat ekstrapolasi)


##  Deskripsi Program
Aplikasi ini menggunakan metode numerik Integrasi Romberg untuk menghitung nilai integral tertentu secara lebih akurat dibandingkan metode trapesium biasa. Program dibuat dengan Python dan Streamlit agar hasil perhitungan dapat dilihat melalui antarmuka web yang mudah digunakan.

### Tujuan dan Fitur Program
- Memberikan kemudahan bagi pengguna untuk mencari hasil integral tentu dengan memasukkan fungsi beserta batas atas (α) dan batas bawahnya (β)
- Menampilkan hasil integral, iterasi dari tabel romberg, dan grafik fungsi secara visual

### Struktur Program
- `romberg.py` - Program implementasi integrasi romberg
- `app.py` - Antarmuka (UI) berbasis web (Streamlit)


### Prerequisites
- Python (yang digunakan pada praktikum ini adalah versi 3.14)
- pip
- Sistem operasi (Windows / MacOS / Linux)

Dependensi yang digunakan: `streamlit`, `sympy`, `pandas`, `numpy`, `matplotlib`

## Kode Program

### Untuk `romberg.py` 
File ini berisi fungsi untuk melakukan integrasi dengan formula romberg

#### Kode Lengkap
```Python
import math

def romberg(f, a, b, n):
    
    R = [[0.0] * n for _ in range(n)]

    R[0][0] = (b - a) * (f(a) + f(b)) / 2

    for i in range(1, n):

        m = 2 ** i
        h = (b - a) / m

        sum = 0

        for k in range(1, m, 2):
            sum += f(a + k * h)

        R[i][0] = 0.5 * R[i - 1][0] + h * sum

        for j in range(1, i + 1):
            R[i][j] = ( 4**j * R[i][j - 1] - R[i - 1][j - 1]) / (4**j - 1)

    return R
```

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

### Untuk `app.py`

#### Kode Lengkap

```Python
import re
from sympy import symbols
from sympy import sympify
from sympy import lambdify
import streamlit as st
from romberg import romberg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def preprocess_fungsi(fungsi: str) -> str:
    fungsi = fungsi.replace("^", "**")
    fungsi = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', fungsi)
    fungsi = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', fungsi)
    fungsi = re.sub(r'\)(\()', r')*\1', fungsi)
    return fungsi


st.title("Integrasi Romberg")
st.write("Input fungsi: (sin(x), exp(x), sqrt(x), x**2 + 1)")

fungsi = st.text_input(
    "Fungsi f(x)",
    ""
)

if fungsi :
    try:
        preview = preprocess_fungsi(fungsi)
        preview = preview.replace("**", "^")
        st.caption("Preview:")
        st.latex(preview)
    except:
        pass


a = st.number_input(
    "Batas Bawah (α)",
    value=1.0
)

b = st.number_input(
    "Batas Atas (β)",
    value=4.0
)

iterasi = st.slider(
    "Jumlah Iterasi",
    min_value=1,
    max_value=40,
    value=4
)

if st.button("Calculate"):

    try:

        fungsi = preprocess_fungsi(fungsi)
        x = symbols("x")
        expr = sympify(fungsi)
        f = lambdify(x,expr,modules=["numpy"])


        tabel = romberg(f,a,b,iterasi)
        result = tabel[-1][-1]

        st.success(f"Hasil Integral = {result}")
        st.subheader("Tabel Romberg")
        df = pd.DataFrame(tabel)
        st.dataframe(df)
        st.subheader("Grafik Fungsi")

        xs = np.linspace(a, b, 500)
        ys = f(xs)
        ys = np.ones_like(xs) * ys
     
        fig, ax = plt.subplots()

        ax.plot(xs, ys, label="f(x)")

        ax.fill_between(
        xs,
        ys,
        0,  
        alpha=0.3,
        label=f"Integral [{a}, {b}]"
        )

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

    except Exception as e:
        st.error(
            f"Error: {e}"
        )
```

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



## Dokumentasi



## Kredit

Proyek ini dibuat sebagai praktikum Komputasi Numerik mengenai Integrasi Romberg oleh tim dengan anggota sebagai berikut:
- Ary Gustaf Muzaky — 5025251030
- Aston Justin Holiwono - 5025251035
- Darwisy Ahmad Alfayyadl - 5025251036


