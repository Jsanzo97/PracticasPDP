#Autores: Jose Manuel Illan Cuadrado y Jorge sanzo Hernando
#Grupo T3, segunda entrega
#Realizado en Eclipse Mars.2 (4.5.2) en Windows

#Introduccion: El programa consta de 4 clases distintas(una por cada ventana creada) que se iran
#mostrando segun se ejecute, al final del codigo se encuentra el main que efectua las llamadas a
#las ventanas y guarda y actualiza el fichero de puntos
#NOTA: La transicion entre ventanas puede resultar un poco lenta a veces y tenemos una excepcion que salta cuando hemos ganado 
#pero no nos influye en nada del programa y no sabemos que la produce ni como eliminarla puesto que no genera errores al ejecutar

#Importamos los modulos necesarios
from Tkinter import *
import random
import math

class VentanaLvL():
    #Esta clase almacena una ventana en la cual el usuario debe introducir el nivel de dificultada
    #que desea jugar
    def __init__(self):
        
        self.ventana = Tk() #Creamos la ventana
        self.ventana.title("Juego by Jorge & Chema") #Titulo de la ventana
        self.ventana.geometry("700x450+300+50") #Dimension y colocacion de la ventana
        self.ventana.config(bg="black") #Ponemos el fondo de la ventana en negro
        
        self.etiqueta = Label (self.ventana, text= "Introduzca el nivel",font=("Ravie",18)) #Etiqueta que pide que se introduzca el nivel
        self.etiqueta.config(bg="black",fg="white") #Ponemos fondo negro y letra blanca
        self.etiqueta.pack() #Finalizamos esta etiqueta
        
        self.entrada_texto = Entry(self.ventana, width=10) #Creamos un campo de escritura donde se introduce el nivel
        self.entrada_texto.pack() #Finalizamos el campo de entrada
        
        self.ok = Button (self.ventana, text="OK", command= self.leer_nivel,cursor="hand2") #Creamos un boton y le asiganamos el metodo 'leer_nivel' cuando sea clickado
        self.ok.config(bg="grey",fg="black") #Ponemos fondo gris y letra negra
        self.ok.pack() #Finalizamos boton
        
        #Creamos etiqueta que muestre el objetivo del juego
        self.etiqueta2 = Label (self.ventana, text= "OBJETIVO: Trate de dejar todo el tablero \n lleno de puntos , su objetivo sera \n eliminar todas las X \n clicando en ellas.",font=("Ravie",12))
        self.etiqueta2.config(bg="black",fg="white") #Ponemos fondo negro y letra blanca
        self.etiqueta2.pack() #Finalizamos etiqueta
        
        self.gif=[None] #Creamos una lista vacia
        for n in range(44):
            self.gif.append(PhotoImage (file= "welcome.gif", format="gif -index "+str(n)))
            #EL bucle anade a la lista gif los distintos 'fragmentos' en forma de imagen que contiene
            #la animacion que queremos colocar, tenemos una lista de imagenes
        
        self.etiqueta_welcome = Label(self.ventana ,text="") #Creamos una etiqueta sin texto que contendra nuestra animacion
        self.etiqueta_welcome.pack() #Finalizamos la etiqueta
        
        self.welcome() #Llamada al metodo welcome
        
    def welcome(self):
        #Este metodo actualiza la imagen que se muestra en la etiqueta recorriendo la lista de
        #imagenes anterior, de esta manera llamamos de forma recursiva a esta funcion cada 0.08 segundos
        #creando asi una animacion de bienvenida
        global i
        
        i=i+1       #Nuestra lista tiene 44 elementos, si se llega al ultimo se empieza de 0
        if i>44:    #creando asi una animacion 'infinita'
            i=0
        
        self.etiqueta_welcome.configure(image=self.gif[i]) #Actualizamos la imagen de la etiqueta
        self.ventana.after(80,self.welcome) #Establecemos el tiempo (milisegundos) tras el que se llamara otra vez a la misma funcion
        
    def leer_nivel(self):
        #Este metodo asignado al boton anterior recoge el nivel introducido por el usuario
        global dificultad
        global listapuntos
        
        dificultad=int(self.entrada_texto.get()) #Recogemos el nivel en forma de entero
        if dificultad<0:
            dificultad=int(math.sqrt(dificultad*dificultad)) #Si introduce un negativo tomamos su modulo positivo
        
        if dificultad==0: #Si introduce un 0 en la dificultad jugaremos el nivel 1 por defecto
            dificultad=1
        
        listapuntos=[0]*dificultad #Creamos una lista de tantos ceros como nivel haya introducido que sera necesaria mas adelante
        #para guardar cada puntuacion del nivel en su posiocion correcta
        
        self.salir() #Llamamos al metodo salir
    
    def salir(self):
        #Destruimos la ventana y el programa continua
        self.ventana.destroy()
        
    def abrir(self):
        #Bucle que mantiene abierta la ventana, es el que recibe todos los mensajes de eventos quedandose a la espera siempre hasta que recibe alguno
        self.ventana.mainloop()

