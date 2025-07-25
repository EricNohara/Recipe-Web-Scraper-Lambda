RATING_DIV_ID = "mm-recipes-review-bar__rating_1-0"
RECIPE_DETAILS_CLASS = '.mm-recipes-details__item'
RECIPE_DETAILS_LABEL = '.mm-recipes-details__label'
RECIPE_DETAILS_VALUE = '.mm-recipes-details__value'
INGREDIENTS_LIST_CLASS = ".mm-recipes-structured-ingredients__list"
RECIPE_STEPS_ID = "mm-recipes-steps_1-0"
RECIPE_STEPS_TEXT = ".mntl-sc-block-html"
RECIPE_NAME_CLASS = ".article-heading"

def parse_recipe_data(soup):
    if not soup:
        return {}

    # Parse name
    name_header = soup.select_one(RECIPE_NAME_CLASS)
    name = name_header.text if name_header else None

    # Parse rating
    rating_div = soup.find(id=RATING_DIV_ID)
    rating = rating_div.text if rating_div else None

    # Parse total time + servings
    total_time = None
    servings = None
    for item in soup.select(RECIPE_DETAILS_CLASS):
        label = item.select_one(RECIPE_DETAILS_LABEL)
        value = item.select_one(RECIPE_DETAILS_VALUE)
        if not label or not value:
            continue
        label_text = label.get_text(strip=True).lower()
        if label_text == "total time:":
            total_time = value.get_text(strip=True)
        elif label_text == "servings:":
            servings = value.get_text(strip=True)

    # Parse ingredients
    ingredients = []
    for list in soup.select(INGREDIENTS_LIST_CLASS):
        all_ingredients = list.find_all("li")
        for ingredient in all_ingredients:
            if ingredient:
                ingredients.append(ingredient.text.strip())

    # Parse directions
    directions = []
    steps = soup.find(id=RECIPE_STEPS_ID)
    if steps:
        step_text = steps.select(RECIPE_STEPS_TEXT)
        for step in step_text:
            if step:
                directions.append(step.text.strip())

    # return the recipe
    return {
        "name": name,
        "total_time": total_time,
        "servings": servings,
        "rating": rating,
        "ingredients": ingredients,
        "directions": directions
    }