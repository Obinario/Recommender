from flask import Flask, render_template, request, jsonify, redirect, url_for
from gradio_client import Client
import os

app = Flask(__name__)

# Initialize the Gradio client
client = Client("markobinario/chatbot")

@app.route('/')
def index():
    """Main page with course recommendation form"""
    return render_template('index.html')

@app.route('/recommendations')
def recommendations():
    """Page to display course recommendations"""
    return render_template('recommendations.html')

@app.route('/courses')
def courses():
    """Page to view available courses"""
    return render_template('courses.html')

@app.route('/api/get_recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get course recommendations"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['stanine', 'gwa', 'strand', 'hobbies']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate stanine score (1-9)
        try:
            stanine = int(data['stanine'])
            if stanine < 1 or stanine > 9:
                return jsonify({'error': 'Stanine score must be between 1 and 9'}), 400
        except ValueError:
            return jsonify({'error': 'Stanine score must be a valid number'}), 400
        
        # Validate GWA (75-100)
        try:
            gwa = float(data['gwa'])
            if gwa < 75 or gwa > 100:
                return jsonify({'error': 'GWA must be between 75 and 100'}), 400
        except ValueError:
            return jsonify({'error': 'GWA must be a valid number'}), 400
        
        # Validate strand
        valid_strands = ['STEM', 'ABM', 'HUMSS', 'GAS', 'TVL']
        if data['strand'] not in valid_strands:
            return jsonify({'error': f'Invalid strand. Must be one of: {", ".join(valid_strands)}'}), 400
        
        # Call the Hugging Face API
        result = client.predict(
            stanine=str(data['stanine']),
            gwa=str(data['gwa']),
            strand=data['strand'],
            hobbies=data['hobbies'],
            api_name="/get_course_recommendations"
        )
        
        # Parse the result
        recommendations = {
            'course1': result[0],
            'course2': result[1],
            'course3': result[2],
            'rating1': result[3],
            'rating2': result[4],
            'rating3': result[5]
        }
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500

@app.route('/api/submit_ratings', methods=['POST'])
def submit_ratings():
    """API endpoint to submit ratings for recommendations"""
    try:
        data = request.get_json()
        print(f"Received ratings data: {data}")  # Debug log
        
        # Validate required fields
        required_fields = ['course1_rating', 'course2_rating', 'course3_rating']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate rating values
        valid_ratings = ['👍 Like', '👎 Dislike']
        for field in required_fields:
            if data[field] not in valid_ratings:
                return jsonify({'error': f'Invalid rating for {field}. Must be "👍 Like" or "👎 Dislike"'}), 400
        
        print(f"Calling Gradio API with: course1_rating={data['course1_rating']}, course2_rating={data['course2_rating']}, course3_rating={data['course3_rating']}")  # Debug log
        
        # Call the Hugging Face API
        result = client.predict(
            course1_rating=data['course1_rating'],
            course2_rating=data['course2_rating'],
            course3_rating=data['course3_rating'],
            api_name="/submit_all_ratings"
        )
        
        print(f"Gradio API result: {result}")  # Debug log
        
        return jsonify({
            'success': True,
            'feedback': result
        })
        
    except Exception as e:
        print(f"Error in submit_ratings: {str(e)}")  # Debug log
        return jsonify({'error': f'Failed to submit ratings: {str(e)}'}), 500

@app.route('/api/train_model', methods=['POST'])
def train_model():
    """API endpoint to train the model"""
    try:
        result = client.predict(api_name="/train_model")
        
        return jsonify({
            'success': True,
            'status': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to train model: {str(e)}'}), 500

@app.route('/api/get_courses', methods=['GET'])
def get_courses():
    """API endpoint to get available courses information"""
    try:
        result = client.predict(api_name="/get_available_courses_info")
        
        return jsonify({
            'success': True,
            'courses': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get courses: {str(e)}'}), 500

@app.route('/api/test_connection', methods=['GET'])
def test_connection():
    """Test endpoint to verify Gradio client connection"""
    try:
        # Test with a simple API call
        result = client.predict(api_name="/get_available_courses_info")
        return jsonify({
            'success': True,
            'message': 'Connection to Gradio API successful',
            'test_result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Connection test failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
