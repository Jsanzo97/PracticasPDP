# -*- encoding: utf-8 -*-
'''
@author: 
'''

#carmenpazosparamo@gmail.com

from random import shuffle
from time import time

tiempoActual = 0
tiempoInicio = time()

def main():
    print "BUSCAMINAS"
    print "----------"
    print "1. Principiante (9x9, 10 minas)"
    print "2. Intermedio (16x16, 40 minas)"
    print "3. Experto (16x30, 99 minas)"
    print "4. Leer de fichero"
    print "5. Salir"
    
    opcion = input ("Escoja opcion: ")
    minasTablero = [] #Contiene 1 si hay mina o 0 si no
    estado = [] #Contiene si esta abierta o no
    tablero = [] #Contine vecinas - marcadas
    
    if(opcion == 1):
        crearTableroAleatorio(9, 9, 10, minasTablero, estado, tablero)
        dibujar(estado, minasTablero)
        jugar(minasTablero, estado, tablero)
        
    elif(opcion == 2):
        crearTableroAleatorio(16, 16, 40, minasTablero, estado, tablero)
        dibujar(estado, minasTablero)
        jugar(minasTablero, estado, tablero)

    elif(opcion == 3):
        crearTableroAleatorio(16, 30, 99, minasTablero, estado, tablero)
        dibujar(estado, minasTablero)
        jugar(minasTablero, estado, tablero)

    elif(opcion == 4):
        ruta = raw_input("Introduzca la ruta del fichero:\n")
        leerFichero(ruta, minasTablero, estado, tablero)
        dibujar(estado, minasTablero)
        numMinas = 0
        for i in range (len(minasTablero)):
            for j in range (len(minasTablero[i])):
                if(minasTablero[i][j] == 1):
                    numMinas = numMinas+1
        jugar(minasTablero, estado, tablero)

    elif(opcion == 5):
        print "Has salido del juego, bye!"
        
#Lee del fichero de texto
def leerFichero(ruta, minasTablero, estado, tablero):
    fichero = open(ruta, "r")
    informacion = []
    
    for linea in fichero.readlines():
        informacion.append(linea)
    
    fichero.close() 
    crearTableroDesdeFichero(informacion, minasTablero, estado, tablero)

#Inicia el vector estado con todas cerradas
def estadoInicial (filas, columnas, estado):
    CSOM = u'\u2593' # ▒ 
    for i in range(filas):
        estado.append([])
        for j in range (columnas):
            estado[i].append(CSOM)
            
#Crea el tablero correspondiente a la informacion del fichero
def crearTableroDesdeFichero(informacionFichero, minasTablero, estado, tablero):
    informacionFichero.pop(0) #Eliminamos la primera linea
    
    estadoInicial(len(informacionFichero), len(informacionFichero[0])-1, estado)
    
    #Recorremos y si es * añadimos 1 si no añadimos 0
    for i in range (len(informacionFichero)):
        minasTablero.append([])
        for j in range (len(informacionFichero[i])):
            if(informacionFichero[i][j] == "*"):
                minasTablero[i].append(1)
            if(informacionFichero[i][j] == "."):
                minasTablero[i].append(0)   
    
    #Calculamos vecinas - marcadas para cada posicion menos la ultima(salto de linea)
    for i in range (len(informacionFichero)):
        tablero.append([])
        if(i<len(informacionFichero)-1):
            limite = len(informacionFichero[i])-1
        else:
            limite = len(informacionFichero[i])
        for j in range (limite):
            tablero[i].append(minasVecinas(i,j,minasTablero) - marcadasVecinas(i, j, estado))  

