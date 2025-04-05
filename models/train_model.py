import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import joblib
from sklearn.model_selection import train_test_split
import numpy as np

movies = pd.read_csv(f"data/movie.csv")
ratings = pd.read_csv(f"data/rating.csv")

filtered_ratings = ratings[ratings['userId'].between(1, 20000)]

scaler = MinMaxScaler()
filtered_ratings.loc[:, 'rating'] = scaler.fit_transform(filtered_ratings[['rating']])

ratings_with_titles = filtered_ratings.merge(movies, on='movieId')

user_movie_matrix = ratings_with_titles.pivot_table(
    index='userId', columns='title', values='rating'
).fillna(0)

train_data, test_data = train_test_split(
    user_movie_matrix.values, test_size=0.2, random_state=42
)

knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(train_data)

joblib.dump(knn, f"models/knn_model.pkl")
user_movie_matrix.to_pickle(f"models/user_movie_matrix.pkl")
np.save(f"models/train_data.npy", train_data)
np.save(f"models/test_data.npy", test_data)
