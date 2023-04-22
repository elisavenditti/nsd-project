import socket
import subprocess
import time

HOST_IP = "192.168.1.86"
first = True

try:
    s = socket.socket()
    print("Socket creata con successo.")
except:
    print("Creazione socket fallita.")
    
port = 50060

try:
    s.bind((HOST_IP, port))
    s.listen(1)
    print("binding concluso con successo.")
except:
    print("Errore binding socket.")
    
while True:

    try:
        c, addr = s.accept()
        print("Connessione accettata con successo da ", addr)
    except:
        print("Errore nell'accettazione della connessione.")
    
    # Determino il comando che dovrà essere eseguito
    if(first):
        command = 'snapshotVB.bat'
    else:
        command = 'restoreVB.bat'
        
    try:        
        process = subprocess.Popen([command], shell=True)
        process.wait()
        if(not first):
            time.sleep(5)
            command = 'restartVB.bat'
            process = subprocess.Popen([command], shell=True)
            process.wait()
        else:
            first = False
        c.send('La richiesta è stata soddisfatta con successo.'.encode())
    except Exception as e:
        print("Errore: %s" %(e))
        c.send('La richiesta non è stata soddisfatta con successo.'.encode())
        
    
    
    c.close()
