# -*- coding: utf-8 -*-
import math
import csv
from random import shuffle
import operator
from copy import deepcopy
import sys

def classificador_centroid(matriz_centroid, matriz_teste):
	classificados = []
	for linha_teste in matriz_teste:
		menor_dist = get_menor_distancia_centroid(matriz_centroid, linha_teste)
		classificados.append(menor_dist)
	#print(classificados)
	return classificados

def get_menor_distancia_centroid(matriz_centroid, instancia_teste):
	distancias = []


	#para toda a matriz de treinamento calcula a distancia euclidiana
	#para a instancia teste do paramentro
	for i in range(len(matriz_centroid)):
		dist = calcula_distancia_euclidiana(matriz_centroid[i], instancia_teste)
		#adiciona a instancia e a distancia em um vetor
		distancias.append((matriz_centroid[i][-1], dist))
	#ordena as distancias
	distancias.sort(key = operator.itemgetter(1))
	#print(distancias[0])
	#print("\n")
	return distancias[0]

#calcula a distancias euclidiana entre dois vetores
def calcula_distancia_euclidiana(instancia1, instancia2):
	distancia = 0.0
	for i in range(len(instancia1)-1):
		distancia += pow((instancia1[i] - instancia2[i]), 2)
	return math.sqrt(distancia)


#calcular a taxa de acerto, verifica se cada classe classes encontradas corresponde a uma classe de treino
def calcula_taxa_acerto_centroid(matriz_teste, classes, qtdeInstancia):
	# print (classes)
	acerto = 0
	for i in range(len(matriz_teste)):
		#print((matriz_teste[i][-1]))
		#print(classes[i][0][0])
		#print("\n")
		if (matriz_teste[i][-1])== classes[i][0][0]:
			print((matriz_teste[i][-1]))
			print(classes[i][0][0])
			print("\n")
			
			acerto += 1
	return (acerto/float(qtdeInstancia)) * 100
