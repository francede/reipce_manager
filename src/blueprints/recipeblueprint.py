from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.DBC.recipeManagerDBC import RecipeManagerDBC
from src.DBC.authenticationDBC import AuthenticationDBC

from src.model.recipeschema import InsertRecipeSchema, UpdateRecipeSchema


recipe_blueprint = Blueprint("recipe_endpoints", __name__)
dbc = RecipeManagerDBC.get_instance()
a_dbc = AuthenticationDBC.get_instance()

insert_recipe_schema = InsertRecipeSchema()
update_recipe_schema = UpdateRecipeSchema()


@recipe_blueprint.route("/recipes", methods=["GET"])
def get_recipes():
    return json.dumps(dbc.select_recipes()), 200


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = dbc.select_recipe(recipe_id)
    if recipe is None:
        return json.dumps({"message": "Recipe not found"}), 404
    recipe["recipe_tags"] = dbc.select_tags_by_recipe_id(recipe_id)
    recipe["recipe_steps"] = dbc.select_steps_by_recipe_id(recipe_id)
    return json.dumps(recipe), 200


@recipe_blueprint.route("/recipe", methods=["POST"])
def add_recipe():
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    if role is None:
        return json.dumps({"message": "unauthorized"}), 401

    try:
        data = insert_recipe_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_recipe_id = dbc.insert_recipe(data, 1)

    if "recipe_tags" in data:
        for tag_name in data["recipe_tags"]:
            dbc.insert_ignore_tag(tag_name)
            dbc.insert_tag_to_recipe(inserted_recipe_id, tag_name)

    if "recipe_steps" in data:
        dbc.insert_steps(inserted_recipe_id, data["recipe_steps"])

    return json.dumps({"message": "insertion successful", "recipe_id": inserted_recipe_id}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.recipe_exists(recipe_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401

    try:
        data = update_recipe_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    tags = data.pop("recipe_tags", None)
    steps = data.pop("recipe_steps", None)

    updated_row_count = dbc.update_recipe(recipe_id, data)

    if tags is not None:
        dbc.delete_tags_from_recipe(recipe_id)
        for tag_name in tags:
            dbc.insert_ignore_tag(tag_name)
            dbc.insert_tag_to_recipe(recipe_id, tag_name)

    if steps is not None:
        dbc.delete_steps(recipe_id)
        dbc.insert_steps(recipe_id, steps)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.recipe_exists(recipe_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401

    return json.dumps({"message": f"deleted {dbc.delete_recipe(recipe_id)} row(s)"}), 200

