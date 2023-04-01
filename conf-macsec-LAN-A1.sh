#! /bin/bash

# Setto le variabili globali per la connessione macsec.
export MKA_CAK=00112233445566778899aabbccddeeff
export MKA_CKN=00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff

# Elimino l'eventuale connessione.
nmcli connection delete macsec-connection

# Aggiungo la connessione macsec.
nmcli connection add type macsec \
con-name macsec-connection \
ifname macsec0 connection.autoconnect yes \
macsec.parent enp0s3 \
macsec.mode psk \
macsec.mka-cak $MKA_CAK \
macsec.mka-cak-flags 0 \
macsec.mka-ckn $MKA_CKN \
ipv4.method manual \
ipv4.address 10.0.10.2/24
