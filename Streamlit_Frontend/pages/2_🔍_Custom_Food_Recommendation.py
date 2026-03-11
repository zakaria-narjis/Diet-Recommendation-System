import pandas as pd
import streamlit as st
from Generate_Recommendations import Generator
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Custom Food Recommendation", page_icon="🔍", layout="wide")

NUTRITION_COLUMNS = [
    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
    'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
]

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'generated' not in st.session_state:
    st.session_state.generated = False


@st.cache_data(show_spinner=False, ttl=300)
def fetch_recommendations(nutrition_list: tuple, nb_recommendations: int, ingredient_txt: str):
    ingredients = [i.strip() for i in ingredient_txt.split(';') if i.strip()]
    params = {'n_neighbors': nb_recommendations, 'return_distance': False}
    generator = Generator(list(nutrition_list), ingredients, params)
    response = generator.generate()
    response.raise_for_status()
    return response.json()['output']


class Display:
    def display_recommendation(self, recommendations):
        st.subheader('Recommended recipes:')
        if recommendations is not None:
            rows = len(recommendations) // 5
            for column, row in zip(st.columns(5), range(5)):
                with column:
                    for recipe in recommendations[rows * row: rows * (row + 1)]:
                        recipe_name = recipe['Name']
                        expander = st.expander(recipe_name)
                        recipe_link = recipe['image_url']
                        nutritions_df = pd.DataFrame(
                            {value: [recipe[value]] for value in NUTRITION_COLUMNS}
                        )
                        expander.image(recipe_link, width=200)
                        expander.markdown(
                            '<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values (g):</h5>',
                            unsafe_allow_html=True,
                        )
                        expander.dataframe(nutritions_df)
                        expander.markdown(
                            '<h5 style="text-align: center;font-family:sans-serif;">Ingredients:</h5>',
                            unsafe_allow_html=True,
                        )
                        for ingredient in recipe['RecipeIngredientParts']:
                            expander.markdown(f"- {ingredient}")
                        expander.markdown(
                            '<h5 style="text-align: center;font-family:sans-serif;">Recipe Instructions:</h5>',
                            unsafe_allow_html=True,
                        )
                        for instruction in recipe['RecipeInstructions']:
                            expander.markdown(f"- {instruction}")
                        expander.markdown(
                            '<h5 style="text-align: center;font-family:sans-serif;">Cooking and Preparation Time:</h5>',
                            unsafe_allow_html=True,
                        )
                        expander.markdown(
                            f"- Cook Time: {recipe['CookTime']} min\n"
                            f"- Preparation Time: {recipe['PrepTime']} min\n"
                            f"- Total Time: {recipe['TotalTime']} min"
                        )
        else:
            st.info("Couldn't find any recipes with the specified ingredients", icon="🙁")

    def display_overview(self, recommendations):
        if recommendations is not None:
            st.subheader('Overview:')
            col1, col2, col3 = st.columns(3)
            with col2:
                selected_recipe_name = st.selectbox(
                    'Select a recipe', [recipe['Name'] for recipe in recommendations]
                )
            st.markdown(
                '<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>',
                unsafe_allow_html=True,
            )
            selected_recipe = next(r for r in recommendations if r['Name'] == selected_recipe_name)
            options = {
                "title": {
                    "text": "Nutrition values",
                    "subtext": selected_recipe_name,
                    "left": "center",
                },
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left"},
                "series": [{
                    "name": "Nutrition values",
                    "type": "pie",
                    "radius": "50%",
                    "data": [
                        {"value": selected_recipe[v], "name": v} for v in NUTRITION_COLUMNS
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }],
            }
            st_echarts(options=options, height="600px")
            st.caption('You can select/deselect an item (nutrition value) from the legend.')


display = Display()

title = "<h1 style='text-align: center;'>Custom Food Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)

with st.form("recommendation_form"):
    st.header('Nutritional values:')
    Calories = st.slider('Calories', 0, 2000, 500)
    FatContent = st.slider('FatContent', 0, 100, 50)
    SaturatedFatContent = st.slider('SaturatedFatContent', 0, 13, 0)
    CholesterolContent = st.slider('CholesterolContent', 0, 300, 0)
    SodiumContent = st.slider('SodiumContent', 0, 2300, 400)
    CarbohydrateContent = st.slider('CarbohydrateContent', 0, 325, 100)
    FiberContent = st.slider('FiberContent', 0, 50, 10)
    SugarContent = st.slider('SugarContent', 0, 40, 10)
    ProteinContent = st.slider('ProteinContent', 0, 40, 10)
    nutritions_values_list = [
        Calories, FatContent, SaturatedFatContent, CholesterolContent,
        SodiumContent, CarbohydrateContent, FiberContent, SugarContent, ProteinContent,
    ]
    st.header('Recommendation options (OPTIONAL):')
    nb_recommendations = st.slider('Number of recommendations', 5, 20, step=5)
    ingredient_txt = st.text_input(
        'Specify ingredients to include in the recommendations separated by ";" :',
        placeholder='Ingredient1;Ingredient2;...',
    )
    st.caption('Example: Milk;eggs;butter;chicken...')
    generated = st.form_submit_button("Generate")

if generated:
    with st.spinner('Generating recommendations...'):
        try:
            recommendations = fetch_recommendations(
                tuple(nutritions_values_list), nb_recommendations, ingredient_txt
            )
            st.session_state.recommendations = recommendations
            st.session_state.generated = True
        except Exception as e:
            st.error(f"Could not connect to the backend: {e}")

if st.session_state.generated:
    with st.container():
        display.display_recommendation(st.session_state.recommendations)
    with st.container():
        display.display_overview(st.session_state.recommendations)
