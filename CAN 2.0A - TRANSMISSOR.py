# ------------ Trabalho de Redes Digitais e Industriais ------------
# ---------------- Professor: Diego Stéfano (Dinho) ----------------
# ----------------- Atividade: Formação de Quadros -----------------
# ----------------- Protocolo: CAN 2.0A - STANDART -----------------
# --------- Equipe: Laiana Rios, Robson Barbosa, Samuel Dias -------
# --------------------- Código do Transmissor ----------------------

#-------Esse código representa o cliente (Envio dos dados)----------

# Importa o Socket para poder se comunicar com o servidor e obter uma resposta de volta
import socket

# Do arquivo fGeral irá importar todas as funções
from fGeral import *

# Endereco IP do Servidor
HOST = "127.0.0.1"    

 # Porta que o Servidor estar
PORT = 5000   

# Irá se conectar ao servidor e permanecerá conectado
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz conexão ao servidor
dest = (HOST, PORT)
tcp.connect(dest)

print ("PARA SAIR USE CTRL+X\n")

flag = True

while flag:

    print(("-")*150)
    
    # Recebe a mensagem do cliente e armazena na variavel msg
    msg = input("DIGITE A MENSAGEM EM BINARIO QUE VOCÊ DESEJA ENVIAR: ")

    if(msg == "\x18"):
        flag = False
        break

    print("MENSAGEM RECEBIDA:    ",msg)


    # Define o CRC
    key = "1100010110011001"

    # encodeData = Codificação da mensagem
    ans = encodeData(msg, key)

    print("MENSAGEM COM CRC:    ",ans)

    # Entra com o verificador de segurança!
    ans = paridadesIN(ans)

    # Faz o encapsulamento da mensagem
    encap = "0100110001000001000" #len = 19
    encap2 = "011111111" #len = 9

    ans = str(encap) + ans + str(encap2)
    
    print("MENSAGEM ENCAPSULADA E ENVIADA:    ",ans)

    # Faz o envio da variável ans através do servidor
    # encode = Faz a conversão para binário
    tcp.send(ans.encode('UTF-8'))
    
    # Resposta do servidor
    # 1024 = Faixa de comunicação do servidor 
    print (str(tcp.recv(1024),"UTF-8"))

# Encerra o servidor
tcp.close()
