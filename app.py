import PySimpleGUI as sg
import pyttsx3
from datetime import datetime
from os import path, getcwd
from configuracacoes import *
from textos import *

sg.theme()    # Keep things interesting for your users

def name(name):
    return sg.Text(name + ': ', size=(NAME_SIZE, 1), justification='l', font='Courier 10')

#iniciando pyttsx3
motor = pyttsx3.init()
vozes = motor.getProperty('voices')
nome_vozes = [voz.name for voz in vozes]

layout = [[name(MENSAGEM_ENTRADA_USUARIO)],
          [name('Voz'), sg.Combo(key='-VOICES-', size=(35, 10), values=nome_vozes, default_value=nome_vozes[0])],
          [name('Velocidade'), sg.Slider(key='-RATE-',  range=(0.25, 2), orientation='h', resolution=0.05, default_value=1.0, enable_events=True, disable_number_display=True),
          sg.Text('1.0x', size=(4, 1), key=('-SLIDER-TEXT-'))],
          [sg.Multiline(key='-TEXT-', size=(50, 10))],
          [sg.Button('Converter'), sg.Save('Salvar'), sg.Exit('Sair')]]

window = sg.Window(NOME_APP, layout)

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values)

    if event == 'Converter':
        # print('Convertendo texto...')
        # print(values['-TEXT-'])

        rate = int(MAX_RATE * values['-RATE-'])
        # print('RATE:', rate)
        motor.setProperty('rate', rate)     # configurando nova taxa de voz

        motor.say(values['-TEXT-'])
        motor.runAndWait()
        motor.stop()

    if event == 'Salvar':
        nome_arquivo = f'audio_{datetime.now().timestamp():.0f}.mp3'
        # print(nome_arquivo, 'criado com sucesso!')

        nome_customizado = sg.popup_get_text('Nome do arquivo', default_text=nome_arquivo)
        # print(nome_customizado)

        diretorio_arquivo = sg.popup_get_folder('Escolha o local onde deseja salvar o arquivo', default_path=getcwd())
        sg.popup('Results', f'O arquivo {nome_customizado} foi salvo com sucesso!')

        if diretorio_arquivo:
            diretorio_absoluto_arquivo = path.join(diretorio_arquivo, nome_customizado)

            motor.save_to_file(values['-TEXT-'], diretorio_absoluto_arquivo)
            motor.runAndWait()

        else:
            sg.popup_error('Insira um diretório válido.')

    try:
        window['-SLIDER-TEXT-'].update(f"{values['-RATE-']:.2f}x")
    except TypeError:
        pass

    if event == sg.WIN_CLOSED or event == 'Sair':
        break

window.close()