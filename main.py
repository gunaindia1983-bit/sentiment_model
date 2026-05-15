from flask import Flask, request, jsonify
import joblib
import os
import __main__
import pymongo
import random
from datetime import datetime
from flask_cors import CORS

# List of customer names for random selection
customer_names = [
    "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Ethan Hunt",
    "Fiona Gallagher", "George Miller", "Hannah Abbott", "Ian Wright", "Jane Doe",
    "Kevin Hart", "Laura Palmer", "Michael Scott", "Nina Simone", "Oscar Wilde"
]

# Define custom transformer for joblib loading compatibility
class DenseTransformer:
    def fit(self, X, y=None): return self
    def transform(self, X): return X.toarray()

setattr(__main__, 'DenseTransformer', DenseTransformer)

app = Flask(__name__)
CORS(app)
#CORS(app,origins=["http://localhost:5173/comments", "http://localhost:5173"])

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
sentiment = db['sentiment']

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    if model is None:
        return jsonify({"error": "Sentiment model not found"}), 500

    # Get current date/time
    current_date = datetime.now().isoformat()

    data = request.get_json()
    customer_name = random.choice(customer_names)
    # customer_name = data.get('customerName', 'Anonymous')
    food_id = data.get('foodId')
    food_name = data.get('food')
    comments = data.get('comments')
    category = data.get('category')

    try:
        prediction = model.predict([comments])[0]
        star_map = {"POSITIVE": 5, "NEUTRAL": 3, "NEGATIVE": 1}
        stars = int(star_map.get(prediction.upper(), 3))

        food_data = foods_collection.find_one({"name": food_name})
        price = float(food_data.get('price', 14.99)) if food_data else 14.99
        # category = str(food_data.get('category', 'Entre')) if food_data else 'Unknown'

        result= {
            "customer_name": str(customer_name),
            "foodId": str(food_id),
            "food": str(food_name),
            "newComment": comments,
            "sentiment_score_5": stars,
            "sentiment_label": str(prediction),
            "price": price,
            "date": current_date,
            "category": str(category)
            
        }

        output = sentiment.insert_one(result)
        
        return jsonify({
            "message": "Data loaded successfully",
            "inserted_id": str(output.inserted_id),
            "customerName": str(customer_name),
            "foodId": str(food_id),
            "foodName": str(food_name),
            "newCOmment": comments,
            "sentiment_score_5": stars,
            "sentiment_label": str(prediction),
            "price": price,
            "category": str(category),
            "date": current_date
            
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# from flask import Flask
# import os

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World"

# if __name__ == '__main__':
#     # Render assigns a port via the PORT environment variable
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

