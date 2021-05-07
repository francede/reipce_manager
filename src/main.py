from flask import Flask
from src.DBC.recipeManagerDBC import RecipeManagerDBC

from src.blueprints.recipeblueprint import recipe_blueprint
from src.blueprints.bookblueprint import book_blueprint
from src.blueprints.tagblueprint import tag_blueprint


app = Flask(__name__)
app.register_blueprint(recipe_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(tag_blueprint)


@app.after_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
