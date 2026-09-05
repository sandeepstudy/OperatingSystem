import matplotlib.pyplot as plt

def fcfs(processes, arrival_time, burst_time):
    n = len(processes)
    completion_time = [0] * n
    waiting_.time = [0] * n
    turnaround_time = [0] * n

    # Sort processes by arrival time (and keep original order for ties)
    proc_data = sorted(zip(processes, arrival_time, burst_time), key=lambda x: x[1])
    gantt = []
    current_time = 0

    for p, at, bt in proc_data:
        if current_time < at:
            current_time = at  # CPU idle before this process starts
        start_time = current_time
        waiting_time[processes.index(p)] = start_time - at
        current_time += bt
        completion_time[processes.index(p)] = current_time
        turnaround_time[processes.index(p)] = bt + waiting_time[processes.index(p)]
        gantt.append((p, start_time, bt, current_time))

    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    # Table rows
    rows = []
    for i in range(n):
        rows.append([
            processes[i],
            arrival_time[i],
            burst_time[i],
            completion_time[i],
            waiting_time[i],
            turnaround_time[i]
        ])

    # ---- Single Figure with 2 Subplots ----
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), height_ratios=[1.1, 1.4])

    # Gantt Chart
    ax1.set_title("Gantt Chart — First Come First Serve (FCFS)")
    ax1.set_xlabel("Time")
    ax1.set_yticks([])
    ax1.set_ylim(0, 10)
    ax1.set_xlim(0, max(completion_time) + 2)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.4)

    for p, start, dur, ct in gantt:
        ax1.broken_barh([(start, dur)], (2, 6), edgecolor='black')
        ax1.text(start + dur/2, 5, p, ha='center', va='center', fontweight='bold')
        ax1.text(ct, 1, str(ct), ha='center', va='top', fontsize=9)

    if gantt:
        ax1.text(gantt[0][1], 1, str(gantt[0][1]), ha='center', va='top', fontsize=9)

    # Table
    ax2.set_title("FCFS — Metrics", pad=8)
    ax2.axis('off')
    table = ax2.table(
        cellText=rows,
        colLabels=["Process", "Arrival Time", "Burst Time", "Completion Time", "Waiting Time", "Turnaround Time"],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.2)

    fig.text(0.1, 0.02, f"Average Waiting Time: {avg_wt:.2f}", fontsize=10)
    fig.text(0.55, 0.02, f"Average Turnaround Time: {avg_tat:.2f}", fontsize=10)

    fig.tight_layout()
    plt.show()


def get_int(prompt, min_value=None):
    """Robust integer input helper."""
    while True:
        s = input(prompt).strip()
        try:
            val = int(s)
            if min_value is not None and val < min_value:
                print(f"Please enter an integer ≥ {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    try:
        n = get_int("Enter number of processes: ", min_value=1)
        processes, arrival_time, burst_time = [], [], []

        ask_arrival = input("Do you want to enter arrival times? (y/n): ").strip().lower() == 'y'

        for i in range(n):
            p = f"P{i+1}"
            processes.append(p)
            if ask_arrival:
                at = get_int(f"Enter Arrival Time for {p}: ", min_value=0)
            else:
                at = 0
            bt = get_int(f"Enter Burst Time for {p}: ", min_value=1)
            arrival_time.append(at)
            burst_time.append(bt)

        fcfs(processes, arrival_time, burst_time)

    except Exception as e:
        print("\nAn unexpected error occurred:", e)
        input("\nPress Enter to exit...")
