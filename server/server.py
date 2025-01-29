import PySimpleGUI as sg
import socket
import matplotlib.pyplot as plt

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local

layout_server = [

    [sg.Checkbox(' Mensagem ', default=True, key='CHK_MSG', enable_events=True)],
    [sg.Multiline(size=(50, 3), key='MSG', disabled=False, no_scrollbar=True)],

    [sg.Checkbox(' Mensagem Criptografada:', default=True, key='CHK_MSG_CRIPTO', enable_events=True)],
    [sg.Multiline(size=(50, 3), key='MSG_CRIPTO', disabled=False, no_scrollbar=True)],

    [sg.Checkbox(' Mensagem em Binário:', default=True, key='CHK_MSG_BIN', enable_events=True)],
    [sg.Multiline(size=(50, 5), key='MSG_BIN', disabled=False, no_scrollbar=True)],

    [sg.Checkbox(' Algoritmo aplicado a mensagem:', default=True, key='CHK_MSG_ALG', enable_events=True)],
    [sg.Multiline(size=(50, 5), key='MSG_ALG', disabled=False, no_scrollbar=True)],

    [sg.Text(' Gráfico:')],
    [sg.Canvas(key='GRAFICO', size=(400, 150))],

    [sg.Button('Enviar', key='ENVIAR', disabled=False)],
]

layout_conexao = [
    [sg.Text('IP:'), sg.InputText(get_local_ip(), key='IP', disabled=True, size=(15, 1))],
    [sg.Button('Abrir Conexão', key='CONNECT', disabled=False), sg.Button('Encerrar Conexão', key='DISCONNECT',disabled=False)],
    [sg.Text('Status:'), sg.Text('Desconectado', key='STATUS', size=(15, 1))],
    [sg.HSeparator()],
    [sg.Text('Clientes Conectados:')],
    [sg.Listbox(values=['Sem clientes conectados'], key='CLIENTES', size=(30, 6), enable_events=False)]
]

layout = [
    [sg.Column(layout_server, key='SERVER', visible=True), sg.VSeparator(), sg.Column(layout_conexao, key='CONEXAO', visible=True, vertical_alignment='top')]
]

window = sg.Window('Projeto Comunicacao - SERVER', layout)

clientes_conectados = []


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    elif event == 'CHK_MSG':
        valor = not values['CHK_MSG']
        window['MSG'].update(disabled=valor, value = '' if valor else None)
    
    elif event == 'CHK_MSG_CRIPTO':
        valor = not values['CHK_MSG_CRIPTO']
        window['MSG_CRIPTO'].update(disabled=valor, value = '' if valor else None)
    
    elif event == 'CHK_MSG_BIN':
        valor = not values['CHK_MSG_BIN']
        window['MSG_BIN'].update(disabled=valor, value = '' if valor else None)
    
    elif event == 'CHK_MSG_ALG':
        valor = not values['CHK_MSG_ALG']
        window['MSG_ALG'].update(disabled=valor, value = '' if valor else None)
    
    if clientes_conectados:
        window['CLIENTES'].update(values=clientes_conectados)
    else:
        window['CLIENTES'].update(values=['Sem clientes conectados'])


    print('Valores: ', values)

window.close()