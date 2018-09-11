# -*- coding:utf-8 -*-
coches=[]
nivel=0
class Pieza:

    def __init__(self, valor, letra):
        
        COE = u'\u2500'
        CNS = u'\u2502' 
        CES = u'\u250C'
        CSO = u'\u2510'
        CNE = u'\u2514'
        CON = u'\u2518'
        CNES = u'\u251C'
        CONS = u'\u2524'
        
        if valor =="basIzq": #Pieza basica del lado izquierdo
            superiorPieza= CNES
            medioPieza= CNS
            inferiorPieza= CNS
        elif valor == "basDer": #Pieza basica del lado derecho
            superiorPieza= CONS
            medioPieza= CNS
            inferiorPieza= CNS
        elif valor == "inCocheH": #Pieza inicial del coche
            superiorPieza= CES+COE*4
            medioPieza= CNS+" "+letra.upper()+" "*2
            inferiorPieza= CNE+COE*4
        elif valor=="medCocheH": #Pieza intermedia del coche
            superiorPieza= COE*5
            medioPieza= " "*5
            inferiorPieza= COE*5
        elif valor=="finCocheH": #Pieza del final coche
            superiorPieza= COE*4+CSO
            medioPieza= " "*2+letra.lower()+" "+CNS
            inferiorPieza= COE*4+CON
        elif valor == "inCocheV": #Pieza inicial del coche en Vertical
            superiorPieza= CES+COE*3+CSO
            medioPieza= CNS+" "+letra.upper()+" "+CNS
            inferiorPieza= CNS+" "*3+CNS
        elif valor=="medCocheV": #Pieza intermedia del coche en Vertical
            superiorPieza= CNS+" "*3+CNS
            medioPieza= CNS+" "*3+CNS
            inferiorPieza= CNS+" "*3+CNS
        elif valor=="finCocheV": #Pieza del final coche en Vertical
            superiorPieza= CNS+" "*3+CNS
            medioPieza=  CNS+" "+letra.lower()+" "+CNS
            inferiorPieza= CNE+COE*3+CON
        else: #ERROR
            superiorPieza = "ERROR0a"
            medioPieza = "ERROR0b"
            inferiorPieza = "ERROR0c"
        
        self.superiorPieza = superiorPieza
        self.medioPieza = medioPieza
        self.inferiorPieza = inferiorPieza
    
    def dev(self, cont):
        if cont == 0:
            a=self.superiorPieza
        elif cont == 1:
            a=self.medioPieza
        elif cont == 2:
            a=self.inferiorPieza
        else:
            a="ERROR2"
        return a        

def imprimirTablero(matriz):
    #forma matriz
    #ladoIzquierdo=Pieza("basIzq",0)
    #ladoDerecho=Pieza("basDer",0)
    #fila0=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0, ladoDerecho]
    #fila1=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    #fila2=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,-1]
    #fila3=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    #fila4=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    #fila5=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    #tablero = [fila0, fila1, fila2, fila3, fila4, fila5]
    COE = u'\u2500' 
    CES = u'\u250C' 
    CSO = u'\u2510' 
    CNE = u'\u2514' 
    CON = u'\u2518' 
    COES = u'\u252C' 
    CONE = u'\u2534' 
    CSOM = u'\u2593'
    primeraLinea = CES+(COES+COE+COE+COE+COE)*8+CSO
    ultimaLinea= CNE+(CONE+COE+COE+COE+COE)*8+CON
    cont = 0
    print(primeraLinea)
    aux=""
    for i in matriz:
        a= 3
        cont=0 
        while a!=0 :           
            for e in i:
                if e==0:
                    aux +=" "*5
                elif e==-1:
                    aux +=CSOM
                else:  
                    aux+=e.dev(cont)
            a=a-1
            cont+=1
            print (aux)
            aux=""
    print(ultimaLinea)
    return

