import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Reporte Meteorológico')

# Cargar el archivo Excel directamente desde el repositorio
archivo = 'PRUEBANUEVA.xlsx'

try:
    df = pd.read_excel(archivo)

    # Redondear la columna 'Acumulado' a 1 decimal
    if 'Acumulado' in df.columns:
        df['Acumulado'] = df['Acumulado'].round(1)

    # Redondear la columna 'Anomalía' a 1 decimal
    if 'Anomalía' in df.columns:
        df['Anomalía'] = df['Anomalía'].round(1)

    # Mostrar la tabla
    st.subheader('Registro diario de Precipitación')
    st.dataframe(df)

    # Gráfico de barras para 'Acumulado' y '1*Normal Decadiaria'
    if 'Estación' in df.columns and 'Acumulado' in df.columns and '1*Normal Decadiaria' in df.columns:
        st.subheader('Gráfico de Barras - Precipitación')
        fig = px.bar(df, x='Estación', y=['Acumulado', '1*Normal Decadiaria'],
                     labels={'Estación': 'Estación', 'value': 'mm'}, barmode='group')
        st.plotly_chart(fig)
    else:
        st.error("Las columnas 'Estación', 'Acumulado' o '1*Normal Decadiaria' no están en el archivo.")

    # Gráfico de barras para 'Anomalía'
    if 'Estación' in df.columns and 'Anomalía' in df.columns:
        st.subheader('')

        # Definir colores: azul si es positiva, rojo si es negativa
        colores = ['blue' if val > 0 else 'red' for val in df['Anomalía']]

        fig_anomalia = go.Figure(
            data=[go.Bar(
                x=df['Estación'],
                y=df['Anomalía'],
                marker_color=colores
            )]
        )
        fig_anomalia.update_layout(
            xaxis_title='Estación',
            yaxis_title='Anomalía (mm)',
            title='Anomalía de Precipitación'
        )
        st.plotly_chart(fig_anomalia)
    else:
        st.warning("La columna 'Anomalía' no está en el archivo.")

except Exception as e:
    st.error(f"Ocurrió un error al cargar el archivo: {e}")





















