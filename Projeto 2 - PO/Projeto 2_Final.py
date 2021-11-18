'''
Projeto: Enumeração de soluções básicas
Autores: Laura Campos e Wendson Carlos
Linguagem: Python
Biblioteca: Numpy e Itertools
'''

import numpy as np
from itertools import combinations
from itertools import permutations
import re

def crie_matriz(n_linhas, n_colunas, valor):

    matriz = [] # lista vazia

    for i in range(n_linhas):
        linha = [] # lista vazia
        for j in range(n_colunas):
            linha += [valor]
        matriz += [linha]

    return matriz


#Leitura da instância

# Matriz C: Coeficientes da FO
# Matriz A: Coeficientes das restrições
# Matriz B: Coeficientes de recursos

file = open("instance1.txt","r")

instancia = []

for line in file:
    instancia.append(line.rstrip())

tArcos = instancia[4:]

tMatriz = instancia[0:]

matriz = []
for i in tMatriz:
    matriz.append(i.split())
    
nVariaveis = int(matriz[0][0]) 
nRestricoes = int(matriz[0][1])   

#Criação das matrizes do problema

matrizA = crie_matriz(nRestricoes,nVariaveis,0)

for i in range(2, nRestricoes + 2):
    for j in range(nVariaveis):
        matrizA[i - 2][j] = int(matriz[i][j])
        
        
matrizB = crie_matriz(nRestricoes,1,0)

for i in range(2, nRestricoes + 2):
    for j in range(nVariaveis, nVariaveis + 1):
        matrizB[i - 2][j - nVariaveis] = int(matriz[i][j])


matrizC = crie_matriz(nVariaveis,1,0)

for i in range(nVariaveis):
    matrizC[i][0] = int(matriz[1][i]) 


c = np.array(matrizC)
c.T

#Transformar para forma padrão

matrizC_padrao = crie_matriz(nRestricoes + nVariaveis,1,0)

for i in range(nVariaveis):
    matrizC_padrao[i][0] = int(matrizC[i][0]) 


A = np.array(matrizC_padrao)

matrizA_padrao = crie_matriz(nRestricoes,nVariaveis + nRestricoes,0)

for i in range(nRestricoes):
    for j in range(nVariaveis):
        matrizA_padrao[i][j] = int(matrizA[i][j])
        
for i in range(nRestricoes):
    matrizA_padrao[i][i + nVariaveis] = -1

#Enumerando as soluções básicas

def rSubset(arr, r):
    return list(combinations(arr, r))

matrizX = list()

for i in range(nVariaveis + nRestricoes):
    matrizX.append(i)


combinacao = list()
combX = list()

for i in range(nRestricoes):
    arr = matrizA_padrao[i]
    r = nRestricoes
    combinacao.append(rSubset(arr, r))

r = nRestricoes
combX.append(rSubset(matrizX, r))

matrizes = list() #Lista de matrizes


for linha in combinacao[0]:
    matrizes.append(list())
    matrizes[len(matrizes)-1].append(linha)
    

for index,linha in enumerate(matrizes):
    for n in range (1, nRestricoes):
        matrizes[index].append(combinacao[n][index])
        
print('\n')

solucoes = list()

s = [0 for i in range(nVariaveis + nRestricoes)]
sb = [0 for i in range(nVariaveis + nRestricoes)]

Solucao = crie_matriz(nRestricoes + nVariaveis,1,0)

i = 0
sol = 0
flag = 0
solucoes_viaveis = list()
solucoes_basicas = list()

for matriz in matrizes:
    determinante = np.linalg.det(matriz)
    if determinante != 0:
        print(f'Colunas: {matriz}')
        inversa = np.linalg.inv(matriz)
        matrizSol = inversa.dot(matrizB)
       
        for j in range (nRestricoes):
            Solucao[combX[0][i][j]][0] = matrizSol[j][0]

        for j in range (nRestricoes + nVariaveis):
            s[j] = Solucao[j][0]
            sb[j] = Solucao[j][0]
            
        
        solucoes_basicas.append(sb)
        sb = [0 for i in range(nVariaveis + nRestricoes)] 
        
        print(f'Solução básica: {Solucao}')
        
        for j in range (nRestricoes + nVariaveis):
            sol = sol + (matrizC_padrao[j][0])*(Solucao[j][0])
            
        for j in range (nRestricoes):
           if matrizSol[j][0] <= 0:
             flag = -1
        
        if flag == 0:
            print("Classificação: Solução Viável")
            print(f'Valor da função objetivo: {sol}')
            solucoes.append(sol)
            solucoes_viaveis.append(s)
            s = [0 for i in range(nVariaveis + nRestricoes)]   
            
        else:
             print("Classificação: Solução Inviável")
            
        print("___________________________________________________________________________")
        
        
        for j in range (nRestricoes + nVariaveis):
            Solucao[j][0] = 0
            
        
    i = i + 1        
    sol = 0
    flag = 0 

print('\n')        
print(f'O conjunto de soluções básicas é: {solucoes_basicas}')


solOtima = 0
sOtima = [0 for i in range(nVariaveis + nRestricoes)] 

j = 0

for i in solucoes:
    if i > solOtima:
        solOtima = i
        sOtima = solucoes_viaveis[j]
        print(sOtima)
    j = j + 1    


print('\n')
print(f'Solução(ões) ótima(s): {sOtima}')
print(f'A FO resulta em: {solOtima}')

