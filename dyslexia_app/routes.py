from flask import render_template, jsonify, request
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from . import dyslexia_bp

load_dotenv()
client = MongoClient("mongodb://localhost:27017")
db = client["Dyslexia"]

# MongoDB collections
questions_collection = db["Assessment"]
patterns_collection = db["Pattern"]
users_collection = db["User"]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_suggestions(score):
    prompt = f"A user scored {score} on a dyslexia assessment. Provide three helpful suggestions."
    model = genai.GenerativeModel()
    response = model.generate_content(prompt)
    return response.text.strip().split("\n")[:3]

@dyslexia_bp.route('/dyslexia')
def dyslexia_home():
    return render_template('landing.html')

@dyslexia_bp.route('/get_suggestions', methods=['GET'])
def fetch_suggestions():
    score = int(request.args.get('score', 0))
    suggestions = get_suggestions(score)
    return jsonify({"suggestions": suggestions})

@dyslexia_bp.route('/registerapi', methods=["POST"])
def registerapi():
    data = request.json
    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "Email already registered"}), 400

    users_collection.insert_one(data)
    return jsonify({"message": "Registration successful"}), 201

@dyslexia_bp.route('/loginapi', methods=["POST"])
def loginapi():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})
    if not user or user["password"] != data["password"]:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "username": user["username"]}), 200


@dyslexia_bp.route('/activity')
def activity():
    return render_template('activity.html')

@dyslexia_bp.route('/assessment')
def assessment():
    return render_template('assessment.html')

@dyslexia_bp.route('/pattern')
def pattern():
    return render_template("pattern.html")

@dyslexia_bp.route('/reading')
def reading():
    return render_template('reading.html')


@dyslexia_bp.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@dyslexia_bp.route('/login')
def login():
    return render_template('login.html')