all:
	gcc -o battery_monitor battery_monitor.c -DLOG=\"${HOME}/.battery_monitor\" -DINTERVAL=60000000

clean:
	rm battery_monitor

install:
	cp battery_monitor ~/.kde4/Autostart/

uninstall:
	rm ~/.kde4/Autostart/battery_monitor