class VentanaPlay():
    #Esta clase almacena una ventana que servira cmo tablero de juego
    def __init__(self):
        global dificultad #Es una variable global para pasar el dato de una clase a otra
        
        self.ventana = Tk() #Creamos la ventana
        self.ventana.title('TABLERO') #Titulo de la ventana
        self.ventana.attributes('-fullscreen',TRUE) #Establecemos el modo pantalla completa 
        
        self.listaBotones = [] #Lista que almacenara botones de juego
        self.CreaMatriz() #Llamamos al metodo que dibujara el tablero
                   
    def abrir(self):
        #Bucle que mantiene abierta la ventana, es el que recibe todos los mensajes de eventos quedandose a la espera siempre hasta que recibe alguno
        self.ventana.mainloop()
    
    def Aleatorio (self,m):
        #Metodo que nos devuelve un numero aleatorio entre 2 y 12 
        ran= random.randrange(0,m,1)
        return ran+2
    
    def CreaMatriz(self):
        #Metodo que creara una matriz de botones de 14x14 para tener un marco alrededor del tablero del juego
        n=0 #Variable que ayuda a generar el nivel
        k=0 #Variable que ayuda a generar el nivel
        self.listaCoordenadas=[]
        
        #Dos bucles for van a ir creando la matriz completa , separando el tablero de juego del marco
        for x in range(0,14):
            self.casillas_fila = []
            
            for y in range(0,14):
                if x<12 and x>1 and y<12 and y>1:
                    #Entre el 2 y el 11 creamos los botones de juego con '.', les ponemos color gris cuando son pulsados y utilizamos una funcion lambda como comando a jecutar si son clickados
                    self.boton = Button(self.ventana, width=13, height=3,text=".", command=lambda a=x,b=y: self.modificar(a,b,self.etiquetaPuntos2,listaCoordenadas,k),cursor="hand2",activebackground="grey")
                    self.boton.grid(row=x, column=y) #Les posicionamos en forma de matriz
                    self.casillas_fila.append( self.boton )
                    
                else:
                    #Los que pertenezca al marco seran de color gris y no tandran asignada ninguna funcion
                    self.boton = Button(self.ventana, width=13, height=3, text=" ", bg="grey",cursor="no",activebackground="grey", fg="grey", activeforeground="grey")
                    self.boton.grid(row=x, column=y) #Les posicionamos alrededeor
                    self.casillas_fila.append( self.boton )
                    
            self.listaBotones.append( self.casillas_fila ) #Lista con todos los botones ordenados por posicion
        
        #Definimos los botones del 'menu' del juego
        #El boton deshacer permite deshacer todos los movimientos realizados en ese nivel
        self.botonDeshacer = Button (self.ventana, width=13, height=3, text="Deshacer", bg="green",activebackground="green",cursor="hand2",command=self.deshacer)
        self.botonDeshacer.grid(row=6, column=0)
                
        #El boton cambio permite cambiar de nivel en cualquier momento de la partida
        self.botonCambio = Button (self.ventana, width=13, height=3, text="Cambiar Nivel", bg="brown", activebackground="brown",cursor="hand2",command=self.cambio)
        self.botonCambio.grid(row=9, column=0)
        
        #El boton reiniciar permite reiniciar el mismo nivel en el que se esta jugando       
        self.botonReiniciar = Button (self.ventana, width=13, height=3, text="Reiniciar", bg="purple",activebackground="purple",cursor="hand2",command=self.reiniciar)
        self.botonReiniciar.grid(row=7, column=0)
        
        #EL boton salir finaliza el programa        
        self.botonSalir = Button (self.ventana, width=13, height=3, text="SALIR", bg="red",activebackground="red",cursor="hand2", command=exit)
        self.botonSalir.grid(row=4, column=0)
        
        #EL boton records abre una ventana mostrando los datos del fichero        
        self.botonRecords = Button (self.ventana, width=13, height=3, text="Records", bg="yellow",activebackground="yellow",cursor="hand2", command=self.record)
        self.botonRecords.grid(row=5, column=0)
        
        #El boton nuevo permite iniciar una nueva partida del mismo nivel        
        self.botonNuevo = Button (self.ventana, width=13, height=3, text="NUEVO", bg="blue",activebackground="blue",cursor="hand2", command=self.nuevo)
        self.botonNuevo.grid(row=8, column=0)
        
        #Etiqueta con el texto puntos       
        self.etiquetaPuntos = Label(self.ventana, width=13, height=3, text="Puntos:", bg="grey")
        self.etiquetaPuntos.grid(row=0, column=6)
        
        #Etiqueta que muestra los puntos actuales del nivel, empezando en 0
        self.etiquetaPuntos2 = Label(self.ventana, width=6, height=2, text="0",bg="grey")
        self.etiquetaPuntos2.grid(row=0, column=7)
        
        #Llamamos al metodo modificar con parametros aleatorios n veces 
        while n < dificultad:
            k=1
            self.modificar(self.Aleatorio(10),self.Aleatorio(10),self.etiquetaPuntos2,listaCoordenadas,k)
            n=n+1
        k=0 #Ponemos k=0 para empezar a almacenar las coordenadas seleccionadas una vez generada la matriz aleatoria
    
    def nuevo(self):
        #Metodo que reinicia las variables a su estado inicial para iniciar otra partida del mismo nivel
        global nuevo
        nuevo=1
        global bucle
        bucle=TRUE
        global contador
        contador=0
        
        self.salir() #Salimos de esta ventana
        
    def cambio(self):
        #Metodo que reinicia las variables pero especifica con nuevo=0 que se quiere cambiar de nivel , no inciar un juego nuevo igual
        global nuevo
        nuevo=0
        global bucle
        bucle=TRUE
        global contador
        contador=0
        
        self.salir() #Salimos de esta ventana
        
    def reiniciar(self):
        #Metodo que permite reiniciar l apartida , en el mismo nivel
        #Llamamos al metodo deshacer con todos los elementos de la lista de coordenadas
        global listaCoordenadas
        x=len(listaCoordenadas)
        
        if len(listaCoordenadas)==0:
            None
        
        else:
            while x>0:
                self.deshacer()
                x=x-1
                
    def deshacer(self):
        #Metodo que deshace las jugadas
        global listaCoordenadas
      
        if len(listaCoordenadas)==0: #Si no quedan elementos en la lista no se deshace nada
            None
        
        else:
            i=listaCoordenadas[len(listaCoordenadas)-1] #Guardamos en i el ultimo elemento y le borramos de la lista
            del listaCoordenadas[len(listaCoordenadas)-1]
            
            j=listaCoordenadas[len(listaCoordenadas)-1] #Guardamos en j el penultimo elemento y le borramos de la lista
            del listaCoordenadas[len(listaCoordenadas)-1]
              
            self.deshacer2(j,i,listaCoordenadas) #Llamamos a deshacer2 con i y j que representarian las columnas y filas para deshacer ese golpeo
             
    def deshacer2(self,a,b,listaCoordenadas):
        #Metodo que recibe las coordenadas de la lista y llama a golpe2 con a y b y sus adyacentes
        self.Golpe2(a,b)
        self.Golpe2(a,b+1)
        self.Golpe2(a,b+2)
        self.Golpe2(a,b-1)
        self.Golpe2(a,b-2)
        self.Golpe2(a+1,b)
        self.Golpe2(a+1,b+1)
        self.Golpe2(a+1,b+2)
        self.Golpe2(a+1,b-1)
        self.Golpe2(a+1,b-2)
        self.Golpe2(a+2,b)
        self.Golpe2(a+2,b+1)
        self.Golpe2(a+2,b-1)
        self.Golpe2(a-1,b)
        self.Golpe2(a-1,b+1)
        self.Golpe2(a-1,b+2)
        self.Golpe2(a-1,b-1)
        self.Golpe2(a-1,b-2)
        self.Golpe2(a-2,b)
        self.Golpe2(a-2,b+1)
        self.Golpe2(a-2,b-1)
    
    def Golpe2(self,x,y):
        #Metodo que cambia los '.' por 'X' y viceversa del boton con coordenadas x,y
        if self.listaBotones[x][y]['text'] == '.':
            self.listaBotones[x][y]['text'] = 'X'
        
        else:
            self.listaBotones[x][y]['text'] = '.'
    
    def modificar(self,a,b,etiquetaPuntos2, listaCoordenadas,k):
        #Metodo que modofica el tablero, vinculado a los botones del juego
        #Si k=0 quiere decir que el tablero ya esta generado y empieza a guaradar coordenadas en la lista
        if k==0:
            listaCoordenadas.append(a)
            listaCoordenadas.append(b)
            
        #Llamamos a golpe con las coordenadas a,b y sus adyacentes y la etiqueta que muestra los puntos por pantalla
        self.Golpe(a,b,etiquetaPuntos2)
        self.Golpe(a,b+1,etiquetaPuntos2)
        self.Golpe(a,b+2,etiquetaPuntos2)
        self.Golpe(a,b-1,etiquetaPuntos2)
        self.Golpe(a,b-2,etiquetaPuntos2)
        self.Golpe(a+1,b,etiquetaPuntos2)
        self.Golpe(a+1,b+1,etiquetaPuntos2)
        self.Golpe(a+1,b+2,etiquetaPuntos2)
        self.Golpe(a+1,b-1,etiquetaPuntos2)
        self.Golpe(a+1,b-2,etiquetaPuntos2)
        self.Golpe(a+2,b,etiquetaPuntos2)
        self.Golpe(a+2,b+1,etiquetaPuntos2)
        self.Golpe(a+2,b-1,etiquetaPuntos2)
        self.Golpe(a-1,b,etiquetaPuntos2)
        self.Golpe(a-1,b+1,etiquetaPuntos2)
        self.Golpe(a-1,b+2,etiquetaPuntos2)
        self.Golpe(a-1,b-1,etiquetaPuntos2)
        self.Golpe(a-1,b-2,etiquetaPuntos2)
        self.Golpe(a-2,b,etiquetaPuntos2)
        self.Golpe(a-2,b+1,etiquetaPuntos2)
        self.Golpe(a-2,b-1,etiquetaPuntos2)
        
        #Llamamos al metodo hacer_click
        self.hacer_click(etiquetaPuntos2)
            
    def Golpe(self, x, y, etiquetaPuntos2):
        #Metodo que cambia '.' por 'X' y viceversa y llama al metodo comprobar
        if self.listaBotones[x][y]['text'] == '.':
            self.listaBotones[x][y]['text'] = 'X'
        
        else:
            self.listaBotones[x][y]['text'] = '.'
            
        self.comprobar(etiquetaPuntos2)
                
    def comprobar(self,etiquetaPuntos2):
        #Metodo que recorre toda la matriz para saber si quedan 'X' sin eliminar 
        global cont
        global conta
        cont=0
        
        for i in range(2,12):
            for j in range(2,12):
                if self.listaBotones[i][j]['text']=='X': #Por cada 'x' que encuentra suma 1 al contador
                    cont=cont+1
                
                else:
                    cont=cont+0
                    
        if cont==0: #Si el contador es 0, es decir, no quedan 'X', guardamos en el varible total los puntos obtenidos
            conta=0
            global nuevo
            nuevo=0
            global total
            total=str(self.hacer_click(etiquetaPuntos2))
            
            #Llamamos al metodo puntos
            self.puntos()
                
    def hacer_click(self,etiquetaPuntos2):
        #Metodo que cambia el texto de la etiqueta de los puntos para mostrar los puntos que llevas en ese nivel
        valor = str((self.contador())-dificultad)
        etiquetaPuntos2.config(text=valor)
        
        return valor

    def contador(self):
        #Metodo que cuenta los puntos que llevas en el nivel que se esta jugando 
        global contador
        contador=contador+1
       
        return contador
    
    def salir(self):
        #Metodo que elimina esta ventana
        self.ventana.destroy()
       
    def record(self):
        #Metodo asociado al boton de records que abre la ventana de las puntuaciones
        VentanaRecords().abrir()
    
    def puntos(self):
        #Metodo que guarda los puntos obtenidos en la posicion de la lista equivalente al nivel jugado 
        global listapuntos
        global total
        
        listapuntos[dificultad-1]=total
        
        #Finalizamos esta ventana
        self.ventana.destroy()

