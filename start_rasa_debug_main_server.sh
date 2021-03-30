#!/bin/sh
#------------------------------------------------------------------------------
# Rasa Server
#------------------------------------------------------------------------------

public_ip=$(curl -s icanhazip.com)

RASA_PORT=5005
RASA_ACTION_PORT=5055

echo Rasa MAIN server will now listen on http://$public_ip:$RASA_PORT
echo ****************************************************************
echo Pls check that Rasa Action Server is running on $RASA_ACTION_PORT
 
rasa run -m models --enable-api --cors "*" --endpoints endpoints.yml -p $RASA_PORT

# we can specify multiple domain YMLs in a domain folder e.g. domain_intents.yml, domain_entitiesnslots.yml, etc.
# rasa train --domain path_to_domain_directory

# rasa run -vv -m models/ --endpoints endpoints.yml -p 5005