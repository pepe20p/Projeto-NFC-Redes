import PySimpleGUI as sg
import os
from mrz.generator.td3 import TD3CodeGenerator
from Crypto.Cipher import AES
from mrz.checker.td3 import TD3CodeChecker
from Crypto.Util.Padding import pad,unpad

senha = 'arlindo'

def emitir(dados):
    code = str(TD3CodeGenerator(dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[7],dados[8])).encode()
    numero_documento = dados[4]
    while (len(numero_documento) < 9):
        numero_documento = numero_documento+'0'
    senha_atual = numero_documento+senha
    senha_atual = senha_atual.encode()
    cipher = AES.new(senha_atual,AES.MODE_CBC)
    c_code = cipher.encrypt(pad(code,AES.block_size))
    final = numero_documento.encode()+cipher.iv+c_code
    with open(dados[4],'wb') as file:
        file.write(final)

def ler(arquivo):
    try:
        with open(arquivo,'rb') as ler:
            ler_numero_doc = ler.read(9)
            ler_iv = ler.read(16)
            ler_cripto = ler.read()
    except:
        raise Exception("Arquivo Não encontrado")
    senha_atual = ler_numero_doc+senha.encode()
    cifra2 = AES.new(senha_atual, AES.MODE_CBC,ler_iv)
    descri = unpad(cifra2.decrypt(ler_cripto), AES.block_size).decode()
    return TD3CodeChecker(descri).fields()

def menu():
    layout_menu = [
        [sg.Text("Bem vindo ao emissor e verificador de TAG's")],
        [sg.Button("Emitir"),sg.Button("Ler e Verificar")]
    ]
    main = sg.Window("Emissor e verificador de TAG's",layout_menu,element_justification='c')
    while(True):
        evento,valores = main.read()
        if evento == sg.WIN_CLOSED or evento == "Emitir" or evento == "Ler e Verificar":
            break
    main.close()
    if evento == "Emitir":
        emissor()
    if evento == "Ler e Verificar":
        leitor()
    

def emissor():
    ronaldo = sg.Column([[sg.Image(filename='ronaldo.png')]])
    campos = sg.Column( [
            [sg.Text("Nome:"),sg.InputText(key='nome',size=(20,1)),sg.Text("Sobrenome:"),sg.InputText(key='sobrenome',size=(20,1))],
            [sg.Text("Nacionalidade:"),sg.InputText(key='nacionalidade',size=(6,1)),sg.Text("Número do Documento:"),sg.InputText(key='doc',size=(10,1))],
            [sg.CalendarButton("Data de Nascimento",close_when_date_chosen=True,target="nasc",format='%y%m%d'),sg.Input(key="nasc",size=(10,1)),sg.CalendarButton("Data de Vencimento",close_when_date_chosen=True,target="venc",format='%y%m%d'),sg.Input(key="venc",size=(10,1))],
            [sg.Radio('Masculino', "RADIO1", default=True), sg.Radio('Feminino', "RADIO1"),sg.Push(),sg.Button("Emitir")]
        ])
    layout_emissor = [[ronaldo,campos]]
    main = sg.Window("Emissor",layout_emissor)
    while(True):
        evento,valores = main.read()
        if evento == sg.WIN_CLOSED or evento == "Emitir":
            break
    main.close()
    if evento == "Emitir":
        try:
            if valores[1] == True:
                sexo = 'M'
            else:
                sexo = 'F'
            print(sexo)
            dados = ['P',valores['nacionalidade'],valores['sobrenome'],valores['nome'],valores['doc'],valores['nacionalidade'],valores['nasc'],sexo,valores['venc']]
            emitir(dados)
            sg.popup_auto_close("TAG {} gerada com sucesso!".format(valores["doc"]))
        except:
            sg.popup_auto_close("Dados invalidos! Verifique e tente novamente")
    menu()


def leitor():
    nome_do_arquivo = "Nenhum arquivo selecionado"
    layout_leitor = [
        [sg.Text("Arquivo:"),sg.Text("{}".format(nome_do_arquivo)),sg.FileBrowse(initial_folder=os.getcwd,key="arquivo")],
        [sg.Button("Confirmar")]
    ]
    main = sg.Window("Selecione o arquivo da TAG",layout_leitor,element_justification='c')
    while(True):
        evento, valores = main.read()
        if evento == sg.WIN_CLOSED or evento == "Confirmar":
            break
    main.close()
    if evento == "Confirmar":
        try:
            dados = ler(valores['arquivo'])
            resultado(dados)
        except:
            sg.popup_auto_close("Arquivo inválido!")
            menu()
    else:
        menu()


def resultado(campos):
    certo = sg.Column([[sg.Image(filename='certo.png')]])
    campos = sg.Column( [
            [sg.Text("Nome:"),sg.Text("{}".format(campos.name)),sg.Text("Sobrenome:"),sg.Text("{}".format(campos.surname))],
            [sg.Text("Nacionalidade:"),sg.Text("{}".format(campos.nationality)),sg.Text("Número do Documento:"),sg.Text("{}".format(campos.document_number))],
            [sg.Text("Data de nascimento:"),sg.Text("{}".format(campos.birth_date)),sg.Text("Data de vencimento:"),sg.Text("{}".format(campos.expiry_date))],
            [sg.Text("Sexo:"),sg.Text("{}".format(campos.sex)),sg.Button("Voltar")]
        ])
    layout_resultado = [[certo,campos]]
    main = sg.Window("Resultado",layout_resultado)
    
    while (True):
        evento, valores = main.read()
        if evento == sg.WINDOW_CLOSED or evento == "Voltar":
            break
    main.close()
    menu()

menu()