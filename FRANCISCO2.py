import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# Título de la aplicación
st.title('Reporte Meteorológico - Feb 2025')

# Cargar el archivo Excel directamente desde el repositorio
archivo = 'PRUEBANUEVA.xlsx'

try:
    df = pd.read_excel(archivo)

    # Redondear las columnas relevantes a 1 decimal
    for col in ['1*Decada', 'Anomalía', 'Acumulado Mes', 'Anomalía Mes']:
        if col in df.columns:
            df[col] = df[col].round(1)

    # Mostrar la tabla
    st.subheader('Registro diario de Precipitación')
    with st.expander("Ver datos de precipitación"):
        st.dataframe(df)

    # Gráfico de barras para '1*Decada' y '1*N. Decadiaria'
    if 'Estación' in df.columns and '1*Decada' in df.columns and '1*N. Decadiaria' in df.columns:
        st.subheader('Precipitación Decadal')
        fig_decada = px.bar(df, x='Estación', y=['1*Decada', '1*N. Decadiaria'],
                            labels={'Estación': 'Estación', 'value': 'mm'}, barmode='group')
        st.plotly_chart(fig_decada)

    # Gráfico de barras para 'Anomalía'
    if 'Estación' in df.columns and 'Anomalía' in df.columns:
        st.subheader('Anomalía de Precipitación - 1*Decada')
        colores_anomalia = ['blue' if val > 0 else 'red' for val in df['Anomalía']]
        fig_anomalia = go.Figure(
            data=[go.Bar(x=df['Estación'], y=df['Anomalía'], marker_color=colores_anomalia)]
        )
        fig_anomalia.update_layout(xaxis_title='Estación', yaxis_title='Anomalía')
        st.plotly_chart(fig_anomalia)

    # Gráfico de barras para 'Acumulado Mes' y 'N. Mensual'
    if 'Estación' in df.columns and 'Acumulado Mes' in df.columns and 'N. Mensual' in df.columns:
        st.subheader('Precipitación Mensual')
        fig_mensual = px.bar(df, x='Estación', y=['Acumulado Mes', 'N. Mensual'],
                             labels={'Estación': 'Estación', 'value': 'mm'}, barmode='group')
        st.plotly_chart(fig_mensual)

    # Gráfico de barras para 'Anomalía Mes'
    if 'Estación' in df.columns and 'Anomalía Mes' in df.columns:
        st.subheader('Anomalía de Precipitación - Mensual')
        colores_anomalia = ['blue' if val > 0 else 'red' for val in df['Anomalía Mes']]
        fig_anomalia_mes = go.Figure(
            data=[go.Bar(x=df['Estación'], y=df['Anomalía Mes'], marker_color=colores_anomalia)]
        )
        fig_anomalia_mes.update_layout(xaxis_title='Estación', yaxis_title='Anomalía Mes')
        st.plotly_chart(fig_anomalia_mes)

    # Agregar el mapa con el GeoJSON
    st.subheader("Estaciones Meteorológicas - Dirección Zonal 6")
    geojson_file = "arequipa.geojson"
    
    try:
        m = folium.Map(location=[-16.409, -71.537], zoom_start=7)
        folium.GeoJson(geojson_file, name="Estaciones Meteorológicas").add_to(m)

        # Cargar datos de estaciones con latitud, longitud y precipitación
        archivo_estaciones = 'COORDENADAS.xlsx'
        
        try:
            df_estaciones = pd.read_excel(archivo_estaciones)
            
            if {'Latitud', 'Longitud', 'Estación', 'Precipitación'}.issubset(df_estaciones.columns):
                with st.expander("Ver datos de estaciones"):
                    st.write(df_estaciones)
                
                for _, row in df_estaciones.iterrows():
                    if pd.notna(row['Latitud']) and pd.notna(row['Longitud']):
                        folium.Marker(
                            location=[row['Latitud'], row['Longitud']],
                            popup=f"{row['Estación']}: {row['Precipitación']} mm",
                            icon=folium.Icon(color="blue")
                        ).add_to(m)
            else:
                st.error("El archivo 'COORDENADAS.xlsx' debe contener las columnas 'Latitud', 'Longitud', 'Estación' y 'Precipitación'.")
        
        except Exception as e:
            st.error(f"Error al cargar el archivo de estaciones: {e}")

        st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"Error al cargar el GeoJSON: {e}")

except Exception as e:
    st.error(f"Ocurrió un error al cargar el archivo: {e}")






















