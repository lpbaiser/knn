# -*- coding: utf-8 -*-
import csv
from random import shuffle
import math
import operator
from copy import deepcopy
import sys
import numpy as np

# from sklearn.metrics import confusion_matrix

#calcula a distancias euclidiana entre dois vetores
def calcula_distancia_euclidiana(instancia1, instancia2):
    distancia = 0.0
    for i in range(len(instancia1)-1):
        distancia += pow((instancia1[i] - instancia2[i]), 2)
    return math.sqrt(distancia)

#encontra as k menores distancias na instancia teste
def get_k_menores_distancias(matriz_treino, instancia_teste, k):
    distancias = []
    #para toda a matriz de treinamento calcula a distancia euclidiana
    #para a instancia teste do paramentro
    for i in range(len(matriz_treino)):
        dist = calcula_distancia_euclidiana(matriz_treino[i], instancia_teste)
        #adiciona a instancia e a distancia em um vetor
        distancias.append((matriz_treino[i][-1], dist))
    #ordena as distancias

    distancias.sort(key = operator.itemgetter(1))
   
    menores_distancias = []
    #adiciona no vetor menores_distancias as k primeiras do vetor distancias
    for i in range(k):
        menores_distancias.append(distancias[i][0])
    return menores_distancias

#classifica o vetor de menor distancia de acordo com o número de votos, ganha a instancia que tiver mais votos
def classifica_voto_majoritario(menores_distancias):
    voto_majoritario = {}
    for i in range(len(menores_distancias)):
        response = menores_distancias[i][-1]
        if response in voto_majoritario:
            voto_majoritario[response] += 1
        else:
            voto_majoritario[response] = 1
        votos_classificados = sorted(voto_majoritario.iteritems(), key = operator.itemgetter(1))
    return votos_classificados[0][0]


#calcular a taxa de acerto, verifica se cada classe classes encontradas corresponde a uma classe de treino
def calcula_taxa_acerto(matriz_teste, classes, qtdeInstancia):
    #print (classes)
    acerto = 0
    for i in range(len(matriz_teste)):
        if matriz_teste[i][-1] == classes[i]:
            acerto += 1
    return (acerto/float(qtdeInstancia)) * 100

#função para normalizaro os dados
def normaliza_dados(matriz_dados):
    for i in range(len(matriz_dados)):
        menor = menor_da_lista(matriz_dados[i])
        maior = maior_da_lista(matriz_dados[i])
        for j in range(len(matriz_dados[i])-1):
            x = (matriz_dados[i][j] - menor)/(maior - menor)
            matriz_dados[i][j] = x
    return matriz_dados

#encontra o maior valor da lista (não utilizado a função max pois a lista contem float e string)
def maior_da_lista(lista):
    maior = 0.0
    for i in range(len(lista)-1):
        if (lista[i] > maior):
            maior = lista[i]
    return maior

#encontra o menor valor da lista (não utilizado a função min pois a lista contem float e string)
def menor_da_lista(lista):
    menor = lista[0]
    for i in range(len(lista)-1):
        if (lista[i] < menor):
            menor = lista[i]
    return menor

#carrega a matriz do arquivo e os parse necessários 
def carrega_matriz(path):
    arquivo = open(path, 'r')
    classes = {}

    matriz = []
    id = 0
    for line in arquivo:
        # quebra linha por ,
        str_line_split = line.split(' ')
                
        # faz o cast dos dados lidos de string para float
        for j in range(len(str_line_split)-1):
            str_line_split[j] = float(str_line_split[j])
            j = j + 1
        if (not classes.has_key(str_line_split[j])):
            classes[str_line_split[j]]= id
            id += 1
        # adiciona o vetor na matriz
        matriz.append(str_line_split)
        
    arquivo.close()
    return matriz,classes

def classificador(matriz_treino, matriz_teste, k):
    classificados = []
    for i in range(len(matriz_teste)):
        menores_distancias = get_k_menores_distancias(matriz_treino, matriz_teste[i], k)
        result = classifica_voto_majoritario(menores_distancias)
        classificados.append(result)
    return classificados

def get_classes(matriz_teste):
    classes = []
    for i in range(len(matriz_teste)):
        if (matriz_teste[i][-1] not in classes):
            classes.append(matriz_teste[i][-1])
    return classes