#Crea un tablero aleatorio con los parametros filas columnas y minas
def crearTableroAleatorio(filas, columnas, minas, minasTablero, estado, tablero):
    estadoInicial(filas, columnas, estado)
    
    #Hacemos que haya minas en poiciones aleatorias
    posiciones = []
    for i in range (filas * columnas):
        posiciones.append(i)
        
    shuffle(posiciones)
    posMinas = posiciones[:minas]
    
    #Añadimos las minas al tablero
    for i in range(filas):
        minasTablero.append([])
        for j in range(columnas):
            if((j + i * columnas) in posMinas):
                minasTablero[i].append(1)
            else: 
                minasTablero[i].append(0)
    
    #Calculamos n = vecinas - marcadas   
    for i in range (filas):
        tablero.append([])
        for j in range (columnas):
            tablero[i].append(minasVecinas(i,j,minasTablero) - marcadasVecinas(i, j, estado))
          
#Bucle principal del juego
def jugar(minasTablero, estado, tablero):
    jugando = True;

    while(jugando == True):
        orden = raw_input("Indique celda y accion (! marcar, * abrir): ")
        
        if(orden == "Salir" or orden == "salir" or orden == "SALIR"):
            print "Has salido del juego"
            exit(0)
        
        if(comprobarJugada(orden, len(minasTablero), len(minasTablero[0])) == True):
            realizarJugada(orden, minasTablero, estado, tablero)
            dibujar(estado, minasTablero)
            jugando = comprobarGanado(minasTablero, estado, jugando)
            
    print "ENHORABUENA HAS GANADO!!"
            
#Efectuamos la jugada ya sea marcar o abrir
def realizarJugada(orden, minasTablero, estado, tablero):
    letrasColumnas = "abcdefghijklmnopqrstuvwxyz=+-:/"
    letrasFilas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    for i in range(len(orden)):
        if(i > 0 and (i+1) % 3 == 0):
            if(orden [i:i+1] == "!"):
                fila = orden [i-2:i-1]
                columna = orden[i-1:i]
                marcar(fila, columna, estado)
            if(orden [i:i+1] == "*"):
                fila = orden [i-2:i-1]
                columna = orden[i-1:i]
                
                #Hallamos el indice asociado a cada letra que hemos recibido
                for i in range (len(letrasColumnas)):
                    if(letrasColumnas[i:i+1] == columna):
                        indiceColumna = i
                
                for i in range (len(letrasFilas)):
                    if(letrasFilas[i:i+1] == fila):
                        indiceFila = i
               
                abrir(indiceFila, indiceColumna, estado, minasTablero, tablero)

#Calcula el numero de minas vecinas a la posicion fila, columna
#Comprobamos esquinas, bordes y el centro             
def minasVecinas(fila, columna, minasTablero):
    i = fila
    j = columna
    contador = 0
    
    #Comprobar esquinas
    if(i == 0 and j == 0):
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
    elif(i == len(minasTablero)-1 and j == 0):
        if(minasTablero[i-1][j] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
    elif(i == 0 and j == len(minasTablero[i])-1):
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i+1][j-1] == 1):
            contador = contador+1
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
    elif(i == len(minasTablero)-1 and j == len(minasTablero[i])-1):
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i-1][j] == 1):
            contador = contador+1
        if(minasTablero[i-1][j-1] == 1):
            contador = contador+1
    
    #Comprobar bordes        
    elif(i > 0 and i < len(minasTablero) and j == 0):
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
    elif(j > 0 and j < len(minasTablero[i]) and i == 0):
        if(minasTablero[i+1][j-1] == 1):
            contador = contador+1
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
    elif(i == len(minasTablero)-1 and j > 0 and j < len(minasTablero[i])):
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
        if(minasTablero[i-1][j-1] == 1):
            contador = contador+1
        if(minasTablero[i-1][j+1] == 1):
            contador = contador+1
        if(minasTablero[i-1][j] == 1):
            contador = contador+1
    elif(i > 0 and i < len(minasTablero) and j == len(minasTablero[i]) -1):
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
        if(minasTablero[i-1][j] == 1):
            contador = contador+1
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
    
    #Las demas casillas normales
    elif(j > 0 and j < (len(minasTablero[i])) -1 and i < (len(minasTablero) -1) and i > 0):
        if(minasTablero[i+1][j] == 1):
            contador = contador+1
        if(minasTablero[i-1][j] == 1):
            contador = contador+1
        if(minasTablero[i][j-1] == 1):
            contador = contador+1
        if(minasTablero[i][j+1] == 1):
            contador = contador+1
        if(minasTablero[i-1][j-1] == 1):
            contador = contador+1
        if(minasTablero[i+1][j-1] == 1):
            contador = contador+1
    
    return contador

