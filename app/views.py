from google import genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


@api_view(["POST"])
def get_recipe(request):
    ingredients = request.data.get("ingredients", [])

    if not ingredients or not isinstance(ingredients, list):
        return Response({"error": "Invalid ingredients"}, status=400)

    prompt = f"Suggest a recipe using: {', '.join(ingredients)}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return Response({"recipe": response.text})

    except Exception as e:
        print("ERROR:", e)
        return Response({"error": str(e)}, status=500)



