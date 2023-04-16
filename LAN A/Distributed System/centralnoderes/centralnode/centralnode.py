import grpc
import time
import socket
import secrets
from concurrent import futures

from flask import Flask, render_template, flash, request
from threading import Thread
from proto import av_pb2
from proto import av_pb2_grpc
from proto import av_pb2
from proto import centralnode_pb2
from proto import centralnode_pb2_grpc

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

CENTRAL_NODE_IP = "10.23.1.2"
CENTRAL_NODE_GRPC_PORT = "50051"
AV1_IP = "10.123.0.2"
AV1_PORT = "50053"
AV1_ADDRESS = "10.123.0.2:50053"

# Dimensione del chunk
CHUNK_DIM = 1024

# Numero di ACK ricevuti per la fine delle configurazioni
num_acks = 0

# Numero degli AVs
NUM_AV = 1

# Mi dice se il server è stato avviato
launch_server_grpc = True

# Mi dice se l'host deve effettuare gli snapshot iniziali
do_snapshot = True

# Restaurare lo snapshot
do_restore = False

# La porta su cui contattare l'host
port = 50060



class CentralnodeServicer(centralnode_pb2_grpc.SendACKServicer):



	"""
	Questa RPC consente di registrare la conclusione
	della configurazione da parte di un antivirus. Al
	termine delle configurazioni sarà possibile avviare
	le prime scansioni.
	Lo scambio degli ACK rappresenta la parte iniziale
	del protocollo di comunicazione distribuita tra gli
	antivirus e il centralnode.
	"""
	def sendACK(self, request, context):
		global num_acks
		global NUM_AV

		print("Messaggio di ACK ricevuto dall'antivirus " + request.id_av)
		
		# Effettuo un check sul numero di ACK attualmente ricevuti
		if(num_acks > NUM_AV):
			print("Errore inconsistenza numero di ACKS: " + str(num_acks))
			return centralnode_pb2.code(result=1)
			
		# Registro la conclusione di una configurazione
		num_acks = num_acks + 1
		print("Registrazione conclusione della configurazione avvenuta con successo.")
		
		return centralnode_pb2.code(result=0)


def check_conf_and_initial_snapshot():
	global num_acks
	global NUM_AV
	global do_restore
	global do_snapshot
	
	"""
	I primi due IF riguardano la parte iniziale
	del protocollo di comunicazione distribuita.
	E' necessario attendere che i tre AVs terminino
	la propria configurazione e che vengano eseguiti
	dall'host gli snapshot iniziali in modo da poter
	ripristinare un ambiente pulito a seguito dell'
	esecuzione del binario.
	"""
	if(num_acks != NUM_AV):
		return 1
		
	# if(do_snapshot):
	# 	return 2

	"""
	Bisogna controllare se è in corso il ripristino
	dello snapshot a seguito dell'esecuzione e dell'
	analisi del binario. Questo IF riguarda il check
	a seguito dello snapshot iniziale.
	"""
	# if(do_restore):
	# 	return 3
		
	return 0





"""
Comunica con l'host per avvertirlo di eseguire lo
snapshot degli AVs.
"""
def safe_environment():
	global port
	global do_snapshot

	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Creazione socket avvenuta con successo.")
		except socket.error as err:
			print("Creazione socket conclusa con errore %s" %(err))
			continue

		try:
			s.connect(("192.168.1.108", port))
			print("Connessione avvenuta con successo")
		except Exception as e:
			print("Errore connessione socket %s" %(e))
			continue
			
		try:
			msg = s.recv(1024).decode()
			print("Messaggio di risposta ricevuto dall'host: %s" %(msg))
		except Exception as e:
			print("Errore nella ricezione della risposta da parte dell'host")
			continue
		break
	do_snapshot = False	
	print("Gli snapshot sono stati effettuati con successo dall'host.")



"""
Questa funzione crea un server GRPC per processare
le richieste che arrivano dagli antivirus. Nel momento
in cui le richieste attese sono terminate allora il
server viene sospeso in modo da non averlo inutilmente
in esecuzione e per motivi di sicurezza.
"""
def wait_acks():
	global NUM_AV
	global num_acks
	global launch_server_grpc
	global CENTRAL_NODE_IP
	global CENTRAL_NODE_GRPC_PORT
	
	# Tengo traccia che il server sta per essere lanciato
	launch_server_grpc = False
	print("sono in wait acks")
	while True:
		try:
			server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))	
			centralnode_pb2_grpc.add_SendACKServicer_to_server(CentralnodeServicer(), server)	
			server.add_insecure_port(CENTRAL_NODE_IP + ":" + CENTRAL_NODE_GRPC_PORT)	
			server.start()		
			break
		except Exception as e:
			print("Errore creazione del server GRPC")
			time.sleep(10)		
		
	print("Il server è stato lanciato con successo")
	
	try:	
		while True:
			if(num_acks == NUM_AV):
				print("Numero totale di ACK raggiunti con successo.")
				server.stop(0)
				print("Il server è stato interrotto con successo")				
				# Comunicazione con l'host per il ripristino dell'ambiente degli AVs
				#safe_environment()				
				break
			else:
				print("Non ancora raggiunti")
			time.sleep(10)			
	except KeyboardInterrupt:	
		server.stop(0)



