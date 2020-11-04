import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

heladeras = []
botellasSobrantes = 0
latasSobrantes = 0

monitor = threading.Condition()

cantidadHeladeras = 2
cantidadProveedores = 1

# def verificarHeladera():

#Preguntar a la heladera primero cuanto espacio tiene antes de meter las cervezas
class Heladera(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.botellas = []
        self.latas  = []
        self.id = id

    def heladeraBotellas(self):
        return len(self.botellas)

    def heladeraLatas(self):
        return len(self.latas)

    def espacioDisponible(self):
        return 

    # def run(self):
        #self.llenarHeladera()

#Mientras la cantidad a poner sea > a 0 que entre
class Proveedores(threading.Thread):
    def __init__(self):
        super().__init__()

    def cantidadBotellas(self):
        return random.randint(1, 10)

    def cantidadLatas(self):
        return random.randint(1, 10)

    def generarCervezas(self, heladera):
        botellasAEntregar = self.cantidadBotellas() + botellasSobrantes
        latasAEntregar = self.cantidadLatas() + latasSobrantes
        logging.info(f'Hay stock de {botellasAEntregar} botellas y {latasAEntregar} latas')
        time.sleep(2)
        self.entregarBotellas(heladera, botellasAEntregar)
        self.entregarLatas(heladera, latasAEntregar)

    def entregarBotellas(self, heladera, botellasAEntregar):
        while (botellasAEntregar > 0 & heladera.heladeraBotellas() < 10):
            heladera.botellas.append(0)
            logging.info(f'En esta heladera hay {len(heladera.botellas)} botellas')
            botellasAEntregar -= botellasAEntregar

            botellasSobrantes = botellasAEntregar
            logging.info(f'Sobraron {botellasSobrantes} botellas')
            time.sleep(2)

    def entregarLatas(self, heladera, latasAEntregar):
        while (latasAEntregar > 0 & heladera.heladeraLatas() < 15):
            heladera.latas.append(0)
            logging.info(f'En esta heladera hay {len(heladera.latas)} latas')
            latasAEntregar -= latasAEntregar
            
            latasSobrantes = latasAEntregar
            logging.info(f'Sobraron {latasSobrantes} latas')
            time.sleep(2)

    def run(self):
        while(True):
            self.generarCervezas(heladeras[0])

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

Proveedores().start()