import socket
import subprocess

first = True

try:
    s = socket.socket()
    print("Socket creata con successo.")
except:
    print("Creazione socket fallita.")
    
port = 50060

try:
    s.bind(('192.168.1.108', port))
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
        first = False
    else:
        command = 'restoreVB.bat'
        
    try:        
        process = subprocess.Popen([command], shell=True)
        process.wait()
        c.send('La richiesta è stata soddisfatta con successo.'.encode())
    except Exception as e:
        print("Errore: %s" %(e))
        c.send('La richiesta non è stata soddisfatta con successo.'.encode())
    
    c.close()

"""
while True:
    c, addr = s.accept()
    print("Connessione accettata da", addr)
    
    try:
        command = 'snapshotVB.bat'
        process = subprocess.Popen([command], shell=True)
        process.wait()
        c.send('Snapshots effettuati con successo.'.encode())
    except Exception as e:
        print("Errore: %s" %(e))
    
    c.close()
    break
"""
