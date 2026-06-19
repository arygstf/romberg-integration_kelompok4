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