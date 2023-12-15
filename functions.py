import urllib.parse, urllib.request, urllib.error, json
import pprint

api_key = "7e3xxc6au+loQLEqfw6vpg==fRlupYA9MlQkIyEs"
recipe_baseurl = "https://api.api-ninjas.com/v1/recipe?query="
nutrition_baseurl = "https://api.api-ninjas.com/v1/nutrition?query="

def format_query(query):
    return query.strip().replace(" ", "+").replace("\t", "").replace("\n", "")

def get_recipe_data(query):
    formatted_query = format_query(query)
    endpoint = recipe_baseurl + formatted_query
    request = urllib.request.Request(endpoint, headers={'X-Api-Key': api_key})
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read())
        return data
    except urllib.error.URLError as e:
       print("Error code: {}".format(e.code))


def get_nutrition_data(query):
    formatted_query = format_query(query)
    endpoint = nutrition_baseurl + formatted_query
    request = urllib.request.Request(endpoint, headers={'X-Api-Key': api_key})
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read())
        return data
    except urllib.error.URLError as e:
       print("Error code: {}".format(e.code))


def get_recipe_nutrition(recipe):
    total_nutrition = {
        "calories": 0,
        "total_fat": 0,
        "total_sugar": 0,
        "protein": 0,
        "sodium": 0
    }

    ingredients = recipe["ingredients"]
    ingredients_list = ingredients.split("|")
    for ingredient in ingredients_list:
        nutrition_info = get_nutrition_data(ingredient)
        if nutrition_info and len(nutrition_info) > 0:
            total_nutrition["calories"] += nutrition_info[0]["calories"]
            total_nutrition["total_fat"] += nutrition_info[0]["fat_total_g"]
            total_nutrition["total_sugar"] += nutrition_info[0]["sugar_g"]
            total_nutrition["protein"] += nutrition_info[0]["protein_g"]
            total_nutrition["sodium"] += nutrition_info[0]["sodium_mg"]

    servings = recipe["servings"].split()
    serving_size = next((int(word) for word in servings if word.isdigit()), 1)

    for category in total_nutrition.keys():
        total_nutrition[category] = round(total_nutrition[category] / serving_size)

    return total_nutrition