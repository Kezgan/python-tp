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
cantidadProveedores = 1



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

    def hayEspacio(self):
        return (self.hBotellas() < 10) | (self.hLatas() < 15)        

class Proveedores(threading.Thread):
    def __init__(self, monitorProveedor):
        super().__init__()
        self.monitorProveedor = monitorProveedor

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
        
        with self.monitorProveedor:
            for i in range(cantidadHeladeras):
                
                while (heladeras[i].hayEspacio()):
                    self.generarCervezas()
                    self.entregarBotellas(heladeras[i])
                    self.entregarLatas(heladeras[i])

                    logging.info(f'En la heladera {heladeras[i].id} hay {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
                    time.sleep(2)
                    logging.info(f'Sobraron {botellasSobrantes} botellas y {latasSobrantes} latas')
                    time.sleep(2)
                logging.info(f'La heladera {heladeras[i].id} esta llena con {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
                time.sleep(2)

# Intenté varias formas pero no me termina de funcionar con varios proveedores porque lo que pasa
# es que entra el primer proveedor y hasta que no se llenan todas las heladeras no viene el siguiente.
# Probé metiendo algun monitor/semaforo en el run de proveedores pero no hay caso.        

monitorProveedor = threading.Condition()

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    Proveedores(monitorProveedor).start()

