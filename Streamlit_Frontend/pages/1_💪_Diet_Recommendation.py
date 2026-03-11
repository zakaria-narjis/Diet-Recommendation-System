import os

import pandas as pd
import requests
import streamlit as st
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪", layout="wide")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8080")

NUTRITION_COLUMNS = [
    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
    'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
]

if 'generated' not in st.session_state:
    st.session_state.generated = False
    st.session_state.meal_plan = None
    st.session_state.weight_loss_option = None


@st.cache_data(show_spinner=False, ttl=300)
def fetch_meal_plan(age, height, weight, gender, activity, number_of_meals, weight_loss):
    payload = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "activity": activity,
        "number_of_meals": number_of_meals,
        "weight_loss": weight_loss,
    }
    response = requests.post(url=f"{BACKEND_URL}/generate-meal-plan/", json=payload)
    response.raise_for_status()
    return response.json()


class Display:
    PLANS = ["Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"]
    WEIGHTS = [1, 0.9, 0.8, 0.6]
    LOSSES = ['-0 kg/week', '-0.25 kg/week', '-0.5 kg/week', '-1 kg/week']
    # (threshold, category, color) — evaluated in order; last entry is the fallback.
    BMI_CATEGORIES = [
        (18.5, 'Underweight', 'Red'),
        (25.0, 'Normal', 'Green'),
        (30.0, 'Overweight', 'Yellow'),
    ]

    def display_bmi(self, bmi):
        st.header('BMI CALCULATOR')
        category, color = 'Obesity', 'Red'
        for threshold, cat, col in self.BMI_CATEGORIES:
            if bmi < threshold:
                category, color = cat, col
                break
        st.metric(label="Body Mass Index (BMI)", value=f'{bmi} kg/m²')
        st.markdown(
            f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>',
            unsafe_allow_html=True,
        )
        st.markdown("Healthy BMI range: 18.5 kg/m² - 25 kg/m².")

    def display_calories(self, maintain_calories):
        st.header('CALORIES CALCULATOR')
        st.write(
            'The results show a number of daily calorie estimates that can be used as a guideline '
            'for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.'
        )
        for plan, weight, loss, col in zip(self.PLANS, self.WEIGHTS, self.LOSSES, st.columns(4)):
            with col:
                st.metric(
                    label=plan,
                    value=f'{round(maintain_calories * weight)} Calories/day',
                    delta=loss,
                    delta_color="inverse",
                )

    def display_recommendation(self, meal_plan):
        st.header('DIET RECOMMENDATOR')
        st.subheader('Recommended recipes:')
        meals = meal_plan['meals']
        for meal, column in zip(meals, st.columns(len(meals))):
            with column:
                st.markdown(f'##### {meal["meal_name"].upper()}')
                for recipe in meal['recipes']:
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

    def display_meal_choices(self, meal_plan, target_calories):
        meals = meal_plan['meals']
        st.subheader('Choose your meal composition:')
        choices = []
        for meal, col in zip(meals, st.columns(len(meals))):
            with col:
                choice = st.selectbox(
                    f'Choose your {meal["meal_name"]}:',
                    [recipe['Name'] for recipe in meal['recipes']],
                )
                choices.append((choice, meal['recipes']))

        total_nutrition_values = {v: 0 for v in NUTRITION_COLUMNS}
        for choice, recipes in choices:
            for recipe in recipes:
                if recipe['Name'] == choice:
                    for col in NUTRITION_COLUMNS:
                        total_nutrition_values[col] += recipe[col]

        total_calories_chose = total_nutrition_values['Calories']
        bar_color = "#FF3333" if total_calories_chose > target_calories else "#33FF8D"

        st.markdown(
            f'<h5 style="text-align: center;font-family:sans-serif;">'
            f'Total Calories in Recipes vs {st.session_state.weight_loss_option} Calories:</h5>',
            unsafe_allow_html=True,
        )
        total_calories_graph_options = {
            "xAxis": {
                "type": "category",
                "data": ['Total Calories you chose', f"{st.session_state.weight_loss_option} Calories"],
            },
            "yAxis": {"type": "value"},
            "series": [{
                "data": [
                    {"value": total_calories_chose, "itemStyle": {"color": bar_color}},
                    {"value": target_calories, "itemStyle": {"color": "#3339FF"}},
                ],
                "type": "bar",
            }],
        }
        st_echarts(options=total_calories_graph_options, height="400px")
        st.markdown(
            '<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>',
            unsafe_allow_html=True,
        )
        nutritions_graph_options = {
            "tooltip": {"trigger": "item"},
            "legend": {"top": "5%", "left": "center"},
            "series": [{
                "name": "Nutritional Values",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [
                    {"value": round(total_nutrition_values[v]), "name": v}
                    for v in total_nutrition_values
                ],
            }],
        }
        st_echarts(options=nutritions_graph_options, height="500px")


display = Display()

title = "<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)

with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age', min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)', min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)', min_value=10, max_value=300, step=1)
    gender = st.radio('Gender', ('Male', 'Female'))
    activity = st.select_slider(
        'Activity',
        options=[
            'Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)',
            'Very active (6-7 days/wk)', 'Extra active (very active & physical job)',
        ],
    )
    option = st.selectbox('Choose your weight loss plan:', display.PLANS)
    st.session_state.weight_loss_option = option
    number_of_meals = st.slider('Meals per day', min_value=3, max_value=5, step=1, value=3)
    generated = st.form_submit_button("Generate")

if generated:
    with st.status("Generating your meal plan...", expanded=True) as status:
        st.write("Calculating nutritional targets and finding matching recipes...")
        try:
            meal_plan = fetch_meal_plan(age, height, weight, gender, activity, number_of_meals, option)
            st.session_state.meal_plan = meal_plan
            st.session_state.generated = True
            status.update(label="Meal plan ready!", state="complete", expanded=False)
        except requests.RequestException as e:
            status.update(label="Failed to generate meal plan", state="error")
            st.error(f"Could not connect to the backend: {e}")

if st.session_state.generated and st.session_state.meal_plan:
    meal_plan = st.session_state.meal_plan
    with st.container():
        display.display_bmi(meal_plan['bmi'])
    with st.container():
        display.display_calories(meal_plan['maintain_calories'])
    with st.container():
        display.display_recommendation(meal_plan)
        st.success('Recommendation Generated Successfully!', icon="✅")
    with st.container():
        display.display_meal_choices(meal_plan, meal_plan['target_calories'])
