import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

heladeras = []

botellasSobrantes = 0
latasSobrantes = 0

localBotellas = 0
localLatas = 0

semaforoProveedor = threading.Semaphore(1)
semaforoHeladera = threading.Semaphore(1)

cantidadHeladeras = 3
cantidadProveedores = 2

# No dar importancia a este archivo, esta de ejemplo para mi nada mas

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

    def meterBotellas(self):
        global localBotellas

        logging.info(f'Ahora en el local hay {localBotellas}')
        time.sleep(2)

        while (localBotellas > 0) & (self.hBotellas() < 10):
            self.botellas.append(0)
            localBotellas = localBotellas - 1

    def meterLatas(self):
        global localLatas

        logging.info(f'Ahora en el local hay {localLatas}')
        time.sleep(2)

        while (localLatas > 0) & (self.hLatas() < 15):
            self.latas.append(0)
            localLatas = localLatas - 1

    def hayEspacio(self):
        return (self.hBotellas() < 10) | (self.hLatas() < 15)

    def run(self):
        semaforoHeladera.acquire()
        while (self.hayEspacio()):
            self.meterBotellas()
            self.meterLatas()

            logging.info(f'En la heladera {self.id} hay {self.hBotellas()} botellas y {self.hLatas()} latas')
            time.sleep(2)
            logging.info(f'Sobraron {botellasSobrantes} botellas y {latasSobrantes} latas')
            time.sleep(2)
            semaforoProveedor.release()
            
        logging.info(f'La heladera {self.id} esta llena con {self.hBotellas()} botellas y {self.hLatas()} latas')
        time.sleep(1)
        semaforoHeladera.release()

class Local(threading.Thread):
    def __init__(self):
        super().__init__()

    def comenzarALlenar(self):
        for i in range(cantidadHeladeras):
            heladeras[i].start()


    def run(self):
        self.comenzarALlenar()
        

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

    def entregarBotellas(self):
        global botellasAEntregar, localBotellas

        time.sleep(2)

        while (botellasAEntregar > 0):
            localBotellas = localBotellas + 1
            botellasAEntregar = botellasAEntregar - 1

        logging.info(f'Entregué al local {localBotellas} botellas. Me quedé con {botellasAEntregar}')

    def entregarLatas(self):
        global latasAEntregar, localLatas

        time.sleep(2)

        while (latasAEntregar > 0):
            localLatas = localLatas + 1
            latasAEntregar = latasAEntregar - 1

        logging.info(f'Entregué al local {localLatas} latas. Me quedé con {latasAEntregar}')

    def run(self):
        #while(True):
        semaforoProveedor.acquire()
        self.generarCervezas()
        self.entregarBotellas()
        self.entregarLatas()
        time.sleep(3)
        Local().start()
        
        


monitorProveedor = threading.Condition()

for i in range(cantidadHeladeras):
    heladeras.append(Heladera(i))

for i in range(cantidadProveedores):
    Proveedores(monitorProveedor).start()
