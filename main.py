from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import pickle
from fastapi.staticfiles import StaticFiles
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templetes")

# Modeli ve gerekli dönüşüm fonksiyonlarını yükleyin
load_model = pickle.load(open('logreg_l2_model.pkl', 'rb'))
label_encoder_att_work_rate = LabelEncoder()
label_encoder_def_work_rate = LabelEncoder()
label_encoder_foot = LabelEncoder()

# Att_Work_Rate, Def_Work_Rate ve Foot için LabelEncoder nesnelerini eğitme
att_work_rate_values = ['Low', 'Medium', 'High']
def_work_rate_values = ['Low', 'Medium', 'High']
foot_values = ['Left', 'Right']

label_encoder_att_work_rate.fit(att_work_rate_values)
label_encoder_def_work_rate.fit(def_work_rate_values)
label_encoder_foot.fit(foot_values)

Att_Work_Rate = att_work_rate_values
Def_Work_Rate = def_work_rate_values
Foot = foot_values

scaler = StandardScaler()

# Ana sayfa
@app.get("/") 
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Model sayfası
@app.get("/model", response_class=HTMLResponse)
async def read_model_page(request: Request):
    return templates.TemplateResponse("model.html", {"request": request})

# Index'ten model sayfasına yönlendirme
@app.get("/redirect_to_model_page")
async def redirect_to_model_page():
    return RedirectResponse("/model")