class VentanaEnhorabuena():
    #Almacena la ventana que se abre cuando has ganado en el juego
    def __init__(self): 
        global dificultad
        global total
        
        self.ventana = Tk() #Creamos la ventana
        self.ventana.title("ENHORABUENA!!") #Titulo de la ventana
        self.ventana.config(bg="medium sea green") #Color de fondo
        self.ventana.attributes("-fullscreen",TRUE) #Establecemos la pantalla completa
        
        #Etiqueta que nos mostrara un texto
        self.etiqueta = Label (self.ventana, text="Puntos obtenidos en el nivel "+ str(dificultad)+ ":",font=("Ravie",18))
        self.etiqueta.config(bg="medium sea green") #Color etiqueta
        self.etiqueta.pack() #Finalizamos etiqueta
        
        #Etiqueta que nos mostrara los puntos que hayamos obtenido
        self.etiqueta2 = Label (self.ventana, text=str(total),font=("Ravie",18))
        self.etiqueta2.config(bg="medium sea green") #Color etiqueta
        self.etiqueta2.pack() #Finalizamos etiqueta
        
        #Boton para volver a jugar de nuevo
        self.Jugar = Button (self.ventana, text="Volver a jugar",cursor="hand2",command=self.click, bg="goldenrod",activebackground="goldenrod")
        self.Jugar.pack()
        
        #Boton para salir
        self.salir = Button (self.ventana, text="SALIR",cursor="hand2",command=exit, bg="red3",activebackground="red3")
        self.salir.pack()
        
        #Etiqueta con el texto de enhorabuena
        self.enhorabuena= Label (self.ventana, text="ENHORABUENA", font=("Ravie",24))
        self.enhorabuena.config(bg="medium sea green") #Color etiqueta
        self.enhorabuena.pack() #Finalizamos etiqueta
        
        self.gif=[None] #Creamos una lista vacia
        for n in range(0,13):
            #Anadimos a la lista cada uno de los fragmentos de la animacion en forma de imagenes
            self.gif.append(PhotoImage (file= "win.gif", format="gif -index "+str(n)))
        
        #Creamos una lista con colores
        self.colores=["red","white","blue","yellow","brown","orange","green","pink","black"]
        
        #Creamos otra etiqueta sin texto donde ire la animacion
        self.label = Label(self.ventana,text="")
        self.label.config(bg="medium sea green") #Color etiqueta
        self.label.pack() #Finalizamos la etiqueta
        
        self.animation() #Llamamos al metodo animation
        
    def animation(self):
        #Metodo que recorre la lista de imagenes y las va mostrando cada 0.1 segundos creando la animacion
        #Tambien recorre la lista de colores cambiando el color de la etiqueta enhorabuena
        global x
        global y
        
        self.enhorabuena.config(fg=self.colores[y])
        self.label.configure(image=self.gif[x])
        x=x+1
        y=y+1
        
        if x>12:
            x=0
        
        if y>8:
            y=0
        
        self.ventana.after(100,self.animation) #Llamada recursiva a la funcion cada 100 milisegundos
        
    def click(self):
        #Metodo asociado al boton volver a jugar que restablece el bucle principal dle programa permitiendo una nueva partida
        global bucle
        bucle=TRUE
        
        #Cerramos esta ventana
        self.ventana.destroy()
        
    def abrir(self):
        #Bucle que mantiene abierta la ventana, es el que recibe todos los mensajes de eventos quedandose a la espera siempre hasta que recibe alguno
        self.ventana.mainloop()
    
    def salir(self):
        #Metodo que cierra esta ventana
        self.ventana.destroy()
            
