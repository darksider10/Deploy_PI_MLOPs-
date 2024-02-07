import pandas as pd
from fastapi import FastAPI
app = FastAPI()
steam = pd.read_csv("steam.csv")
@app.get("/Developer_Free/{desarrollador}")
def Developer_Free(desarrollador: str):
    """Cantidad de items y porcentaje de contenido Gratis por año según empresa desarrolladora"""

    # Filtrar el DataFrame para obtener solo las filas donde 'developer' es el desarrollador de entrada
    df_filt1 = steam[(steam['developer'] == desarrollador)].copy()

    # Agrupe por 'release_date', cuente los valores únicos de 'item_id' y cuente la cantidad de valores de 'price' que son 0
    df_group1 = df_filt1.groupby('release_date').agg(
        {'developer': 'count', 'item_id': pd.Series.nunique, 'price': lambda x: (x == 0).sum()}).reset_index()

    # Calcular el porcentaje de contenido gratuito.
    df_group1['% contenido free'] = round(
        (df_group1['price']/df_group1['developer'])*100, 0)

    df_group1.rename(
        columns={'item_id': 'Cantidad de items', 'release_date': 'Año'}, inplace=True)

    # Elimine las columnas 'developer' y 'price'
    df_group1.drop('price', axis=1, inplace=True)
    df_group1.drop('developer', axis=1, inplace=True)

    result_dicc1 = {
        "Año": df_group1['Año'].to_dict(),
        "Cantidad de items": df_group1['Cantidad de items'].tolist(),
        "% contenido free": df_group1['% contenido free'].tolist()
    }

    return result_dicc1


@app.get('/User_Data/{user_id_}')
def User_Data(user_id_: str):
    """Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en
    base a reviews.recommend y cantidad de items"""

    df_filt1 = steam[steam['user_id'] == user_id_]

    df_group1 = df_filt1.agg({
        'price': 'sum',
        'recommend': 'sum',
        'user_id': 'count'
    }).rename(
        index={'user_id': 'cantidad de items', 'price': 'gasto total'})

    df_group1['% recomendacion'] = (
        (df_group1['recommend']/df_group1['cantidad de items'])*100)

    result_dicc1 = {
        'Usuario': user_id_,
        'Dinero Gastado': str(round(df_group1['gasto total'], 2)) + ' USD',
        '% de Recomendacion': str(round(df_group1['% recomendacion'], 0)) + ' %',
        'Cantidad de Items': df_group1['cantidad de items']
    }

    return result_dicc1


@app.get('/user_For_Genre/{genero}')
def User_For_Genre(genero: str):
    """Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la 
    acumulación de horas jugadas por año"""

    # Filtrar el DataFrame para el género especificado
    df_filt1 = steam[steam['genre'] == genero]

    # Agrupar por 'user_id' y sumar 'playtime_forever'
    df_group1 = df_filt1.groupby('user_id').agg(
        {'playtime_forever': 'sum'}).reset_index()

    # Ordenar por 'playtime_forever'
    df_sort1 = df_group1.sort_values('playtime_forever', ascending=False)

    # Filtrar el DataFrame original para el 'user_id' con el mayor 'playtime_forever'
    df_filt11 = steam[steam['user_id'] == df_sort1.iloc[0, 0]]

    # Agrupar por 'year_posted' y sumar 'playtime_forever'
    df_group11 = df_filt11.groupby('year_posted').agg(
        {'playtime_forever': 'sum'}).reset_index()

    df_group11 = df_group11.rename(
        columns={'year_posted': 'Año', 'playtime_forever': 'Horas'})

    # Convertir el resultado a un diccionario
    result_dicc1 = {
        'usuario con mas horas jugadas para el genero ' + genero: df_sort1.iloc[0, 0],
        'horas jugadas': df_group11.to_dict('records')
    }

    return result_dicc1


@app.get("/Best_Developer_Year/{año}")
def Best_Developer_Year(año: int):
    """Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado"""
    # Filtra el DataFrame 'steam' para obtener solo las filas correspondientes al año especificado.
    df_filtro1 = steam[steam["year_posted"] == año].copy()

    # Calcula la nueva columna "reviews.recommend" sumando las columnas "recommend" y "sentiment_analysis".
    df_filtro1["reviews.recommend"] = df_filtro1["recommend"] + df_filtro1["sentiment_analysis"]

    # Agrupa por desarrollador y suma las recomendaciones y análisis de sentimientos.
    df_group1 = df_filtro1.groupby("developer")["reviews.recommend"].sum().reset_index()

    # Ordena el DataFrame por la suma de recomendaciones y análisis de sentimientos de forma ascendente.
    df_sort1 = df_group1.sort_values("reviews.recommend", ascending=False)

    # Crea una lista de diccionarios con los tres desarrolladores con mejor calificación.
    result_list1 = [{"Puesto " + str(i + 1): df_sort1.iloc[i, 0]} for i in range(3)]

    return result_list1


@app.get("/Sentiment_Analysis/{desarrolladora}")
def Sentiment_Analysis(desarrolladora: str):
    """Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista 
    con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de 
    sentimiento como valor positivo o negativo"""
    # Filtra el DataFrame 'steam' para obtener solo las filas correspondientes a la desarrolladora especificada y con sentimientos válidos (0, 1, 2).
    df_filtro1 = steam[(steam["developer"] == desarrolladora) & steam["sentiment_analysis"].isin([0, 1, 2])]

    # Realiza un grupo por la desarrolladora y el análisis de sentimientos, contando el número de ocurrencias.
    df_group1 = df_filtro1.groupby(["developer", "sentiment_analysis"]).size().reset_index(name="count")

    # Crea un diccionario con la información del análisis de sentimientos para la desarrolladora especificada.
    result_dicc1 = {
        desarrolladora: [
            "Negativo = " + str(df_group1[df_group1["sentiment_analysis"] == 0]["count"].values[0]),
            "Neutral = " + str(df_group1[df_group1["sentiment_analysis"] == 1]["count"].values[0]),
            "Positivo = " + str(df_group1[df_group1["sentiment_analysis"] == 2]["count"].values[0])
        ]
    }

    return result_dicc1
