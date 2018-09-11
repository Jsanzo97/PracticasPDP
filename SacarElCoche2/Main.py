#!/usr/bin/env python
import pygtk
from sys import argv
pygtk.require('2.0')
import gtk
import os.path

#Ventana de inicio donde se elegira el nivel a jugar entre el 1 y el 12
class VentanaMenu:
    
    nivel=0
    
    def __init__(self,nivel):
        self.nivel=nivel
        
        #Si se reinicia el mismo nivel no hace falta elegir otro nuevo
        if(nivel != 0):
            VentanaJuego(self.nivel)
            
        #Creamos la ventana y sus elementos
        else:
            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.set_title("BIENVENIDO")
    
            self.window.set_size_request(500, 500)
            self.window.connect("delete_event", self.delete_event)
            
            infile = open('niveles.txt')#abrir los ficheros
            numeroNiveles=int(infile.readline())
            infile.close # Cerramos el fichero.
            
            label = gtk.Label("Introduzca un nivel(min. 1, max. "+str(numeroNiveles)+")")
            label.show()
            
            entrada = gtk.Entry(max=3)
            entrada.show()
            
            boton = gtk.Button("Continuar")
            boton.connect("clicked", self.continuar, entrada)
            boton.show()
            
            gif = gtk.gdk.PixbufAnimation("bienvenida.gif")
            imagen = gtk.Image()
            imagen.set_from_animation(gif)
            imagen.show()
            
            table = gtk.Table(8, 8, gtk.TRUE)
            table.attach(label, 1,7,0,1)
            table.attach(imagen, 0,8,2,5)
            table.attach(entrada, 2,6,1,2)
            table.attach(boton, 3,5,6,7)
            table.show()
            
            self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#F7FFA9"))
            self.window.add(table)
            self.window.show()
    
    def delete_event(self, widget, data=None):
        gtk.main_quit()
        return gtk.FALSE
       
    #Metodo para confirmar el nivel y pasar al juego 
    def continuar(self, widget, data):
        nivel = int(data.get_text())
        if(nivel>0):
            if(nivel<13):
                self.window.destroy()
                VentanaJuego(nivel)

