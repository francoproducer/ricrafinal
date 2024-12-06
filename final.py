import streamlit as st
import pandas as pd


# Cargar las bases de datos
file_path_1 = '1.csv'  # Cambia el nombre si es necesario
file_path_2 = '2.csv'  # Cambia el nombre si es necesario

# Leer los archivos CSV con codificación 'latin1'
db1 = pd.read_csv(file_path_1, encoding='latin1')
db2 = pd.read_csv(file_path_2, encoding='latin1')

# Normalizar los nombres de las empresas en ambas bases para evitar problemas de coincidencia
db2['EMPRESA'] = db2['EMPRESA'].str.strip().str.upper()

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>Catálogo de Equipos Audiovisuales</h1>", unsafe_allow_html=True)

# Paso 1: Seleccionar el tipo de dispositivo
tipos_dispositivo = db1['TIPO DE DISPOSITIVO'].dropna().unique()
tipo_seleccionado = st.selectbox("Seleccione el tipo de dispositivo:", tipos_dispositivo)

# Filtrar modelos según el tipo seleccionado
modelos_filtrados = db1[db1['TIPO DE DISPOSITIVO'] == tipo_seleccionado]
modelos = modelos_filtrados['MODELO'].unique()
modelo_seleccionado = st.selectbox("Seleccione el modelo del dispositivo:", modelos)

# Filtrar detalles del modelo seleccionado
detalles_dispositivo = modelos_filtrados[modelos_filtrados['MODELO'] == modelo_seleccionado]

# Mostrar información del dispositivo
if not detalles_dispositivo.empty:
    st.markdown("### Detalles del dispositivo seleccionado:")
    costo = detalles_dispositivo.iloc[0]['COSTO']
    st.write(f"- **Costo de alquiler por día:** {costo}")
    
    # Mostrar empresas que tienen el producto disponible
    st.markdown("### Empresas que tienen este dispositivo disponible:")
    empresas_mostradas = False  # Bandera para verificar si se muestra al menos una empresa

    for empresa_columna in db1.columns[3:]:  # Empresas están desde la columna 3 en adelante
        disponibilidad = detalles_dispositivo.iloc[0][empresa_columna]
        if disponibilidad == 1:  # Solo mostrar empresas que tienen el dispositivo
            empresas_mostradas = True
            # Buscar información en la base 2 usando el nombre de la columna como referencia
            empresa_info = db2[db2['EMPRESA'] == empresa_columna.strip().upper()]
            if not empresa_info.empty:
                empresa_nombre = empresa_info.iloc[0]['EMPRESA']
                locacion = empresa_info.iloc[0]['LOCACION']
                contacto = empresa_info.iloc[0]['CONTACTO']

                # Mostrar información en formato compacto
                st.markdown(f"<h4>{empresa_nombre}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5>Ubicación:</h5> {locacion}", unsafe_allow_html=True)
                st.markdown(f"<h5>Contacto:</h5> {contacto}", unsafe_allow_html=True)

    if not empresas_mostradas:
        st.write("No se encontraron empresas que tengan este producto disponible.")
else:
    st.write("No se encontró información para el modelo seleccionado.")
