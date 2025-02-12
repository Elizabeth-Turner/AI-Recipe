import os
from openai import AzureOpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)
    
client = AzureOpenAI(
    api_version=API_VERSION,
    api_key=API_KEY,
    azure_endpoint=AZURE_ENDPOINT
)

def getPicture(recipe):
    try:
        result = client.images.generate(
            model="dall-e-2",
            prompt=f"Picture of {recipe} that is aesthetically pleasing",
            n=1
        )
        url = result.data[0].url
        return url
    except Exception as e:
        return None

def getRecipeTitle(recipe):
    match = re.search(r'<h1>(.*?)</h1>', recipe)
    if match:
        recipeTitle = match.group(1)
        return recipeTitle

@app.route('/api/recipe', methods=['POST'])
def getRecipe():
    data = request.json
    ingredients = data.get('ingredients')
    restrictions = data.get('restrictions')
    servings = data.get('servings')
    type = data.get('type')
    
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "Generate an HTML code for a recipe that includes the desired ingredients and considers dietary restrictions. The response should only include the HTML. The response should not include a head, the word html, or `."
            },
            {
                "role": "user",
                "content": f"Create a recipe using the ingredients {ingredients}."
                    f"The dietary restrictions I have are {restrictions}"
                    f"I want the food to be {type}"
                    f"I want the recipe to make enough for {servings} servings"
                    f"Please provide a title, description, ingredients, and instructions.\n"
                    f"Format the ingredients and instructions as follows: Ingredients should be bulleted, and instructions should be numbered."
            }
        ],
        "temperature": 0.1,
        "top_p": 0.1,
        "max_tokens": 1000
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": "eba097990b844f1ab8dceb36025d74a3",
    }

    ENDPOINT = "https://genai-training-october2024.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview" 

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        return None

    recipe = response.json().get('choices', [{}])[0].get('message', {}).get('content')

    recipeTitle = getRecipeTitle(recipe)

    picture = getPicture(recipeTitle)

    return jsonify({"recipe": recipe, "image": picture})

if __name__ == '__main__':
    app.run(port=5000)