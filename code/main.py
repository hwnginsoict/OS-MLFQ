import tkinter as tk
import customtkinter as ctk
from CTkTable import *
from Queue import Queue
from Process import Process
from copy import deepcopy

# Q0: 10 Q1: 20 Q3: 40 P0: 0,90 P1: 100,80 P2:80,60 P3:130,75
inf = 10**9

# System settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Global variable
queue_cnt = 0
queue_list  = []

process_cnt = 0
process_list = []
allprocess_list = []
reset_process_list = []

process_with_cpu = None
last_timestep = 0
upgrade_bound = 100
last_cpu = None
finish_check = False

# Add queue window
def add_queue_window():
    addqueueWindow = ctk.CTk()

    addqueueWindow.geometry("480x80+400+180")
    addqueueWindow.resizable(0, 0)
    addqueueWindow.title("Add Queue")
    
    addqueueWindow.grid_columnconfigure((0, 1), weight=1)
    addqueueWindow.grid_rowconfigure((0, 1), weight=1)
    
    # Label
    addqueue_label = ctk.CTkLabel(addqueueWindow, text=f"Add Queue:\tRR{queue_cnt}:\t")
    addqueue_label.grid(row=0, column=0)

    addqueue_quantum = ctk.CTkLabel(addqueueWindow, text="Quantum")
    addqueue_quantum.grid(row=0, column=1)

    # Entry
    addqueue_entry = ctk.CTkEntry(addqueueWindow)
    addqueue_entry.grid(row=1, column=1)

    # Add queue
    def add_queue():
        global queue_cnt
        queue_list.append(Queue(queue_cnt, int(addqueue_entry.get())))
        queue_cnt += 1
        addqueueWindow.destroy()

    # Submit button
    addqueue_button = ctk.CTkButton(addqueueWindow, text="Submit", command=add_queue)
    addqueue_button.grid(row=1, column=0)

    addqueueWindow.mainloop()

