# ------------ Trabalho de Redes Digitais e Industriais ------------
# ---------------- Professor: Diego Stéfano (Dinho) ----------------
# ----------------- Atividade: Formação de Quadros -----------------
# ----------------- Protocolo: CAN 2.0A - STANDART -----------------
# --------- Equipe: Laiana Rios, Robson Barbosa, Samuel Dias -------
# -------------------- Código com Funções Gerais -------------------

# Motivo do fGeral = deixar os códigos do transmissor e receptor mais limpos porque eles usam algumas funções iguais

# Importa o Socket para poder se comunicar com o servidor e obter uma resposta de volta
import socket

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
   
# A função mod2div faz um XOR entre o divisor e dividendo
# Realiza a junção dos elementos após passar pela função XOR
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
# encodeData = coloca os zeros necessários após o dado enviado (número da chave - 1)
# Manda essa informação para o mod2div (que faz a divisão exclusiva) e retorna para o transmissor
def encodeData(msg, key):
   
     l_key = len(key)
   
    # Adiciona n-1 de "0" no final da mensagem
     appended_data = msg + '0'*(l_key-1)
     remainder = mod2div(appended_data, key)

    # Anexar o restante nos dados originais
     codeword = msg + remainder

     return codeword

# decodeData = coloca os zeros necessários após o dado enviado (número da chave - 1)
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

        pos_final = pos_inicial + (n + 1)

        if pos_final >= len(dividendo):
            fim = True

# paridadesIN = recebe os dados e os converte em uma lista de ints, printa a lista, determina a posição e o valor do bit que precisa ser inserido
def paridadesIN(entrada):
   
    par = list(map(int, str(entrada)))

    #print("PARIDADES:",par)

    posicoes=[]
    elementos=[]

    # Calcula onde o bit precisa ser inserido
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

    #print("POSIÇÕES ONDE DEVE INSERIR: {}".format(posicoes))
    #print("ELEMENTOS A SEREM INSERIDOS: {}".format(elementos))

    saida = par
    #print(saida)
    # Coloca o bit extra no lugar
    for x in range(len(par)):
        if x in posicoes:
            #print(par[0:x+1])
            #print([elementos[posicoes.index(x)]])
            #print(par[x:len(par)-1])
            saida = par[0:x] + [elementos[posicoes.index(x)]] + par[x:len(par)]
            #print(saida)

    return "".join([str(elem) for elem in saida])

# paridadesOFF = recebe os dados e os converte em uma lista de ints, printa a lista, determina a posição e o valor do bit que precisa ser retirado
def paridadesOFF(entrada):
   
    #print(entrada)
    par = list(map(int, str(entrada)))

    #print("PARIDADES:",par)

    posicoes=[]
    elementos=[]

   # Calcula onde o bit precisa ser retirado
    for idx in range(len(par)):

        if idx >= 5:
            s = sum(par[idx - 4:idx])

            if s == 0:
                if par[idx] == 0:
                    posicoes.append(idx)
                    elementos.append(1)
            elif s == 5:
                if par[idx] == 1:
                    posicoes.append(idx)
                    elementos.append(0)

    #print("POSIÇÕES ONDE DEVE INSERIR: {}".format(posicoes))
    #print("ELEMENTOS A SEREM INSERIDOS: {}".format(elementos))

    saida = par

    # Retira o bit inserido
    for x in posicoes:
        saida[x+1] = "BIT_DE_SAIDA"

    #print(saida)

    saida.remove("BIT_DE_SAIDA")

    return "".join([str(elem) for elem in saida])

#print(paridadesOFF(paridadesIN("110100000101110")))