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