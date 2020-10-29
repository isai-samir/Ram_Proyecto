#Equipo 
# Isai Samir Hernandez Lira
# Ruben Padilla

from random import choice

MAX_SIZE = 40

class Proceso:
    def __init__(self,id,size,estado):
        self.id = id
        self.size = size
        self.estado = estado
    def __str__(self):
        return "Id: %s, Tamaño: %d, Estado: %s"%(self.id,self.size,self.estado)

class DatoLista:
    def __init__(self):
        self.estado = 'H'
        self.posicionI = 0
        self.tamaño = 0
    
    def __str__(self):
        return "|%c|%d|%d|"%(self.estado,self.posicionI,self.tamaño)

class Nodo:
    def __init__(self):
        self.datoL = DatoLista()
        self.siguiente = None

class ListaLibre:
    def __init__(self):
        self.cabeza = None
    
    def mostrar(self):
        if self.cabeza != None:
            actual = self.cabeza
            print(actual.datoL,end="")
            actual = actual.siguiente
            while actual != None:
                print("->",actual.datoL,end="")
                actual = actual.siguiente
        print()

    def generarLista(self,procesos):
        tamaño = 0
        actual = self.cabeza = None
        for i in range(len(procesos)):
            nuevo = Nodo()
            if procesos[i].id == '@':
                nuevo.datoL.estado = 'H'
            else:
                nuevo.datoL.estado = 'P'
            nuevo.datoL.posicionI = tamaño
            nuevo.datoL.tamaño = procesos[i].size
            tamaño += procesos[i].size
            if self.cabeza == None:
                self.cabeza = nuevo
                actual = self.cabeza
            else:
                actual.siguiente = nuevo
                actual = actual.siguiente

def mapaBits(procesos):
    mapa = []
    suma = 0
    for i in range(len(procesos)):
        if procesos[i].id == '@':
            for _ in range(procesos[i].size):
                mapa.append(0)
                suma += 1
        else:
            for _ in range(procesos[i].size):
                mapa.append(1)
                suma += 1
    for _ in range(suma,MAX_SIZE,1):
        mapa.append(0)
    for i in range(len(mapa)):
        if i%10 == 0:
            print(" ")
        print(mapa[i],end=" ")
    print("\n")

def compactacion(procesos):
    i = 0
    print("Compactacion")
    while i < len(procesos) - 1:
        if procesos[i].id == '@': procesos.pop(i)
        else: i += 1

def agregar2(procesos,id,size,tamaño,estadoProceso):
    if tamaño+size > MAX_SIZE:
        return False
    if len(procesos) == 0:
        procesos.append(Proceso(id,size,estadoProceso))
        return True
    bandera = False
    for i in range(len(procesos)):
        if procesos[i].id == '@':
            if procesos[i].size == size:
                procesos[i].estado = estadoProceso
                procesos[i].id = id
                return True
            elif procesos[i].size > size:
                procesos[i].id = id
                procesos[i].estado = estadoProceso
                procesos.insert(i+1,Proceso('@',procesos[i].size - size,"null"))
                procesos[i].size = size
                return True
    if not bandera:
        casillas = 0
        for i in procesos:
            casillas += i.size
        if casillas + size > MAX_SIZE:
            compactacion(procesos)
        procesos.append(Proceso(id,size,estadoProceso))
        return True
    return bandera

def agregarElemntos(procesos,tamaño,hdd,id2,tamProceso,estadoProceso):
    if not agregar2(procesos,id2,tamProceso,tamaño,estadoProceso):
        #RAM llena
        tamHDD = 0
        for proceso in hdd: 
            if proceso.id != '@': tamHDD += proceso.size
        if estadoProceso != "Ejecucion":
            if not agregar2(hdd,id2,tamProceso,tamHDD,estadoProceso):
                print("\tNo se pudo agregar a RAM ni a HDD 1")
                return tamaño   
            else: print("\tSe agrego el proceso",id2," al disco HDD 1")
            return tamaño
        #Mover un proceso de RAM a HDD
        print("mover a hdd proceso")
        disponibleHDD = MAX_SIZE - tamHDD
        disponibleRAM = MAX_SIZE - tamaño
        disponibleAMover = 0
        print("Disponible RAM ",disponibleRAM," Disponible HDD ",disponibleHDD)
        for i in range(len(procesos)):
            if procesos[i].estado == "Listo" or procesos[i].estado == "Espera":
                #Mover un elemento a hdd
                if procesos[i].size + disponibleRAM >= tamProceso and procesos[i].size <= disponibleHDD:
                    print("Se movio ",procesos[i].id," a HDD 1.5")
                    agregar2(hdd,procesos[i].id,procesos[i].size,tamHDD,procesos[i].estado)
                    tamaño -= procesos[i].size
                    borrarProceso(procesos[i].id,procesos)
                    agregar2(procesos,id2,tamProceso,tamaño,estadoProceso)
                    print("Se agrego el proceso ",id2," a la RAM 2")
                    return tamaño + tamProceso
                else: disponibleAMover += procesos[i].size
        print("Mover a hdd varios ",disponibleAMover)
        if disponibleAMover >= tamProceso:
            disponibleAMover = 0
            for i in range(len(procesos)):
                if procesos[i].estado == "Listo" or procesos[i].estado == "Espera":
                    disponibleAMover += procesos[i].size
                    if disponibleAMover + disponibleRAM >= tamProceso:
                        j = k = 0
                        while k <= i:
                            print(j)
                            if procesos[j].estado == "Listo" or procesos[j].estado == "Espera":
                                print("Se movio ",procesos[j].id," a HDD 3")
                                agregar2(hdd,procesos[j].id,procesos[j].size,tamHDD,procesos[j].estado)
                                tamHDD += procesos[j].size
                                tamaño -= procesos[j].size
                                borrarProceso(procesos[j].id,procesos)
                            else: j +=1
                            k += 1
                        agregar2(procesos,id2,tamProceso,tamaño,estadoProceso)
                        print("\tSe agrego el proceso ",id2," a la RAM 3")
                        return tamaño + tamProceso
        else: 
            print("\tNo se pudo agregar RAM y HDD LLeno")
            return tamaño
    print("\tSe agrego el proceso ",id2," a la RAM 4")
    return tamaño + tamProceso