class VentanaRecords():
    #Esta clase almacena una ventana que nos muestra los puntos del fichero, los records
    #Si no caben en la pantalla porque hay demasiados niveles, hemos creado una scrollbar para que puedan ver todos
    def __init__(self):
        global listapuntos
        
        self.window=Tk() #Creamos la ventana
        self.window.attributes("-fullscreen",TRUE) #Establecemos el modo de pantalla completa
        self.window.config(bg="skyblue") #Color de fondo
        
        #Etiqueta con texto
        self.label= Label(self.window,text="RECORDS POR NIVEL") 
        self.label.config(bg="skyblue") #Color etiqueta
        self.label.pack() #Finalizamos etiqueta

        #Boton que cierra la ventana para seguir jugando
        self.salir = Button(self.window, text="SALIR", command=self.salir, width=13, height=3, bg="red")
        self.salir.pack() #Finalizamos boton

        #Etiqueta con un salto de linea
        self.label= Label(text="\n")
        self.label.pack() #Finalizamos etiqueta

        #Dividimos la patalla en dos mediante un objeto tipo Canvas para crear la scrollbar en esa parte de la ventana
        self.pantalla = Canvas(self.window) 
        self.pantalla.config(bg="skyblue") #Establecemos color
        
        #Seleccinamos una parte de esa division de la ventana para crear la scrollbar , el resto de la division de la pantalla no se usa
        self.espacio = Frame(self.pantalla) 
        self.espacio.config(bg="skyblue") #Establecemos color
        self.espacio.pack() #Finalizamos el frame
        
        #Creamos la scrollbar que ira de arriba abajo(modo vertical)
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.pantalla.yview)
        self.scrollbar.config(bg="skyblue") #Establecemos color
        self.scrollbar.pack(side="right", fill="y") #La colocamos a la derecha de la pantalla
        
        #Configuramos nuestra division de ventana
        self.pantalla.configure(yscrollcommand=self.scrollbar.set) #Asignamos el comando scrollbar en el eje y , es decir en vertical
        self.pantalla.pack(side="left", fill="both", expand=True) #Colocamos la division de la ventana a la izquierda
        self.pantalla.create_window((4,4), window=self.espacio,tags="frame") #Activamos la scrollbar asignada al frame que habiamos realizado antes
        
        #Configuramos ahora las funciones de la ventana y su division
        self.espacio.bind("<Configure>", lambda x: self.pantalla.configure(scrollregion=self.pantalla.bbox("all"))) #Activamos la zona de scroll en toda la ventana
        self.window.bind("<Down>", lambda x: self.pantalla.yview_scroll(3, 'units')) #Permitimos deslizar hacia abajo 3 unidad
        self.window.bind("<Up>", lambda x: self.pantalla.yview_scroll(-3, 'units')) #Permitimos deslizar hacia arriba -3 unidad
        self.window.bind("<MouseWheel>", lambda x: self.pantalla.yview_scroll(int(-1*(x.delta/40)), "units")) #Permitimos tambien que se pueda deslizar con la ruleta del raton, el valor depende de si deslizmos hacia arriba o hacia abajo la ruleta
        
        #Creamos las etiquetas con los niveles y sus mejores puntuaciones del fichero
        self.labels = [Label(self.espacio,bg="skyblue", text="                                                                                                                                                                                     PUNTOS OBTENIDOS EN EL NIVEL : "+str(i+1)+" = " + str(listapuntos[i])+" PUNTOS \n") for i in range(len(listapuntos))] 
        for l in self.labels:
            l.pack() #Finalizamos todas las etiquetas
        
    def abrir(self):
        #Bucle que mantiene abierta la ventana, es el que recibe todos los mensajes de eventos quedandose a la espera siempre hasta que recibe alguno
        self.window.mainloop()

    def salir(self):
        #Metodo que cierra esta ventana
        self.window.destroy()

