from sympy import symbols
from sympy import sympify
from sympy import lambdify
import streamlit as st
from romberg import romberg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Integrasi Romberg")
st.write("Masukkan fungsi: (sin(x), exp(x), sqrt(x), x**2 + 1)")

fungsi = st.text_input(
    "Fungsi f(x)",
    ""
)

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

        fungsi = fungsi.replace("^", "**")
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