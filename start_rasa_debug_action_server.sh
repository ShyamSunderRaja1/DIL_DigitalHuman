#!/bin/sh
#------------------------------------------------------------------------------
# Rasa Action Server
# ***  restart whenever there are env/rasa/actions/actions.py code changes
#------------------------------------------------------------------------------

public_ip=$(curl -s icanhazip.com)

#RASA_PORT=5005
RASA_ACTION_PORT=5055

echo Rasa ACTION server will now listen on http://$public_ip:$RASA_ACTION_PORT
 
rasa run actions -p $RASA_ACTION_PORT

