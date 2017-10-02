server/server 8000 &
sleep 2
client/client 127.0.0.1 8000 ludo.py &
sleep 2
client/client 127.0.0.1 8000 ludo.py --noBoard &
