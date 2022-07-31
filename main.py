from fastapi import FastAPI
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.get('/')
def home():
    return "API Online" 

@app.post('/pico')
async def post_pico():
    data = pd.read_csv('data.csv')
    now = datetime.now()
    pd.concat([data,pd.DataFrame(data={'date':[now.date()],'hour':[f'{now.hour}:{now.minute}'],'type':['pico']})],ignore_index=True).to_csv('data.csv',index=False)
    return 'Sucesso'

@app.post('/vale')
async def post_vale():
    data = pd.read_csv('data.csv')
    now = datetime.now()
    pd.concat([data,pd.DataFrame(data={'date':[now.date()],'hour':[f'{now.hour}:{now.minute}'],'type':['vale']})],ignore_index=True).to_csv('data.csv',index=False)
    return 'Sucesso'