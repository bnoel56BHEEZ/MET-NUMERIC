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
asistencia = {}

st.subheader("📋 Selecciona quién está presente:")
for alumno in alumnos:
    asistencia[alumno] = st.checkbox(alumno)

# Guardar asistencia en CSV
if st.button("✅ Enviar Asistencia"):
    presentes = [nombre for nombre, presente in asistencia.items() if presente]
    if presentes:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo_csv = "registro_asistencia.csv"

        with open(archivo_csv, "a", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            for alumno in presentes:
                writer.writerow([fecha, alumno])
        st.success("¡Asistencia registrada con éxito!")
    else:
        st.warning("Marca al menos un alumno para registrar asistencia.")

# Mostrar código QR (enlace público o local)
url_app = "https://paselista3402.streamlit.app/"  # cambia si ya tienes la versión en la nube
qr = qrcode.make(url_app)
buf = BytesIO()
qr.save(buf)

st.subheader("📱 Escanea para abrir:")
st.image(buf, caption="Código QR de acceso", use_column_width=False)

# Mostrar historial si existe
if os.path.exists("registro_asistencia.csv"):
    st.subheader("📖 Historial de Asistencias")
    df = pd.read_csv("registro_asistencia.csv", names=["Fecha", "Alumno"])
    st.dataframe(df)
else:
    st.info("Aún no hay asistencias registradas.")
