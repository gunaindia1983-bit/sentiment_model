# Sentiment Analysis Web Application

A Flask web application that utilizes machine learning for sentiment analysis. This application provides REST API endpoints to classify text sentiment using scikit-learn's trained models.

## 📋 Features

- **Sentiment Classification**: Analyze text and classify it as positive, negative, or neutral sentiment
- **REST API**: Easy-to-use HTTP endpoints for sentiment analysis
- **MongoDB Integration**: Store and retrieve sentiment analysis results
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
- **Production Ready**: Deployed with Gunicorn WSGI server
- **Scalable**: Built with scikit-learn for efficient ML inference

## 🛠️ Technology Stack

- **Framework**: Flask 3.0.0
- **ML Library**: scikit-learn
- **Server**: Gunicorn 21.2.0
- **Database**: MongoDB
- **Data Processing**: Pandas, NumPy
- **Model Serialization**: joblib
- **CORS**: Flask-CORS

## 📦 Requirements

- Python 3.7 or higher
- MongoDB (for data persistence)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gunaindia1983-bit/sentiment_model.git
   cd sentiment_model
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB connection**
   - Ensure MongoDB is running on your system
   - Update the MongoDB connection string in your configuration (if needed)

## 💻 Usage

### Running the Application

**Development Server:**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

**Production Deployment:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### API Documentation

The application provides REST API endpoints for sentiment analysis:

#### Analyze Sentiment
- **Endpoint**: `POST /api/sentiment/analyze`
- **Request Body**:
  ```json
  {
    "text": "I love this product, it's amazing!"
  }
  ```
- **Response**:
  ```json
  {
    "text": "I love this product, it's amazing!",
    "sentiment": "positive",
    "confidence": 0.95,
    "timestamp": "2024-05-20T10:30:00Z"
  }
  ```

#### Get Analysis History
- **Endpoint**: `GET /api/sentiment/history`
- **Response**: List of previously analyzed texts with their sentiments

## 📁 Project Structure

```
sentiment_model/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── models/               # Trained ML models (joblib files)
├── config.py            # Configuration settings
├── routes/              # API route definitions
├── utils/               # Utility functions
├── static/              # CSS, JavaScript files
├── templates/           # HTML templates
└── README.md            # This file
```

## 🔄 Workflow

1. User sends text to the API endpoint
2. Flask receives and validates the request
3. scikit-learn model processes the text
4. Sentiment prediction is generated
5. Result is stored in MongoDB
6. Response is returned to the user

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Requirements Details

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Gunicorn | 21.2.0 | WSGI HTTP Server |
| joblib | Latest | Model serialization and loading |
| pymongo | Latest | MongoDB client |
| scikit-learn | Latest | Machine Learning library |
| pandas | Latest | Data manipulation and analysis |
| numpy | Latest | Numerical computing |
| flask-cors | Latest | CORS handling |

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository or contact the maintainers.

---

**Happy Sentiment Analysis! 🎉**
