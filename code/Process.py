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

    # def __eq__(self, other):
    #     return self.arrival_time == other.arrival_time and self.process_id == other.process_id

    def __lt__(self, other):
        return (self.arrival_time, self.process_id) < (other.arrival_time, other.process_id)
    
    def get_name(self):
        return f"P{self.process_id}"