#Calcula el numero de marcadas vecinas a la posicion fila, columna
#Comprobamos esquinas, bordes y el centro 
def marcadasVecinas(fila, columna, estado):
    i = fila
    j = columna
    contador = 0
    
    #Comprobar esquinas
    if(i == 0 and j == 0):
        if(estado[i+1][j] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
    elif(i == len(estado)-1 and j == 0):
        if(estado[i-1][j] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
    elif(i == 0 and j == len(estado[i])-1):
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i+1][j-1] == 'X'):
            contador = contador+1
        if(estado[i+1][j] == 'X'):
            contador = contador+1
    elif(i == len(estado)-1 and j == len(estado[i])-1):
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i-1][j] == 'X'):
            contador = contador+1
        if(estado[i-1][j-1] == 'X'):
            contador = contador+1
    
    #Comprobar bordes        
    elif(i > 0 and i < len(estado) and j == 0):
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
        if(estado[i+1][j] == 'X'):
            contador = contador+1
    elif(j > 0 and j < len(estado[i]) and i == 0):
        if(estado[i+1][j-1] == 'X'):
            contador = contador+1
        if(estado[i+1][j] == 'X'):
            contador = contador+1
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
    elif(i == len(estado)-1 and j > 0 and j < len(estado[i]) -1):
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
        if(estado[i-1][j-1] == 'X'):
            contador = contador+1
        if(estado[i-1][j+1] == 'X'):
            contador = contador+1
        if(estado[i-1][j] == 'X'):
            contador = contador+1
    elif(i > 0 and i < len(estado)-1 and j == len(estado[i]) -1):
        if(estado[i+1][j] == 'X'):
            contador = contador+1
        if(estado[i-1][j] == 'X'):
            contador = contador+1
        if(estado[i][j-1] == 'X'):
            contador = contador+1 
    
    #Las demas casillas normales
    elif(j > 0 and j < (len(estado[i])) -1 and i < (len(estado) -1) and i > 0):
        if(estado[i+1][j] == 'X'):
            contador = contador+1
        if(estado[i-1][j] == 'X'):
            contador = contador+1
        if(estado[i][j-1] == 'X'):
            contador = contador+1
        if(estado[i][j+1] == 'X'):
            contador = contador+1
        if(estado[i-1][j-1] == 'X'):
            contador = contador+1
        if(estado[i+1][j-1] == 'X'):
            contador = contador+1
    
    return contador
 
#Marca una casilla como posible mina                  
def marcar(fila, columna, estado):
    CSOM = u'\u2593' # ▒ 
    letrasColumnas = "abcdefghijklmnopqrstuvwxyz=+-:/"
    letrasFilas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"

    #Como recibimos letras hallamos el indice asociado a cada una
    for i in range (len(letrasColumnas)):
        if(letrasColumnas[i:i+1] == columna):
            indiceCol = i
    
    for i in range (len(letrasFilas)):
        if(letrasFilas[i:i+1] == fila):
            indiceFil = i
    
    if(estado[indiceFil][indiceCol] == "X"):
        estado[indiceFil][indiceCol] = CSOM
    else:
        estado[indiceFil][indiceCol] = "X"
 
#Abre una casilla          
def abrir(fila,columna, estado, minasTablero, tablero):
    fila = abs(fila)
    columna = abs(columna)
    
    if(minasTablero[fila][columna] != 0):
        print "BOMBA! Has perdido"
        dibujar(minasTablero, estado)
        exit()
        
    if(estado[fila][columna] != " "):
        estado[fila][columna] = " "
        if(tablero[fila][columna] <= 0): #Si n<0 abrimos mas celdas vecinas
            abrirMas(fila, columna, estado, minasTablero, tablero)
        else:
            if(columna>=0):
                estado[fila][columna] = tablero[fila][columna]