@app.get("/about.html",response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/details.html",response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})

@app.get("/iletisim.html",response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("iletisim.html", {"request": request})

@app.get("/model.html",response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("model.html", {"request": request})

@app.get("/index.html", response_class=HTMLResponse)
async def details_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Form verileri için Pydantic modeli
class PredictSchema(BaseModel):
    Positioning: int
    Acceleration: int
    Sprint_Speed: int
    Finishing: int
    Shot_Power: int
    Long_Shots: int
    Volleys: int
    Penalties: int
    Vision: int
    Crossing: int
    Free_Kick_Accuracy: int
    Shot_Passing: int
    Long_Passing: int
    Curve: int
    Agility: int
    Balance: int
    Reactions: int
    Ball_Control: int
    Detailed_Dribbling: int
    Composure: int
    Interception: int
    Heading_Accuracy: int
    Def_Awareness: int
    Standing_Tackle: int
    Sliding_Tackle: int
    Jumping: int
    Stamina: int
    Strength: int
    Aggression: int
    Age: int
    Att_Work_Rate: str
    Def_Work_Rate: str
    Foot: str

# Tahmin endpoint'i
@app.post("/position_predict", response_class=HTMLResponse)
async def position_predict(
    request: Request,
    Positioning: int = Form(...),
    Acceleration: int = Form(...),
    Sprint_Speed: int = Form(...),
    Finishing: int = Form(...),
    Shot_Power: int = Form(...),
    Long_Shots: int = Form(...),
    Volleys: int = Form(...),
    Penalties: int = Form(...),
    Vision: int = Form(...),
    Crossing: int = Form(...),
    Free_Kick_Accuracy: int = Form(...),
    Shot_Passing: int = Form(...),
    Long_Passing: int = Form(...),
    Curve: int = Form(...),
    Agility: int = Form(...),
    Balance: int = Form(...),
    Reactions: int = Form(...),
    Ball_Control: int = Form(...),
    Detailed_Dribbling: int = Form(...),
    Composure: int = Form(...),
    Interception: int = Form(...),
    Heading_Accuracy: int = Form(...),
    Def_Awareness: int = Form(...),
    Standing_Tackle: int = Form(...),
    Sliding_Tackle: int = Form(...),
    Jumping: int = Form(...),
    Stamina: int = Form(...),
    Strength: int = Form(...),
    Aggression: int = Form(...),
    Age: int = Form(...),
    Att_Work_Rate: str = Form(...),
    Def_Work_Rate: str = Form(...),
    Foot: str = Form(...),
):
    try:
        # Form verilerini ModelSchema'ya dönüştürme
        predict_values = PredictSchema(
            Positioning=Positioning,
            Acceleration=Acceleration,
            Sprint_Speed=Sprint_Speed,
            Finishing=Finishing,
            Shot_Power=Shot_Power,
            Long_Shots=Long_Shots,
            Volleys=Volleys,
            Penalties=Penalties,
            Vision=Vision,
            Crossing=Crossing,
            Free_Kick_Accuracy=Free_Kick_Accuracy,
            Shot_Passing=Shot_Passing,
            Long_Passing=Long_Passing,
            Curve=Curve,
            Agility=Agility,
            Balance=Balance,
            Reactions=Reactions,
            Ball_Control=Ball_Control,
            Detailed_Dribbling=Detailed_Dribbling,
            Composure=Composure,
            Interception=Interception,
            Heading_Accuracy=Heading_Accuracy,
            Def_Awareness=Def_Awareness,
            Standing_Tackle=Standing_Tackle,
            Sliding_Tackle=Sliding_Tackle,
            Jumping=Jumping,
            Stamina=Stamina,
            Strength=Strength,
            Aggression=Aggression,
            Age=Age,
            Att_Work_Rate=Att_Work_Rate,
            Def_Work_Rate=Def_Work_Rate,
            Foot=Foot
        )

        # Encoding işlemlerini gerçekleştir
        Att_Work_Rate_encoded = label_encoder_att_work_rate.transform([predict_values.Att_Work_Rate])[0]
        Def_Work_Rate_encoded = label_encoder_def_work_rate.transform([predict_values.Def_Work_Rate])[0]
        Foot_encoded = label_encoder_foot.transform([predict_values.Foot])[0]

        # Convert Pydantic model to DataFrame
        df = pd.DataFrame([{
            "Positioning": predict_values.Positioning,
            "Acceleration": predict_values.Acceleration,
            "Sprint_Speed": predict_values.Sprint_Speed,
            "Finishing": predict_values.Finishing,
            "Shot_Power": predict_values.Shot_Power,
            "Long_Shots": predict_values.Long_Shots,
            "Volleys": predict_values.Volleys,
            "Penalties": predict_values.Penalties,
            "Vision": predict_values.Vision,
            "Crossing": predict_values.Crossing,
            "Free_Kick_Accuracy": predict_values.Free_Kick_Accuracy,
            "Shot_Passing": predict_values.Shot_Passing,
            "Long_Passing": predict_values.Long_Passing,
            "Curve": predict_values.Curve,
            "Agility": predict_values.Agility,
            "Balance": predict_values.Balance,
            "Reactions": predict_values.Reactions,
            "Ball_Control": predict_values.Ball_Control,
            "Detailed_Dribbling": predict_values.Detailed_Dribbling,
            "Composure": predict_values.Composure,
            "Interception": predict_values.Interception,
            "Heading_Accuracy": predict_values.Heading_Accuracy,
            "Def_Awareness": predict_values.Def_Awareness,
            "Standing_Tackle": predict_values.Standing_Tackle,
            "Sliding_Tackle": predict_values.Sliding_Tackle,
            "Jumping": predict_values.Jumping,
            "Stamina": predict_values.Stamina,
            "Strength": predict_values.Strength,
            "Aggression": predict_values.Aggression,
            "Age": predict_values.Age,
            "Att_Work_Rate": Att_Work_Rate_encoded,
            "Def_Work_Rate": Def_Work_Rate_encoded,
            "Foot": Foot_encoded
        }])

        # scaler'ı uygun şekilde eğitin
        scaler.fit(df)

        scaled_values = scaler.transform(df)
        # Make predictions
        position_prediction = load_model.predict(scaled_values)

        # Tahmin sonucunu sınıfa çevirme
        position_mapping = {0: 'Hücum Hattı', 1: 'Orta Saha', 2: 'Defans', 3: 'Kale'}
        predicted_position = position_mapping[position_prediction[0]]

        return templates.TemplateResponse("prediction_result.html", {"request": request, "result": predicted_position})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