"""
Questa funzione consente di generare i messaggi in
modo da poter utilizzare lo stream per le request.
Il contenuto del file viene inviato a chunk in modo
da poter gestire scenari in cui il file ha grandi
dimensioni.
"""
def generate_messages(contenuto):
	
	global CHUNK_DIM
	messages = []
	
	# Computo il numero di bytes da trasferire
	dim = len(contenuto)
	
	print("Dimensione del contenuto: " + str(dim))
	
	# Computo il numero di chunk
	q = dim // CHUNK_DIM	
	print("Il valore di q: " + str(q))
	
	# Computo la dimensione dell'eventuale ultimo chunk
	r = dim % CHUNK_DIM
	print("Il valore di r: " + str(r))
	
	if(q == 0):	
		# Sono nel caso in cui ho un solo chunk
		messages.append(av_pb2.input(file=contenuto, num_chunk=0))
	else:
		count=0
		for i in range(0, q):
			try:
				messages.append(av_pb2.input(file=contenuto[i*CHUNK_DIM:i*CHUNK_DIM+CHUNK_DIM], num_chunk=i))
			except:			
				print("Errore trasferimento chunk " + str(i))				
			count = count + 1

		if(r > 0):
			lower_bound = count * CHUNK_DIM
			messages.append(av_pb2.input(file=contenuto[lower_bound:lower_bound+r], num_chunk=count))

	# Restituisco i messaggi che sono stati precedentemente creati
	for msg in messages:	
		print("chunk #" + str(msg.num_chunk) + " inviato.")		
		time.sleep(1/10)
		yield msg
		
	# print(messages)



@app.route('/')
def index():

	if(launch_server_grpc):
		# Creazione del thread che si occuperà dalla gestione degli ACKs dagli AV
		try:
			thread = Thread(target = wait_acks)
			thread.start()
		except:
			print("Errore creazione del thread")
			render_template("error.html", error="Impossibile contattare gli antivirus, ricaricare la pagina.")
			
		print("Creazione del thread avvenuta con successo")
		
		
	error = check_conf_and_initial_snapshot()
	
	if error == 1 or error == 2:
		return render_template("index.html")
	
	elif error == 3:
		return render_template("error.html", error="Comportamento anomalo dell'applicazione.")
	
	return render_template("menu.html")



def restore_snapshots():

	global port
	global do_restore
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Creazione socket avvenuta con successo.")
		except socket.error as err:
			print("Creazione socket conclusa con errore %s" %(err))
			continue

		try:
			s.connect(("192.168.1.108", port))
			print("Connessione avvenuta con successo")
		except Exception as e:
			print("Errore connessione socket %s" %(e))
			continue
			
		try:
			msg = s.recv(1024).decode()
			print("Messaggio di risposta ricevuto dall'host: %s" %(msg))
			break
		except Exception as e:
			print("Errore nella ricezione della risposta da parte dell'host")
		
	do_restore = False	
	print("Gli snapshot sono stati restaurati con successo dall'host.")





@app.route('/malwareAnalysis', methods=('GET','POST'))
def analysis():

	global AV1_IP
	global AV1_PORT
	global do_restore
	
	ret = check_conf_and_initial_snapshot()
	
	if (ret == 1 or ret == 2):
		return render_template("error.html", error="Errore di inconsistenza nell'applicazione.")
	# 	print("Il numero di ACK ricevuti è pari a " + str(num_acks))
	# 	return '<h1>Attendi, configurazioni AVs in corso...</h1>'
	# elif(ret == 2):
	# 	print("In attesa degli snapshot...")
	# 	return '<h1>Attendi, snapshots in corso...</h1>'
	elif(ret == 3):
		flash('Attendi qualche secondo, ripristino snapshot in corso...')
		#restore_snapshots()

		print("In attesa della pulizia dell'ambiente a seguito dell'analisi.")
	else:
		print("Si recupera il contenuto del binario richiesto")


	# Recupero il nome del file che dovrà essere inviato agli AVs per la scansione.
	filename = ""
	if request.method == "POST":
		filename = request.form['formFile']
		print(filename)

	
	# Apro il file
	try:
		f = open(filename, mode='rb')
	except:
		return render_template("error.html", error="Il file selezionato non esiste.")
	
	# Leggo il contenuto del file
	contenuto = f.read()

	# Chiusura del file	
	f.close()
	
	try:
		channel = grpc.insecure_channel(AV1_IP + ":" + AV1_PORT)
		stub = av_pb2_grpc.SendBinaryStub(channel)
		responses = stub.sendBinary(generate_messages(contenuto))
		for response in responses:
			print(response.response)	
	except:
		print("Errore invio messaggi agli AV.")
		
	do_restore = True
	
	# Restituisci i risultati dell'analisi del binario fatta dagli AVs
		
	return render_template("results.html", results=response.response)





if __name__== "__main__":		
	app.run()