#Comprobamos si podemos abrir mas celdas vecinas que no tengan mina
def abrirMas(fila, columna, estado, minasTablero, tablero):
    i = fila
    j = columna
    
    #Comprobar esquinas
    if(i == 0 and j == 0):
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
    elif(i == len(minasTablero)-1 and j == 0):
        if(minasTablero[i-1][j] != 1):
            abrir(fila-1,columna,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
    elif(i == 0 and j == len(minasTablero[i])-1):
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i+1][j-1] != 1):
            abrir(fila+1,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
    elif(i == len(minasTablero)-1 and j == len(minasTablero[i])-1):
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i-1][j] != 1):
            abrir(fila-1,columna,estado,minasTablero,tablero)
        if(minasTablero[i-1][j-1] != 1):
            abrir(fila-1,columna-1,estado,minasTablero,tablero)
    
    #Comprobar bordes        
    elif(i > 0 and i < len(minasTablero) and j == 0):
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
    elif(j > 0 and j < len(minasTablero[i]) and i == 0):
        if(minasTablero[i+1][j-1] != 1):
            abrir(fila+1,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
    elif(i == len(minasTablero)-1 and j > 0 and j < len(minasTablero[i]) -1):
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
        if(minasTablero[i-1][j-1] != 1):
            abrir(fila-1,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i-1][j+1] != 1):
            abrir(fila-1,columna+1,estado,minasTablero,tablero)
        if(minasTablero[i-1][j] != 1):
            abrir(fila-1,columna,estado,minasTablero,tablero)
    elif(i > 0 and i < len(minasTablero)-1 and j == len(minasTablero[i]) -1):
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
        if(minasTablero[i-1][j] != 1):
            abrir(fila-1,columna,estado,minasTablero,tablero)
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero) 
    
    #Las demas casillas normales
    elif(j > 0 and j < (len(minasTablero[i])) -1 and i < (len(minasTablero) -1) and i > 0):
        if(minasTablero[i+1][j] != 1):
            abrir(fila+1,columna,estado,minasTablero,tablero)
        if(minasTablero[i-1][j] != 1):
            abrir(fila-1,columna,estado,minasTablero,tablero)
        if(minasTablero[i][j-1] != 1):
            abrir(fila,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i][j+1] != 1):
            abrir(fila,columna+1,estado,minasTablero,tablero)
        if(minasTablero[i-1][j-1] != 1):
            abrir(fila-1,columna-1,estado,minasTablero,tablero)
        if(minasTablero[i+1][j-1] != 1):
            abrir(fila+1,columna-1,estado,minasTablero,tablero)

#Comprobamos si la jugada recibida es correcta o no
def comprobarJugada(orden, filas, columnas):
    correcta = True
    letrasColumnas = "abcdefghijklmnopqrstuvwxyz=+-:/"
    letrasFilas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    
    letrasColumnas = letrasColumnas[0:columnas]
    letrasFilas = letrasFilas[0:filas] 
    
    if(len(orden) < 3):
        print "ENTRADA ERRONEA"
        correcta=False
    
    else:
        for i in range (len(orden)):
            if((i+1) % 3 == 0):
                if(orden[i:i+1] != "!" and orden[i:i+1] != "*"):
                    print "ENTRADA ERRONEA"
                    correcta = False
            else:
                if(i % 3 == 0):
                    if(orden[i:i+1] not in letrasFilas):
                        print "FILA INCORRECTA"
                        correcta = False
                elif((i+2) % 3 == 0):
                    if(orden[i:i+1] not in letrasColumnas):
                        print "COLUMNA INCORRECTA"
                        correcta = False
    
    return correcta

