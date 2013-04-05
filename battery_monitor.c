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

