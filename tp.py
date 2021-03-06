import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

heladeras = []
botellasSobrantes = 0
latasSobrantes = 0

semaforo = threading.Semaphore(1)

cantidadHeladeras = 3
cantidadProveedores = 2



class Heladera(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.botellas = []
        self.latas  = []
        self.id = id

    def id(self):
        return self.id

    def hBotellas(self):
        return len(self.botellas)

    def hLatas(self):
        return len(self.latas)
 

class Proveedores(threading.Thread):
    def __init__(self):
        super().__init__()

    def cantidadBotellas(self):
        return random.randint(1, 10)

    def cantidadLatas(self):
        return random.randint(1, 10)

    def generarCervezas(self):
        global botellasAEntregar, latasAEntregar

        botellasAEntregar = self.cantidadBotellas()
        latasAEntregar = self.cantidadLatas()
        logging.info(f'Listo para entregar {botellasAEntregar} botellas y {latasAEntregar} latas')
        time.sleep(2)

    def entregarBotellas(self, heladera):
        global botellasAEntregar, botellasSobrantes

        botellasSobrantes = botellasSobrantes + botellasAEntregar

        logging.info(f'Botellas stock = {botellasSobrantes}')
        time.sleep(2)

        while (botellasSobrantes > 0) & (heladera.hBotellas() < 10):
            heladera.botellas.append(0)
            botellasSobrantes = botellasSobrantes - 1

    def entregarLatas(self, heladera):
        global latasAEntregar, latasSobrantes

        latasSobrantes = latasAEntregar + latasSobrantes

        logging.info(f'Latas stock = {latasSobrantes}')
        time.sleep(2)

        while (latasSobrantes > 0) & (heladera.hLatas() < 15):
            heladera.latas.append(0)
            latasSobrantes = latasSobrantes - 1

    def run(self):
    
        for i in range(cantidadHeladeras):
            
            while (heladeras[i].hBotellas() < 10) | (heladeras[i].hLatas() < 15):
                semaforo.acquire()
                try:
                    self.generarCervezas()
                    self.entregarBotellas(heladeras[i])
                    self.entregarLatas(heladeras[i])

                    logging.info(f'En la heladera {heladeras[i].id} hay {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
                    time.sleep(2)
                    logging.info(f'Sobraron {botellasSobrantes} botellas y {latasSobrantes} latas')
                    time.sleep(2)
                finally:
                    semaforo.release()
                    logging.info("Liberé semaforo")

            logging.info(f'La heladera {heladeras[i].id} esta llena con {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
            time.sleep(2)
            

# Intenté varias formas pero no me termina de funcionar con varios proveedores porque lo que pasa
# es que entra el primer proveedor y hasta que no se llenan todas las heladeras no viene el siguiente.
# Probé metiendo algun monitor/semaforo en el run de proveedores pero no hay caso.
# Perdi bastante tiempo con esto porque encima queria manejar todo desde proveedor, pero bueno ¯\_(ツ)_/¯

#----------------------------------------------------------

# Actualización:
# Ahora agregando semaforo en el run "funciona", el tema es que si el proveedor 1 llenó la heladera 0,
# al pasar al proveedor 2 este se queda con la heladera 0 de antes, entonces vuelve a verificar si está llena y vuelve a tirar el mensaje de que se llenó la healdera 0.
# Recién cuando se vuelve al proveedor 1 pasa a la siguiente heladera. No pude arreglar esto.

#listaProveedores = []

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    #p = Proveedores()
    #listaProveedores.append(p)
    #p.start()
    Proveedores().start()
