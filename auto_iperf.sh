#!/bin/sh

# iperf ping (client) function definition

SERVER_IP="192.168.1.3"
TIME=30

ping_iperf()
{
	iperf3 -c $SERVER_IP -t $TIME > stdout.txt > stderr.txt || echo "WiFi CONNECTIVITY FAILED"
} 

# infinte looped ping

looped_ping()
{
	while :
	do
		ping_iperf 
		sleep 10
	done
}

# main execution

looped_ping