#Comprobamos si hemos ganada la partida o no
def comprobarGanado(minasTablero, estado, jugando):
    CSOM = u'\u2593' # ▒
    contadorMinas = 0
    contadorTapadas = 0
        
    for i in range (len(minasTablero)):
        for j in range (len(minasTablero[i])):
            if(minasTablero[i][j] == 1):
                contadorMinas = contadorMinas + 1
    
    for i in range (len(estado)):
        for j in range (len(estado[i])):
            if(estado[i][j] == CSOM):
                contadorTapadas = contadorTapadas + 1
    
    if(contadorTapadas == contadorMinas):
        jugando = False
    
    return jugando

#Dibujamos el tablero 
def dibujar(estado, minasTablero):
    COE = u'\u2500' # ─
    CNS = u'\u2502' # │
    CES = u'\u250C' # ┌
    CSO = u'\u2510' # ┐
    CNE = u'\u2514' # └
    CON = u'\u2518' # ┘
    COES = u'\u252C' # ┬
    CONE = u'\u2534' # ┴
    
    columnas = "abcdefghijklmnopqrstuvwxyz=+-:/"
    filas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    
    contadorMinas = 0
    contadorMarcadas = 0
        
    for i in range (len(minasTablero)):
        for j in range (len(minasTablero[i])):
            if(minasTablero[i][j] == 1):
                contadorMinas = contadorMinas + 1
                
    for i in range (len(estado)):
        for j in range (len(estado[i])):
            if(estado[i][j] == "X"):
                contadorMarcadas = contadorMarcadas + 1
    
    global tiempoActual
    tiempoActual = time()
    global tiempoInicio       
    tiempo = str(tiempoActual - tiempoInicio)
    tiempo = tiempo[:5]
    print "MINAS RESTANTES: ",contadorMinas," | MARCADAS: ",contadorMarcadas," |TIEMPO: ",tiempo,"s."
     
    print " ",
    for i in range (len(estado[0])):
        print " ",
        print columnas[i],
    
    print
    print " ",
    print CES,
    for i in range (len(estado[0]) * 2):
        if(i == (len(estado[0])* 2)-1):
            print CSO,
        else:   
            if(i % 2 != 0):
                print COES,
            else:
                print COE,
    print
    
   
    for i in range (len(estado)):
        for j in range (len(estado[i])):
            if(j == 0 and i % 2 == 0):
                print filas[i],
                print CNS,
            if(j == 0 and i % 2 != 0):
                print filas[i],
                print " ",
            if(i % 2 == 0):
                print estado[i][j],
                print CNS,
            else:
                print CNS,
                print estado[i][j],
            if(i % 2 != 0 and j == (len(estado[i])-1)):
                print CNS,         
        print
        
        print " ",
        for j in range (len(estado[0])*2):
            if(j == 0):
                if(i % 2 == 0):
                    print CNE,
                else:
                    if(i < len(estado) -1):
                        print CES,
            
            elif(i == len(estado)-1):
                if( (len(estado) % 2) != 0):
                    if(j % 2 != 0):
                        print COE,
                    else:
                        print CONE,
                    if(j == (len(estado * 2) -1 )):
                        print CON,
                else:
                    if((j-1) == 0):
                        print " ",
                        print CNE,
                        print COE,
                    else:
                        if(j % 2 != 0):
                            print COE,
                        else:
                            print CONE,
                            
            else:                  
                if(i % 2 == 0):
                    if(j % 2 != 0):
                        print COES,
                    else:
                        print CONE,
                    if(j == (len(estado * 2) -1 )):
                        print CONE,
                        print CSO,
                else:
                    if(j % 2 != 0):
                        print CONE,
                    else:
                        print COES, 
                    if(j == (len(estado * 2) -1 )):
                        print COES,
                        print CON,
    
        if(len(estado) % 2 == 0 and i == len(estado)-1):
            print CON, 
            print
        else:                  
            print  
          
if __name__ == '__main__':
    main()