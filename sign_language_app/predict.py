import os
import re
import google.generativeai as genai

def remove_consecutive_duplicates(text):
    return re.sub(r'(.)\1+', r'\1', text)  # Replaces repeated characters with a single one

def predict_sentence(text):
    api_key = "AIzaSyC-AublNqOvjvJ5zMNj9gDKoEgagDwU85g"

    if not api_key:
        print("API key is missing.")
        return []

    client = genai.Client(api_key=api_key)

    try:
        # Remove consecutive duplicate characters
        cleaned_text = remove_consecutive_duplicates(text)

        # Split into words
        words = cleaned_text.split()

        # Form the task prompt
        task = "Using the following random words or alphabets, generate coherent sentences. Only use additional words if necessary to correct grammar or improve sentence structure. The output should consist of complete sentences, each beginning with an asterisk (*), with minimal extra words. Here are the words and alphabets: "  
        task += ", ".join(words)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=task,
        )

        # Print the generated response text
        generated_text = response.text.strip()

        # Extract sentences that start with an asterisk
        sentences = [sentence[4:].strip() for sentence in generated_text.split('\n') if sentence.strip().startswith('*')]

        return sentences

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'na'
