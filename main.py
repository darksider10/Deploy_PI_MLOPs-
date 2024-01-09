import pandas as pd
from fastapi import FastAPI
app = FastAPI()
steam = pd.read_csv("steam.csv")
@app.get("/playtime_genre/{genero}")
def PlayTimeGenre(genero: str):
    # Filtra el DataFrame 'steam' para obtener solo las filas con el género especificado.
    df_filtro1 = steam[steam["genre"] == genero]

    # Agrupa por año y suma las horas jugadas.
    df_group1 = df_filtro1.groupby("release_date").agg(
        {"playtime_forever": "sum"}).reset_index()

    # Ordena el DataFrame por horas jugadas de forma descendente.
    df_sort1 = df_group1.sort_values("playtime_forever", ascending=False)

    # Filtra el DataFrame original para obtener las filas correspondientes al año con más horas jugadas.
    df_filtro2 = steam[steam["release_date"] == df_sort1.iloc[0, 0]]

    # Agrupa por año y suma las horas jugadas nuevamente.
    df_group2 = df_filtro2.groupby("release_date").agg(
        {"playtime_forever": "sum"}).reset_index()

    # Renombra las columnas del segundo DataFrame para mayor claridad.
    df_group2 = df_group2.rename(
        columns={"release_date": "Año", "playtime_forever": "Horas"})

    # Crea un diccionario con la información resultante.
    result_dicc1 = {
        "año con mas horas jugadas para el genero " + genero: df_sort1.iloc[0, 0]
    }

    return result_dicc1

@app.get("/user_for_genre/{genero}")
def user_for_genre(genero: str):
    # Filtra el DataFrame 'steam' para obtener solo las filas con el género especificado.
    df_filtro1 = steam[steam["genre"] == genero]

    # Agrupa por usuario y suma las horas jugadas para obtener la cantidad total de horas jugadas por usuario.
    df_group1 = df_filtro1.groupby("user_id").agg(
        {"playtime_forever": "sum"}).reset_index()

    # Ordena el DataFrame por horas jugadas de forma descendente.
    df_sort1 = df_group1.sort_values("playtime_forever", ascending=False)

    # Filtra el DataFrame original para obtener las filas correspondientes al usuario con más horas jugadas.
    df_filtro2 = steam[steam["user_id"] == df_sort1.iloc[0, 0]]

    # Agrupa por año y suma las horas jugadas para obtener la distribución de horas jugadas por año para ese usuario.
    df_group2 = df_filtro2.groupby("year_posted").agg(
        {"playtime_forever": "sum"}).reset_index()

    # Renombra las columnas del segundo DataFrame para mayor claridad.
    df_group2 = df_group2.rename(
        columns={"year_posted": "Año", "playtime_forever": "Horas"})

    # Crea un diccionario con la información del usuario con más horas jugadas y la distribución de horas jugadas por año.
    result_dicc1 = {
        "usuario con mas horas jugadas para el genero " + genero: df_sort1.iloc[0, 0],
        "horas jugadas": df_group2.to_dict("records")
    }

    return result_dicc1

@app.get("/worst_developer_year/{anio}")
def worst_developer_year(anio: int):
    # Filtra el DataFrame 'steam' para obtener solo las filas correspondientes al año especificado.
    df_filtro1 = steam[steam["year_posted"] == año].copy()

    # Calcula la nueva columna "reviews.recommend" sumando las columnas "recommend" y "sentiment_analysis".
    df_filtro1["reviews.recommend"] = df_filtro1["recommend"] + df_filtro1["sentiment_analysis"]

    # Agrupa por desarrollador y suma las recomendaciones y análisis de sentimientos.
    df_group1 = df_filtro1.groupby("developer")["reviews.recommend"].sum().reset_index()

    # Ordena el DataFrame por la suma de recomendaciones y análisis de sentimientos de forma ascendente.
    df_sort1 = df_group1.sort_values("reviews.recommend", ascending=True)

    # Crea una lista de diccionarios con los tres desarrolladores con peor calificación.
    result_list1 = [{"Puesto " + str(i + 1): df_sort1.iloc[i, 0]} for i in range(3)]

    return result_list1


@app.get("/SentimentAnalysis/{desarrolladora}")
def SentimentAnalysis(desarrolladora: str):
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


@app.get("/User_Recommend/{anio}")
def User_Recommend(anio: int):
    # Filtra el DataFrame 'steam' para obtener solo las filas correspondientes al año especificado.
    df_filtro1 = steam[steam["year_posted"] == año].copy()

    # Calcula la nueva columna "reviews.recommend" sumando las columnas "recommend" y "sentiment_analysis".
    df_filtro1["reviews.recommend"] = df_filtro1["recommend"] + df_filtro1["sentiment_analysis"]

    # Agrupa por título y suma las recomendaciones y análisis de sentimientos.
    df_group1 = df_filtro1.groupby("title")["reviews.recommend"].sum().reset_index()

    # Ordena el DataFrame por la suma de recomendaciones y análisis de sentimientos de forma descendente.
    df_sort1 = df_group1.sort_values("reviews.recommend", ascending=False)

    # Crea una lista de diccionarios con los tres juegos con la mayor cantidad de recomendaciones y análisis de sentimientos.
    result_list1 = [{"Puesto " + str(i + 1): df_sort1.iloc[i, 0]} for i in range(3)]

    return result_list1