def fromRAMtoHDD(id_to_move,hdd,procesos):
    for proceso in procesos:
        if proceso.id == id_to_move:
            print("Proceso encontrado")
            if proceso.estado != "Ejecucion":
                actual = 0
                for i in hdd:
                    if i.id != '@': actual += i.size
                if agregar2(hdd,id_to_move,proceso.size,actual,proceso.estado):
                    tamaño = proceso.size
                    borrarProceso(id_to_move,procesos)
                    return tamaño
            else: 
                print("No se puede mover un proceso en estado de Ejecucion")
                return 0
    return 0

def fromHDDtoRAM(id_to_move,hdd,procesos,actual):
    for proceso in hdd:
        if proceso.id == id_to_move:
            tam = proceso.size
            if agregar2(procesos,id_to_move,proceso.size,actual,proceso.estado):
                borrarProceso(id_to_move,hdd)
                return tam
            else:
                print("No hay espacio disponible en RAM")
                return 0
    return 0

def borrarProceso(id_to_delet, procesos):
    for i in range(len(procesos)):
        if procesos[i].id == id_to_delet:
            procesos[i].id = '@'
            procesos[i].estado = "null"
            tam = procesos[i].size
            try:
                if i+1 == len(procesos):
                    if procesos[i-1].id == '@':
                        procesos.pop(i)
                        procesos.pop(i-1)
                    else:
                        procesos.pop(i)
                if procesos[i+1].id == '@':
                    procesos[i].size += procesos[i+1].size
                    procesos.pop(i+1)
                if procesos[i-1].id == '@':
                    procesos[i].size += procesos[i-1].size
                    procesos.pop(i-1)
            except IndexError:
                return tam
            return tam
    return 0

def cambiarEstadoUno(procesos,hdd,id2,tamaño):
    #Busca en Ram
    for i in procesos:
        if i.id == id2:
            estado = choice(["Listo","Ejecucion","Espera"])
            print("Estado nuevo ",estado)
            i.estado = estado
            return tamaño
    #Busca en HDD
    for i in range(len(hdd)):
        print("Busca ",id2," es ",hdd[i].id)
        if hdd[i].id == id2:
            estado = choice(["Listo","Ejecucion","Espera"])
            print("Estado nuevo ",estado)
            hdd[i].estado = estado
            if hdd[i].estado == "Ejecucion":
                tam = hdd[i].size
                borrarProceso(hdd[i].id,hdd)
                tamaño = agregarElemntos(procesos,tamaño,hdd,id2,tam,"Ejecucion")
        return tamaño
    print("No existe la id")
    return tamaño

def cambiarEstadoTodos(procesos,hdd,tamaño):
    auxiliarHDD = []
    #Cambia en Ram
    for i in procesos: i.estado = choice(["Listo","Ejecucion","Espera"])
    #Cambiar en HDD
    i = 0
    while i < len(hdd) - 1:
        hdd[i].estado = choice(["Listo","Ejecucion","Espera"])
        if hdd[i].estado == "Ejecucion": auxiliarHDD.append(hdd.pop(i))
        else: i += 1
    for i in auxiliarHDD: tamaño = agregarElemntos(procesos,tamaño,hdd,i.id,i.size,"Ejecucion")
    return tamaño

def mostrar(procesos):
    if len(procesos) == 0:
        print("\tMemoria vacia")
    else:
        for i in range(len(procesos)):
            print("\t",procesos[i])

