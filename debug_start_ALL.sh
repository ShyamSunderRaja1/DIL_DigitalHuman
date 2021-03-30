#!/bin/sh

sh ./start_rasa_debug_action_server.sh &  PID_RASA_ACTION=$!
sh ./start_rasa_debug_main_server.sh &  PID_RASA_MAIN=$!
wait $PID_RASA_ACTION
wait $PID_RASA_MAIN