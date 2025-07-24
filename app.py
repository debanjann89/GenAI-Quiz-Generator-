import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import get_quiz_prompt # Import the prompt function

# Load environment variables
load_dotenv()

# Configure the Flask app
app = Flask(__name__)

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except AttributeError:
    print("Error: Gemini API Key not found. Please check your .env file.")
    exit()


# --- ROUTES ---

@app.route('/')
def index():
    # This will serve the main HTML page
    return render_template('index.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        source_text = data.get('source_text')
        num_questions = data.get('num_questions', 5) # Default to 5 questions
        difficulty = data.get('difficulty', 'High School') # Default difficulty

        if not source_text:
            return jsonify({"error": "Source text is required."}), 400

        # Get the formatted prompt
        prompt = get_quiz_prompt(source_text, num_questions, difficulty)

        # Generate content
        response = model.generate_content(prompt)

        # Clean up the response and parse it as JSON
        # The model sometimes wraps the JSON in ```json ... ```
        clean_response = response.text.strip().replace('```json', '').replace('```', '')
        quiz_data = json.loads(clean_response)

        return jsonify(quiz_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate quiz. The AI might be busy or the input was invalid."}), 500

# --- Main execution ---
if __name__ == '__main__':
    app.run(debug=True)