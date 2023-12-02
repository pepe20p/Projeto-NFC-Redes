from mrz.generator.td3 import TD3CodeGenerator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

senha = 'arlindo'

def gerar_mrz():
    print("Insira o tipo de documento(Para passaporte \"P\"):")
    tipo_de_documento = input()
    print("Insira o código do pais(Brasil = BRA):")
    cod_pais = input()
    print("Insira o sobrenome:")
    sobrenome = input() #identificador primario
    print("Insira o primeiro nome:")
    nome = input() #identificador secundario
    print("Insira o numero do documento:")
    numero_documento = input()
    print("Insira a nacionalidade:(Brasil = BRA)")
    nacionalidade = input()
    print("Insira a data do nascimento:(YYMMDD)")
    nascimento = input() #YYMMDD
    print("Insira o genero (M ou F):")
    sexo = input()
    print("Insira a data de vencimento(YYMMDD):")
    vencimento = input()
    dados = [tipo_de_documento,cod_pais,sobrenome,nome,numero_documento,nacionalidade,nascimento,sexo,vencimento]
    code = str(TD3CodeGenerator(dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[7],dados[8])).replace('\n','').encode()
    while (len(numero_documento) < 9):
        numero_documento = numero_documento+'0'
    senha_atual = numero_documento+senha
    senha_atual = senha_atual.encode()
    cipher = AES.new(senha_atual,AES.MODE_CBC)
    c_code = cipher.encrypt(pad(code,AES.block_size))
    final = numero_documento.encode()+cipher.iv+c_code
    with open(dados[4],'wb') as file:
        file.write(final)
    print("Tag NFC {} gerada com sucesso!".format(dados[4]))

def ler(arquivo):
    try:
        with open(arquivo,'rb') as ler:
            ler_numero_doc = ler.read(9)
            ler_iv = ler.read(16)
            ler_cripto = ler.read()
    except:
        print("Não encontrado")
        return
    senha_atual = ler_numero_doc+senha.encode()
    cifra2 = AES.new(senha_atual, AES.MODE_CBC,ler_iv)
    descri = unpad(cifra2.decrypt(ler_cripto), AES.block_size).decode()
    print(descri)

def menu():
    print("Selecione uma opção:\n1-Gravar\n2-Ler\nPara sair digite \"sair\"")
    opcao = input()
    match opcao:
        case '1':
            try:
                gerar_mrz()
            except:
                print("Dados inseridos incorretamente")
            menu()
        case '2':
            try:
                print("Insira o número do documento")
                ler(input())
            except:
                print("Tag inválida ou alterada!!")
            menu()
        case 'sair':
            exit()
        case default:
            menu()

menu()