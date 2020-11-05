import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

heladeras = []
botellasSobrantes = 0
latasSobrantes = 0

semaforo = threading.Semaphore(1)

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

    def hBotellas(self):
        return len(self.botellas)

    def hLatas(self):
        return len(self.latas)

#Mientras la cantidad a poner sea > a 0 que entre
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
        time.sleep(1)

    def entregarBotellas(self, heladera):
        global botellasAEntregar, botellasSobrantes

        botellasSobrantes = botellasSobrantes + botellasAEntregar

        logging.info(f'Botellas stock = {botellasSobrantes}')
        time.sleep(1)

        while (botellasSobrantes > 0):
            if (heladera.hBotellas() < 10):
                heladera.botellas.append(0)
                botellasSobrantes = botellasSobrantes - 1
            else:
                logging.info(f'En esta heladera hay {heladera.hBotellas()} botellas')
                logging.info(f'Sobraron {botellasSobrantes} botellas')
                break

    def entregarLatas(self, heladera):
        global latasAEntregar, latasSobrantes

        latasSobrantes = latasAEntregar + latasSobrantes

        logging.info(f'Latas stock = {latasSobrantes}')
        time.sleep(1)

        while (latasSobrantes > 0):
            if (heladera.hLatas() < 15):
                heladera.latas.append(0)
                latasSobrantes = latasSobrantes - 1
            else:
                logging.info(f'En esta heladera hay {heladera.hLatas()} latas')
                logging.info(f'Sobraron {latasSobrantes} latas')
                break

    def run(self):
        semaforo.acquire()
        
        for i in range(cantidadHeladeras):
            while not (heladeras[i].hBotellas() == 10) & (heladeras[i].hLatas() == 15):
                self.generarCervezas()
                self.entregarBotellas(heladeras[i])
                self.entregarLatas(heladeras[i])

            logging.info(f'Esta heladera esta llena con {heladeras[i].hBotellas()} y {heladeras[i].hLatas()}')

        semaforo.release()

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

Proveedores().start()

#dsadsad