#Ventana del juego
class VentanaJuego:

    #Atributos de la clase
    coches = []
    botones = []
    cochesADibujar = []
    numCochesEsteNivel=0
    nivel=0
    puntos=0
    labelNivel = None
    labelPuntos = None
    table = None
    salir = None
    repetir = None
    lvl = None
    puntuaciones = None

    def __init__(self,nivel):

        #Creamos la ventana y sus elementos
        
        self.nivel=nivel

        self.ficheroAVector(nivel)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("VENTANA DE JUEGO")
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#008A1E"))

        self.window.set_size_request(500, 500)
        self.window.connect("delete_event", self.delete_event)

        self.labelNivel = gtk.Label("Nivel elegido: "+str(nivel))
        self.labelNivel.show()
        
        self.labelPuntos = gtk.Label("Puntos: "+str(self.puntos))
        self.labelPuntos.show()
        
        self.salir = gtk.Button("Salir")
        self.salir.connect("clicked", self.exit, None)
        self.salir.show()
        
        self.repetir = gtk.Button("Volver a empezar")
        self.repetir.connect("clicked", self.reiniciar, nivel)
        self.repetir.show()
        
        self.puntuaciones = gtk.Button("Ver puntuaciones")
        self.puntuaciones.connect("clicked", self.verPuntos, None)
        self.puntuaciones.show()
        
        self.lvl = gtk.Button("Cambiar nivel")
        self.lvl.connect("clicked", self.cambio, None)
        self.lvl.show()

        self.table = gtk.Table(10, 9, gtk.TRUE)
        self.table.attach(self.labelNivel, 6,9,1,2)
        self.table.attach(self.labelPuntos, 6,9,4,5)
        self.table.attach(self.repetir, 1,4,7,8)
        self.table.attach(self.puntuaciones, 1,4,8,9)
        self.table.attach(self.lvl, 5,8,7,8)
        self.table.attach(self.salir, 5,8,8,9)
        
        self.window.add(self.table)
        
        self.pintar(self.window,self.table,self.coches)
        
        self.table.show()
        self.window.show()
     
    #Metodo para cambiar de nivel
    def cambio(self,widget,data):
        self.window.destroy() 
        os.system("Main.py")    #Reiniciamos el programa 
    
    #Metodo que abre la ventana con las puntuaciones
    def verPuntos(self,widget,data):
        VentanaPuntos()
      
    #Metodo para reiniciar el mismo nivel  
    def reiniciar(self,widget,data):
        self.window.destroy()
        os.system("Main.py "+str(self.nivel)) #Reiniciamos el programa con el nivel que estabamos jugando
    
    #Metodo para salir del juego
    def exit(self,widget,data):
        exit(0)

    #Metodo para leer el fichero y pasarlo a un vector
    def ficheroAVector(self,nivel):
        nivel = int(nivel)
        infile = open('niveles.txt') #escoger los datos del nivel
        cochesPorNivel=[]
        lineaActual=0
        contador=0
        acumulador=1
        for line in infile:
            if(lineaActual==acumulador):
                cochesPorNivel.append(int(line))
                acumulador=acumulador+int(line)+1
            lineaActual=lineaActual+1
        infile.close
        
        infile = open('niveles.txt')#abrir los ficheros
        lineaActual=1
        acumulador=2
        for line in infile:
            if(lineaActual==acumulador):
                acumulador=acumulador+int(line)+1
                contador=contador+1
            if(nivel==contador):
                if(len(line)>3):
                    self.coches.append((line)[:4])
            lineaActual=lineaActual+1
            infile.close
        #El vector contiene toda la info del nivel, coches, posiciones etc
    
    #Metodo para pintar el juego, coloca los coches y les asigna una letra a cada uno
    def pintar (self,window,table,vector):
        contador=0
        x=0
        y=0
        id = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        contId = 0
        
        for i in vector:
            index = int((vector[contador])[3:4])
            for j in range (index):
                if(vector[contador][0:1] == "V"):
                    self.cochesADibujar.append(((vector[contador][1:2])+(str((int(vector[contador][2:3]))+x)))+id[contId:contId+1])
                    x=x+1
                else:
                    self.cochesADibujar.append((str((int(vector[contador][1:2]))+y)+(vector[contador][2:3]))+id[contId:contId+1])
                    y=y+1
            x=0
            y=0        
            contId=contId+1
            contador=contador+1
            
        contador = 0
        x=1
        y=1
        contId=0
        for i in range(0, 6):
            for j in range(0, 6):
                s1 = str(x)+str(y)+"A"
                s2 = str(x)+str(y)+"B"
                s3 = str(x)+str(y)+"C"
                s4 = str(x)+str(y)+"D"
                s5 = str(x)+str(y)+"E"
                s6 = str(x)+str(y)+"F"
                s7 = str(x)+str(y)+"G"
                s8 = str(x)+str(y)+"H"
                s9 = str(x)+str(y)+"J"
                s10 = str(x)+str(y)+"K"
                s11 = str(x)+str(y)+"L"
                if(s1 in self.cochesADibujar):
                    button = gtk.Button(s1[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s1)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s2 in self.cochesADibujar):
                    button = gtk.Button(s2[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s2)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s3 in self.cochesADibujar):
                    button = gtk.Button(s3[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s3)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s4 in self.cochesADibujar):
                    button = gtk.Button(s4[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s4)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s5 in self.cochesADibujar):
                    button = gtk.Button(s5[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s5)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s6 in self.cochesADibujar):
                    button = gtk.Button(s6[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s6)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s7 in self.cochesADibujar):
                    button = gtk.Button(s7[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s7)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s8 in self.cochesADibujar):
                    button = gtk.Button(s8[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s8)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1 
                elif(s9 in self.cochesADibujar):
                    button = gtk.Button(s9[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s9)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s10 in self.cochesADibujar):
                    button = gtk.Button(s10[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s10)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1
                elif(s11 in self.cochesADibujar):
                    button = gtk.Button(s11[2:])
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, s11)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1  
                else:
                    button = gtk.Button("")
                    self.botones.append(button)
                    button.connect("clicked", self.botonCrear, None)
                    self.table.attach(button, i, i + 1, j, j + 1)
                    button.show()
                    contador = contador + 1
                    y=y+1    
            
            x=x+1
            y=1
                          
    def delete_event(self, widget, data=None):
        gtk.main_quit()
        return gtk.FALSE

    #Metodo que llama al de mover para los botones que ya se han movido al menos 1 vez
    def botonMover(self, widget, data, mov):
        
        if(data != None):
            self.mover(mov,widget,data)
 
    #Crea los botones y les asigna hacia donde moverse
    def botonCrear(self, widget, data):
        if(data!=None):
            if (data[2:]=="A"):
                if((str((int(data[:2]))-10))+"A" in self.cochesADibujar):
                    self.mover("D",widget,data[:2]) #Derecha
                elif((str((int(data[:2]))+10))+"A" in self.cochesADibujar):
                    self.mover("I",widget,data[:2]) #Izquierda
                elif((str((int(data[:2]))-1))+"A" in self.cochesADibujar):
                    self.mover("A",widget,data[:2]) #Abajo
                elif((str((int(data[:2]))+1))+"A" in self.cochesADibujar):
                    self.mover("U",widget,data[:2]) #Arriba (up)
                    
            if (data[2:]=="B"):
                if((str((int(data[:2]))-10))+"B" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"B" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"B" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"B" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="C"):
                if((str((int(data[:2]))-10))+"C" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"C" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"C" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"C" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="D"):
                if((str((int(data[:2]))-10))+"D" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"D" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"D" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"D" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
                    
            if (data[2:]=="E"):
                if((str((int(data[:2]))-10))+"E" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"E" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"E" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"E" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
                    
            if (data[2:]=="F"):
                if((str((int(data[:2]))-10))+"F" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"F" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"F" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"F" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="G"):
                if((str((int(data[:2]))-10))+"G" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"G" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"G" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"G" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
                    
            if (data[2:]=="H"):
                if((str((int(data[:2]))-10))+"H" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"H" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"H" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"H" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
                    
            if (data[2:]=="I"):
                if((str((int(data[:2]))-10))+"I" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"I" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"I" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"I" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="J"):
                if((str((int(data[:2]))-10))+"J" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"J" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"J" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"J" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="K"):
                if((str((int(data[:2]))-10))+"K" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"K" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"K" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"K" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
            
            if (data[2:]=="L"):
                if((str((int(data[:2]))-10))+"L" in self.cochesADibujar):
                    self.mover("D",widget,data[:2])
                elif((str((int(data[:2]))+10))+"L" in self.cochesADibujar):
                    self.mover("I",widget,data[:2])
                elif((str((int(data[:2]))-1))+"L" in self.cochesADibujar):
                    self.mover("A",widget,data[:2])
                elif((str((int(data[:2]))+1))+"L" in self.cochesADibujar):
                    self.mover("U",widget,data[:2])
     
    #Metodo que mueve los coches cuando clickas en su lateral derecho o izquierdo
    def mover(self,mov,boton,pos):
        
        x=int(pos[0:1])
        y=int(pos[1:2])
        pos = int(pos[:2])-11
          
        if(x==1):
            pos=pos
        elif(x==2):
            pos=pos-4
        elif(x==3):
            pos=pos-8
        elif(x==4):
            pos=pos-12
        elif(x==5):
            pos=pos-16
        elif(x==6):
            pos=pos-20
        
        if(mov == "D"):
            pos=pos+6
            index=0
            if(pos<36):
                self.puntos=self.puntos+1
                if(self.botones[pos].get_label() == ""):
                    for i in self.table:
                        self.table.remove(i)
                        
                    data=str(x+1)+str(y)+self.botones[pos-6].get_label()
                    
                    button = gtk.Button("")
                    button.show()
                    button2 = gtk.Button(self.botones[pos-6].get_label())
                    button2.connect("clicked",self.botonMover, data, "D")
                    button2.show()
                    self.botones[pos]=button2
                    self.botones[pos-6]=button
                    pos=pos-6
                    
                    if(self.botones[pos+6].get_label() == self.botones[pos-6].get_label() and pos>0):
                        data=str(x)+str(y)+self.botones[pos-6].get_label()

                        button = gtk.Button("")
                        button.show()
                        button2 = gtk.Button(self.botones[pos-6].get_label())
                        button2.connect("clicked",self.botonMover, data, "I")
                        button2.show()
                        self.botones[pos]=button2
                        self.botones[pos-6]=button
                        pos=pos-6
                    
                        if(self.botones[pos-6].get_label() == self.botones[pos+6].get_label() and pos>0):
                            data=str(x-1)+str(y)+self.botones[pos-6].get_label()
                            
                            button = gtk.Button("")
                            button.show()
                            button2 = gtk.Button(self.botones[pos-6].get_label())
                            button2.connect("clicked",self.botonMover, data, "I")
                            button2.show()
                            self.botones[pos]=button2
                            self.botones[pos-6]=button
                    
                    self.cochesADibujar.append(str(x)+str(y)+button2.get_label())
                    for j in range(0,6):
                        for k in range(0,6):
                            self.table.attach(self.botones[index], j, j+1, k, k+1)
                            index=index+1
                            
                    self.labelPuntos.set_text("Puntos: "+str(self.puntos))
                    self.table.attach(self.labelNivel, 6,9,1,2)
                    self.table.attach(self.labelPuntos, 6,9,4,5)
                    self.table.attach(self.repetir, 1,4,7,8)
                    self.table.attach(self.puntuaciones, 1,4,8,9)
                    self.table.attach(self.lvl, 5,8,7,8)
                    self.table.attach(self.salir, 5,8,8,9)
                    
                else:
                    print "Ocupado Dcha"
            else:
                if(self.botones[pos-6].get_label()=="A"):
                    self.window.destroy()
                    VentanaWin(self.nivel,self.puntos)
                else:
                    print "Bordes Dcha"
        
        if(mov == "I"):
            pos=pos-6
            index=0
            if(pos>-1):
                self.puntos=self.puntos+1
                if(self.botones[pos].get_label() == ""):
                    for i in self.table:
                        self.table.remove(i)
                        
                    data=str(x-1)+str(y)+self.botones[pos+6].get_label()

                    button = gtk.Button("")
                    button.show()
                    button2 = gtk.Button(self.botones[pos+6].get_label())
                    button2.connect("clicked",self.botonMover, data, "I")
                    button2.show()
                    self.botones[pos]=button2
                    self.botones[pos+6]=button
                    pos=pos+6
                    
                    if(self.botones[pos+6].get_label() == self.botones[pos-6].get_label() and pos>0 and pos<36):
                        data=str(x)+str(y)+self.botones[pos+6].get_label()

                        button = gtk.Button("")
                        button.show()
                        button2 = gtk.Button(self.botones[pos+6].get_label())
                        button2.connect("clicked",self.botonMover, data, "D")
                        button2.show()
                        self.botones[pos]=button2
                        self.botones[pos+6]=button
                        pos=pos+6
                    
                        if(pos+6<36):
                            
                            if(self.botones[pos-6].get_label() == self.botones[pos+6].get_label() and pos>0):
                                data=str(x+1)+str(y)+self.botones[pos+6].get_label()
                                
                                button = gtk.Button("")
                                button.show()
                                button2 = gtk.Button(self.botones[pos+6].get_label())
                                button2.connect("clicked",self.botonMover, data, "D")
                                button2.show()
                                self.botones[pos]=button2
                                self.botones[pos+6]=button
                    
                    self.cochesADibujar.append(str(x)+str(y)+button2.get_label())
                    for j in range(0,6):
                        for k in range(0,6):
                            self.table.attach(self.botones[index], j, j+1, k, k+1)
                            index=index+1
                            
                    self.labelPuntos.set_text("Puntos: "+str(self.puntos))
                    self.table.attach(self.labelNivel, 6,9,1,2)
                    self.table.attach(self.labelPuntos, 6,9,4,5)
                    self.table.attach(self.repetir, 1,4,7,8)
                    self.table.attach(self.puntuaciones, 1,4,8,9)
                    self.table.attach(self.lvl, 5,8,7,8)
                    self.table.attach(self.salir, 5,8,8,9)
        
                else:
                    print "Ocupado Izqda"
            else:
                if(self.botones[pos+6].get_label()=="A"):
                    self.window.destroy()
                    VentanaWin(self.nivel,self.puntos)
                print "Bordes Izqda"
                
        if(mov == "A"):
            pos=pos+1
            index=0
            if(pos != 6 and pos != 12 and pos != 18 and pos != 24 and pos != 30 and pos !=36):
                self.puntos=self.puntos+1
                if(self.botones[pos].get_label() == ""):
                    for i in self.table:
                        self.table.remove(i)
                        
                    data=str(x)+str(y+1)+self.botones[pos-1].get_label()

                    button = gtk.Button("")
                    button.show()
                    button2 = gtk.Button(self.botones[pos-1].get_label())
                    button2.connect("clicked",self.botonMover, data, "A")
                    button2.show()
                    self.botones[pos]=button2
                    self.botones[pos-1]=button
                    pos=pos-1
                    
                    if(self.botones[pos-1].get_label() == self.botones[pos+1].get_label() and pos>0):
                        data=str(x)+str(y)+self.botones[pos-1].get_label()

                        button = gtk.Button("")
                        button.show()
                        button2 = gtk.Button(self.botones[pos-1].get_label())
                        button2.connect("clicked",self.botonMover, data, "U")
                        button2.show()
                        self.botones[pos]=button2
                        self.botones[pos-1]=button
                        pos=pos-1
                    
                        if(self.botones[pos-1].get_label() == self.botones[pos+1].get_label() and pos>0):
                            data=str(x)+str(y-1)+self.botones[pos-1].get_label()
                            
                            button = gtk.Button("")
                            button.show()
                            button2 = gtk.Button(self.botones[pos-1].get_label())
                            button2.connect("clicked",self.botonMover, data, "U")
                            button2.show()
                            self.botones[pos]=button2
                            self.botones[pos-1]=button
                    
                    self.cochesADibujar.append(str(x)+str(y)+button2.get_label())
                    for j in range(0,6):
                        for k in range(0,6):
                            self.table.attach(self.botones[index], j, j+1, k, k+1)
                            index=index+1
                            
                    self.labelPuntos.set_text("Puntos: "+str(self.puntos))
                    self.table.attach(self.labelNivel, 6,9,1,2)
                    self.table.attach(self.labelPuntos, 6,9,4,5)
                    self.table.attach(self.repetir, 1,4,7,8)
                    self.table.attach(self.puntuaciones, 1,4,8,9)
                    self.table.attach(self.lvl, 5,8,7,8)
                    self.table.attach(self.salir, 5,8,8,9)
                    
                else:
                    print "Ocupado Abajo"
            else:
                print "Bordes Abajo"
                
        if(mov == "U"):
            pos=pos-1
            index=0
            if(pos >= 0 and pos != 5 and pos != 11 and pos != 17 and pos !=23 and pos != 29):
                self.puntos=self.puntos+1
                if(self.botones[pos].get_label() == ""):
                    for i in self.table:
                        self.table.remove(i)
                        
                    data=str(x)+str(y-1)+self.botones[pos+1].get_label()

                    button = gtk.Button(".")
                    button.show()
                    button2 = gtk.Button(self.botones[pos+1].get_label())
                    button2.connect("clicked",self.botonMover, data, "U")
                    button2.show()
                    self.botones[pos]=button2
                    self.botones[pos+1]=button
                    pos=pos+1
                    
                    if(self.botones[pos+1].get_label() == self.botones[pos-1].get_label() and pos>0):
                        data=str(x)+str(y)+self.botones[pos-1].get_label()

                        button = gtk.Button("")
                        button.show()
                        button2 = gtk.Button(self.botones[pos+1].get_label())
                        button2.connect("clicked",self.botonMover, data, "A")
                        button2.show()
                        self.botones[pos]=button2
                        self.botones[pos+1]=button
                        pos=pos+1
                    
                        if(pos+1<36):
                            if(self.botones[pos+1].get_label() == self.botones[pos-1].get_label() and pos>0):
                                data=str(x)+str(y+1)+self.botones[pos+1].get_label()
                                
                                button = gtk.Button("")
                                button.show()
                                button2 = gtk.Button(self.botones[pos+1].get_label())
                                button2.connect("clicked",self.botonMover, data, "A")
                                button2.show()
                                self.botones[pos]=button2
                                self.botones[pos+1]=button
                    
                    self.cochesADibujar.append(str(x)+str(y)+button2.get_label())
                    for j in range(0,6):
                        for k in range(0,6):
                            self.table.attach(self.botones[index], j, j+1, k, k+1)
                            index=index+1
                        
                    self.labelPuntos.set_text("Puntos: "+str(self.puntos))
                    self.table.attach(self.labelNivel, 6,9,1,2)
                    self.table.attach(self.labelPuntos, 6,9,4,5)
                    self.table.attach(self.repetir, 1,4,7,8)
                    self.table.attach(self.puntuaciones, 1,4,8,9)
                    self.table.attach(self.lvl, 5,8,7,8)
                    self.table.attach(self.salir, 5,8,8,9)
                
                else:
                    print "Ocupado Arriba"
            else:
                print "Bordes Arriba"

#Ventana para cuando ganas                
class VentanaWin:
    
    nivel=0
    puntos=0
            
    def __init__(self,nivel,puntos):
        #Creamos la ventana y sus elementos
        
        self.nivel=nivel
        self.puntos=puntos
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("FIN DEL JUEGO")

        self.window.set_size_request(500, 500)
        self.window.connect("delete_event", self.delete_event)
    
        label = gtk.Label("ENHORABUENA!! HAS CONSEGUIDO: "+str(self.puntos)+" PUNTOS")
        label.show()
    
        caja = gtk.EventBox()
        caja.add(label)
        caja.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        caja.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        caja.show()
        
        gif = gtk.gdk.PixbufAnimation("win.gif")
        imagen = gtk.Image()
        imagen.set_from_animation(gif)
        imagen.show()
        
        label2 = gtk.Label("SALIR")
        label2.show()
    
        caja2 = gtk.EventBox()
        caja2.add(label2)
        caja2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        caja2.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("black"))
        caja2.modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("black"))
        caja2.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("black"))
        caja2.modify_bg(gtk.STATE_INSENSITIVE, gtk.gdk.color_parse("black"))
        caja2.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        caja2.get_child().modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("red"))
        caja2.get_child().modify_fg(gtk.STATE_SELECTED, gtk.gdk.color_parse("red"))
        caja2.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("red"))
        caja2.get_child().modify_fg(gtk.STATE_INSENSITIVE, gtk.gdk.color_parse("red"))
        caja2.show()
        
        salir = gtk.Button()
        salir.connect("clicked",self.salir, None)
        salir.set_relief(gtk.RELIEF_NONE)
        salir.add(caja2)
        salir.show()
        
        label3 = gtk.Label("VOLVER A EMPEZAR")
        label3.show()
        
        caja3 = gtk.EventBox()
        caja3.add(label3)
        caja3.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        caja3.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("black"))
        caja3.modify_bg(gtk.STATE_SELECTED, gtk.gdk.color_parse("black"))
        caja3.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("black"))
        caja3.modify_bg(gtk.STATE_INSENSITIVE, gtk.gdk.color_parse("black"))
        caja3.get_child().modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        caja3.get_child().modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("green"))
        caja3.get_child().modify_fg(gtk.STATE_SELECTED, gtk.gdk.color_parse("green"))
        caja3.get_child().modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("green"))
        caja3.get_child().modify_fg(gtk.STATE_INSENSITIVE, gtk.gdk.color_parse("green"))
        caja3.show()
        
        restart = gtk.Button()
        restart.connect("clicked",self.empezar, None)
        restart.set_relief(gtk.RELIEF_NONE)
        restart.add(caja3)
        restart.show()
        
        table = gtk.Table(10, 10, gtk.TRUE)
        table.attach(caja, 0,10,0,2)
        table.attach(imagen, 0,10,2,7)
        table.attach(salir, 1,4,7,9)
        table.attach(restart, 5,8,7,9)
        table.show()
        
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.window.add(table)
        self.window.show()
        
        self.guardar()
    
    #Metodo para volver a empezar
    def empezar(self,widget,data):
        self.window.destroy()
        os.system("Main.py") #Reiniciamos el programa
         
         
    #Metodo para guardar los puntos en el fichero
    def guardar(self):
        fichero = []
                
        if(os.path.exists("records.txt")):
            infile = open("records.txt","r")
            for i in infile:
                if(i[14:15]=="1" and i[15:16] != " "):
                    if (str(self.nivel) == i[14:16]):
                        if(int(i[19:]) == 0):
                            fichero.append("Puntos nivel: "+str(self.nivel)+" = "+str(self.puntos)+"\n")
                        elif(self.puntos<int(i[19:])):
                            fichero.append("Puntos nivel: "+str(self.nivel)+" = "+str(self.puntos)+"\n")
                        else:
                            fichero.append(i)
                    else: 
                        fichero.append(i)
                else:
                    if (str(self.nivel) == i[14:15]):
                        if(int(i[18:]) == 0):
                            fichero.append("Puntos nivel: "+str(self.nivel)+" = "+str(self.puntos)+"\n")
                        elif(self.puntos<=int(i[18:])):
                            fichero.append("Puntos nivel: "+str(self.nivel)+" = "+str(self.puntos)+"\n")
                        else:
                            fichero.append(i)
                            
                    else: 
                        fichero.append(i)

            wfile = open("records.txt","w")
            for i in range(0,12):
                wfile.write(fichero[i])
            wfile.close()
            
        else:
            wfile = open("records.txt","w")
            for i in range(0,12):
                wfile.write("Puntos nivel: "+str(i+1)+" = 0\n")
            wfile.close()
            self.guardar     
    #Metodo para salir del programa
    def salir(self,widget,data):
        self.window.destroy()
        exit(0)
    
    def delete_event(self, widget, data=None):
        gtk.main_quit()
        return gtk.FALSE

