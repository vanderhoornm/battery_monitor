/*
Reads the battery status file and graphs the data points
Copyright (C) 2013 Maurits van der Hoorn

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#include <stdio.h>
#include <time.h>

int get_battery_level()
{
    int level = -1;
    FILE *f = fopen("/sys/class/power_supply/BAT1/charge_now", "r");
    if (f) {
        fscanf(f, "%i", &level);
        fclose(f);
    }
    return level;
}

int main()
{
    int level = 0;
    time_t time_now;
    FILE *o;
    while (level != -1) {
        o = fopen(LOG, "ab");
        if (o) {
            level = get_battery_level();
            time_now = time(0);
            fwrite(&level, sizeof(int), 1, o);
            fwrite(&time_now, sizeof(time_t), 1, o);
            fclose(o);
            usleep(INTERVAL);
        } else {
            break;
        }
    }
    return 0;
}

