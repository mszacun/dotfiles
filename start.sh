#!/bin/sh
# mount -t ecryptfs /home/mandrak /home/mandrak
hdparm -B 255 /dev/sda
hdparm -S0 /dev/sda
smartctl -d ata -a /dev/sda | grep Load_Cycle_Count 
# modprobe acpi-cpufreq
# cpufreq-set -g ondemand
rmmod pcspkr
