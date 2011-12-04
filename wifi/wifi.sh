#!/usr/bin/sh

wpa_supplicant -B -Dwext -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
dhcpcd wlan0
route add default gw 192.168.1.1
