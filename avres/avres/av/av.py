import grpc
import time
import logging
import subprocess
import os

from concurrent import futures
# from threading import Thread

from proto import av_pb2
from proto import av_pb2_grpc

CHUNK_DIM = 5000

class AVServicer(av_pb2_grpc.SendBinaryServicer):

	def sendBinary(self, request_iterator, context):
		binary = bytes()
		filename = "binary"
		logname = "log.txt"
		
		print("Sono stato invocato.")
		for chunk in request_iterator:
			print("chunk = " + str(chunk.num_chunk))
			binary += chunk.file
			# ret = av_pb2.output(response="OK", num_chunk=chunk.num_chunk)
			# yield ret
		# print(binary)
		
		f = open(filename, mode="wb")
		f.write(binary)
		f.close()
		
		command = "chmod +x binary && ./binary"
		process = subprocess.Popen([command], shell=True)
		process.wait()
		
		command = "clamscan " + filename + " > " + logname
		process = subprocess.Popen([command], shell=True)
		process.wait()
		
		# Apro il file contenente il risultato della scansione
		f_log = open(logname, mode="r")
		
		# Leggo il risultato della scansione
		contenuto = f_log.read()
		
		# Determino i chunks
		dim = len(contenuto)
		
		# print("Dimensione del contenuto: " + str(dim))
		
		# Computo il numero di chunk
		q = dim // CHUNK_DIM
		# print("Il valore di q: " + str(q))
		
		# Computo la dimensione dell'eventuale ultimo chunk
		r = dim % CHUNK_DIM
		# print("Il valore di r: " + str(r))
		
		if(q==0):
		
			#Sono nel caso in cui ho un solo chunk
			yield av_pb2.output(response=contenuto, num_chunk=0)
			
		else:
			count = 0
			for i in range(0,q):
				try:
					yield av_pb2.output(file=contenuto[i*CHUNK_DIM:i*CHUNK_DIM + CHUNK_DIM], num_chunk=i)
				except:
					print("Errore nel trasferimento chunk " + str(i))
				count = count + 1
				
			if(r > 0):
				lower_bound = count * CHUNK_DIM
				yield av_pb2.output(file=contenuto[lower_bound:lower_bound+r], num_chunk=count)
				# print("Inviato chunk non completo.")
				
		print("I risultati dell'analisi sono stati inviati con successo.")
		
		try:
			os.remove(filename)
			os.remove(logname)
		except:
			print("Errore nella rimozione dei file.")
		
	

# Logging
logging.basicConfig(filename="av.log", format=f'%(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger("av")
logger.setLevel(logging.INFO)

#create gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
av_pb2_grpc.add_SendBinaryServicer_to_server(AVServicer(), server)

logger.info('Avvio del server in ascolto sulla porta 50053...')
server.add_insecure_port('192.168.0.3:50053')
server.start()
logger.info('Server avviato con successo.')

try:
    while True:
        time.sleep(86400)   #86400 seconds == 24 hours
except KeyboardInterrupt:
    server.stop(0)
