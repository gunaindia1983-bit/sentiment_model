from flask import Flask, request, jsonify
import joblib
import os
import __main__
import pymongo

# Define custom transformer for joblib loading compatibility
class DenseTransformer:
    def fit(self, X, y=None): return self
    def transform(self, X): return X.toarray()

setattr(__main__, 'DenseTransformer', DenseTransformer)

app = Flask(__name__)

# Setup the model loading
# NOTE: For Render, ensure you upload the .pkl file to your repo or use an external link/storage
model_path = 'sklearn_sentiment_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Setup MongoDB Connection (Best practice: use environment variables)
mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://reactapp:12345@cluster0.vzwkwrj.mongodb.net/?appName=Cluster0')
client = pymongo.MongoClient(mongo_uri)
db = client['food-delivery-app']
foods_collection = db['foods']

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    if model is None:
        return jsonify({"error": "Sentiment model not found"}), 500

    data = request.get_json()
    customer_name = data.get('customerName', 'Anonymous')
    food_id = data.get('foodId')
    food_name = data.get('food')
    comments = data.get('comments')

    try:
        prediction = model.predict([comments])[0]
        star_map = {"POSITIVE": 5, "NEUTRAL": 3, "NEGATIVE": 1}
        stars = int(star_map.get(prediction.upper(), 3))

        food_data = foods_collection.find_one({"name": food_name})
        price = float(food_data.get('price', 14.99)) if food_data else 14.99
        category = str(food_data.get('category', 'Entre')) if food_data else 'Unknown'

        return jsonify({
            "customerName": str(customer_name),
            "foodId": str(food_id),
            "foodName": str(food_name),
            "sentiment_label": str(prediction),
            "star_rating": stars,
            "price": price,
            "category": category
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='https://sentiment-model-cl77.onrender.com', port=int(os.environ.get('PORT', 5000)))
