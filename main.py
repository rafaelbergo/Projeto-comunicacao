import PySimpleGUI as sg
import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  # Conecta a um servidor externo para determinar o IP
    ip_local = s.getsockname()[0]
    s.close()
    return ip_local

# Define o layout do emissor
layout_emissor = [

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

# Define o layout do receptor
layout_receptor = [
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
    [sg.Text('IP:'), sg.InputText(get_local_ip(), key='IP', disabled=True, size=(15, 1))],
    [sg.Text('IP da conexao:'), sg.Multiline(size=(15, 1), key='IP_CONEXAO', disabled=False, no_scrollbar=True)],
    [sg.Button('Conectar', key='CONNECT', disabled=False), sg.Button('Desconectar', key='DISCONNECT',disabled=False)],
    [sg.Text('Status:'), sg.Text('Desconectado', key='STATUS', size=(15, 1))],
]

layout = [
    [sg.Checkbox(' Emissor ', default=False, key='CHK_EMISSOR', enable_events=True), sg.Checkbox(' Receptor ', default=False, key='CHK_RECEPTOR', enable_events=True)],

    [sg.Column(layout_emissor, key='EMISSOR', visible=True), sg.VSeparator(), sg.Column(layout_receptor, key='RECEPTOR', visible=True), sg.VSeparator(), sg.Column(layout_conexao, key='CONEXAO', visible=True, vertical_alignment='top')]
]

window = sg.Window('Projeto Comunicacao', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break


    # Define se o programa e o emissor ou o receptor
    elif event == 'CHK_EMISSOR':
        if values['CHK_EMISSOR']:
            window['CHK_RECEPTOR'].update(value=False, disabled=True)
            window['CONNECT'].update(disabled=True)
            window['DISCONNECT'].update(disabled=True)
            window['IP_CONEXAO'].update(disabled=True, value='')


        else:
            window['CHK_RECEPTOR'].update(disabled=False)


    elif event == 'CHK_RECEPTOR':
        if values['CHK_RECEPTOR']:
            window['CHK_EMISSOR'].update(value=False, disabled=True)
            window['CHK_MSG'].update(disabled=True)
            window['CHK_MSG_CRIPTO'].update(disabled=True)
            window['CHK_MSG_BIN'].update(disabled=True)
            window['CHK_MSG_ALG'].update(disabled=True)
            window['MSG'].update(disabled=True, value='')
            window['MSG_CRIPTO'].update(disabled=True, value='')
            window['MSG_BIN'].update(disabled=True, value='')
            window['MSG_ALG'].update(disabled=True, value='')
            window['ENVIAR'].update(disabled=True)
            window['CONNECT'].update(disabled=False)
            window['DISCONNECT'].update(disabled=False)
            window['IP_CONEXAO'].update(disabled=False, )
  
        else:
            window['CHK_EMISSOR'].update(disabled=False)
            window['CHK_MSG'].update(disabled=False)
            window['CHK_MSG_CRIPTO'].update(disabled=False)
            window['CHK_MSG_BIN'].update(disabled=False)
            window['CHK_MSG_ALG'].update(disabled=False)
            window['ENVIAR'].update(disabled=False)
            window['MSG'].update(disabled=False)
            window['MSG_CRIPTO'].update(disabled=False)
            window['MSG_BIN'].update(disabled=False)
            window['MSG_ALG'].update(disabled=False)


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
    


    print('Valores:  ', values)


window.close()