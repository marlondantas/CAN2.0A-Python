# ------------ Trabalho de Redes Digitais e Industriais ------------
# ---------------- Professor: Diego Stéfano (Dinho) ----------------
# ----------------- Atividade: Formação de Quadros -----------------
# ----------------- Protocolo: CAN 2.0A - STANDART -----------------
# --------- Equipe: Laiana Rios, Robson Barbosa, Samuel Dias -------
# -------------------- Código com Funções Gerais -------------------


import socket
# Dados do CAN:

# Função para realizar o cálculo do XOR
def xor(data, crc): 
   
    # Inicializa resultado
    result = []

   # Atravessa todos os bits, se os bits forem iguais, então XOR é 0, caso contrário 1

    for i in range(1, len(crc)):
        if data[i] == crc[i]: 
            result.append('0') 
        else: 
            result.append('1') 
   
    return ''.join(result) 
   
    # Executa a divisão Modulo-2

def mod2div(divident, divisor):
    # Número de bits a serem XORed por vez.

    pick = len(divisor)
   
    tmp = divident[0 : pick]
   
    while pick < len(divident): 
   
        if tmp[0] == '1': 
   
            # Substitui o dividendo pelo resultado do XOR e puxa 1 bit para baixo

            tmp = xor(divisor, tmp) + divident[pick] 
   
        else:
            # Se o bit mais a esquerda for '0'

            # Se o bit mais à esquerda do dividendo (ou a parte usada em cada etapa) for 0, a etapa não poderá
            # usar o divisor regular; precisamos usar um divisor de todos os 0s.

            tmp = xor('0'*pick, tmp) + divident[pick]
   
        pick += 1

   # Nos últimos n bits, precisamos executá-lo normalmente, pois o aumento do valor de pick causará o Índice fora dos limites.

    if tmp[0] == '1':
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
   
    checkword = tmp 
    return checkword

    # Função usada no lado do remetente para codificar dados, acrescentando o restante da divisão modular no final dos dados.

def encodeData(msg, key):
   
     l_key = len(key)
   
    # Adiciona n-1 de "0" no final da mensagem

     appended_data = msg + '0'*(l_key-1)
     remainder = mod2div(appended_data, key)

    # Anexar o restante nos dados originais

     codeword = msg + remainder

     return codeword

def decodeData(data, key):
     l_key = len(key)

     # Anexa n-1 zeros no final dos dados

     appended_data = data + '0'*(l_key-1)
     remainder = mod2div(appended_data, key)
   
     return remainder

def crc(bits, n, divisor):
    dividendo = bits.copy()
    dividendo.extend([0] * n)

    pos_inicial = dividendo.index(1)
    pos_final = pos_inicial + (n + 1)

    novo_dividendo = xor(dividendo[pos_inicial : pos_final], divisor)

    fim = False

    while (not fim):

        pos_inicial = novo_dividendo.index(1)

        pedaco_novo_dividendo = novo_dividendo[novo_dividendo.index(1) :]
        pedaco_antigo_dividendo = dividendo[pos_final:]

        novo_dividendo = xor(pedaco_novo_dividendo + pedaco_antigo_dividendo, divisor)

        pos_final = pos_inicial + ( n + 1)

        if pos_final >= len(dividendo):
            fim = True

def paridades(entrada):
    par = list(map(int, str(entrada)))

    print("Paridades:",par)

    posicoes_zero = []
    posicoes_um = []

    for idx in range(len(par)):

        if idx >= 5:
            s = sum(par[idx - 5:idx])

            if s == 0:
                if par[idx] == 0:
                    posicoes_um.append(idx)
            elif s == 5:
                if par[idx] == 1:
                    posicoes_zero.append(idx)

    print("Posições onde deve inserir 1: {}".format(posicoes_um))
    print("Posições onde deve inserir 0: {}".format(posicoes_zero))


def paridadesIN(entrada):
    par = list(map(int, str(entrada)))

    print("Paridades:",par)

    posicoes=[]
    elementos=[]

    #calcular onde
    for idx in range(len(par)):

        if idx >= 5:
            s = sum(par[idx - 5:idx])

            if s == 0:
                if par[idx] == 0:
                    posicoes.append(idx)
                    elementos.append(1)
            elif s == 5:
                if par[idx] == 1:
                    posicoes.append(idx)
                    elementos.append(0)

    print("Posições onde deve inserir: {}".format(posicoes))
    print("elemtnso a serem inseridos: {}".format(elementos))

    saida = par

    #COLOCAR NO LUGAR

    for x in range(len(par)):
        if x in posicoes:
            print(par[0:x+1])
            print([elementos[posicoes.index(x)]])
            print(par[x:len(par)-1])
            saida = par[0:x] + [elementos[posicoes.index(x)]] + par[x:len(par)-1]
            print(saida)

    return "".join([str(elem) for elem in saida])

def paridadesOFF(entrada):
    print(entrada)
    par = list(map(int, str(entrada)))

    print("Paridades:",par)

    posicoes=[]
    elementos=[]

    #calcular onde
    for idx in range(len(par)):

        if idx >= 5:
            print("entrou")
            s = sum(par[idx - 4:idx])

            if s == 0:
                if par[idx] == 0:
                    posicoes.append(idx)
                    elementos.append(1)
            elif s == 5:
                if par[idx] == 1:
                    posicoes.append(idx)
                    elementos.append(0)

    print("Posições onde deve inserir: {}".format(posicoes))
    print("elemtnso a serem inseridos: {}".format(elementos))

    saida = par

    #Tira NO LUGAR
    for x in posicoes:
        saida.pop(x+1)
    print(saida)

paridadesOFF(paridadesIN("11010000001110"))