import PySimpleGUI as sg

# Define o layout da janela principal
layout = [
    [sg.Checkbox(' Emissor ', default=False, key='CHK_EMISSOR', enable_events=True)],
    [sg.Checkbox(' Receptor ', default=False, key='CHK_RECEPTOR', enable_events=True)],

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


    [sg.Button('Enviar')],

]

# Create the Window
window = sg.Window('Projeto Comunicacao', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # Define se o programa e o emissor ou o receptor
    elif event == 'CHK_EMISSOR':
        if values['CHK_EMISSOR']:
            window['CHK_RECEPTOR'].update(value=False, disabled=True)
        else:
            window['CHK_RECEPTOR'].update(disabled=False)
    elif event == 'CHK_RECEPTOR':
        if values['CHK_RECEPTOR']:
            window['CHK_EMISSOR'].update(value=False, disabled=True)
        else:
            window['CHK_EMISSOR'].update(disabled=False)


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