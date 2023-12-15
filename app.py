from flask import Flask, render_template, request
import functions

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    recipes = functions.get_recipe_data(query)
    nutrition_data = []

    if recipes:
        for recipe in recipes:
            total_nutrition = functions.get_recipe_nutrition(recipe)

            nutrition_data.append({
                'calories': total_nutrition['calories'],
                'total_fat': total_nutrition['total_fat'],
                'total_sugar': total_nutrition['total_sugar'],
                'protein': total_nutrition['protein'],
                'sodium': total_nutrition['sodium']
            })

        return render_template('results.html', recipes=recipes, nutrition_data=nutrition_data)
    else:
        return render_template('no_results.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)