#-------------------------MAIN------------------------#

def Actualizar (archi,listapuntos,dificultad):   #Metodo que vuelca los datos del fichero en una lista para comprobar y actualizar despues los puntos    
    archi=open('puntos.txt', 'r')   #Abrimos modo lectura
    x=0
    listapuntos2=archi.readlines()  #Guardamos todo el fichero en una lista
    
    if len(listapuntos2)<=len(listapuntos):                         #Si el fichero es mas pequenio que la lista de niveles del juego
        while x<len(listapuntos2):
            listapuntos[x]=listapuntos2[int(x)].replace('\n',"")    #Eliminamos los saltos de linea en la lista para que no se descoloquen los elementos y se cambien de posicion
            x=x+1                                                   
    else:                                                           #Si es mas pequenia la lista de niveles del juego que el fichero
        while x<len(listapuntos):
            listapuntos[x]=listapuntos2[x].replace('\n',"")         #Eliminamos los saltos de linea en la lista para que no se descoloquen los elementos y se cambien de posicion
            str(listapuntos[x]).replace('\n',"")
            x=x+1
        while x<len(listapuntos2):
            listapuntos.append(listapuntos2[x].replace('\n',""))    #Si nuestro fichero es mas grande que la lista de niveles del juego debemos aniadir los elementos sobrantes a la lista
            str(listapuntos[x]).replace('\n',"")
            x=x+1
              
    archi.close

