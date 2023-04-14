from flask import Flask, render_template

import grpc
from proto import av_pb2
from proto import av_pb2_grpc

app = Flask(__name__)

CHUNK_DIM = 5000


def generate_messages(contenuto):
	
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
		# yeld av_pb2.input(file=contenuto, num_chunk=0)
		messages.append(av_pb2.input(file=contenuto, num_chunk=0))
		# print("Abbiamo un solo chunk del file.")

	else:
		count=0
		for i in range(0, q):
			try:
				# yeld av_pb2.input(file=contenuto[i*CHUNK_DIM:i*CHUNK_DIM+CHUNK_DIM], num_chunk=i)
				messages.append(av_pb2.input(file=contenuto[i*CHUNK_DIM:i*CHUNK_DIM+CHUNK_DIM], num_chunk=i))
				# print("Inserito nella lista chunk #" + str(i))
			except:
				print("Errore trasferimento chunk " + str(i))
			count = count + 1

		if(r > 0):
			lower_bound = count * CHUNK_DIM
			# yeld av_pb2.input(file=contenuto[lower_bound:lower_bound+r], num_chunk=count)
			messages.append(av_pb2.input(file=contenuto[lower_bound:lower_bound+r], num_chunk=count))
			# print("Inserito chunk non completo.")
	# print(messages)
			
	for msg in messages:
		print("chunk #" + str(msg.num_chunk) + " inviato.")
		yield msg
		
	print(messages)



@app.route('/')
def index():
	return render_template("Menu.html")
	
@app.route('/malwareAnalysis')
def analysis():

	filename = "prova"
	# Apro il file
	f = open(filename, mode='rb')
	
	# Leggo il contenuto del file
	contenuto = f.read()

	# Chiusura del file	
	f.close()
	
	# Creazione del canale e dello stub
	try:
		channel = grpc.insecure_channel('192.168.0.3:50053')
	except:
		print("Errore creazione canale.")
		
	stub = av_pb2_grpc.SendBinaryStub(channel)
	
	# Genero i chunk del file
	try:
		responses = stub.sendBinary(generate_messages(contenuto))
		for response in responses:
			print(response.response)	
	except:
		print("Errore invio messaggi agli AV.")
		
	return '<h1>Malware Analysis</h1>'




@app.route('/results')
def results():
	return '<h1>Questi sono i risultati</h1>'

if __name__=="__main__":
	app.run()