def pasarAPiezas(matriz):
    '''PRE: coche debe un string codificado asi orientacion/ columna inicial(no mayor que 6 ni menor que 1)/ 
    fila inicial(no mayor que 6 ni menor que 0)/ longitud (no menor que 2 ni mayor que 6). matriz debe ser una "matriz" de 6x6.'''
    '''Es necesario cambiar el formato de los coches anadiendo una letra al final que sea la letra que represente al coche.
    Pasa cualquier str en el formato adecuado que se encuentra en la matriz'''
    fila = 0
    for i in matriz:
        columna = 0
        for e in i:
            if type(e) is str:
                coche = e
                longitud=int(coche[3])
                orientacion=coche[0]
                letra=coche[4]
                if orientacion == "H":
                    matriz[fila][columna] = Pieza("inCocheH", letra)
                    
                    for i in range(columna+1,columna+longitud-1):
                        matriz[fila][i] = Pieza("medCocheH",0)
                    
                    matriz[fila][columna+longitud-1] = Pieza("finCocheH",letra)
                elif orientacion == "V":
                    matriz[fila][columna] = Pieza("inCocheV", letra)
                    
                    for i in range(fila+1,fila+longitud-1):
                        matriz[i][columna] = Pieza("medCocheV",0)
                    
                    matriz[fila+longitud-1][columna] = Pieza("finCocheV",letra)
                else:
                    print ("ERROR3")
            columna+=1
        fila+=1
    return

def getMovestr(s):
    abecedario="abcdefghijqlmnopqrstuvwxyz"
    moveSTR=""
    errorIn = False
    lista = []
    for caracter in s:
        if (abecedario.__contains__(caracter)) or (abecedario.upper().__contains__(caracter)):
            moveSTR+=caracter
        else:
            errorIn = True
            break
    lista.append(moveSTR)
    lista.append(errorIn)
    return lista

def reescribir(listaDeCoches):
    abecedario="abcdefghijqlmnopqrstuvwxyz"
    contador = 0
    lista = []
    for s in listaDeCoches:
        lista.append(s+abecedario[contador])
        contador+=1
    return lista

def introducir(matriz,listaDeCochesReescrita):
    fila = 0
    columna = 0
    for s in listaDeCochesReescrita:
        fila = int(s[2])
        columna = int (s[1])
        matriz[fila-1][columna] = s
    return

def mover(movimientos, listaDeCochesReescrita, error,puntos):
    '''PRE: los coches contienen en la posicion 4 del str la letra asociada que les correspondde, movimientos no contiene ningun caracter que no pertenezca al abecedario
    estando la  no incluida, error debe ser boolean. codificacion coche en listaDeCochesReescrita: orientacion-columna-fila-longitud-letra asociada. listaDeCochesReescrita
    debe ser una lista de coches y los coches deben ser str de acuerdo a la codificacion dada'''
    
    s = ""
    salir = False
    for letra in movimientos:
        cont = 0
        for coche in listaDeCochesReescrita:
            
            letraCoche = coche[4]
            fila =int( coche[2])
            columna =int( coche[1])
            orientacion = coche[0]
            longitud = int(coche[3])
            
            if letraCoche.lower()==letra:
                if orientacion=="H":
                    if posible(fila, columna+longitud, listaDeCochesReescrita,puntos):
                        columna+=1
                    else:
                        salir = True
                        
                elif orientacion == "V":
                    if posible(fila+longitud, columna, listaDeCochesReescrita,puntos):
                        fila+=1
                    else:
                        salir = True
                        
                s = orientacion + str(columna) + str(fila) + coche[3] + letraCoche
                listaDeCochesReescrita[cont] = s
                break                   
               
            elif letraCoche.upper()==letra:
                if orientacion=="H":
                    if posible(fila, columna-1, listaDeCochesReescrita,puntos):
                        columna-=1
                    else:
                        salir = True
                        
                elif orientacion == "V":
                    if posible(fila-1, columna, listaDeCochesReescrita,puntos):
                        fila-=1
                    else:
                        salir = True
                        
                s = orientacion + str(columna) + str(fila) + coche[3] + letraCoche
                listaDeCochesReescrita[cont] = s
                break
            cont+=1 
        if (salir == True):
            print ("Movimiento: "+letra+" imposible por bloqueo")
            break
        
    if error == True and (salir==False) : 
            print ("El caracter numero "+str(len(movimientos)+1)+" no es valido")
    return

def posible (filaAavanzar, columnaAavanzar, listaDeCochesReescrita,puntos):
    posible = True
    cont = 0
    if (filaAavanzar<1) or (filaAavanzar > 6) or (columnaAavanzar < 1) or (columnaAavanzar > 6):
        posible =False
    if posible == True:

        for coche in listaDeCochesReescrita:
            ori = coche[0]
            col = int(coche[1])
            fil = int(coche[2])
            lon = int(coche[3])
            
            if (ori =="H"):
                for i in range(lon):
                    #print lon, fil, col, filaAavanzar, columnaAavanzar
                    if ((fil == filaAavanzar) and (col+cont == columnaAavanzar)):
                        print "Error"
                        posible = False
                    cont=cont+1
                cont=0
            else:
                for i in range(lon):
                    if (col == columnaAavanzar) and (fil+cont == filaAavanzar) :
                        print "error"
                        posible = False
                    cont=cont+1
                cont=0
    if filaAavanzar==3 and columnaAavanzar == 7:
        enhorabuena(puntos)
    return posible