def Record (listapuntos, archi):   #Metodo que vuelca la lista de niveles y puntos del programa en el fichero comparandoles uno a uno

    archi=open('puntos.txt', 'r')  #Abrimos el fichero modo lectura
    listapuntos2=archi.readlines() #Guardamos en una lista los datos del fichero para compararles
    archi.close()
    
    archi=open('puntos.txt', 'w')  #Abrimos el fichero modo escritura
    x=len(listapuntos)
    
    k=0
    if len(listapuntos2)!=0:                                        #Solo miramos los satos de linea si el fichero no esta vacio
        while k<len(listapuntos2):
            listapuntos2[k]=str(listapuntos2[k]).replace('\n',"")   #Eliminamos los saltos de linea para que no haya errores
            k=k+1
    
    j=0
    while j<len(listapuntos):
        listapuntos[j]=str(listapuntos[j]).replace('\n',"")         #Eliminamos los saltos de linea para que no haya errores
        j=j+1
    
    y=0                                                             
    a=len(listapuntos2)
    
    if len(listapuntos2)<len(listapuntos):              #Si nuestro fichero es mas pequenio que la lista de niveles del juego , aniadimos los que faltan
        while len(listapuntos2)<len(listapuntos):
            listapuntos2.append(listapuntos[a])
            a=a+1
        
    while x>0:  
        
        #Comparamos todos los elementos de la lista de puntos del juego y la del fichero para actualizar los posibles records
        #Si son iguales da igual cual se guarde
        if listapuntos2[y]==listapuntos[y] and listapuntos2[y]!=0 and y<=len(listapuntos2) and len(listapuntos2)==len(listapuntos) and x!=-1:
            listapuntos2[y]=listapuntos[y]
        
        #Si un nivel no se ha jugado y tenemos un cero , guardaremos la puntuacion que se haya obtenido sea cual sea
        elif listapuntos2[y]==0 and len(listapuntos2)!=0 and y<=len(listapuntos2) and len(listapuntos2)==len(listapuntos) and x!=-1:
            listapuntos2[y]=listapuntos[y]
        
        #Si en un nivel se consigue una puntuacion menor se actualiza el record en ese nivel
        elif listapuntos[y]<listapuntos2[y] and listapuntos2[y]!=0 and y<=len(listapuntos2) and len(listapuntos2)==len(listapuntos) and x!=-1:
            listapuntos2[y]=listapuntos[y]
        
        #Si en un nivel se consigue una puntuacion mayor se mantiene la que habia que era menor   
        elif listapuntos[y]>listapuntos2[y] and listapuntos2[y]!=0 and y<=len(listapuntos2) and len(listapuntos2)==len(listapuntos) and x!=-1:
            
            #Si el valor era 0 se guarda la que se obtiene aunque sea mayor , si habia 0 no se habia jugado
            if listapuntos2[y] == '0':
                listapuntos2[y]=listapuntos[y]
            else:
                listapuntos[y]=listapuntos2[y]
        
        y=y+1
        x=x-1
        
    x=len(listapuntos)
    y=0
    while x>0:   #Escribimos en nuestro fichero la lista de puntos ya actualizada
        
        archi.write(str(listapuntos2[y]))
        archi.write('\n')
        listapuntos[y]=listapuntos2[y]
        y=y+1
        x=x-1      
        
    archi.close

