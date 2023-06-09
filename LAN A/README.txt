PASSAGGI PER CONFIGURARE IL SISTEMA DISTRIBUITO:
1) Eseguire gli script di configurazione nelle sottocartelle di DistributedSystem
2) Eseguire gli script di configurazione di rete presenti nella cartella A3 per il centralnode e A2 per gli antivirus
3) Assicurarsi di avere la comunicazione tra central node e host.:
	a. interfaccia di rete di virtualbox deve essere connessa alla NAT
	b. abilitare esplicitamente una rotta per l'host altrimenti i pacchetti 
	   vengono inoltrati di default verso il CE_A2. Usare: 
	   "sudo ip r a <ip host> via 10.0.3.2"