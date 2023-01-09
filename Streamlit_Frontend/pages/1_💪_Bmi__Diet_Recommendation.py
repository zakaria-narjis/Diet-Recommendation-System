import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪",layout="wide")

class Person:

    def __init__(self,age,height,weight,gender,activity,meals_calories_perc,weight_loss):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.meals_calories_perc=meals_calories_perc
        self.weight_loss=weight_loss
    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories

    def generate_recommendations(self,):
        total_calories=self.weight_loss*self.calories_calculator()
        recommendations=[]
        for meal in self.meals_calories_perc:
            meal_calories=self.meals_calories_perc[meal]*total_calories
            if meal=='breakfast':        
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            elif meal=='launch':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
            elif meal=='dinner':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)] 
            else:
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            generator=Generator(recommended_nutrition)
            recommended_recipes=generator.generate().json()['output']
            recommendations.append(recommended_recipes)
        return recommendations

class Display:
    def __init__(self):
        self.plans=["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        self.weights=[1,0.9,0.8,0.6]
        self.losses=['','(0.25 kg/week)','(0.5 kg/week)','(1 kg/week)']
        pass

    def display_bmi(self,person):
        st.header('BMI CALCULATOR')
        bmi_string,category,color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """)   

    def display_calories(self,person):
        st.header('CALORIES CALCULATOR')        
        maintain_calories=person.calories_calculator()
        st.write('The results show a number of daily calorie estimates that can be used as a guideline for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.')
        for plan,weight,loss in zip(self.plans,self.weights,self.losses):
            st.write(f'{plan} :{round(maintain_calories*weight)} Calories/day {loss}')

    def display_recommendation(self,person):
        st.header('DIET RECOMMENDATOR')  
        with st.spinner('Generating recommendations...'): 
            meals=person.meals_calories_perc
            recommendations=person.generate_recommendations()
            columns=''
            for meal_name,recommendation in zip(meals,recommendations):
                #st.subheader(meal_name.upper())
                recipes=''
                # st.markdown(f'<div style="text-align: center;">{meal_name.upper()}</div>', unsafe_allow_html=True)     
                for recipe in recommendation:
                #     st.write(recipe['Name'])
                    recipe_name=recipe['Name']
                    recipe_img=f'<img src={find_image(recipe_name)} alt={recipe_name}>'
                    recipe=f'<div style="width: 100%; height: 80px;display:flex; align-items:center; justify-content:center;fontWeight: 600; color: #000000; text-align: center; background: #E0E0EF; border-radius: 8px;margin-bottom: 8px;" >{recipe_name}{recipe_img}</div>'
                    recipes+=recipe
                meal_text=f'<div style="width:33%";><div style="text-align:center;"><h2 style="font-weight:600;font-size:18px;color:#333;margin-bottom:16px;">{meal_name.upper()}</h2></div>{recipes}</div>'                    
                columns+=meal_text
            st.markdown(f'<div style="display:flex;justifyContent: space-between;gap:16px;">{columns}</div>', unsafe_allow_html=True)
                        
display=Display()

with st.container():
    title="<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
    st.markdown(title, unsafe_allow_html=True)
    #st.header('Automatic Diet Recommendation')
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age',min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
    'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:',display.plans)
    weight_loss=display.weights[display.plans.index(option)]
    number_of_meals=st.slider('Meals per day',min_value=3,max_value=5,step=1,value=3)
    if number_of_meals==3:
        meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}
    elif number_of_meals==4:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
    else:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}
    
if st.button("Generate"):
    person = Person(age,height,weight,gender,activity,meals_calories_perc,weight_loss)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.container():
        display.display_recommendation(person)
        # st.success('Recommendation Generated Successfully !', icon="✅")

