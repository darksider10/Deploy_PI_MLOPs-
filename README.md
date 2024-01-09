# Deploy_PI_MLOPs-


#Machine Learning Operations (MLOps)

Este proyecto tiene como objetivo desarrollar un sistema de recomendación de videojuegos para usuarios de Steam. La metodología adoptada sigue las prácticas de Extracción, Transformación y Carga (ETL) para procesar y unificar múltiples conjuntos de datos, y culmina en la implementación de una API robusta utilizando FastAPI. A continuación, se profundizará en cada fase del proyecto:
Introducción

La industria de los videojuegos es vasta y diversa, con miles de títulos disponibles en plataformas como Steam. Ofrecer recomendaciones personalizadas a los usuarios es crucial para mejorar la experiencia del usuario y aumentar la participación. Este proyecto aborda precisamente esa necesidad, utilizando datos de juegos de Steam para construir un sistema de recomendación efectivo.

Enlace al deployment https://deploy-pi-mlops.onrender.com/docs

Extracción, Transformación y Carga de Datos (ETL)

El proceso de ETL es esencial para garantizar que los datos estén en un formato adecuado para el análisis y la creación de modelos. En este proyecto, hemos realizado ETL en tres conjuntos de datos clave:

ETL para Items (ETL_items.ipynb)

-Filtrado y Selección de Columnas: Se seleccionan las columnas 'user_id', 'item_id', y 'playtime_forever'.

-Creación de Identificador Único (id): Se concatena 'user_id' y 'item_id' para crear una columna identificadora única.

-Tipo de Dato: La columna 'item_id' se convierte a tipo cadena.

-Almacenamiento de Resultados: El resultado se guarda en 'user_items.csv'.

ETL para Reseñas (ETL_reviews.ipynb)

-Expansión de Listas: Se utilizan los métodos 'explode' y 'pd.Series' para manejar columnas con listas.
-Análisis de Sentimientos: Se realiza un análisis de sentimientos utilizando la biblioteca TextBlob.
-Filtrado de Registros Válidos: Se eliminan registros nulos y aquellos sin comentarios, valoraciones y recomendaciones.
-Selección de Columnas y Almacenamiento: Se seleccionan las columnas necesarias y se almacenan los resultados en'user_reviews.csv'.

ETL para Juegos (ETL_games.ipynb)

-Conversión de Fecha: La columna 'release_date' se convierte a formato datetime y se extrae el año.
-Manejo de Precios: La columna 'price' se ajusta para permitir conversiones numéricas.
-Eliminación de Filas con Valores Nulos: Se eliminan filas con valores nulos en columnas clave.
-Selección de Columnas y Almacenamiento: Se seleccionan las columnas necesarias y se almacenan los resultados en 'games.csv'.

    
adjunto el link para el user_reviews.csv https://drive.google.com/file/d/1vsR2aGH_wUlfYgRWtjPBOD6jZiE2QyiS/view?usp=drive_link

Relación y Unión de Tablas
Fusión de Datos (MERGE_PI.ipynb)

El proceso de fusión de datos implica la combinación de los DataFrames 'items', 'reviews', y 'games' para crear un conjunto de datos completo. Se crea un identificador único ('id'), y se seleccionan las columnas específicas necesarias. El resultado final se almacena en 'data_steam.csv'.

Este enfoque estructurado garantiza que los datos estén listos para el análisis y la construcción de modelos, proporcionando una base sólida para el desarrollo de la API de recomendación.

Funciones y API
Documento: main.py

El desarrollo de la aplicación FastAPI se encuentra en 'main.py'. La API proporciona varios endpoints para consultas y análisis de datos de juegos de Steam. Algunas funciones destacadas son:

-/playtime_genre/{genero}: Devuelve el año con más horas jugadas para un género específico.
-/user_for_genre/{genero}: Proporciona el usuario con más horas jugadas y la distribución de horas jugadas por año para un género dado.
-/worst_developer_year/{año}: Devuelve los tres desarrolladores con peor calificación en un año determinado.
-/sentiment_analysis/{desarrolladora}: Realiza un análisis de sentimientos para las reseñas de una desarrolladora específica.
-/user_recommend/{año}: Devuelve una lista de los tres juegos con más recomendaciones y análisis de sentimientos en un año específico.

Nota: Para consultas efectivas, respetar mayúsculas y minúsculas.
