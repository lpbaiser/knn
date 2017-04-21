# -*- coding: utf-8 -*-
#carrega a matriz do arquivo e os parse necessários 
def carrega_matriz(path):
    arquivo = open(path, 'r')

    
    matriz = []
    
    for line in arquivo:
        # remove os espaços em branco
        line = line.replace("\n", '')
        # quebra linha por ,
        str_line_split = line.split(' ')

        # faz o cast dos dados lidos de string para float
        for j in range(len(str_line_split)-1):
            str_line_split[j] = float(str_line_split[j])
            j = j + 1

        
        # adiciona o vetor na matriz
        matriz.append(str_line_split)
        
    arquivo.close()
    
    return matriz

def carrega_matriz_centroid(path):
    arquivo = open(path, 'r')

    classes = {}
    classes_volta = {}
    matriz = []
    id = 0
    for line in arquivo:
        # remove os espaços em branco
        line = line.replace("\n", '')
        # quebra linha por ,
        str_line_split = line.split(' ')
        

        # faz o cast dos dados lidos de string para float
        for j in range(len(str_line_split)-1):
            str_line_split[j] = float(str_line_split[j])
            j = j + 1
        #print(str_line_split[j][:-2])

        if (not classes.has_key(str_line_split[j])):
            classes[str_line_split[j]]= id
            classes_volta[id] = [str_line_split[j]]
            id += 1
        # adiciona o vetor na matriz
        matriz.append(str_line_split)
    print(classes)

    arquivo.close()
    
    return matriz, classes, classes_volta

if __name__ == '__main__':
    main()