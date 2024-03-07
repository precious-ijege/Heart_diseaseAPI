from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json


app = FastAPI()


origins = ["*"]

# Setting up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Using Pydantic to define the data type  of our request object.
class ModelInput(BaseModel):
    age : int
    sex : int
    cp :int
    trestbps : int
    chol : int
    fbs : int
    restecg : int
    thalach : int
    exang : int
    oldpeak : float
    slope : int
    ca : int
    thal : int


#  Load the trained model.pkl file
heart_model = pickle.load(open('heart_model.sav', 'rb'))


@app.get("/")
def home():
    return {"message": "Welcome to the Heart Disease Prediction API"}

# Define a route for predicting heart disease
@app.post('/heart_prediction')
def heart_prediction(input_parameters : ModelInput):
    # extracting the JSON data from the request body
    input_data = input_parameters.json()
    # convert it into a Python dictionary 
    input_dictionary = json.loads(input_data)
    
    age = input_dictionary['age']
    sex = input_dictionary['sex']
    cp = input_dictionary['cp']
    trestbps = input_dictionary['trestbps']
    chol = input_dictionary['chol']
    fbs = input_dictionary['fbs']
    restecg = input_dictionary['restecg']
    thalach = input_dictionary['thalach']
    exang = input_dictionary['exang']
    oldpeak = input_dictionary['oldpeak']
    slope = input_dictionary['slope']
    ca = input_dictionary['ca']
    thal = input_dictionary['thal']
    
    input_list = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]    
    prediction = heart_model.predict([input_list])[0]

    if prediction:
        return  {'Message': 'Patient has Heart Disease'}
    else:
        return  {'Message':'Patient does NOT Have Heart Disease'}

