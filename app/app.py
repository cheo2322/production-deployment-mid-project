from flask import Flask, request, jsonify
import joblib
import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

def create_app():
    app = Flask(__name__)

    knn = joblib.load(f"models/knn_model.pkl")
    user_movie_matrix = pd.read_pickle(f"models/user_movie_matrix.pkl")

    def get_user_recommendations(user_id, k_neighbors=5, top_n=20):
        if user_id not in user_movie_matrix.index:
            return []

        user_vector = user_movie_matrix.loc[user_id].values.reshape(1, -1)
        _, indices = knn.kneighbors(user_vector, n_neighbors=k_neighbors)

        recommended_movies = []
        for neighbor_index in indices.flatten():
            similar_user_movies = user_movie_matrix.iloc[neighbor_index]
            top_movies = similar_user_movies[similar_user_movies > 0].sort_values(ascending=False).index.tolist()
            recommended_movies.extend(top_movies)

        user_movies = user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] > 0].index.tolist()
        recommended_movies = [movie for movie in recommended_movies if movie not in user_movies]

        return recommended_movies[:top_n]

    @app.route('/recommendations/<int:user_id>', methods=['GET'])
    def recommendations(user_id):
        try:
            k_neighbors = int(request.args.get('k_neighbors', 5))
            top_n = int(request.args.get('top_n', 20))

            recommended_titles = get_user_recommendations(user_id, k_neighbors=k_neighbors, top_n=top_n)

            return jsonify({'recommendations': recommended_titles})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    @app.route('/recommendations/random', methods=['GET'])
    def random_recommendations():
        try:
            random_user_id = user_movie_matrix.sample(1).index[0]
            k_neighbors = int(request.args.get('k_neighbors', 5))
            top_n = int(request.args.get('top_n', 20))

            recommended_titles = get_user_recommendations(random_user_id, k_neighbors=k_neighbors, top_n=top_n)

            return jsonify({'user_id': str(random_user_id), 'recommendations': recommended_titles})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    @app.route('/recommendations', methods=['POST'])
    def recommendations_post():
        try:
            data = request.get_json()

            # Here the input data should be added to database

            message = f"{data.get('userId')}, {data.get('movieId')}, {data.get('rating')}"
            producer.send('recommendations', value=message)
            
            return jsonify({"status": "Message sent", "message": message}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
