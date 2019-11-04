#!/usr/bin/env python
import datetime

def big_word(frase):
    ''' Recibe un str con una frase y devuelve su palabra mas larga. En caso de haber 2 palabras con el mismo largo, retorna la primera.

    Parameters:
        frase (str): String que se desea obtener la palabra mas larga

    Returns:
        str: palabra mas larga de la frase
    '''

    #orden por largo
    obl = sorted(frase.split(" "), key=len, reverse=True)
    #retorno el primer elemento
    return obl[0] if obl else None

def order_list(lista):
    ''' Recibe una lista de enteros y devuelve la lista ordenada de menor a mayor.
    BigO: n log(n)

    Parameters:
        lista (list): Lista de enteros

    Returns:
        list: lista con sus elementos ordenados de menor a mayor
    '''
    return sorted(lista)

def ordenar_lista(lista):
    ''' Recibe una lista de enteros y devuelve la lista ordenada de menor a mayor sin utilizar el método sorted.

    Parameters:
        lista (list): Lista de enteros

    Returns:
        list: lista con sus elementos ordenados de menor a mayor
    '''
    ordenada = []
    for elemento in range(len(lista)):
        m = min(lista)
        ordenada.append(m)
        lista.remove(m)

    return ordenada

class Aerolinea(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = []

    def __str__(self):
        return self.nombre
    def __repr__(self):
        return self.__str__()

    def add_client(self, nombre):
        ''' Agrega un cliente a la lista de los clientes que pueden ser transportados por la aerolinea.
        
        Parameters:
            nombre (str): Nombre del cliente que se desea agregar.
        '''
        self.clientes.append(nombre)

    def is_client(self, nombre):
        ''' Verifica si la aerolinea puede transportar un cliente.
        
        Parameters:
            nombre (str): Nombre del cliente que se desea comprobar.

        Returns:
            True: En caso de que el cliente se encuentre en la lista de clientes de la aerolínea.
            False: En caso de que el cliente no se encuentre en la lista de clientes de la aerolínea.
        '''
        return True if nombre in self.clientes else None

class Viaje(object):
    MPP = 10    #Monto por paquete

    def __init__(self, aerolinea, cliente, paquetes, fecha):
        self.aerolinea = aerolinea
        self.cliente = cliente
        self.paquetes = paquetes
        self.fecha = fecha if isinstance(fecha, datetime.date) else datetime.datetime.strptime(fecha, '%Y-%m-%d').date()

    def __str__(self):
        return f'Aerolinea: {self.aerolinea} | Cliente: {self.cliente} | Paquetes: {self.paquetes} | Fecha: {self.fecha}'
    def __repr__(self):
        return self.__str__()

    @property
    def monto_recaudado(self):
        ''' Obtiene el total recaudado por un viaje, multiplicando la cantidad de paquetes del viaje por el precio de cada uno de ellos.
        
        Returns:
            int: Total de recaudado por la aerolinea en el viaje.
        '''
        return self.paquetes * self.MPP if self.aerolinea.is_client(self.cliente) else 0

    @property
    def types_ok(self):
        ''' Evalua que todos los tipos de datos del objeto sean correctos.
        
        Returns:
            True: En caso de que todos los tipos de datos sean correctos.
            False: En caso de que algun tipo de dato no sea correcto.
        '''
        if isinstance(self.aerolinea, Aerolinea) and isinstance(self.cliente, str) and isinstance(self.paquetes, int) and isinstance(self.fecha, datetime.date):
            return True
        else:
            return False

class Transportes(object):
    def __init__(self):
        self.viajes = []

    def __str__(self):
        return ", ".join( map(str, self.viajes))
    def __repr__(self):
        return self.__str__()

    def add_viaje(self, viaje):
        ''' Evalua si es posible y en dicho caso, agrega un viaje a los transportes realizados.

        Parameters:
            viaje (Viaje): Objeto de instancia Viaje.
        
        Raises:
            TypeError: En caso que el viaje no sea una instancia de Viaje o que haya un error en los tipos de datos.
            ValueError: En caso que el cliente del viaje no sea 'cliente' de la aerolinea.
        '''
        if not isinstance(viaje, Viaje):
            raise TypeError("El viaje debe ser una instancia de Viaje.")
        if not viaje.types_ok:
            raise TypeError("Error en los tipos de datos")

        if not viaje.aerolinea.is_client(viaje.cliente):
            raise ValueError(f'La aerolinea {viaje.aerolinea.nombre} no puede transportar paquetes del cliente {viaje.cliente}.')

        self.viajes.append(viaje)

    def recaudado_por_fecha(self, aerolinea, fecha):
        ''' Informa la cantidad de paquetes transportados y monto recaudados por una aerolínea en una fecha puntual.

        Parameters:
            aerolinea (Aerolinea): Aerolínea de la cual se desea obtener el total
            fecha (str "YYYY-MM-DD" or datetime.date): Fecha en la que se desea obtener el total
        Returns:
            dict: Diccionario con paquetes y monto recaudado en una fecha puntual.
        Raises:
            TypeError: Si la aerolinea no es una instancia de Aerolinea
        '''
        if not isinstance(aerolinea, Aerolinea):
            raise TypeError("La aerolinea debe ser una instancia de Aerolinea.")

        dt = fecha if isinstance(fecha, datetime.date) else datetime.datetime.strptime(fecha, '%Y-%m-%d').date()

        #return sum([viaje.monto_recaudado for viaje in self.viajes if dt == viaje.fecha and aerolinea == viaje.aerolinea])
        paq, mr = 0, 0
        for viaje in self.viajes:
            if dt == viaje.fecha and aerolinea == viaje.aerolinea:
                paq += viaje.paquetes
                mr += viaje.monto_recaudado

        return ({"Paquetes": paq, "Monto recaudado": mr})

class Conexion(object):
    def __init__(self, origen, destino, transportador):
        self.origen = origen
        self.destino = destino
        self.transportador = transportador

    def __str__(self):
        return f'Origen: {self.origen} | Destino: {self.destino} | Transportador: {self.transportador}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other): 
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.origen == other.origen and self.destino == other.destino and self.transportador == other.transportador

class Itinerario(object):
    def __init__(self):
            self.conexiones = []
            self.conexiones_reprogramadas = []

    def __str__(self):
        if not self.conexiones_reprogramadas:
            return ", ".join( map( str, self.conexiones ) )
        else:
            return ", ".join( map(str, self.conexiones_reprogramadas))

    def __repr__(self):
        return self.__str__()

    @property
    def diferencias(self):
        return self.compare_conections()
    

    def check_for_add_conection(self, conexion, reprogramado = False):
        ''' Verifica si es posible agregar una conexion al itinerario.

        Parameters:
            conexion (Conexion): Un objeto instancia de la clase Conexion
            reprogramado (bool): Opcional en caso que se desee evaluar para añadir como reprogramado.

        Returns:
            True: En caso que el origen sea igual al último destino del itinerario o aun no se dispongan de conexiones en el itinerario (original o reprogramado)
            False: En caso que el origen de la nueva conexión no sea igual al destino de la última conexión del itinerario

        Raises:
            TypeError: En caso que el parámetro conexion no sea una instancia de la clase Conexion.
            ValueError: En caso que el origen sea igual al destino
        '''
        if not isinstance(conexion, Conexion):
            raise TypeError("Para agregar, debe ser una instancia de Conexion")

        #retorno True si es la primera conexion de cualquier tipo (original o reprogramada)
        if not self.conexiones and not reprogramado:
            return True
        elif not self.conexiones_reprogramadas and reprogramado:
            return True

        if conexion.origen is conexion.destino:
            raise ValueError("El destino es igual al origen")

        if not reprogramado:
            return True if self.conexiones[-1].destino is conexion.origen else False
        else:
            return True if self.conexiones_reprogramadas[-1].destino is conexion.origen else False

    def add_conection(self, *args, **kwargs):
        ''' Evalua si es posible y en dicho caso, agrega una conexión al itinerario.

        Parameters:
            args (Conexion): Objetos instancias de la clase Conexion.
            kwargs reprogramado (bool): Opcional en caso que se desee añadir como reprogramado
        '''
        for conexion in args:
            #self.conexiones.extend([conexion for conexion in args ]) #if isinstance(arg, Conexion) else None])
            if kwargs.get("reprogramado") is not True:
                self.conexiones.append(conexion) if self.check_for_add_conection(conexion) else None
            else:
                self.conexiones_reprogramadas.append(conexion) if self.check_for_add_conection(conexion, reprogramado=True) else None

    def search_destino(self, destino):
        ''' Busca un destino en las conexiones reprogramadas para devolver su posicion

        Parameters:
            destino (str): Destino que se desea buscar

        Returns:
            int: En caso que se encuentre el destino buscado, se devuelve su posición
            None: En aso que no se encuentre el destino
        '''
        for i in range(len(self.conexiones_reprogramadas)):
            if self.conexiones_reprogramadas[i].destino == destino:
                return i    #Retorno la posicion encontrada

        return None     #En caso que no se encuentre el destino buscado

    def compare_transporter(self, place_orig, place_reprogram):
        ''' Compara el transportador (Aerolínea) entre una conexión original y una reprogramada

        Parameters:
            place_orig (int): Indice de la posición del itinerario origial
            place_reprogram (int): Indice de la posición del itinerario reprogramado

        Returns:
            True: En caso de que las aerolíneas sean iguales
            False: En caso de que las aerolíneas sean distintas
        '''
        return True if self.conexiones[place_orig].transportador is self.conexiones_reprogramadas[place_reprogram].transportador else False

    def compare_destinos(self, place_orig, place_reprogram):
        ''' Compara los destinos entre una conexión original y una reprogramada

        Parameters:
            place_orig (int): Indice de la posición del itinerario origial
            place_reprogram (int): Indice de la posición del itinerario reprogramado

        Returns:
            True: En caso de que los destinos sean iguales
            False: En caso de que los destinos sean distintos
        '''
        return True if self.conexiones[place_orig].destino is self.conexiones_reprogramadas[place_reprogram].destino else False

    def compare_conections(self):
        ''' Devuelve las diferencias de conexiones originales y reprogramadas.

        Parameters:
            None
        Returns:
            list: Lista con las porciones modificadas entre las conexiones originales y reprogramadas.
            None: En caso de no haber diferencia
        Raises:
            ValueError: En caso de que exista y no se pueda encontrar la diferencia.
        '''

        if not self.conexiones_reprogramadas:
            return None    #no hay reprogramaciones

        if self.conexiones_reprogramadas == self.conexiones:
            return None    #son iguales

        diferencias = []
        
        repr_offset = 0
        saltar = 0

        for i in range(len(self.conexiones)):
            
            if saltar:  #trayectos a ignorar
                saltar -= 1
                repr_offset += 1
                continue

            if self.conexiones[i] is not self.conexiones_reprogramadas[repr_offset]:    #se encuentra una diferencia

                if not self.compare_destinos(i, repr_offset):   #se verifica que la diferencia sea de destino
                    
                    posic_reprogr = self.search_destino(self.conexiones[i].destino)

                    if posic_reprogr:   #Indica que se cambia un origen-destino por origen-escala-destino
                        diferencias.append(dict(
                            original=self.conexiones[i:i+1], 
                            reprogramado=self.conexiones_reprogramadas[repr_offset : posic_reprogr +1]))
                        repr_offset += posic_reprogr - i
                    else:
                        try:
                            #comparo si un origen-escala1-destino fue reemplazado por un origen-escala2-destino
                            if self.conexiones[i+1].destino is self.conexiones_reprogramadas[repr_offset+1].destino:

                                diferencias.append(dict(
                                    original=self.conexiones[i:i+2],
                                    reprogramado=self.conexiones_reprogramadas[repr_offset:repr_offset+2]
                                    ))
                        except:
                            pass

                elif not self.compare_transporter(i, repr_offset):  #Asegura que haya una diferencia de aerolinea en caso que el el destino sea el mismo
                    diferencias.append(dict(
                        original=self.conexiones[i:i+1],
                        reprogramado=self.conexiones_reprogramadas[repr_offset:repr_offset+1]
                        ))
                else:
                    pass

            repr_offset += 1

        if diferencias:
            return diferencias
        else:
            raise ValueError("Error obteniendo las diferencias.")
