import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Reporte Meteorológico')

# Subir archivo Excel
archivo = st.file_uploader("D:/AUTOMATICAS FTP/PRUEBANUEVA", type=["xlsx"])

if archivo is not None:
    try:
        # Cargar datos del archivo Excel
        df = pd.read_excel(archivo)

        # Redondear la columna '1Decada' a 1 decimal
        if 'Acumulado' in df.columns:
            df['Acumulado'] = df['Acumulado'].round(1)

        # Verificar si el archivo tiene datos
        if df.empty:
            st.error("El archivo está vacío. Por favor, verifica el contenido del archivo.")
        else:
            # Mostrar la tabla
            st.subheader('Registro diario de Precipitación')
            st.dataframe(df)

            # Verificar si las columnas necesarias están presentes
            if 'Estación' in df.columns and 'Acumulado' in df.columns and '1*Normal Decadiaria' in df.columns:
                # Graficar las columnas "Acumulado" y "1*Normal Decadiaria"
                st.subheader('Gráfico de Barras')
                fig = px.bar(df, x='Estación', y=['Acumulado', '1*Normal Decadiaria'],
                             title='',
                             labels={'Estación': 'Estación', 'value': 'mm'}, barmode='group')
                st.plotly_chart(fig)
            else:
                st.error("Las columnas 'Estación', 'Acumulado' o '1*Normal Decadiaria' no están en el archivo.")
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el archivo: {e}")
else:
    st.info("Por favor, sube un archivo Excel.")



















