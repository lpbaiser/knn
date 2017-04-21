# -*- coding: utf-8 -*-
def getMatrizCentroid(matriz_treino, classes, classes_volta):
	matriz_centroid = []
	vetor_qtd_por_instacia = [0]*len(classes.keys())
	for i in range(len(classes.keys())):
		vetor = [0]*(len(matriz_treino[0])-1)
		vetor.append(classes_volta[i])
		matriz_centroid.append(vetor)

	qtd_caract = len(matriz_treino[0])
	
	for linha_treino in matriz_treino:
		for j in range(qtd_caract-1):
			i = classes[linha_treino[-1]]
			matriz_centroid[i][j] += linha_treino[j]
		vetor_qtd_por_instacia[classes[linha_treino[-1]]] += 1

	for i in range(len(classes.keys())):
		for j in range(qtd_caract-1):
			matriz_centroid[i][j] = matriz_centroid[i][j]/vetor_qtd_por_instacia[i]
	#print(matriz_centroid)
	#print("^ Matriz Centroid\n")
	return matriz_centroid