def paginacion(procesos):
    size_per_page = 5
    if len(procesos) == 0: print("Memoria vacia")
    else:
        i = 0
        max1 = 0
        pag = 1
        for proceso in procesos:
            tam = proceso.size
            for _ in range(tam):
                if i == size_per_page:
                    print("Pagina ",pag)
                    i = 0
                    pag += 1
                print(f"[{proceso.id}]",end=" ")
                i += 1
                max1 +=1
        while max1 != MAX_SIZE:
            if i == size_per_page:
                print("Pagina ",pag)
                i = 0
                pag += 1
            print("[@]",end=" ")
            i += 1
            max1 +=1
        print("Pagina ",pag)
    print()

if __name__ == "__main__":
    procesos = []
    hdd = []
    lista = ListaLibre()
    actualSize = 0
    while(True):
        ocupadoHdd = 0
        for i in hdd: 
            if i.id != '@': ocupadoHdd += i.size
        print("\tTamaño ocupado en RAM ",actualSize)
        print("\tTamaño ocupado en HDD ",ocupadoHdd)
        print("1.- Crear Proceso")
        print("2.- Ver Ram")
        print("3.- Ver Paginacion")
        print("4.- Ver HDD")
        print("5.- Representacion RAM")
        print("6.- Intercambio")
        print("7.- Cambiar estados")
        print("8.- Mostrar Procesos")
        print("9.- Salir ",end="")
        menu = int(input())
        #Crear proceso
        if menu == 1:
            bandera = True
            print("Ingresa identificador del proceso: ", end="")
            id2 = input()
            for i in procesos:
                if i.id == id2:
                    print("Ya hay un porceso con el mismo id")
                    bandera = False
                    break
            for i in hdd:
                if i.id == id2:
                    print("Ya hay un porceso con el mismo id")
                    bandera = False
                    break
            if bandera:
                estadoProceso = choice(["Listo","Ejecucion","Espera"])
                print("Estado ",estadoProceso)
                print("Ingresa el tamaño del proceso: ", end="")
                tamProceso = int(input())
                if tamProceso <= 1 or tamProceso >= MAX_SIZE: print("\tTamaño invalido")
                else:
                    actualSize = agregarElemntos(procesos,actualSize,hdd,id2,tamProceso,estadoProceso)
        #Ver RAM
        elif menu == 2: mostrar(procesos)
        #Ver Paginacion
        elif menu == 3:
            paginacion(procesos)
        #Ver Hdd
        elif menu == 4: mostrar(hdd)
        #Representacion de RAM
        elif menu == 5: 
            print("\t1.-Mapa de bits")
            print("\t2.-Listas Libres",end=" ")
            opcion = int(input())
            if opcion == 1: mapaBits(procesos)
            elif opcion == 2:
                lista.generarLista(procesos)
                lista.mostrar()
        #Intercambio de procesos
        elif menu == 6: 
            print("\t1.-Pasar proceso de RAM a HDD")
            print("\t2.-Pasar proceso de HDD a RAM")
            opc =  int(input('Opcion deseada: '))
            if opc == 1:
                if len(procesos) == 0 :
                    print("Memoria RAM sin procesos")
                else:
                    mostrar(procesos)
                    id_to_move = input('Ingresa el ID del proceso a mover a HDD: ')
                    t = fromRAMtoHDD(id_to_move,hdd,procesos)
                    if t > 0:
                        print("Proceso movido")
                        actualSize -= t
                    else: 
                        print("No se pudo mover el proceso")
            elif opc ==2:
                if len(hdd) == 0:
                    print("El Disco esta vacio. Intente agregar un proceso desde RAM")
                else:
                    mostrar(hdd)
                    id_to_move = input('Ingresa el ID del proceso a mover a RAM: ')
                    t = fromHDDtoRAM(id_to_move,hdd,procesos,actualSize)
                    if t > 0:
                        actualSize += t
                        print("Proceso movido")
                    else:
                        print("No se pudo mover el proceso")
            else:
                print("Opcion invalida")
        #Cambiar Estados
        elif menu == 7:
            print("1.- Cambiar un Proceso")
            print("2.- Cambiar todos los procesos ",end=" ")
            opc = int(input())
            if opc == 1: #Cambiar un proceso
                print("Da el PID del proceso ",end="")
                pid = input()
                actualSize = cambiarEstadoUno(procesos,hdd,pid,actualSize)
            #Cambiar todos los procesos
            elif opc == 2: actualSize = cambiarEstadoTodos(procesos,hdd,actualSize)
            else: print("\tOpcion incorrecta")
        #Mostrar Procesos
        elif menu == 8:
            print("Memoria RAM")
            mostrar(procesos)
            print("Almacenamiento HDD")
            mostrar(hdd)
        #Salir
        elif menu == 9:
            print("\t\tGracias por usar este programa")
            break
        else: print("\tOpcion incorrecta, de otra")