import streamlit as st
import qrcode
from io import BytesIO
import csv
from datetime import datetime
import pandas as pd
import os

# Configuración de la app
st.set_page_config(page_title="Pase de Lista", layout="centered")
st.title("📝 Pase de Lista - Grupo A")

# Lista de alumnos
alumnos = ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo']
archivo_csv = "registro_asistencia.csv"

# Selección de rol
rol = st.selectbox("Selecciona tu rol:", ["Alumno", "Profesor"])

# --- Sección ALUMNO ---
if rol == "Alumno":
    st.subheader("📖 Historial de Asistencias")
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv, names=["Fecha", "Alumno"])
        st.dataframe(df)
    else:
        st.info("Aún no hay asistencias registradas.")
    st.stop()

# --- Sección PROFESOR ---
st.subheader("🔐 Acceso para profesores")
pwd = st.text_input("Ingresa la contraseña:", type="password")

if pwd != "ASP5005PROF":
    st.warning("Introduce la contraseña correcta para continuar.")
    st.stop()

# Acceso concedido
st.success("✅ Acceso autorizado como profesor.")

# Selección de fecha
st.subheader("📅 Selecciona la fecha de asistencia")
fecha_seleccionada = st.date_input("Día a registrar", value=datetime.today())

# Registro de asistencia
st.subheader("📋 Marca los alumnos presentes:")
asistencia = {
    alumno: st.checkbox(alumno, key=f"{alumno}_{fecha_seleccionada}")
    for alumno in alumnos
}

if st.button("✅ Enviar Asistencia"):
    presentes = [nombre for nombre, presente in asistencia.items() if presente]
    if presentes:
        fecha_str = fecha_seleccionada.strftime("%Y-%m-%d")
        with open(archivo_csv, "a", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            for alumno in presentes:
                writer.writerow([fecha_str, alumno])
        st.success("🎉 Asistencia registrada para el día seleccionado.")
    else:
        st.warning("Selecciona al menos un alumno para registrar asistencia.")

# Mostrar historial también al profesor
st.subheader("📖 Historial completo de Asistencias")
if os.path.exists(archivo_csv):
    df = pd.read_csv(archivo_csv, names=["Fecha", "Alumno"])
    st.dataframe(df)
else:
    st.info("Todavía no hay registros guardados.")

# Generar y mostrar código QR
st.subheader("📱 Código QR de acceso para alumnos")
url_app = "https://paselista3402.streamlit.app/"
qr = qrcode.make(url_app)
buf = BytesIO()
qr.save(buf)
st.image(buf, caption="Escanea para abrir la app", use_container_width=False)
