# Praktikum 2 - Metode Integrasi Romberg - Kelompok 4
Proyek ini dibuat sebagai praktikum Komputasi Numerik mengenai Integrasi Romberg oleh tim dengan anggota sebagai berikut:
- Ary Gustaf Muzaky — 5025251030
- Aston Justin Holiwono — 5025251035
- Darwisy Ahmad Alfayyadl — 5025251036


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
- Menampilkan hasil integral, iterasi dari tabel Romberg, dan grafik fungsi secara visual

### Struktur Program
- `romberg.py` - Program implementasi integrasi Romberg
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
Perhitungan dengan menggunakan rumus Romberg hingga dicapai hasil yang paling akurat

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

def set_pi_a():   st.session_state["a_input"] = "3.14159265358979"
def set_pi2_a():  st.session_state["a_input"] = "1.5707963267949"
def set_pi3_a():  st.session_state["a_input"] = "1.0471975511966"
def set_pi6_a():  st.session_state["a_input"] = "0.5235987755983"
def set_pi4_a():  st.session_state["a_input"] = "0.7853981633974"

def set_pi_b():   st.session_state["b_input"] = "3.14159265358979"
def set_pi2_b():  st.session_state["b_input"] = "1.5707963267949"
def set_pi3_b():  st.session_state["b_input"] = "1.0471975511966"
def set_pi6_b():  st.session_state["b_input"] = "0.5235987755983"
def set_pi4_b():  st.session_state["b_input"] = "0.7853981633974"

def parse_batas(nilai: str) -> float:
    nilai = nilai.strip().replace("π", "3.14159265358979")
    nilai = nilai.replace("pi", "3.14159265358979")
    return float(eval(nilai))


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


a_input = st.text_input("Batas Bawah (α)", value="1", key="a_input")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button("π",   key="pi_a",  on_click=set_pi_a)
with col2:
    st.button("π/2", key="pi2_a", on_click=set_pi2_a)
with col3:
    st.button("π/3", key="pi3_a", on_click=set_pi3_a)
with col4:
    st.button("π/4", key="pi4_a", on_click=set_pi4_a)
with col5:
    st.button("π/6", key="pi6_a", on_click=set_pi6_a)

b_input = st.text_input("Batas Atas (β)", value="4", key="b_input")
col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    st.button("π",   key="pi_b",  on_click=set_pi_b)
with col7:
    st.button("π/2", key="pi2_b", on_click=set_pi2_b)
with col8:
    st.button("π/3", key="pi3_b", on_click=set_pi3_b)
with col9:
    st.button("π/4", key="pi4_b", on_click=set_pi4_b)
with col10:
    st.button("π/6", key="pi6_b", on_click=set_pi6_b)

a = parse_batas(a_input)
b = parse_batas(b_input)


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

`import re` merupakan library regex untuk manipulasi string


```Python
from sympy import symbols
from sympy import sympify
from sympy import lambdify
```
Sympy digunakan untuk membuat varibel simbolik, misalnya `x` menjadi variabel dalam matematika

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

```Python
def preprocess_fungsi(fungsi: str) -> str:
    fungsi = fungsi.replace("^", "**")
    fungsi = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', fungsi)
    fungsi = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', fungsi)
    fungsi = re.sub(r'\)(\()', r')*\1', fungsi)
    return fungsi
```
Digunakan untuk mengganti format pangkat '^' dan menambahkan tanda kali di antara bilangan dan variabel

