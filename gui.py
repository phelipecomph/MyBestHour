import PySimpleGUI as sg
import requests
import numpy as np


def get_table_values():
    response = requests.get("http://127.0.0.1:8000/day") #Today data
    entries = np.array(response.json()['entries'])
    columns = list(entries[0].keys())
    values = [list(col) for col in zip(*[d.values() for d in entries])] #list of dicts to list of lists
    values = list(map(list, zip(*values))) #Transpose Values
    return columns, values

def gui():
    cs, vs = get_table_values()

    layout = [
        [sg.Text('Pico ou Vale?')],
        [sg.Button('Pico'),sg.Button('Vale')],
        [sg.Table(values=vs,headings=cs,key='table')]
    ]

    window = sg.Window('Ciclo de Produtividade', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: break #Close Window
        if event == 'Pico': requests.post("http://127.0.0.1:8000/pico") #Post Pico
        if event == 'Vale': requests.post("http://127.0.0.1:8000/vale") #Post Vale
        if event in ['Pico','Vale']: #Update Table
            _, vs = get_table_values()
            window['table'].update(vs)
            

    window.close()

if __name__ == "__main__":
    gui()