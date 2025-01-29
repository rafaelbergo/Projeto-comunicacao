import PySimpleGUI as sg
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local

layout_client = [
    [sg.Text(' Gráfico:')],
    [sg.Canvas(key='GRAFICO', size=(400, 150))],

    [sg.Text('Algoritmo aplicado a mensagem:')],
    [sg.Multiline(size=(50, 5), key='REC_MSG_ALG', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem em Binário:')],
    [sg.Multiline(size=(50, 5), key='REC_MSG_BIN', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem Criptografada:')],
    [sg.Multiline(size=(50, 3), key='REC_MSG_CRIPTO', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem:')],
    [sg.Multiline(size=(50, 3), key='REC_MSG', disabled=True, no_scrollbar=True)],
]

layout_conexao = [
    [sg.Text('IP da conexâo:'), sg.Multiline(size=(15, 1), key='IP_CONEXAO', disabled=False, no_scrollbar=True)],
    [sg.Button('Conectar', key='CONNECT', disabled=False), sg.Button('Desconectar', key='DISCONNECT',disabled=False)],
    [sg.Text('Status:'), sg.Text('Desconectado', key='STATUS', size=(15, 1))],
]

layout = [
    [sg.Column(layout_client, key='CLIENT', visible=True), sg.VSeparator(), sg.Column(layout_conexao, key='CONEXAO', visible=True, vertical_alignment='top')]
]

window = sg.Window('Projeto Comunicacao - CLIENT', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break


    
    print('Valores:  ', values)


window.close()