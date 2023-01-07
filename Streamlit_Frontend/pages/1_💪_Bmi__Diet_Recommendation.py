import streamlit as st


class Person:
    def __init__(self,age,height,weight,gender):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
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

st.set_page_config(page_title="Plotting Demo", page_icon="💪")


with st.container():
   st.write("Modify the values and click the Generate button to use")
   age = st.number_input('Age',min_value=2, max_value=120, step=1)
   height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
   weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
   gender = st.radio('Gender',('Male','Female'))
   person = Person(age,height,weight,gender)
   bmi_string,category = person.display_result()
   st.metric(label="Body Mass Index (BMI)", value=bmi_string)
   st.write(category)
   st.markdown(
    """
    - Healthy BMI range: 18.5 kg/m² - 25 kg/m²
    - Healthy weight for the height: 59.9 kg/m² - 81.0 kg/m²
    - Lose 19.0 kgs to reach a BMI of 25 kg/m².
    """
   ) 
