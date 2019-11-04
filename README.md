# KIU PYTHON OPENING
KIU es un módulo escrito en Python para cumplir con los requisitos solicitados por KIU SYSTEM.

## Instalación
1. Clonar el repositorio.
```bash
git clone https://github.com/lucaslucyk/ITDEV-KIU-PYTHON-OPENING
```
2. Ubicar en la carpeta del proyecto deseado.

## Testear el módulo
Una vez ubicado el módulo en la carpeta del proyecto, se pueden ejecutar los unittest para comprobar el funcionamiento
```bash
python test_kiu.py
```

## Funcionamiento

### big_word(frase)
El método recibe una frase y devuelve la palabra más larga. Ejemplo:
```python
import kiu

kiu.big_word("El veloz murciélago hindú comía feliz cardillo y kiwi")   # retorna "murciélago"
kiu.big_word("Un bebé muy pequeño estaba llorando")     # retorna "llorando"
```

### ordenar_lista(lista)
El método recibe una lista de enteros y retorna la misma lista ordenada de menor a mayor. La misma no utiliza el método "sorted"
```python
import kiu

kiu.ordenar_lista([1, 20, 54, 33, -15, 7])  # retorna [-15, 1, 7, 20, 33, 54]
```

### Transporte de cargas
Para esta problemática, se deben realizar los siguientes pasos:
1. Crear una aerolinea con el nombre deseado.
2. Agregar los clientes correspondientes.
3. Crear una instancia de Transportes() para tener registro de todos los transportes realizados.
4. Agregar viajes mediante add_viaje(Viaje) pasando como parámetro una instancia de Viaje. La misma se crea con los parámetros Aerolínea, cliente, cantidad de paquetes y fecha.
5. Utilizar el método recaudado_por_fecha(Aerolinea, fecha) para obtener el total de paquetes transportados y el monto recaudado en una fecha puntual.

Ejemplo:
```python
import kiu

aa = kiu.Aerolinea("Aerolíneas Argentinas")
aa.add_client("KIU")

tr = kiu.Transportes()
tr.add_viaje(kiu.Viaje(aa, "KIU", 15, "2019-10-01"))
tr.add_viaje(kiu.Viaje(aa, "KIU", 10, "2019-10-01"))

print(tr.recaudado_por_fecha(aa, "2019-10-01")) # Imprime {"Paquetes": 25, "Monto recaudado": 250}
```

Consideraciones:
1. Una Aerolínea solo puede transportar paquetes de los clientes que fueron agregados mediante add_cliente().
2. Al crear una instancia de Viaje, el parámetro aerolínea debe ser una instancia de la clase Aerolinea.
3. Las fechas pueden ser indicadas como str con formato "YYYY-MM-DD" o una instancia de datetime.date.
4. La salida de recaudado_por_fecha() será un dict {"Paquetes": cantidad (int), "Monto recaudado": monto (int)}

### Diferencias en itinerarios
Para esta problemática, se deben realizar los siguientes pasos:
1. Instanciar un objeto de clase Itinerario.
2. Agregar las conexiones del itinerario original mediante el método add_conection(Conexion).
3. Agregar las conexiones del itinerario reprogramado mediante el método add_conection(Conexion) utilizando el kwarg "reprogramado = True".
4. Obtener las diferencias mediante la propiedad "diferencias".

Ejemplo agregando una escala. Origen->Destino se reemplaza por Origen->Escala->Destino
```python
import kiu

viaje = kiu.Itinerario()
viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"))

viaje.add_conection(kiu.Conexion("LIM", "BOG", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("BOG", "LPB", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"), reprogramado=True)


print(viaje.diferencias)
'''
La salida será la siguiente:

[{
    'original': [Origen: LIM | Destino: LPB | Transportador: AA], 
    'reprogramado': [Origen: LIM | Destino: BOG | Transportador: AA, Origen: BOG | Destino: LPB | Transportador: AA]
}]
'''
```

Ejemplo editando una escala. Origen->EscalaX->Destino se reemplaza por Origen->EscalaY->Destino
```python
import kiu

viaje = kiu.Itinerario()
viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
viaje.add_conection(kiu.Conexion("UYU", "LIM", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"))

viaje.add_conection(kiu.Conexion("LIM", "EZE", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("EZE", "UYU", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("UYU", "LIM", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"), reprogramado=True)


print(viaje.diferencias)
'''
La salida será la siguiente:

[{
'original': [Origen: LIM | Destino: LPB | Transportador: AA, Origen: LPB | Destino: UYU | Transportador: AA], 
'reprogramado': [Origen: LIM | Destino: EZE | Transportador: AA, Origen: EZE | Destino: UYU | Transportador: AA]
}]
'''
```

Ejemplo cambiando la aerolínea de conexiones.
```python
import kiu

viaje = kiu.Itinerario()
viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"))
viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"))

viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"), reprogramado=True)   
viaje.add_conection(kiu.Conexion("LPB", "UYU", "LT"), reprogramado=True)    #Se cambia la aerolinea a LATAM
viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"), reprogramado=True)
viaje.add_conection(kiu.Conexion("LPB", "LIM", "LT"), reprogramado=True)

print(viaje.diferencias)
'''
La salida será la siguiente:

[
    {
        'original': [Origen: LPB | Destino: UYU | Transportador: AA], 
        'reprogramado': [Origen: LPB | Destino: UYU | Transportador: LT]
    }, 
    {
        'original': [Origen: LPB | Destino: LIM | Transportador: AA], 
        'reprogramado': [Origen: LPB | Destino: LIM | Transportador: LT]
    }
]
'''
```

Consideraciones:
1. Si un viaje no tiene reprogramación o la reprogramación es igual al itinerario original, la propiedad "diferencias" retorna None.
2. Al agregar conexiones al itinerario, se comprueba que el origen sea igual al último destino (excepto en la primer conexión añadida).
3. Al crear una Conexion, se deben ingresar los parámetros Origen, Destino y Aerolínea; todos str.