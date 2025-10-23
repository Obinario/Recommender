# Course Recommendation System

A Flask web application that integrates with the Hugging Face chatbot API to provide personalized course recommendations based on student academic performance and interests.

## Features

- **Course Recommendations**: Get personalized course recommendations based on:
  - Stanine Score (1-9)
  - Grade Weighted Average (GWA) (75-100)
  - Academic Strand (STEM, ABM, HUMSS, GAS, TVL)
  - Hobbies & Interests

- **Rating System**: Rate the provided recommendations to help improve the system
- **Available Courses**: View information about all available courses
- **Model Training**: Train the recommendation model with current data

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone or download this project** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # Main page with recommendation form
│   └── courses.html      # Available courses and model training page
└── static/               # Static files
    └── style.css         # Custom CSS styling
```

## API Endpoints

The application provides the following API endpoints:

### `/api/get_recommendations` (POST)
Get course recommendations based on user input.

**Request Body:**
```json
{
    "stanine": "7",
    "gwa": "85.5",
    "strand": "STEM",
    "hobbies": "Programming, Mathematics, Science"
}
```

**Response:**
```json
{
    "success": true,
    "recommendations": {
        "course1": "Computer Science",
        "course2": "Data Science",
        "course3": "Software Engineering",
        "rating1": "👍 Like",
        "rating2": "👍 Like",
        "rating3": "👎 Dislike"
    }
}
```

### `/api/submit_ratings` (POST)
Submit ratings for the three recommendations.

**Request Body:**
```json
{
    "course1_rating": "👍 Like",
    "course2_rating": "👍 Like",
    "course3_rating": "👎 Dislike"
}
```

### `/api/train_model` (POST)
Train the recommendation model with current data.

### `/api/get_courses` (GET)
Get information about available courses.

## Usage

1. **Get Recommendations**:
   - Fill out the form on the main page with your academic information
   - Click "Get Recommendations" to receive personalized course suggestions
   - Rate each recommendation using the Like/Dislike buttons
   - Submit your ratings to help improve the system

2. **View Available Courses**:
   - Navigate to the "Available Courses" page
   - Click "Load Available Courses" to see all available courses
   - Use "Train Model" to update the recommendation system

## Configuration

The application connects to the Hugging Face Space `markobinario/chatbot`. If you need to use a different model or private space, you can modify the client initialization in `app.py`:

```python
# For private spaces, you may need to pass your Hugging Face token
client = Client("markobinario/chatbot", hf_token="your_token_here")
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Make sure you have an active internet connection as the app connects to Hugging Face Spaces.

2. **Installation Issues**: Ensure you're using Python 3.7+ and all dependencies are installed correctly:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Port Already in Use**: If port 5000 is already in use, you can change it in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
   ```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