# Add process window
def add_process_window():
    global reset_process_list
    addprocessWindow = ctk.CTk()

    addprocessWindow.geometry("480x80+400+400")
    addprocessWindow.resizable(0, 0)
    addprocessWindow.title("Add Process")

    addprocessWindow.grid_columnconfigure((0, 1, 2), weight=1)
    addprocessWindow.grid_rowconfigure((0, 1), weight=1)

    # Label
    addprocess_label = ctk.CTkLabel(addprocessWindow, text=f"Add Process:\tP{process_cnt}:\t")
    addprocess_label.grid(row=0, column=0)

    addprocess_arrivaltime = ctk.CTkLabel(addprocessWindow, text="Arrival Time")
    addprocess_arrivaltime.grid(row=0, column=1)
    
    addprocess_bursttime = ctk.CTkLabel(addprocessWindow, text="Burst Time")
    addprocess_bursttime.grid(row=0, column=2)

    # Entry
    addprocess_entry_arrivaltime = ctk.CTkEntry(addprocessWindow)
    addprocess_entry_arrivaltime.grid(row=1, column=1)
    
    addprocess_entry_bursttime = ctk.CTkEntry(addprocessWindow)
    addprocess_entry_bursttime.grid(row=1, column=2)

    # Add process
    def add_process():
        global process_cnt
        process_list.append(Process(process_cnt, int(addprocess_entry_arrivaltime.get()), int(addprocess_entry_bursttime.get())))
        reset_process_list.append(Process(process_cnt, int(addprocess_entry_arrivaltime.get()), int(addprocess_entry_bursttime.get())))
        process_cnt += 1
        addprocessWindow.destroy()

    # Submit button
    addprocess_button = ctk.CTkButton(addprocessWindow, text="Submit", command=add_process)
    addprocess_button.grid(row=1, column=0)

    addprocessWindow.mainloop()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App settings
        self.geometry("1200x512+70+100")
        self.title("MLFQ")

        # Grid layout (2x1)
        self.grid_columnconfigure((0, 2, 3, 4), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((2, 5), weight=1)
        self.grid_rowconfigure((0, 1, 3, 4), weight=0)

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")

        # Create input label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Input")
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Create add queue button
        self.addqueue_button = ctk.CTkButton(self.sidebar_frame, text="Add Queue", command=add_queue_window)
        self.addqueue_button.grid(row=1, column=0, padx=20, pady=20)

        # Create add process button
        self.addprocess_button = ctk.CTkButton(self.sidebar_frame, text="Add Process", command=add_process_window)
        self.addprocess_button.grid(row=2, column=0, padx=20, pady=20)

        # Create submit button
        # Submit
        def submit():
            global queue_list, process_list, allprocess_list, process_with_cpu, last_timestep, upgrade_bound, last_cpu, finish_check

            #Reset
            if allprocess_list:
                process_list = deepcopy(reset_process_list)
                queue_list.pop(-1)

                process_with_cpu = None
                last_timestep = 0
                last_cpu = None
                finish_check = False

            # Display frame
            self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
            
            # Add Time label
            self.time_label = ctk.CTkLabel(self.main_frame, text="Time:")
            self.time_label.grid(row=0, column=1, padx=40, pady=20, sticky="nw")
            timetext = tk.StringVar()
            timetext.set("0")
            self.time = ctk.CTkLabel(self.main_frame, textvariable=timetext)
            self.time.grid(row=0, column=2, padx=20, pady=20, sticky="nw")

            # Add next button
            # Finish
            def finish(curtime):
                process_text.set(process_text.get()+f"  P{last_cpu.process_id}  |")
                time_text = f"{curtime}"
                while len(time_text) < 7:
                    time_text = " "+time_text 
                timeline_text.set(timeline_text.get()+time_text)

                self.awt_label = ctk.CTkLabel(self.main_frame, text=f"Average Waiting Time : \t{sum(self.table.get_column(7)[1:])/(len(value_table)-1)}")
                self.awt_label.grid(row=5, column=1, columnspan=4, padx=40, pady=0, sticky="sw")

            # Downgrade a process after using CPU
            def downgrade(process, curtime):
                global last_timestep, process_with_cpu
                for proc in allprocess_list:
                    # Update downgrade process
                    if proc is process:
                        queue_list[proc.cur_queue].queue.pop(0)
                        proc.cur_queue += 1

                        # Remain Time
                        proc.remain_time -= proc.remain_cpu
                        self.table.insert(row=proc.process_id+1, column=5, value=proc.remain_time)

                        # Return CPU
                        self.table.insert(row=proc.process_id+1, column=2, value=".")

                        # Finish process
                        if proc.remain_time == 0:
                            self.table.insert(row=proc.process_id+1, column=1, value="X")
                            proc.completion_time = curtime
                            self.table.insert(row=proc.process_id+1, column=6, value=proc.completion_time)
                            process_with_cpu = None
                        else:
                            # Update State
                            if proc.cur_queue == len(queue_list)-1:
                                self.table.insert(row=proc.process_id+1, column=1, value="FCFS")
                                proc.fcfs_arrive = curtime
                            else:
                                self.table.insert(row=proc.process_id+1, column=1, value=f"RR{proc.cur_queue}")

                            # Move to below queue
                            queue_list[proc.cur_queue].queue.append(proc)

                    # Increase other processes waiting time
                    elif proc.arrival_time < curtime and proc.completion_time == -1:
                        proc.waiting_time += curtime-last_timestep
                        self.table.insert(row=proc.process_id+1, column=7, value=proc.waiting_time)

            # Give the CPU to a new process
            def give_cpu(curtime):
                global last_cpu, process_with_cpu
                for qqueue in queue_list:
                    if qqueue.queue:
                        process = qqueue.queue[0]
                        
                        process.remain_cpu = min(process.remain_time, qqueue.quantum)
                        self.table.insert(row=process.process_id+1, column=2, value="*")
                        process_with_cpu = process

                        # Update Gantt Chart
                        if process is not last_cpu:
                            if last_cpu != None:
                                process_text.set(process_text.get()+f"  P{last_cpu.process_id}  |")
                                time_text = f"{curtime}"
                                while len(time_text) < 7:
                                    time_text = " "+time_text 
                                timeline_text.set(timeline_text.get()+time_text)
                            last_cpu = process
                        return

            # Add a new arriving process
            def add_new_process(process, curtime):
                global last_timestep
                for proc in allprocess_list:
                    # Update process with CPU
                    if proc is process_with_cpu:
                        proc.remain_time -= curtime-last_timestep
                        self.table.insert(row=proc.process_id+1, column=5, value=proc.remain_time)

                        proc.remain_cpu -= curtime-last_timestep

                    # Increase other processes waiting time
                    elif proc.arrival_time < curtime and proc.completion_time == -1:
                        proc.waiting_time += curtime-last_timestep
                        self.table.insert(row=proc.process_id+1, column=7, value=proc.waiting_time)

                # Add arriving process to 1st queue
                queue_list[0].queue.append(process)
                process.cur_queue = 0
                self.table.insert(row=process.process_id+1, column=1, value="RR0")
            
            # Upgrade a process from FCFS queue
            def upgrade(process, curtime):
                global last_timestep
                for proc in allprocess_list:
                    # Update process with CPU
                    if proc is process_with_cpu:
                        proc.remain_time -= curtime-last_timestep
                        self.table.insert(row=proc.process_id+1, column=5, value=proc.remain_time)

                        proc.remain_cpu -= curtime-last_timestep

                    # Increase other processes waiting time
                    elif proc.arrival_time < curtime and proc.completion_time == -1:
                        proc.waiting_time += curtime-last_timestep
                        self.table.insert(row=proc.process_id+1, column=7, value=proc.waiting_time)

                # Move process to high priority queue
                queue_list[0].queue.append(process)
                process.cur_queue = 0
                self.table.insert(row=process.process_id+1, column=1, value="RR0")

            def next_timestep():
                global process_with_cpu, last_timestep, upgrade_bound, last_cpu, finish_check
                # Next time that case 1 happen: the process with CPU finish
                finish_cpu = inf
                if process_with_cpu != None:
                    finish_cpu = last_timestep + process_with_cpu.remain_cpu

                # Next time that case 2 happen: a process arrive
                next_arrival = inf
                if process_list:
                    next_arrival = process_list[0].arrival_time

                # Next time that case 3 happen: a process is upgraded from FCFS
                next_upgrade = inf
                if queue_list[-1].queue:
                    next_upgrade = queue_list[-1].queue[0].fcfs_arrive + upgrade_bound

                # Check if all finish
                if finish_cpu == inf and next_arrival == inf and next_upgrade == inf:
                    if not finish_check:
                        finish(last_timestep)
                        finish_check = True
                    return
                
                # Case 1 happen first
                if finish_cpu <= next_arrival and finish_cpu <= next_upgrade:
                    downgrade(process_with_cpu, finish_cpu)
                    
                    last_timestep = finish_cpu
                    
                    # Add arriving processes
                    next_arrive = next_arrival
                    while next_arrive == finish_cpu and process_list:
                        add_new_process(process_list.pop(0), next_arrival)
                        next_arrive = -1
                        if process_list:
                            next_arrive = process_list[0].arrival_time
                    
                    # Move background processes to high priority queue
                    next_up = next_upgrade
                    while next_up == finish_cpu and queue_list[-1].queue:
                        upgrade(queue_list[-1].queue.pop(0), next_upgrade)
                        next_upgrade = -1
                        if queue_list[-1].queue:
                            next_up = queue_list[-1].queue[0].fcfs_arrive + upgrade_bound

                    give_cpu(finish_cpu)

                # Case 2 happen first
                else:
                    if next_arrival < finish_cpu and next_arrival <= next_upgrade:
                        # Add arriving processes
                        tmp = next_arrive = next_arrival
                        while next_arrive == tmp and process_list:
                            add_new_process(process_list.pop(0), next_arrival)
                            next_arrive = -1
                            if process_list:
                                next_arrive = process_list[0].arrival_time
                        
                        # Preemptive
                        if process_with_cpu != None and process_with_cpu.cur_queue > 0:
                            # queue_tmp = f"RR{process_with_cpu.cur_queue}" if process_with_cpu.cur_queue < len(queue_list)-1 else "FCFS"
                            self.table.insert(row=process_with_cpu.process_id+1, column=2, value=".")

                        last_timestep = next_arrival
                    
                    # Case 3 happen first
                    if next_upgrade < finish_cpu and next_upgrade <= next_arrival:
                        # Move background processes to high priority queue
                        tmp = next_up = next_upgrade
                        while next_up == tmp and queue_list[-1].queue:
                            upgrade(queue_list[-1].queue.pop(0), next_upgrade)
                            next_up = -1
                            if queue_list[-1].queue:
                                next_up = queue_list[-1].queue[0].fcfs_arrive + upgrade_bound
                        
                        # Preemptive
                        if process_with_cpu != None and process_with_cpu.cur_queue > 0:
                            # queue_tmp = f"RR{process_with_cpu.cur_queue}" if process_with_cpu.cur_queue < len(queue_list)-1 else "FCFS"
                            self.table.insert(row=process_with_cpu.process_id+1, column=2, value=".")
                        
                        last_timestep = next_upgrade
                    
                    if process_with_cpu == None or process_with_cpu.cur_queue > 0:
                        give_cpu(min(next_arrival, next_upgrade))
                
                timetext.set(str(last_timestep))

            # Next button
            self.next_button = ctk.CTkButton(self.main_frame, text="Next", command=next_timestep)
            self.next_button.grid(row=0, column=3, padx=20, pady=20, sticky="ne")

            # Reset button
            self.reset_button = ctk.CTkButton(self.main_frame, text="Reset", command=submit)
            self.reset_button.grid(row=0, column=4, padx=40, pady=20, sticky="ne")

            self.main_frame.grid_columnconfigure(3, weight=1)

            # Add scheduling table
            value_table = [["Process", "Queue", "CPU", "Arrival Time", "Burst Time", "Remaining Time", "Completion Time", "Waiting Time"]]
            for process in process_list:
                row = [process.get_name(), "___", ".", process.arrival_time, process.burst_time, process.burst_time, "___", 0]
                value_table.append(row)

            self.table = CTkTable(self.main_frame, values=value_table)
            self.table.grid(row=1, column=1, columnspan=4, padx=20, pady=20, sticky="new")
            
            # Add Gantt Chart label
            self.ganttchart_label = ctk.CTkLabel(self.main_frame, text="Gantt Chart")
            self.ganttchart_label.grid(row=2, column=1, padx=40, pady=20, sticky="sw")

            # Add Gantt Chart process
            process_text = tk.StringVar()
            process_text.set("Process|")
            self.ganttchart_process = ctk.CTkLabel(self.main_frame, textvariable=process_text, font=("Consolas", 12))
            self.ganttchart_process.grid(row=3, column=1, columnspan=4, padx=40, pady=0, sticky="nw")

            # Add Gantt Chart timeline
            timeline_text = tk.StringVar()
            timeline_text.set("       0")
            self.ganttchart_timeline = ctk.CTkLabel(self.main_frame, textvariable=timeline_text, font=("Consolas", 12))
            self.ganttchart_timeline.grid(row=4, column=1, columnspan=4, padx=40, pady=0, sticky="nw")

            self.main_frame.grid_rowconfigure(5, weight=1)
            
            # Add FCFS to queue list
            queue_list.append(Queue(queue_cnt, inf))

            # Sort process_list with respect to arrival time
            allprocess_list = process_list.copy()
            process_list.sort()

        # Submit button
        self.submit_button = ctk.CTkButton(self.sidebar_frame, text="Submit", command=submit)
        self.submit_button.grid(row=5, column=0, sticky="s", padx=20, pady=20)

        self.sidebar_frame.grid_rowconfigure(5, weight=1)

# Run
if __name__ == "__main__":
    app = App()
    app.mainloop()   