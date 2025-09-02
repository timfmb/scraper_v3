from diskcache import Deque, Cache


class PriorityQueue:
    def __init__(self, directory='./priority_queue', num_priorities=10):
        self.directory = directory
        self.num_priorities = num_priorities
        self.queues = [Deque(directory=f"{self.directory}/priority_{i}") for i in range(self.num_priorities)]
        self.in_queue = Cache(directory=f"{self.directory}/in_queue", size_limit=1000000000000)
        self.in_processing = Cache(directory=f"{self.directory}/in_processing", size_limit=1000000000000)


    def __len__(self):
        return sum(len(queue) for queue in self.queues)


    def put(self, item, priority, force=False):
        # Check if item is not in queue and not being processed
        if force or (not self.in_queue.get(item['url']) and not self.is_in_processing(item)):
            self.queues[priority].append(item)
            self.in_queue[item['url']] = True
            return True
        return False


    def get(self):
        for i, queue in enumerate(self.queues):
            if queue:
                item = queue.popleft()
                self.in_queue.pop(item['url'])
                return item, i
        return None
    

    def empty(self):
        return all(len(queue) == 0 for queue in self.queues)
    

    def is_in_queue(self, item):
        return self.in_queue.get(item) is not None
        

    def set_in_processing(self, item):
        self.in_processing[item['url']] = True
    
    def remove_from_processing(self, item):
        self.in_processing.pop(item['url'])

    def is_in_processing(self, item):
        return self.in_processing.get(item['url']) is not None

    def priority_count(self, priority):
        return len(self.queues[priority])

    def details(self):
        total_items = sum(len(queue) for queue in self.queues)
        queues_details = {}
        for i, queue in enumerate(self.queues):
            queues_details[f'priority_{i}'] = len(queue)
        return total_items, queues_details