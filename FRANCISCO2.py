import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Reporte Meteorológico')

# Cargar el archivo Excel directamente desde el repositorio
archivo = 'D:/AUTOMATICAS FTP/PRUEBANUEVA.xlsx'

try:
    df = pd.read_excel(archivo)

    # Redondear la columna 'Acumulado' a 1 decimal
    if 'Acumulado' in df.columns:
        df['Acumulado'] = df['Acumulado'].round(1)

    # Mostrar la tabla
    st.subheader('Registro diario de Precipitación')
    st.dataframe(df)

    # Graficar si están las columnas necesarias
    if 'Estación' in df.columns and 'Acumulado' in df.columns and '1*Normal Decadiaria' in df.columns:
        st.subheader('Gráfico de Barras')
        fig = px.bar(df, x='Estación', y=['Acumulado', '1*Normal Decadiaria'],
                     labels={'Estación': 'Estación', 'value': 'mm'}, barmode='group')
        st.plotly_chart(fig)
    else:
        st.error("Las columnas 'Estación', 'Acumulado' o '1*Normal Decadiaria' no están en el archivo.")
except Exception as e:
    st.error(f"Ocurrió un error al cargar el archivo: {e}")




















