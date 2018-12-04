import sys
from collections import defaultdict

data = sorted(sys.stdin.read().strip().split("\n"))

active_guard = None
active_sleep_time = None
guard_sleep_minutes = defaultdict(lambda: defaultdict(int))
for record in data:
    _, time, action, num = record.split(" ", 3)
    h, m = time[:-1].split(":")
    m = int(m)
    if action == "Guard":
        num = int(num.split(" ")[0][1:])
        active_guard = num
    elif action == "falls":
        active_sleep_time = m
    else:
        for i in range(active_sleep_time, m):
            guard_sleep_minutes[active_guard][i] += 1

guard_sleep_totals = sorted(
    (sum(minutes.values()), g)
    for g, minutes in guard_sleep_minutes.items()
)
chosen_guard = guard_sleep_totals[-1][1]

minutes = sorted(
    (count, m)
    for m, count in guard_sleep_minutes[chosen_guard].items()
)

chosen_minute = minutes[-1][1]

print(chosen_guard, chosen_minute, chosen_guard*chosen_minute)
