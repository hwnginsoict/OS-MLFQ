import streamlit as st
import pandas as pd
from copy import deepcopy


class Queue:
    def __init__(self, queue_id, quantum):
        self.queue_id = queue_id
        self.quantum = quantum
        self.queue = []

class Process():
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remain_time = burst_time
        self.completion_time = -1
        self.waiting_time = 0        
        self.remain_cpu = 0
        self.fcfs_arrive = 0
        self.cur_queue = 0

    def __lt__(self, other):
        return (self.arrival_time, self.process_id) < (other.arrival_time, other.process_id)
    
    def get_name(self):
        return f"P{self.process_id}"

# Constants
inf = 10**9

# Initialize session state
if 'queue_cnt' not in st.session_state:
    st.session_state.queue_cnt = 0
if 'queue_list' not in st.session_state:
    st.session_state.queue_list = []
if 'process_cnt' not in st.session_state:
    st.session_state.process_cnt = 0
if 'process_list' not in st.session_state:
    st.session_state.process_list = []
if 'allprocess_list' not in st.session_state:
    st.session_state.allprocess_list = []
if 'reset_process_list' not in st.session_state:
    st.session_state.reset_process_list = []
if 'process_with_cpu' not in st.session_state:
    st.session_state.process_with_cpu = None
if 'last_timestep' not in st.session_state:
    st.session_state.last_timestep = 0
if 'upgrade_bound' not in st.session_state:
    st.session_state.upgrade_bound = 100
if 'last_cpu' not in st.session_state:
    st.session_state.last_cpu = None
if 'finish_check' not in st.session_state:
    st.session_state.finish_check = False
if 'simulation_started' not in st.session_state:
    st.session_state.simulation_started = False
if 'gantt_process' not in st.session_state:
    st.session_state.gantt_process = "Process|"
if 'gantt_timeline' not in st.session_state:
    st.session_state.gantt_timeline = "       0"
if 'current_time' not in st.session_state:
    st.session_state.current_time = 0

def add_queue(quantum):
    st.session_state.queue_list.append(Queue(st.session_state.queue_cnt, quantum))
    st.session_state.queue_cnt += 1

def add_process(arrival_time, burst_time):
    process = Process(st.session_state.process_cnt, arrival_time, burst_time)
    st.session_state.process_list.append(process)
    st.session_state.reset_process_list.append(Process(st.session_state.process_cnt, arrival_time, burst_time))
    st.session_state.process_cnt += 1

def reset_simulation():
    if st.session_state.allprocess_list:
        st.session_state.process_list = deepcopy(st.session_state.reset_process_list)
        if st.session_state.queue_list:
            st.session_state.queue_list.pop(-1)  # Remove FCFS queue
        
        st.session_state.process_with_cpu = None
        st.session_state.last_timestep = 0
        st.session_state.last_cpu = None
        st.session_state.finish_check = False
        st.session_state.simulation_started = False
        st.session_state.gantt_process = "Process|"
        st.session_state.gantt_timeline = "       0"
        st.session_state.current_time = 0

def start_simulation():
    st.session_state.queue_list.append(Queue(st.session_state.queue_cnt, inf))
    
    st.session_state.allprocess_list = st.session_state.process_list.copy()
    st.session_state.process_list.sort()
    st.session_state.simulation_started = True

def finish_simulation(curtime):
    st.session_state.gantt_process += f"  P{st.session_state.last_cpu.process_id}  |"
    time_text = f"{curtime}"
    while len(time_text) < 7:
        time_text = " " + time_text
    st.session_state.gantt_timeline += time_text

def downgrade(process, curtime):
    for proc in st.session_state.allprocess_list:
        if proc is process:
            st.session_state.queue_list[proc.cur_queue].queue.pop(0)
            proc.cur_queue += 1
            proc.remain_time -= proc.remain_cpu
            
            if proc.remain_time == 0:
                proc.completion_time = curtime
                st.session_state.process_with_cpu = None
            else:
                if proc.cur_queue == len(st.session_state.queue_list) - 1:
                    proc.fcfs_arrive = curtime
                st.session_state.queue_list[proc.cur_queue].queue.append(proc)
        
        elif proc.arrival_time < curtime and proc.completion_time == -1:
            proc.waiting_time += curtime - st.session_state.last_timestep

