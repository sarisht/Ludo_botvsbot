# for i in {1..5}
# do
# 	echo "Run Number $i" 
	# server/server 8000 &
	# sleep 2
	# client/client 127.0.0.1 8000 ludo.py --noBoard &
	# sleep 2
	# client/client 127.0.0.1 8000 ludo_gagan.py  &
	# sleep 10
# done

for i in 1 2 3 4 5
do
	echo "Welcome $i times"
	server/server 8000 &
	sleep 2
	client/client 127.0.0.1 8000 ludo.py --noBoard &
	sleep 2
	client/client 127.0.0.1 8000 ludo_gagan.py  &
	sleep 10
done