import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import joblib

# Cargar datos
movies = pd.read_csv('./data/movie.csv')  # Dataset de películas
ratings = pd.read_csv('./data/rating.csv')  # Dataset de calificaciones

# Preprocesar géneros de las películas (One-Hot Encoding)
movies['genres'] = movies['genres'].str.split('|')  # Separar géneros por '|'
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(movies['genres'])
genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)

# Normalizar características numéricas (año de lanzamiento)
movies['year'] = movies['title'].str.extract(r'\((\d{4})\)')[0].astype(float)  # Extraer año
scaler = StandardScaler()
numeric_features = scaler.fit_transform(movies[['year']].fillna(0))

# Crear la matriz de características combinada
movies_features = pd.concat([genres_df, pd.DataFrame(numeric_features, columns=['year'])], axis=1)

# Entrenar el modelo KNN
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(movies_features.values)

# Agrupar las calificaciones por 'movieId' para optimizar la columna 'user_ratings'
ratings_grouped = ratings.groupby('movieId').apply(
    lambda x: x[['userId', 'rating']].values.tolist()
).reset_index(name='user_ratings')

# Unir las calificaciones agrupadas con el DataFrame de películas
movies = movies.merge(ratings_grouped, on='movieId', how='left')

# Incluir las características preprocesadas dentro del DataFrame de películas
movies['features'] = movies_features.values.tolist()

# Guardar el modelo y los datos en archivos .pkl
joblib.dump(knn, './models/content_knn_model.pkl')  # Guardar el modelo KNN
movies.to_pickle('./models/movies_complete.pkl')  # Guardar el DataFrame de películas completo

print("Modelo KNN y datos procesados guardados correctamente.")