def get_matriz_centroid(matriz_treino, classes_treino):
    matriz_centroid = []
    for classe in classes_treino.keys():
        linha = []
        for j in range(len(matriz_treino[0])-1):
            linha.append(0)
        linha.append(classe)
        matriz_centroid.append(linha)

    contador = [0]*len(classes_treino.keys())

    for linha in matriz_treino:
        linha_centroid = classes_treino[linha[-1]]
        for i in range(len(linha)-1):
            matriz_centroid[linha_centroid][i] += linha[i]
        contador[linha_centroid] +=1
    print("contador")
    print(contador)
    
    for i in range(len(matriz_centroid)):
        for j in range(len(matriz_centroid[i])-1):
            matriz_centroid[i][j] = matriz_centroid[i][j]/contador[i]
            print (matriz_centroid[i][j]/contador[i])

    return matriz_centroid

def classificador_centroid(matriz_centroid, matriz_teste):
    classificados = []
    for i in range(len(matriz_teste)):
        result = (get_k_menores_distancias_centroid(matriz_centroid, matriz_teste[i]))        
        classificados.append(result)
    return classificados

def get_k_menores_distancias_centroid(matriz_centroid, instancia_teste):
    distancias = []
    #para toda a matriz de treinamento calcula a distancia euclidiana
    #para a instancia teste do paramentro
    for i in range(len(matriz_centroid)):
        dist = calcula_distancia_euclidiana(matriz_centroid[i], instancia_teste)
        #adiciona a instancia e a distancia em um vetor
        distancias.append((matriz_centroid[i][-1], dist))
    #ordena as distancias
    print("\nDistancias\n")
    print(distancias)
    distancias.sort(key = operator.itemgetter(1))
    print("\nDistancias Ordenada\n")
    print(distancias)
    '''print("\n distancias")
    print(distancias)
    print("\n")'''
    
    
    
    return distancias[0]


def main():

    if (len(sys.argv) <= 3):
        print ("Falta argumentos - arquivo_treino.data arquivo_teste.data k")
        return -1

    matriz_treino = []
    matriz_teste = []
    matriz_treino,classes_treino = carrega_matriz(str(sys.argv[1]))
    matriz_teste, classes_teste = carrega_matriz(str(sys.argv[2]))

    
    qtdeInstancia = len(matriz_teste)

    #normaliza todos os dados
    matriz_treino = normaliza_dados(matriz_treino)
    matriz_teste = normaliza_dados(matriz_teste)


    #copia 20% da matriz de treinamento
    matriz_de_treino_20 = deepcopy(matriz_treino[:int(len(matriz_treino)*0.25)])
    #copia 50% da matriz de treinamento
    matriz_de_treino_50 = deepcopy(matriz_treino[:int(len(matriz_treino)*0.50)])

    # classes = get_classes(matriz_teste)
    # print (classes)

    k = int(sys.argv[3])
    '''
    classificados = []

    print ("k = %i") % k

    print ("\nClassificador para 25% dos dados de treinamento\n")
    classificados =  classificador(matriz_de_treino_20, matriz_teste, k)
    taxa_de_acerto = calcula_taxa_acerto(matriz_teste, classificados, qtdeInstancia)
    print "taxa_de_acerto: " + repr(taxa_de_acerto) + "%"

    print (confusion_matrix(matriz_teste, classificados))

    print ("\nClassificador para 50% dos dados de treinamento\n")
    classificados =  classificador(matriz_de_treino_50, matriz_teste, k)
    taxa_de_acerto = calcula_taxa_acerto(matriz_teste, classificados, qtdeInstancia)
    print "taxa_de_acerto: " + repr(taxa_de_acerto) + "%"

    '''
    #print ("\nClassificador para 100% dos dados de treinamento\n")
    #classificados =  classificador(matriz_treino, matriz_teste, k)
    #taxa_de_acerto = calcula_taxa_acerto(matriz_teste, classificados, qtdeInstancia)
    #print "taxa_de_acerto: " + repr(taxa_de_acerto) + "%"

    matriz_centroid = (get_matriz_centroid(matriz_treino, classes_treino))
    classificados =  classificador_centroid(matriz_centroid, matriz_teste)
    print("\nClassificados\n")
    print(classificados)
    taxa_de_acerto = calcula_taxa_acerto(matriz_teste, classificados, qtdeInstancia)
    print "taxa_de_acerto: " + repr(taxa_de_acerto) + "%"
    return 0

main()