def give_cpu(curtime):
    for qqueue in st.session_state.queue_list:
        if qqueue.queue:
            process = qqueue.queue[0]
            process.remain_cpu = min(process.remain_time, qqueue.quantum)
            st.session_state.process_with_cpu = process
            
            if process is not st.session_state.last_cpu:
                if st.session_state.last_cpu is not None:
                    st.session_state.gantt_process += f"  P{st.session_state.last_cpu.process_id}  |"
                    time_text = f"{curtime}"
                    while len(time_text) < 7:
                        time_text = " " + time_text
                    st.session_state.gantt_timeline += time_text
                st.session_state.last_cpu = process
            return

def add_new_process(process, curtime):
    for proc in st.session_state.allprocess_list:
        if proc is st.session_state.process_with_cpu:
            proc.remain_time -= curtime - st.session_state.last_timestep
            proc.remain_cpu -= curtime - st.session_state.last_timestep
        elif proc.arrival_time < curtime and proc.completion_time == -1:
            proc.waiting_time += curtime - st.session_state.last_timestep
    
    st.session_state.queue_list[0].queue.append(process)
    process.cur_queue = 0

def upgrade(process, curtime):
    for proc in st.session_state.allprocess_list:
        if proc is st.session_state.process_with_cpu:
            proc.remain_time -= curtime - st.session_state.last_timestep
            proc.remain_cpu -= curtime - st.session_state.last_timestep
        elif proc.arrival_time < curtime and proc.completion_time == -1:
            proc.waiting_time += curtime - st.session_state.last_timestep
    
    st.session_state.queue_list[0].queue.append(process)
    process.cur_queue = 0

def next_timestep():
    finish_cpu = inf
    if st.session_state.process_with_cpu is not None:
        finish_cpu = st.session_state.last_timestep + st.session_state.process_with_cpu.remain_cpu

    next_arrival = inf
    if st.session_state.process_list:
        next_arrival = st.session_state.process_list[0].arrival_time

    next_upgrade = inf
    if st.session_state.queue_list[-1].queue:
        next_upgrade = st.session_state.queue_list[-1].queue[0].fcfs_arrive + st.session_state.upgrade_bound

    if finish_cpu == inf and next_arrival == inf and next_upgrade == inf:
        if not st.session_state.finish_check:
            finish_simulation(st.session_state.last_timestep)
            st.session_state.finish_check = True
        return

    if finish_cpu <= next_arrival and finish_cpu <= next_upgrade:
        downgrade(st.session_state.process_with_cpu, finish_cpu)
        st.session_state.last_timestep = finish_cpu
        
        next_arrive = next_arrival
        while next_arrive == finish_cpu and st.session_state.process_list:
            add_new_process(st.session_state.process_list.pop(0), next_arrival)
            next_arrive = -1
            if st.session_state.process_list:
                next_arrive = st.session_state.process_list[0].arrival_time
        
        next_up = next_upgrade
        while next_up == finish_cpu and st.session_state.queue_list[-1].queue:
            upgrade(st.session_state.queue_list[-1].queue.pop(0), next_upgrade)
            next_upgrade = -1
            if st.session_state.queue_list[-1].queue:
                next_up = st.session_state.queue_list[-1].queue[0].fcfs_arrive + st.session_state.upgrade_bound

        give_cpu(finish_cpu)

    else:
        if next_arrival < finish_cpu and next_arrival <= next_upgrade:
            tmp = next_arrive = next_arrival
            while next_arrive == tmp and st.session_state.process_list:
                add_new_process(st.session_state.process_list.pop(0), next_arrival)
                next_arrive = -1
                if st.session_state.process_list:
                    next_arrive = st.session_state.process_list[0].arrival_time
            
            if st.session_state.process_with_cpu is not None and st.session_state.process_with_cpu.cur_queue > 0:
                pass  
            
            st.session_state.last_timestep = next_arrival
        
        if next_upgrade < finish_cpu and next_upgrade <= next_arrival:
            tmp = next_up = next_upgrade
            while next_up == tmp and st.session_state.queue_list[-1].queue:
                upgrade(st.session_state.queue_list[-1].queue.pop(0), next_upgrade)
                next_up = -1
                if st.session_state.queue_list[-1].queue:
                    next_up = st.session_state.queue_list[-1].queue[0].fcfs_arrive + st.session_state.upgrade_bound
            
            if st.session_state.process_with_cpu is not None and st.session_state.process_with_cpu.cur_queue > 0:
                pass  
            
            st.session_state.last_timestep = next_upgrade
        
        if st.session_state.process_with_cpu is None or st.session_state.process_with_cpu.cur_queue > 0:
            give_cpu(min(next_arrival, next_upgrade))
    
    st.session_state.current_time = st.session_state.last_timestep

