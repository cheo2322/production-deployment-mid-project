from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Inicializar la app Flask
app = Flask(__name__)

# Cargar el modelo KNN y la matriz de usuario-película preprocesados
knn = joblib.load('./models/knn_model.pkl')  # Modelo KNN
user_movie_matrix = pd.read_pickle('./models/user_movie_matrix.pkl')  # Matriz de usuario-película

# Función para generar recomendaciones para un usuario
def get_user_recommendations(user_id, k_neighbors=5, top_n=20):
    # Validar si el usuario existe en la matriz de usuario-película
    if user_id not in user_movie_matrix.index:
        return []  # Si el usuario no existe, devolver una lista vacía

    # Obtener el vector del usuario
    user_vector = user_movie_matrix.loc[user_id].values.reshape(1, -1)

    # Encontrar usuarios similares (vecinos más cercanos)
    _, indices = knn.kneighbors(user_vector, n_neighbors=k_neighbors)

    # Generar recomendaciones basadas en los vecinos
    recommended_movies = []
    for neighbor_index in indices.flatten():
        similar_user_movies = user_movie_matrix.iloc[neighbor_index]
        top_movies = similar_user_movies[similar_user_movies > 0].sort_values(ascending=False).index.tolist()
        recommended_movies.extend(top_movies)

    # Filtrar películas ya vistas por el usuario
    user_movies = user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] > 0].index.tolist()
    recommended_movies = [movie for movie in recommended_movies if movie not in user_movies]

    # Limitar al número máximo de recomendaciones
    return recommended_movies[:top_n]

# Endpoint para obtener recomendaciones
@app.route('/recommendations/<int:user_id>', methods=['GET'])
def recommendations(user_id):
    try:
        # Obtener parámetros de la solicitud
        k_neighbors = int(request.args.get('k_neighbors', 5))  # Por defecto, 5 vecinos
        top_n = int(request.args.get('top_n', 20))  # Por defecto, 20 recomendaciones

        # Generar recomendaciones para el usuario
        recommended_titles = get_user_recommendations(user_id, k_neighbors=k_neighbors, top_n=top_n)

        # Responder con un JSON
        return jsonify({'recommendations': recommended_titles})
    except Exception as e:
        # Manejar errores y devolver un mensaje JSON
        return jsonify({'error': str(e)})

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)