#!/usr/bin/env python
import kiu
import unittest

class TestingBigWord(unittest.TestCase):    #Punto 1a
    def test_ejemplo(self):
        self.assertEqual(kiu.big_word("El veloz murciélago hindú comía feliz cardillo y kiwi"), "murciélago")

class TestingOrderList(unittest.TestCase):  #Punto 1b
    def test_ejemplo(self):
        self.assertEqual(kiu.ordenar_lista([1, 20, 54, 33, -15, 7]), [-15, 1, 7, 20, 33, 54])

class TestingTransportes(unittest.TestCase):    #Punto 2
    #Inicialización de temporales
    aa = kiu.Aerolinea("Aerolíneas Argentinas")
    lan = kiu.Aerolinea("LATAM")
    aa.add_client("KIU")
    lan.add_client("LLUCYK")

    tr = kiu.Transportes()
    tr.add_viaje(kiu.Viaje(aa, "KIU", 15, "2019-10-01"))
    tr.add_viaje(kiu.Viaje(aa, "KIU", 10, "2019-10-01"))
    tr.add_viaje(kiu.Viaje(lan, "LLUCYK", 10, "2019-10-01"))

    def test_montos(self):
        self.assertEqual(self.tr.recaudado_por_fecha(self.aa, "2019-10-01"), {"Paquetes": 25, "Monto recaudado": 250})  #Monto x
        self.assertEqual(self.tr.recaudado_por_fecha(self.aa, "2019-10-02"), {"Paquetes": 0, "Monto recaudado": 0})     #Sin recaudacion
        self.assertEqual(self.tr.recaudado_por_fecha(self.lan, "2019-10-01"), {"Paquetes": 10, "Monto recaudado": 100}) #Monto y

    def test_transportar_no_cliente(self):
        #No permitir transportar si no es cliente
        self.assertRaises(ValueError, self.tr.add_viaje, kiu.Viaje(self.lan, "KIU", 1, "2019-10-01"))

    def test_err_datatypes(self):
        #No debe permitir crear un viaja con una aerolinea como str
        self.assertRaises(TypeError, self.tr.add_viaje, kiu.Viaje("LATAM", "KIU", 1, "2019-10-01"))

class TestingItinerarios(unittest.TestCase):    #Punto 3
    def test_sin_reprogramacion(self):
        viaje = kiu.Itinerario()
        viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
        viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
        self.assertIsNone(viaje.diferencias)    #No hay reprogramacion

        #reprogramacion igual al itinerario original
        viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"), reprogramado=True)
        viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"), reprogramado=True)
        self.assertIsNone(viaje.diferencias)    #No hay reprogramacion

    def test_add_escala(self):
        ''' Test para agregar una escala. Origen->Destino se reemplaza por Origen->Escala->Destino '''
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

        res=[{
            "original": [kiu.Conexion("LIM", "LPB", "AA")],
            "reprogramado": [kiu.Conexion("LIM", "BOG", "AA"), kiu.Conexion("BOG", "LPB", "AA")]
        }]
        self.assertListEqual(viaje.diferencias, res)

    def test_edit_escala(self):
        ''' Test para editar una escala. Origen->EscalaX->Destino se reemplaza por Origen->EscalaY->Destino '''
        viaje = kiu.Itinerario()
        viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
        viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
        viaje.add_conection(kiu.Conexion("UYU", "LIM", "AA"))
        viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"))

        viaje.add_conection(kiu.Conexion("LIM", "EZE", "AA"), reprogramado=True)
        viaje.add_conection(kiu.Conexion("EZE", "UYU", "AA"), reprogramado=True)
        viaje.add_conection(kiu.Conexion("UYU", "LIM", "AA"), reprogramado=True)
        viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"), reprogramado=True)

        res=[{
            "original": [kiu.Conexion("LIM", "LPB", "AA"), kiu.Conexion("LPB", "UYU", "AA")],
            "reprogramado": [kiu.Conexion("LIM", "EZE", "AA"), kiu.Conexion("EZE", "UYU", "AA")]
        }]

        self.assertListEqual(viaje.diferencias, res)

    def test_change_transporter(self):
        ''' Test para cambiar la aerolinea de conexion/es '''
        viaje = kiu.Itinerario()
        viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"))
        viaje.add_conection(kiu.Conexion("LPB", "UYU", "AA"))
        viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"))
        viaje.add_conection(kiu.Conexion("LPB", "LIM", "AA"))

        viaje.add_conection(kiu.Conexion("LIM", "LPB", "AA"), reprogramado=True)   
        viaje.add_conection(kiu.Conexion("LPB", "UYU", "LT"), reprogramado=True)    #Se cambia la aerolinea a LATAM
        viaje.add_conection(kiu.Conexion("UYU", "LPB", "AA"), reprogramado=True)
        viaje.add_conection(kiu.Conexion("LPB", "LIM", "LT"), reprogramado=True)

        res = [
        {
            "original": [kiu.Conexion("LPB", "UYU", "AA")],
            "reprogramado": [kiu.Conexion("LPB", "UYU", "LT")]
        },
        {
            "original": [kiu.Conexion("LPB", "LIM", "AA")],
            "reprogramado": [kiu.Conexion("LPB", "LIM", "LT")],
        }
        ]
        
        self.assertListEqual(viaje.diferencias, res)

if __name__ == '__main__':
    unittest.main()