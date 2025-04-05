from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

def test_model(knn, train_data, test_data):
    predictions = []
    for test_user in test_data:
        _, indices = knn.kneighbors([test_user], n_neighbors=5)
        neighbors = train_data[indices[0]]
        prediction = np.mean(neighbors, axis=0)
        predictions.append(prediction)
    return np.array(predictions)

knn = joblib.load(f"models/knn_model.pkl")
train_data = np.load(f"models/train_data.npy")
test_data = np.load(f"models/test_data.npy")
predictions = test_model(knn, train_data, test_data)

mae = mean_absolute_error(test_data, predictions)
rmse = np.sqrt(mean_squared_error(test_data, predictions))

print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")