```Python
def set_pi_a():   st.session_state["a_input"] = "3.14159265358979"
def set_pi2_a():  st.session_state["a_input"] = "1.5707963267949"
def set_pi3_a():  st.session_state["a_input"] = "1.0471975511966"
def set_pi6_a():  st.session_state["a_input"] = "0.5235987755983"
def set_pi4_a():  st.session_state["a_input"] = "0.7853981633974"

def set_pi_b():   st.session_state["b_input"] = "3.14159265358979"
def set_pi2_b():  st.session_state["b_input"] = "1.5707963267949"
def set_pi3_b():  st.session_state["b_input"] = "1.0471975511966"
def set_pi6_b():  st.session_state["b_input"] = "0.5235987755983"
def set_pi4_b():  st.session_state["b_input"] = "0.7853981633974"

def parse_batas(nilai: str) -> float:
    nilai = nilai.strip().replace("π", "3.14159265358979")
    nilai = nilai.replace("pi", "3.14159265358979")
    return float(eval(nilai))
```
Digunakan untuk mendefinisikan masing-masing nilai `π` pada bagian input field

```Python
st.title("Integrasi Romberg")
st.write("Input fungsi: (sin(x), exp(x), sqrt(x), x**2 + 1)")

fungsi = st.text_input(
    "Fungsi f(x)",
    ""
)
```
Judul pada program serta keterangan untuk contoh input

```Python
_input = st.text_input("Batas Bawah (α)", value="1", key="a_input")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button("π",   key="pi_a",  on_click=set_pi_a)
with col2:
    st.button("π/2", key="pi2_a", on_click=set_pi2_a)
with col3:
    st.button("π/3", key="pi3_a", on_click=set_pi3_a)
with col4:
    st.button("π/4", key="pi4_a", on_click=set_pi4_a)
with col5:
    st.button("π/6", key="pi6_a", on_click=set_pi6_a)

b_input = st.text_input("Batas Atas (β)", value="4", key="b_input")
col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    st.button("π",   key="pi_b",  on_click=set_pi_b)
with col7:
    st.button("π/2", key="pi2_b", on_click=set_pi2_b)
with col8:
    st.button("π/3", key="pi3_b", on_click=set_pi3_b)
with col9:
    st.button("π/4", key="pi4_b", on_click=set_pi4_b)
with col10:
    st.button("π/6", key="pi6_b", on_click=set_pi6_b)

a = parse_batas(a_input)
b = parse_batas(b_input)
```
Bagian input batas bawah (nilai default = 1) dan batas atas (nilai default = 4) dengan pilihan tombol untuk `π`, `π/2`, `π/3`, `π/4`, dan `π/6`

```Python
iterasi = st.slider(
    "Jumlah Iterasi",
    min_value=1,
    max_value=40,
    value=4
)
```
Digunakan untuk menentukan berapa banyak jumlah iterasi untuk proses integrasi fungsi. Nilai minimalnya adalah 1 dan maksimalnya adalah 40

Setelah pengguna meneakan tombol `Calculate`, proses perhitungan dimulai

```Python

        fungsi = preprocess_fungsi(fungsi)
        x = symbols("x")
        expr = sympify(fungsi)
        f = lambdify(x,expr,modules=["numpy"])

```

Fungsi yang diinput akan masuk ke dalam `preprocess_fungsi`, variabel x diinisasi, string diubah menjadi ekspresi sympy dan Python (numpy)

```Python
tabel = romberg(f,a,b,iterasi)
        result = tabel[-1][-1]
        st.success(f"Hasil Integral = {result}")
```
`tabel` menyimpan nilai dari integrasi Romberg, dan menyimpannya dalam result (di tabel [-1][-1]) dan menampilkannya di `st.succes`

```Python
st.subheader("Tabel Romberg")
        df = pd.DataFrame(tabel)
        st.dataframe(df)
```
digunakan untuk menampilkan tabel Romberg

```Python
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
digunakan untuk menampilkan grafik fungsi (luas/integral)

## Dokumentasi

Percobaan dengan menggunakan fungsi `cos(x)` dengan batas bawah 0 dan batas atas π/2


<img width="1789" height="1049" alt="Screenshot From 2026-06-19 22-02-02" src="https://github.com/user-attachments/assets/4c123216-288c-4224-8308-7b6183308a11" />