#Ventana que muestra las puntuaciones            
class VentanaPuntos:
    
    vectorPuntos = []
    
    def __init__(self):
        
        #Creamos la ventana y sus elementos
        self.ficheroAVector()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("PUNTUACIONES")

        self.window.set_size_request(500, 500)
        self.window.connect("delete_event", self.delete_event)
    
        label = gtk.Label("ENHORABUENA!!")
        label.show()
        
        table = gtk.Table(8, 4, gtk.TRUE)
        
        table.show()
        
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#64C7FF"))
        self.window.add(table)
        self.window.show()
        
        self.pintar(table)
      
    #Metodo que pinta la ventana           
    def pintar(self,table):
        index=0
        for i in range(1,3):
            for j in range(1,7):
                label = gtk.Label(self.vectorPuntos[index])
                label.show()
                index=index+1
                table.attach(label, i, i+1, j, j+1)
    #Metodo que pasa el fichero a un vector                
    def ficheroAVector(self):
        if(os.path.exists("records.txt")):
            infile = open("records.txt","r")
            for i in infile:
                self.vectorPuntos.append(i)
        else:
            for i in range(0,12):
                self.vectorPuntos.append("Puntos nivel:"+str(i)+" = 0")
               
    def delete_event(self, widget, data=None):
        self.window.destroy()
     
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    if(len(argv)==1):
        VentanaMenu(0)
        main()
    else:
        VentanaMenu(argv[1])
        main()