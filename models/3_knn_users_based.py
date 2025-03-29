import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import joblib

# Cargar los datos
movies = pd.read_csv('./data/movie.csv')
ratings = pd.read_csv('./data/rating.csv')

# Filtrar usuarios con ID entre 1 y 1000
filtered_ratings = ratings[ratings['userId'].between(1, 20000)]

scaler = MinMaxScaler()

# Aplicar normalización a los datos filtrados
filtered_ratings['rating'] = scaler.fit_transform(filtered_ratings[['rating']])

# Verificar el resultado
filtered_ratings.head()

# Unir los datos con el archivo movies para obtener los títulos
ratings_with_titles = filtered_ratings.merge(movies, on='movieId')

# Crear matriz de usuario-película con títulos
user_movie_matrix = ratings_with_titles.pivot_table(
    index='userId', columns='title', values='rating'
).fillna(0)

# Entrenar el modelo KNN
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(user_movie_matrix.values)

joblib.dump(knn, './models/knn_model.pkl')
user_movie_matrix.to_pickle('./models/user_movie_matrix.pkl')
