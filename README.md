#<h1 align=center>Deploy_PI_MLOPs-  

### <h1 align=center>Machine Learning Operations (MLOps)

Este proyecto tiene como objetivo desarrollar un sistema de recomendación de videojuegos para usuarios de Steam. La metodología adoptada sigue las prácticas de Extracción, Transformación y Carga (ETL) para procesar y unificar múltiples conjuntos de datos, y culmina en la implementación de una API robusta utilizando FastAPI. A continuación, se detallan las responsabilidades y acciones específicas de cada fase del proyecto:

### <h2 align=center>Introducción

La industria de los videojuegos es vasta y diversa, con miles de títulos disponibles en plataformas como Steam. Este proyecto se centra en abordar la necesidad de ofrecer recomendaciones personalizadas a los usuarios, mejorando así su experiencia y aumentando la participación.
Extracción, Transformación y Carga de Datos (ETL)
### <h3 align=left>ETL para Items (ETL_items.ipynb)

-Filtrado y Selección de Columnas: Se seleccionan las columnas 'user_id', 'item_id', y 'playtime_forever'.

-Creación de Identificador Único (id): Concatenamos 'user_id' y 'item_id' para crear una columna identificadora única.

-Tipo de Dato: Convertimos la columna 'item_id' a tipo cadena.

-Almacenamiento de Resultados: Guardamos el resultado en 'user_items.csv'.

### <h3 align=left>ETL para Reseñas (ETL_reviews.ipynb)

-Expansión de Listas: Utilizamos los métodos 'explode' y 'pd.Series' para manejar columnas con listas.

-Análisis de Sentimientos: Implementamos un análisis de sentimientos utilizando la biblioteca TextBlob.

-Filtrado de Registros Válidos: Eliminamos registros nulos y aquellos sin comentarios, valoraciones y recomendaciones.

-Selección de Columnas y Almacenamiento: Seleccionamos las columnas necesarias y almacenamos los resultados en 'user_reviews.csv'.

adjunto el link para el user_reviews.csv https://drive.google.com/file/d/1vsR2aGH_wUlfYgRWtjPBOD6jZiE2QyiS/view?usp=drive_link

### <h3 align=left>ETL para Juegos (ETL_games.ipynb)

-Conversión de Fecha: Convertimos la columna 'release_date' a formato datetime y extraemos el año.

-Manejo de Precios: Ajustamos la columna 'price' para permitir conversiones numéricas.

-Eliminación de Filas con Valores Nulos: Eliminamos filas con valores nulos en columnas clave.

-Selección de Columnas y Almacenamiento: Seleccionamos las columnas necesarias y almacenamos los resultados en 'games.csv'.

### <h2 align=center>Relación y Unión de Tablas
### <h3 align=left>Fusión de Datos (MERGE_PI.ipynb)

El proceso de fusión de datos implica la combinación de los DataFrames 'items', 'reviews', y 'games' para crear un conjunto de datos completo. Creamos un identificador único ('id') y seleccionamos las columnas específicas necesarias. El resultado final se almacena en 'data_steam.csv'.

Este enfoque estructurado garantiza que los datos estén listos para el análisis y la construcción de modelos, proporcionando una base sólida para el desarrollo de la API de recomendación.


### <h2 align=center>Funciones y API
### <h3 align=left>Documento: main.py

El desarrollo de la aplicación FastAPI se encuentra en 'main.py'. La API proporciona varios endpoints para consultas y análisis de datos de juegos de Steam. Algunas funciones destacadas son:

-/playtime_genre/{genero}: Devuelve el año con más horas jugadas para un género específico.

-/user_for_genre/{genero}: Proporciona el usuario con más horas jugadas y la distribución de horas jugadas por año para un género dado.

-/worst_developer_year/{año}: Devuelve los tres desarrolladores con peor calificación en un año determinado.

-/sentiment_analysis/{desarrolladora}: Realiza un análisis de sentimientos para las reseñas de una desarrolladora específica.

-/user_recommend/{año}: Devuelve una lista de los tres juegos con más recomendaciones y análisis de sentimientos en un año específico.

### <h3 align=center>Nota: Para consultas efectivas, respetar mayúsculas y minúsculas.
