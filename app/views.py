import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


HF_URL = "https://router.huggingface.co/v1/chat/completions"


@api_view(["POST"])
def get_recipe(request):
    ingredients = request.data.get("ingredients", [])

    if not ingredients:
        return Response({"error": "No ingredients provided"}, status=400)

    prompt = f"""
You are an assistant that receives a list of ingredients that a user has and suggests a recipe they could make with some or all of those ingredients.

You don't need to use every ingredient they mention in your recipe.
The recipe can include additional ingredients they didn't mention, but try not to include too many extra ingredients.

Format your response in **Markdown** so it can be rendered on a web page.

Here are the ingredients the user has:
{', '.join(ingredients)}
"""


    headers = {
        "Authorization": f"Bearer {settings.HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 512,
}


    try:
        res = requests.post(HF_URL, headers=headers, json=payload)
        data = res.json()
        print("HF RESPONSE:", data)
        recipe = data["choices"][0]["message"]["content"]

        return Response({"recipe": recipe})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

