class Queue:
    def __init__(self, queue_id, quantum):
        self.queue_id = queue_id
        self.quantum = quantum
        self.queue = []