def get_process_table_data():
    data = []
    for process in st.session_state.allprocess_list:
        queue_name = "___"
        cpu_status = "."
        completion_time = "___"
        
        if st.session_state.simulation_started:
            if process.cur_queue == -1:
                queue_name = "___"
            elif process.cur_queue == len(st.session_state.queue_list) - 1:
                queue_name = "FCFS"
            else:
                queue_name = f"RR{process.cur_queue}"
            
            if process is st.session_state.process_with_cpu:
                cpu_status = "*"
            
            if process.completion_time != -1:
                completion_time = process.completion_time
                queue_name = "X"
        
        data.append({
            "Process": process.get_name(),
            "Queue": queue_name,
            "CPU": cpu_status,
            "Arrival Time": process.arrival_time,
            "Burst Time": process.burst_time,
            "Remaining Time": process.remain_time,
            "Completion Time": completion_time,
            "Waiting Time": process.waiting_time
        })
    
    return data

st.set_page_config(page_title="MLFQ Scheduler", layout="wide")

st.title("Multi-Level Feedback Queue (MLFQ) Scheduler")

with st.sidebar:
    st.header("Input")
    
    st.subheader("Add Queue")
    with st.form("add_queue_form"):
        quantum = st.number_input("Quantum", min_value=1, value=1, step=1)
        if st.form_submit_button("Add Queue"):
            add_queue(quantum)
            st.success(f"Added RR{st.session_state.queue_cnt-1} with quantum {quantum}")
    
    st.subheader("Add Process")
    with st.form("add_process_form"):
        arrival_time = st.number_input("Arrival Time", min_value=0, value=0, step=1)
        burst_time = st.number_input("Burst Time", min_value=1, value=1, step=1)
        if st.form_submit_button("Add Process"):
            add_process(arrival_time, burst_time)
            st.success(f"Added P{st.session_state.process_cnt-1}")
    
    if st.session_state.queue_list:
        st.subheader("Current Queues")
        for i, queue in enumerate(st.session_state.queue_list[:-1] if st.session_state.simulation_started else st.session_state.queue_list):
            st.write(f"RR{queue.queue_id}: Quantum = {queue.quantum}")
    
    if st.session_state.process_list or st.session_state.allprocess_list:
        st.subheader("Current Processes")
        process_display_list = st.session_state.allprocess_list if st.session_state.simulation_started else st.session_state.process_list
        for process in process_display_list:
            st.write(f"{process.get_name()}: AT={process.arrival_time}, BT={process.burst_time}")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if not st.session_state.simulation_started:
        if st.button("Submit", type="primary"):
            if st.session_state.queue_list and st.session_state.process_list:
                start_simulation()
                st.rerun()
            else:
                st.error("Please add at least one queue and one process")

with col2:
    if st.session_state.simulation_started and not st.session_state.finish_check:
        if st.button("Next Step"):
            next_timestep()
            st.rerun()

with col3:
    if st.session_state.simulation_started:
        if st.button("Reset"):
            reset_simulation()
            st.rerun()

# Display current time
if st.session_state.simulation_started:
    st.subheader(f"Current Time: {st.session_state.current_time}")

# Display process table
if st.session_state.process_list or st.session_state.allprocess_list:
    st.subheader("Process Table")
    table_data = get_process_table_data()
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

# Display Gantt Chart
if st.session_state.simulation_started:
    st.subheader("Gantt Chart")
    st.code(st.session_state.gantt_process, language=None)
    st.code(st.session_state.gantt_timeline, language=None)

# Display Average Waiting Time when simulation is complete
if st.session_state.finish_check and st.session_state.allprocess_list:
    total_waiting_time = sum(proc.waiting_time for proc in st.session_state.allprocess_list)
    avg_waiting_time = total_waiting_time / len(st.session_state.allprocess_list)
    st.success(f"Average Waiting Time: {avg_waiting_time:.2f}")

# Instructions
with st.expander("Instructions"):
    st.markdown("""
    1. **Add Queues**: Add Round Robin queues with different quantum values
    2. **Add Processes**: Add processes with arrival and burst times
    3. **Submit**: Initialize the simulation (automatically adds FCFS queue at the end)
    4. **Next Step**: Execute the next timestep in the simulation
    5. **Reset**: Reset the simulation to start over
    
    The scheduler uses a Multi-Level Feedback Queue algorithm where:
    - Processes start in the highest priority queue (RR0)
    - If a process uses its full quantum, it moves to the next lower priority queue
    - The lowest priority queue uses FCFS scheduling
    - Processes in FCFS can be upgraded back to RR0 after a certain time period
    """)