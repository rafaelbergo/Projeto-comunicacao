import PySimpleGUI as sg
import socket
from client_functions import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

layout_client = [
    [sg.Text(' Gráfico:')],
    [sg.Canvas(key='GRAFICO', size=(200, 150))],

    [sg.Text('Algoritmo aplicado a mensagem:')],
    [sg.Multiline(size=(100, 5), key='REC_MSG_ALG', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem em Binário:')],
    [sg.Multiline(size=(100, 5), key='REC_MSG_BIN', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem Criptografada:')],
    [sg.Multiline(size=(100, 3), key='REC_MSG_CRIPTO', disabled=True, no_scrollbar=True)],

    [sg.Text('Mensagem:')],
    [sg.Multiline(size=(100, 3), key='REC_MSG', disabled=True, no_scrollbar=True)],
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

client_socket = None

def limpa_campos():
    window['REC_MSG'].update('')
    window['REC_MSG_CRIPTO'].update('')
    window['REC_MSG_BIN'].update('')
    window['REC_MSG_ALG'].update('')
    window.refresh()

def atualizaCampo(campo, valor):
    window[campo].update(value=valor)

# Codigo adaptado de: https://www.tutorialspoint.com/pysimplegui/pysimplegui_matplotlib_integration.htm
def draw_figure(canvas, figure):
    for widget in canvas.winfo_children():
        widget.destroy()

    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def criaGrafico(mensagem):
    mensagem = mensagem.replace(" ", "")

    bit_array = []
    plot_data = list(''.join(mensagem))
    
    for bit in plot_data:
        if bit == '+':
            bit_array.append(1)    # Transforma + em 1
        elif bit == '-':
            bit_array.append(-1)   # Transforma - em -1
        else:
            bit_array.append(0)    # Transforma 0 para qualquer outro caractere
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.step(range(len(bit_array)), bit_array, where='post', color='darkblue', linewidth=3)
    ax.set_title('Algoritmo 8b6T')
    ax.set_yticks([-1, 0, 1])
    
    window['GRAFICO'].TKCanvas.update() 
    draw_figure(window['GRAFICO'].TKCanvas, fig)


while True:
    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    elif event == 'CONNECT':
        server_ip = values['IP_CONEXAO']
        window['STATUS'].update('Conectando...')
        window.refresh()
        client_socket = conectar(server_ip)
        if client_socket:
            window['STATUS'].update('Conectado')
        else:
            window['STATUS'].update('Erro ao conectar')
    
    elif event == 'DISCONNECT':
        if client_socket:
            desconectar(client_socket)
            client_socket = None
        window['STATUS'].update('Desconectado')
        window['REC_MSG'].update('')
        window['REC_MSG_CRIPTO'].update('')
        window['REC_MSG_BIN'].update('')
        window['REC_MSG_ALG'].update('')
        window.refresh()
    
    if client_socket:
        try:
            client_socket.setblocking(False)
            opcao, mensagem= receber_mensagem(client_socket)
            if mensagem is not None and opcao is not None:
                limpa_campos()
                escolhe_opcao(opcao, mensagem, atualizaCampo, criaGrafico)
        except:
            client_socket = None
            window['STATUS'].update('Desconectado')

window.close()