archi=open('puntos.txt', 'a')   #Fichero que usaremos para guardar los puntos
archi.close()

#-------Variables externas a las clases necesarias--------
x=0  #Controlara la animacion final
y=0  #Controlara la animacion final
i=0  #Controlara la animacion inicial
listaCoordenadas=[] #Lista vacia que guardara los botones pulsados para poder deshacer o reiniciar
dificultad=0 #Variable global para poder pasar el valor de la dificultad de una clase a otra
cont=1 
total=0 #Variable global que guardara los puntos obtenidos en un nivel , tambien global para pasar el dato de una clase a otra
bucle=TRUE #Controla que se ejecute siempre el programa si no se desea salir o se cierra
nuevo=0 #Variable que nos permitira saber si el usuario quiere un juego nuevo o un cambio de nivel
listapuntos=[] #Lista vacia que guardara los puntos por nivel

while bucle==TRUE:
    listaCoordenadas=[] #Ponemos la lista de coordenadas siempre vacia al inicio
    
    if nuevo==0: #Como esta jugando un juego nuevo se entra en el if reiniciando todas las variables a su estado inicial
        i=0
        k=0
        dificultad=0
        cont=1
        total=0
        VentanaLvL().abrir() #Abrimos la primera ventana que pedira el nivel al usuario
        listapuntos=[0]*dificultad 
        Actualizar(archi,listapuntos,dificultad)  #Pasamos fichero al programa
        contador=0
        bucle=FALSE
    
    if dificultad!=0: #Si la dificultad no es 0 , es decir, ha seleccionado un nivel, abrimos la ventana del juego
        x=0
        y=0
        VentanaPlay().abrir()
        Record(listapuntos,archi) #Guardamos los puntos si es necesario
    
    if dificultad!=0 and contador!=0: #Si ha ganado abrimos la ventana de enhorabuena
        VentanaEnhorabuena().abrir()
