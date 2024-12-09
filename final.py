# Importar las librerías necesarias
import streamlit as st  # Para crear la interfaz gráfica de usuario
import pandas as pd  # Para manejar y analizar las bases de datos
from PIL import Image  # Para trabajar con imágenes
import os  # Para manejar rutas de archivos

# Cargar las bases de datos
file_path_1 = 'DATOS.csv'  # Este archivo contiene información de los productos
file_path_2 = 'DATOS1.csv'  # Este archivo contiene información de las empresas
imagenes_path = 'FOTEX/'  # Carpeta donde se guardan las imágenes de los productos

# Leer los archivos CSV con codificación 'latin1' porque algunos caracteres especiales pueden fallar sin esta codificación
db1 = pd.read_csv(file_path_1, encoding='latin1')
db2 = pd.read_csv(file_path_2, encoding='latin1')

# Normalizar los nombres de las columnas eliminando espacios adicionales
# Esto es útil porque a veces los nombres de las columnas tienen espacios al inicio o al final que podrían causar errores
db1.columns = db1.columns.str.strip()
db2.columns = db2.columns.str.strip()

# Convertimos los nombres de las empresas a mayúsculas para evitar problemas de coincidencia por minúsculas/mayúsculas
db2['EMPRESA'] = db2['EMPRESA'].str.strip().str.upper()

# Título de la aplicación
# Usamos Markdown para crear un título centralizado y visualmente atractivo
st.markdown("<h1 style='text-align: center;'>Catálogo de Equipos Audiovisuales</h1>", unsafe_allow_html=True)

# Paso 1: Seleccionar el tipo de dispositivo
# Obtenemos los tipos únicos de dispositivos del archivo de productos y los mostramos en un menú desplegable
tipos_dispositivo = db1['TIPO DE DISPOSITIVO'].dropna().unique()
tipo_seleccionado = st.selectbox("Seleccione el tipo de dispositivo:", tipos_dispositivo)

# Filtrar los modelos según el tipo seleccionado
# Aquí filtramos las filas del DataFrame para mostrar solo los modelos correspondientes al tipo de dispositivo seleccionado
modelos_filtrados = db1[db1['TIPO DE DISPOSITIVO'] == tipo_seleccionado]
modelos = modelos_filtrados['MODELO'].unique()
modelo_seleccionado = st.selectbox("Seleccione el modelo del dispositivo:", modelos)

# Filtrar detalles del modelo seleccionado
# Nuevamente, filtramos el DataFrame para obtener solo los datos del modelo seleccionado
detalles_dispositivo = modelos_filtrados[modelos_filtrados['MODELO'] == modelo_seleccionado]

# Mostrar información del dispositivo seleccionado
if not detalles_dispositivo.empty:  # Verificamos que hay datos para mostrar
    st.markdown("### Detalles del dispositivo seleccionado:")
    
    # Mostrar la imagen del producto si existe
    # La columna 'FOTEX' contiene el nombre del archivo de la imagen
    fotex = detalles_dispositivo.iloc[0]['FOTEX'].strip()  # Normalizamos eliminando espacios
    imagen_path = os.path.join(imagenes_path, fotex)  # Creamos la ruta completa para la imagen
    if os.path.exists(imagen_path):  # Verificamos si la imagen existe en la carpeta
        imagen = Image.open(imagen_path)
        st.image(imagen, use_column_width=True)  # Mostramos la imagen sin subtítulo
    else:
        st.write("No se encontró una imagen para este producto.")  # Mensaje si la imagen no está disponible
    
    # Comparativa de precios entre todas las empresas
    st.markdown("### Información de las tres empresas:")
    empresas_disponibles = []  # Lista para almacenar la información de las empresas

    # Listar los costos por empresa
    # Estas son las columnas donde se encuentran los precios de cada empresa
    columnas_costos = ['COSTO_E2', 'COSTO_PCR', 'COSTO_CINEMARENTAL']
    # Correspondencia con los nombres reales de las empresas
    empresas = ['E2 PERU', 'PCR PERU CINE RENTAL', 'CINEMA RENTAL']
    
    for empresa, columna_costo in zip(empresas, columnas_costos):  # Iteramos simultáneamente sobre empresas y columnas
        precio = detalles_dispositivo.iloc[0][columna_costo]  # Obtenemos el precio de la columna correspondiente
        if pd.notna(precio) and precio != '-':  # Si hay un precio válido, lo mostramos
            precio_mostrar = precio
        else:
            precio_mostrar = "No disponible"  # Si no hay precio válido, mostramos "No disponible"

        # Obtenemos la información de la empresa desde la base de datos de empresas
        empresa_info = db2[db2['EMPRESA'] == empresa]
        if not empresa_info.empty:  # Si encontramos la empresa en la base
            empresa_nombre = empresa_info.iloc[0]['EMPRESA']
            locacion = empresa_info.iloc[0]['LOCACION']
            contacto = empresa_info.iloc[0]['CONTACTO']
        else:  # Si no encontramos la empresa, mostramos "No disponible"
            empresa_nombre = empresa
            locacion = "No disponible"
            contacto = "No disponible"

        # Ajustes específicos para Cinema Rental
        if empresa == 'CINEMA RENTAL':  # Actualizamos la ubicación y contacto de Cinema Rental
            locacion = "TIENDA ONLINE"
            contacto = "922 785 337"

        # Agregamos la información de la empresa a la lista
        empresas_disponibles.append({
            'Empresa': empresa_nombre,
            'Precio': precio_mostrar,
            'Ubicación': locacion,
            'Contacto': contacto
        })
    
    # Mostrar siempre las tres empresas
    # Creamos un DataFrame a partir de la lista de empresas disponibles y lo mostramos
    comparativa_df = pd.DataFrame(empresas_disponibles)
    st.write("Empresas y precios disponibles:")
    st.dataframe(comparativa_df)  # Mostramos la tabla de datos en la interfaz
else:
    st.write("No se encontró información para el modelo seleccionado.")  # Mensaje si no hay datos para el modelo
