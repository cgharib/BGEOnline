import socket, sys
import pickle
from threading import Thread
from bge import logic, events
import mathutils

host = "localhost"
port = 12800

class ReceptionMessage(Thread):
    def __init__(self, co):
        Thread.__init__(self)
        self.connexion = co
        self.j2x = 0
        self.j2y = 0
        self.j2z = 5
        self.j2pos = (self.j2x, self.j2y, self.j2z)
        self.j2rx = 100
        self.j2ry = 30
        self.j2rz = 65
        self.j2rot = (self.j2rx, self.j2ry, self.j2rz)
        

    def run(self):
        while 1:
            msg_recu = self.connexion.recv(1024)
            try:
                msg_recu = pickle.loads(msg_recu)
                self.j2x = msg_recu[0]
                self.j2y = msg_recu[1]
                self.j2z = msg_recu[2]
                self.j2rx = msg_recu[3]
                self.j2ry = msg_recu[4]
                self.j2rz = msg_recu[5]
                self.j2pos = (self.j2x, self.j2y, self.j2z)
                self.j2rot = (self.j2rx, self.j2ry, self.j2rz)
                
                
                
                
            except:
                pass



class EnvoiMessage(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.connexion = conn
        self.scene = logic.getCurrentScene()
        self.j1 = self.scene.objects["J1"]

    def run(self):
        while 1:
            self.j1x = self.j1.worldPosition[0]
            self.j1y = self.j1.worldPosition[1]
            self.j1z = self.j1.worldPosition[2]
            self.pos = (self.j1x, self.j1y, self.j1z)
            self.rot = self.j1.worldOrientation.to_euler()
            self.j1rx = self.rot[0]
            self.j1ry = self.rot[1]
            self.j1rz = self.rot[2]
            self.posrot = (self.j1x, self.j1y, self.j1z, self.j1rx, self.j1ry, self.j1rz)
            msg_envoi = pickle.dumps(self.posrot)
            self.connexion.send(msg_envoi)
            



connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("Echouééééé")
print("Connexion établiiiiiiiiiiie.")

th1 = EnvoiMessage(connexion)
th2 = ReceptionMessage(connexion)

th1.start()
th2.start()
print("une seule fois")

def main():
    scene = logic.getCurrentScene()
    J1 = scene.objects["J1"]
    J2 = scene.objects["J2"]
    
    J2.worldPosition = th2.j2pos
    J2.worldOrientation = mathutils.Euler([th2.j2rx, th2.j2ry, th2.j2rz]).to_matrix()
    
    

    





