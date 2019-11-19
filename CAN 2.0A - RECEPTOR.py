# ------------ Trabalho de Redes Digitais e Industriais ------------
# ---------------- Professor: Diego Stéfano (Dinho) ----------------
# ----------------- Atividade: Formação de Quadros -----------------
# ----------------- Protocolo: CAN 2.0A - STANDART -----------------
# --------- Equipe: Laiana Rios, Robson Barbosa, Samuel Dias -------
# --------------------- Código do Receptor -------------------------

# Importa o Socket para poder se comunicar com o servidor
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
orig = (HOST, PORT)

# Informa que está aberto para receber dados 
tcp.bind(orig)

print("SERVER INICIADO")

# Fica a espera dos dados
# 1 = Só irá aceitar 1 cliente 
tcp.listen(1)

# Irá executar o código enquanto o servidor estiver aberto
while True:
    
    # Variáveis definidas quando se estabelece uma conexão
    con, cliente = tcp.accept()
    print ('CONECTADO POR', cliente)

    # Recebimento dos dados
    # Pode receber mais de uma mensagem do mesmo cliente
    while True:
        
        # 1024 = Faixa de comunicação
        msg = con.recv(1024)
        
        # Se a mensagem não existir, o código dará um break
        if not msg: break

        # Recebe os dados
        print("MENSAGEM RECEBIDA: ", cliente, msg)

        #remove o encapsulamento da mensagem
        msg = msg[19 : len(msg)-9]
        print("MENSAGEM SEM ENCAPSULAMENTO: ",msg)

        # Analisa a paridade -> # Retira o bit inserido
        msg = paridadesOFF(str(msg, "ascii"))

        # Chave do CRC
        key = "1100010110011001"

        # Converte do binário de máquina para uma string
        ans = decodeData(msg, key)
        print("RESTANTE APÓS A DECODIFICAÇÃO: " + ans)
        
        # Realiza a verificação de erro - CRC

        # Contabiliza quantos zeros precisa ter na resposta
        temp = "0" * (len(key) - 1)
        
        # Se o ans for igual ao temp, printa a resposta verdadeira
        if ans == temp:
            print("THANKS. DADOS: <SAIDA>" + msg + "</SAIDA> NENHUM ERRO ENCONTRADO")
            
            # Manda o resultado para o cliente
            con.send("OBRIGADA POR CONECTAR -> NENHUM ERRO ENCONTRADO".encode())
        
        else:
            print("ERRO NOS DADOS")
            
            # Manda o resultado para o cliente
            con.send("OBRIGADA POR CONECTAR -> ERRO NOS DADOS".encode())
        
    print('FINALIZANDO CONEXÃO DO CLIENTE', cliente)

    # Encerra a conexão com o servidor
    con.close()

print("SERVER FECHADO")
