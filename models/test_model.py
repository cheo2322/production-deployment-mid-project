from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

path = os.getenv('DATA_PATH')

def test_model(knn, train_data, test_data):
    predictions = []
    for test_user in test_data:
        _, indices = knn.kneighbors([test_user], n_neighbors=5)
        neighbors = train_data[indices[0]]
        prediction = np.mean(neighbors, axis=0)
        predictions.append(prediction)
    return np.array(predictions)

knn = joblib.load(f"{path}/models/knn_model.pkl")
train_data = np.load(f"{path}/models/train_data.npy")
test_data = np.load(f"{path}/models/test_data.npy")
predictions = test_model(knn, train_data, test_data)

mae = mean_absolute_error(test_data, predictions)
rmse = np.sqrt(mean_squared_error(test_data, predictions))

print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")

def precision_recall(predictions, test_data, threshold=0.5):
    precision = []
    recall = []
    for pred, true in zip(predictions, test_data):
        pred_binary = (pred >= threshold).astype(int)
        true_binary = (true >= threshold).astype(int)
        tp = np.sum(pred_binary * true_binary)
        fp = np.sum(pred_binary * (1 - true_binary))
        fn = np.sum((1 - pred_binary) * true_binary)
        precision.append(tp / (tp + fp) if (tp + fp) > 0 else 0)
        recall.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    return np.mean(precision), np.mean(recall)

precision, recall = precision_recall(predictions, test_data)

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
