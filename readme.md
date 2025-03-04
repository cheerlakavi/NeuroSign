## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/gesture_recognition.git . (some folder)
   cd (folder name)
   ```
2. **Create a virtual environment:**
   ```sh
   python3 -m venv neurosign
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up the API Key:**
   - Replace `api_key` in `predict_sentence` function with your Google Gemini API key.

## Running the Project

1. **Start the Flask server:**
   ```sh
   python app.py
   ```
2. **Open the application in your browser:**
   ```
   http://127.0.0.1:5000
   ```
