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
    pd.concat([data,pd.DataFrame(data={'id':data.shape[0]+1,'date':[now.date()],'hour':[f'{now.hour}:{now.minute}'],'type':['pico']})],ignore_index=True).to_csv('data.csv',index=False)
    return 'Success'

@app.post('/vale')
async def post_vale():
    data = pd.read_csv('data.csv')
    now = datetime.now()
    pd.concat([data,pd.DataFrame(data={'id':data.shape[0]+1,'date':[now.date()],'hour':[f'{now.hour}:{now.minute}'],'type':['vale']})],ignore_index=True).to_csv('data.csv',index=False)
    return 'Success'

@app.get('/pico')
def get_picos(): #Return last 'pico'
    data = pd.read_csv('data.csv')
    return data.loc[data['type']=='pico'].to_dict('records')[-3:]

@app.get('/pico/{id}')
def get_pico(id): #Return pico from id
    data = pd.read_csv('data.csv')
    if data.loc[(data['type']=='pico') & (data['id']==int(id))].shape[0]>=1: 
        return data.loc[(data['type']=='pico') & (data['id']==int(id))].to_dict('records')[0]
    else: 
        return 'id não corresponde á um pico'

@app.get('/vale')
def get_vales(): #Return last 'vale'
    data = pd.read_csv('data.csv')
    return data.loc[data['type']=='vale'].to_dict('records')[-3:]

@app.get('/vale/{id}')
def get_vale(id): #Return vale from id
    data = pd.read_csv('data.csv')
    if data.loc[(data['type']=='vale') & (data['id']==int(id))].shape[0]==1: 
        return data.loc[(data['type']=='vale') & (data['id']==int(id))].to_dict('records')[0]
    else: 
        return 'id não corresponde á um vale'

@app.get('/day')
def get_today(): #Return today all entries
    data = pd.read_csv('data.csv')
    now = datetime.now()
    return {'qnt':data.loc[data['date']==str(now.date())].shape[0],'entries':data.loc[data['date']==str(now.date())].to_dict('records')}

@app.get('/day/{day}')
def get_day(day): #Return all entries from day
    if day[4] != '-' or day[7] != '-': return 'invalid date format. It expect this format: YYYY-MM-DD'
    elif int(day.split('-')[1]) > 12: return 'invalid date format. It expect this format: YYYY-MM-DD'
    data = pd.read_csv('data.csv')
    if data.loc[data['date']==day].shape[0]>=1: 
        return {'qnt':data.loc[data['date']==day].shape[0],'entries':data.loc[data['date']==day].to_dict('records')}
    else: 
        return 'Esse dia não possui registros'