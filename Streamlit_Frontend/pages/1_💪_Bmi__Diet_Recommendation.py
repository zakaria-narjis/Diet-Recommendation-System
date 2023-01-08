import streamlit as st

st.set_page_config(page_title="Plotting Demo", page_icon="💪")

class Person:

    def __init__(self,age,height,weight,gender,activity):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity

    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
        elif 18.5<=bmi<25:
            category='Normal'
        elif 25<=bmi<30:
            category='Overweight'
        else:
            category='Obesity'    
        return bmi_string,category

    def calculate_bmr(self):
        if gender=='Male':
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

class Display:
    def __init__(self):
        pass

    def display_bmi(self,person):
        bmi_string,category = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        st.write(category)
        st.markdown(
            """
            - Healthy BMI range: 18.5 kg/m² - 25 kg/m²;
            - Healthy weight for the height: 59.9 kg/m² - 81.0 kg/m²;
            - Lose 19.0 kgs to reach a BMI of 25 kg/m².
            """)   

    def display_calories(self,person):
        maintain_calories=person.calories_calculator()
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.subheader("Maintain weight")
            st.write(f'{round(maintain_calories)} Calories/day')
        with col2:
            st.subheader("Mild weight loss")
            st.write(f'{round(maintain_calories*0.9)} Calories/day')
        with col3:
            st.subheader("Weight loss")
            st.write(f'{round(maintain_calories*0.8)} Calories/day')
        with col4:
            st.subheader("Extreme weight loss")
            st.write(f'{round(maintain_calories*0.6)} Calories/day')           

display=Display()

with st.container():
   st.write("Modify the values and click the Generate button to use")
   age = st.number_input('Age',min_value=2, max_value=120, step=1)
   height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
   weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
   gender = st.radio('Gender',('Male','Female'))
   activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
   'Extra active (very active & physical job)'])

if st.button("Generate"):
    person = Person(age,height,weight,gender,activity)
    with st.container():
        display.display_bmi(person)
        display.display_calories(person)

