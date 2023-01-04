import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

import time

def scaling(dataframe):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    return extracted_data

# def extract_nutritional_filtered_data(dataframe,max_nutritional_values):
#     extracted_data=dataframe.copy()
#     for column,maximum in zip(extracted_data.columns[6:15],max_nutritional_values):
#         extracted_data=extracted_data[extracted_data[column]<maximum]
#     return extracted_data
    
def extract_ingredient_filtered_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    _input=np.array(_input).reshape(1,-1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommend(dataframe,_input,ingredients=[],params={'return_distance':False}):
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]!=0:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
        else:
            return None

def get_total_minutes(time_string):
    # Use a regular expression to extract the number of hours and minutes
    hours_match = re.search(r'(\d+)H', time_string)
    minutes_match = re.search(r'(\d+)M', time_string)
    
    # If the regular expression didn't find any matches, set the values to 0
    hours = 0
    minutes = 0
    
    # If the regular expression found a match for hours, extract the value
    if hours_match:
        hours = int(hours_match.group(1))
    
    # If the regular expression found a match for minutes, extract the value
    if minutes_match:
        minutes = int(minutes_match.group(1))
    
    # Return the total number of minutes
    return str(hours * 60 + minutes)

def extract_quoted_strings(s):
    # Find all the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # Join the strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    if dataframe is not None:
        dataframe['CookTime']=dataframe['CookTime'].map(lambda x:get_total_minutes(x))
        dataframe['PrepTime']=dataframe['PrepTime'].map(lambda x:get_total_minutes(x))
        dataframe['TotalTime']=dataframe['TotalTime'].map(lambda x:get_total_minutes(x))
        output=dataframe.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
        return output
    else:
        return None
