import grpc
import time
import logging
import subprocess
import os

from concurrent import futures
from proto import av_pb2
from proto import av_pb2_grpc
from proto import centralnode_pb2
from proto import centralnode_pb2_grpc

# Dimensione del chunk
CHUNK_DIM = 5000

# Indirizzo IP dell'AV
IP = "192.168.100.5"

# Stringa connessione centralnode
CENTRALNODE = '192.168.100.6:50051'

# Stringa server grpc AV
AV = '192.168.100.5:50053'



"""
Questa funzione ha lo scopo di avvertire il
centralnode che l'antivirus ha terminato la
fase di configurazione e che può iniziare la
scansione dei binari.
"""
def sendACK():
	
	while(True):
		try:
			channel = grpc.insecure_channel(CENTRALNODE)
			stub = centralnode_pb2_grpc.SendACKStub(channel)
			response = stub.sendACK(centralnode_pb2.id(id_av=IP))
			print(str(response.result))
			break
		except Exception as e:
			print("Errore nell'invio del messaggio di ACK")
			print(e)
			time.sleep(10)
			continue
	print("Il centralnode è stato avvertito con successo")
		

class AVServicer(av_pb2_grpc.SendBinaryServicer):

	"""
	Questa RPC ha il compito di inviare i risultati dell'analisi
	del file binario che è stato sottomesso. Il file binario viene
	ricevuto direttamente dal centralnode.
	"""
	def sendBinary(self, request_iterator, context):
		binary = bytes()
		
		# Nome del file binario che verrà utilizzato
		filename = "binary"
		
		# Nome del file contenente i risultati della scansione
		logname = "log.txt"
		
		logger.info("E' stata richiesta dal centralnode la scansione di un binario.")
		
		for chunk in request_iterator:
			print("chunk = " + str(chunk.num_chunk))
			binary += chunk.file
		
		# Creo un nuovo file per la scansione
		f = open(filename, mode="wb")
		
		# Popolo il nuovo file con il binario ricevuto
		f.write(binary)
		
		# Chiudo il file eseguendo il flush dei dati
		f.close()
		
		# Abilito i privilegi di esecuzione ed eseguo il binario ricevuto
		command = "chmod +x binary && ./binary"
		process = subprocess.Popen([command], shell=True)
		
		# Attendo che l'esecuzione del binario sia completata
		process.wait()
		
		logger.info("Esecuzione del binario completata con successo")
		
		# Eseguo la scansione del binario sottomesso
		command = "clamscan " + filename + " > " + logname
		process = subprocess.Popen([command], shell=True)
		
		# Attendo che la scansione del binario sia completata
		process.wait()
		
		logger.info("Scansione del binario completata con successo")
		
		# Apro il file contenente il risultato della scansione
		f_log = open(logname, mode="r")
		
		# Leggo il risultato della scansione
		contenuto = f_log.read()
		
		# Determino i chunks
		dim = len(contenuto)
		
		# Computo il numero di chunk
		q = dim // CHUNK_DIM
		
		# Computo la dimensione dell'eventuale ultimo chunk
		r = dim % CHUNK_DIM
		
		if(q==0):		
			#Sono nel caso in cui ho un solo chunk
			yield av_pb2.output(response=contenuto, num_chunk=0)
			
		else:
			count = 0
			for i in range(0,q):
				try:
					yield av_pb2.output(file=contenuto[i*CHUNK_DIM:i*CHUNK_DIM + CHUNK_DIM], num_chunk=i)
				except:
					logger.info("Errore nel trasferimento chunk " + str(i))
				count = count + 1
				
			if(r > 0):
				lower_bound = count * CHUNK_DIM
				yield av_pb2.output(file=contenuto[lower_bound:lower_bound+r], num_chunk=count)
				
		logger.info("I risultati dell'analisi sono stati inviati con successo.")
		
		try:
			# Rimozione del binario
			os.remove(filename)			
			# Rimozione dei risultati della scansione
			os.remove(logname)			
		except:		
			logger.info("Errore nella rimozione dei file.")
		
	

# Logging
logging.basicConfig(filename="av.log", format=f'%(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger("av")
logger.setLevel(logging.INFO)

#create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
av_pb2_grpc.add_SendBinaryServicer_to_server(AVServicer(), server)

logger.info('Avvio del server in ascolto sulla porta 50053...')
server.add_insecure_port(AV)
server.start()
logger.info('Server avviato con successo.')

logger.info('Invio ACK al centralnode...')
sendACK()
logger.info('Il messaggio di ACK è stato inviato con successo.')


try:
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
    server.stop(0)