def enhorabuena (puntos):
    print "HAS GANADO!! "+str(puntos)
    escribirFichero(puntos)
    
def escribirFichero(puntos):
    linea=""
    cont=0
    infile = open("records.txt","r")
    wfile = open("records.txt","w")
    for i in infile:
        if(cont==nivel):
            linea=infile.readline()
            print linea
            if(len(linea)==0):
                puntos=puntos
            else:
                if(int(linea)<puntos):
                    puntos=linea
                else:
                    puntos=puntos
        cont=cont+1
    infile.close()
    
    wfile.write(str(puntos))   
    wfile.close()
    
    exit(0)
    
def imprimirFinal(listaDeCoches):
    ladoIzquierdo=Pieza("basIzq",0)
    ladoDerecho=Pieza("basDer",0)
    fila0=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0, 0, 0, ladoDerecho]
    fila1=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    fila2=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    fila3=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,-1]
    fila4=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    fila5=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    fila6=[ladoIzquierdo,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,ladoDerecho]
    tablero = [fila0, fila1, fila2, fila3, fila4, fila5, fila6]
    if (listaDeCoches[0].__len__()==4):
        listaDeCoches=reescribir(listaDeCoches)
    introducir(tablero, listaDeCoches)
    pasarAPiezas(tablero)
    imprimirTablero(tablero)
    return 

def moverFinal(listaDeCochesReescrita,puntos):
    movimientos = raw_input("Introduzca los movimiento: ")
    print movimientos
    if (movimientos=="0"):
        print "Has salido"
        exit(0)
    lista = getMovestr(movimientos)
    movSTR = lista[0]
    error = lista [1]
    mover(movSTR, listaDeCochesReescrita, error,puntos)
    imprimirFinal(listaDeCochesReescrita)
    return

def getListaDeCoches():
    listaDeCoches = ["H232","H113","V513","H143","V442","V352","H552","H562"]
    return listaDeCoches

#menu para elgir los niveles
def menu():

    infile = open('niveles.txt')#abrir los ficheros
    numeroNiveles=int(infile.readline())
    print('>>> Lectura completa del fichero')
    infile.close # Cerramos el fichero.

    print ("Selecciona un nivel")
    for i in range (1,numeroNiveles):
            print("Nivel: "+str(i))
        
      
    print ("\t0 - salir") 
    opcionMenu = input("Inserta un numero valor >> ")# solicituamos una opción al usuario

    nivel=opcionMenu
    print nivel
    infile = open('niveles.txt') #escoger los datos del nivel
    cochesPorNivel=[]
    lineaActual=0
    acumulador=1
    for line in infile:
        if(lineaActual==acumulador):
            cochesPorNivel.append(int(line))
            acumulador=acumulador+int(line)+1
        lineaActual=lineaActual+1
    infile.close
    numCochesEsteNivel = cochesPorNivel[opcionMenu-1]
    print "Numero de coches:"+str(numCochesEsteNivel)
    
    infile = open('niveles.txt')#abrir los ficheros
    nivel=0
    lineaActual=1
    acumulador=2
    
    for line in infile:
        if(lineaActual==acumulador):
            acumulador=acumulador+int(line)+1
            nivel=nivel+1
        if(nivel==opcionMenu):
            if(len(line)>3):
                coches.append((line)[:4])
        lineaActual=lineaActual+1
    infile.close
    
    #AL LLEGAR AQUI SE SABE EL NUM DE COCHES DEL NIVEL ELEGIDO Y QUE COCHES HAY
    
   
    
#para poder dibujar la matriz
  
        
def main():
    menu()
    puntos=0
    listaDeCochesReescrita=reescribir(coches)
    imprimirFinal(listaDeCochesReescrita)
    while True:
        
        moverFinal(listaDeCochesReescrita,puntos)
        puntos=puntos+1
        
 #para que inice bien el main   
if __name__=='__main__':
    main()