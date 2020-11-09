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
cantidadBeodes = 1

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
        while(True):
            with self.monitorProveedor:
                with monitorBeode:
                    for i in range(cantidadHeladeras):
                        
                        while (heladeras[i].hayEspacio()):
                            self.generarCervezas()
                            self.entregarBotellas(heladeras[i])
                            self.entregarLatas(heladeras[i])

                            logging.info(f'En la heladera {heladeras[i].id} hay {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
                            time.sleep(2)
                            logging.info(f'Sobraron {botellasSobrantes} botellas y {latasSobrantes} latas')
                            time.sleep(2)
                            monitorBeode.notify()
                        logging.info(f'La heladera {heladeras[i].id} esta llena con {heladeras[i].hBotellas()} botellas y {heladeras[i].hLatas()} latas')
                        time.sleep(2)
        
class Beodes(threading.Thread):
    def __init__(self, id, consumirBotellas, consumirLatas):
        super().__init__()
        self.id = id
        self.consumirBotellas = consumirBotellas
        self.consumirLatas = consumirLatas

        self.elegirHeladera = random.randint(0, cantidadHeladeras-1)

        logging.info(f'Soy el Beode {self.id}, consumiré de la heladera {self.elegirHeladera} un total de {self.consumirBotellas} botellas y  {self.consumirLatas} latas')

    def beberBotella(self):
        logging.info(f'Bebiendo botella de cerveza')
        heladeras[self.elegirHeladera].botellas.pop(0)
        self.consumirBotellas = self.consumirBotellas - 1
        time.sleep(2)
        logging.info(f'Ya bebí, ahora en la heladera {heladeras[self.elegirHeladera]} quedan {heladeras[self.elegirHeladera].hBotellas()} botellas')

    def beberLata(self):
        logging.info(f'Bebiendo lata de cerveza')
        heladeras[self.elegirHeladera].latas.pop(0)
        self.consumirLatas = self.consumirLatas - 1
        time.sleep(2)
        logging.info(f'Ya bebí, ahora en la heladera {heladeras[self.elegirHeladera]} quedan {heladeras[self.elegirHeladera].hLatas()} latas')

    def run(self):
        while(True):
            while (self.consumirBotellas > 0) | (self.consumirLatas > 0):
                with monitorBeode:
                    if (heladeras[self.elegirHeladera].hBotellas() == 0):
                        monitorBeode.wait()
                    self.beberBotella()
                    time.sleep(5)

                    if (heladeras[self.elegirHeladera].hLatas() == 0):
                        monitorBeode.wait()
                    self.beberLata()

monitorProveedor = threading.Condition()
monitorBeode = threading.Condition()

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    Proveedores(monitorProveedor).start()

for i in range(cantidadBeodes):
    tipoBeode = random.randint(1, 3)

    if (tipoBeode == 1):
        consumirBotellas = random.randint(1, 5)
        consumirLatas = 0
        Beodes(i, consumirBotellas, consumirLatas).start()
    elif (tipoBeode == 2):
        consumirBotellas = 0
        consumirLatas = random.randint(1, 5)
        Beodes(i, consumirBotellas, consumirLatas).start()
    elif (tipoBeode == 3):
        consumirBotellas = random.randint(1, 5)
        consumirLatas  = random.randint(1, 5)
        Beodes(i, consumirBotellas, consumirLatas).start()