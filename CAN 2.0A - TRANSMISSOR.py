# ------------ Trabalho de Redes Digitais e Industriais ------------
# ---------------- Professor: Diego Stéfano (Dinho) ----------------
# ----------------- Atividade: Formação de Quadros -----------------
# ----------------- Protocolo: CAN 2.0A - STANDART -----------------
# --------- Equipe: Laiana Rios, Robson Barbosa, Samuel Dias -------
# --------------------- Código do Transmissor ----------------------

import socket

from fGeral import *

HOST = "127.0.0.1"                         # Endereco IP do Servidor
PORT = 5000                                # Porta que o Servidor está

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)
tcp.connect(dest)

print ("Para sair use CTRL+X\n")

flag = True

while flag:

    print(("-")*150)
    # Envia uma mensagem para o servidor
    msg = input("Digite a mensagem em binário (0 ou 1) que você deseja enviar: ")

    if(msg == "\x18"):
        flag = False
        break

    print("Mensagem enviada:    ",msg)

    # converte a mensagem em um codigo binario! (TIRAR DEPOIS)
    msg = (''.join(format(ord(x), 'b') for x in msg))

    print("Mensagem EM BINARIO: ", msg)

    #ENTRA COM O VERIFICADOR DE SEGURANCA
    paridades(msg)

    #DEFINE A CHAVE
    key = "1100010110011001"

    #CODIFICA O CODIGO
    ans = encodeData(msg, key)

    print("Mensagem com CRC:    ",ans)

    tcp.send(ans.encode('UTF-8'))

    print("Mensagem enviada\n")


    print("RESPOSTA:")
    print (str(tcp.recv(1024),"UTF-8"))

tcp.close()