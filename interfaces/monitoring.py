from diskcache import Cache
from applications.detail_page_scraper.priority_queue import PriorityQueue


class MonitoringManager:
    def __init__(self):
        self.monitoring_cache = Cache('monitoring_cache')
        self.priority_queue = PriorityQueue()


    def add_list_page_real_time(
        self, 
        website_name: str, 
        start_time: bool
    ):
        self.monitoring_cache.set('list_page_current_website', website_name)
        self.monitoring_cache.set('list_page_current_start_time', start_time)


    def set_list_page_sleeping(self, sleeping: bool):
        self.monitoring_cache.set('list_page_sleeping', sleeping)
    

    def get_list_page_real_time(self):
        return {
            'website_name': self.monitoring_cache.get('list_page_current_website'),
            'start_time': self.monitoring_cache.get('list_page_current_start_time'),
            'sleeping': self.monitoring_cache.get('list_page_sleeping')
        }
    
    def add_data_extraction_real_time(
        self, 
        website_name: str, 
        start_time: bool
    ):
        self.monitoring_cache.set('data_extraction_current_website', website_name)
        self.monitoring_cache.set('data_extraction_current_start_time', start_time)


    def set_data_extraction_sleeping(self, sleeping: bool):
        self.monitoring_cache.set('data_extraction_sleeping', sleeping)


    def get_data_extraction_real_time(self):
        return {
            'website_name': self.monitoring_cache.get('data_extraction_current_website'),
            'start_time': self.monitoring_cache.get('data_extraction_current_start_time'),
            'sleeping': self.monitoring_cache.get('data_extraction_sleeping')
        }

    def get_all_real_time(self):
        return {
            'list_page': self.get_list_page_real_time(),
            'data_extraction': self.get_data_extraction_real_time()
        }
    
    def get_priority_queue_details(self):
        details = self.priority_queue.details()
        return {
            'total_items': details[0],
            'priority_0': details[1]['priority_0'],
            'priority_1': details[1]['priority_1'],
            'priority_2': details[1]['priority_2'],
            'priority_3': details[1]['priority_3'],
            'priority_4': details[1]['priority_4'],
            'priority_5': details[1]['priority_5'],
            'priority_6': details[1]['priority_6'],
            'priority_7': details[1]['priority_7'],
            'priority_8': details[1]['priority_8'],
            'priority_9': details[1]['priority_9']
        }