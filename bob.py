# Import the 'client' module from the 'http' library
from http import client
# Import the 'os' module to interact with the operating system (like reading environment variables)
import os
# Import the 'load_dotenv' function to read environment variables from a .env file
from dotenv import load_dotenv
# Import the 'genai' module from Google to use the Gemini AI API
from google import genai
# Import Flask components: Flask (main app), request (to handle HTTP requests), jsonify (to convert to JSON), render_template (to render HTML files)
from flask import Flask, request, jsonify, render_template
# Import CORS to allow cross-origin requests (requests from your website to this server)
from flask_cors import CORS
# Import the 'behavior' variable from the 'ex.py' file in the same directory
from ex import behavior
# Load environment variables from the .env file into the system
load_dotenv()

# Create a Flask application instance that will handle web requests
app = Flask(__name__)
# Enable CORS so that requests from your website can reach this server
# Enable CORS so that requests from your website can reach this server
CORS(app)  # Allow requests from your website

# Get the Gemini API key from the environment variables (stored in .env file)
API_KEY = os.getenv("GEMINI_API_KEY")
# Create a Gemini API client using the API key
client = genai.Client(api_key=API_KEY)

# This line is commented out - it was previously used to create a GenerativeModel directly
# model = genai.GenerativeModel("gemini-2.5-flash")

# Store the behavior prompt from the ex.py file (this defines how the AI should behave)
behavior_prompt = behavior

# Create a chat session with the Gemini 2.5 Flash model (this will handle our conversations)
chat_session = client.chats.create(
    model = "gemini-2.5-flash"
)

# Define a route for the root URL "/" - when users visit the home page
@app.route("/")
# Define a function that handles requests to the home page
def home():
    # Return the index.html page to the user's browser
    return render_template("index.html")

# Define a route for "/chat" that accepts POST requests (requests that send data to the server)
@app.route("/chat", methods=["POST"])
# Define a function that handles chat requests
def chat():
     # Start a try-except block to handle errors gracefully
     try:
        # Get the JSON data sent by the user from the request body
        data = request.get_json(force=True)
        # Extract the "message" field from the data (the user's input)
        user_message = data.get("message", "")

        # Create a prompt by combining the behavior prompt, the user's message, and "Bob:" as a prefix for the AI response
        prompt = f"{behavior_prompt}\nUser: {user_message}\nBob:"
        # Send the prompt to the chat session and get the AI's response
        response = chat_session.send_message(prompt)
        # Clean up the response text by replacing asterisks and hashtags with double line breaks for better formatting
        cleaned_text =  response.text
        # Return the cleaned response as JSON to the user
        #response.text = response.text.replace("*", "\n\n").replace("#", "\n")
        return jsonify({"reply": cleaned_text})
     # If an error occurs, catch it and return an error message as JSON
     except Exception as e:
         return jsonify({"error": str(e)})
    
# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
     # Start the Flask development server with debug mode enabled (auto-reloads on code changes)
     app.run(debug=True)