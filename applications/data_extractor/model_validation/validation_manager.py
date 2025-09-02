from .fuzzy_index import FuzzyIndex
from .image_check import image_check
from interfaces.production_db.client import get_db as get_atlas_search_engine_db
from interfaces.scraper_db.client import get_db


class MongoValidationCache:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['model_validation']

    def set(self, url, result):
        self.collection.delete_many({'url': url})
        self.collection.insert_one({'url': url, 'result': result})

    def get(self, url):
        result = self.collection.find_one({'url': url}, {'result': 1})
        if result:
            return result['result']
        else:
            return None



class ValidationManager:
    def __init__(self, db):
        self.db = db
        self.fuzzy_index_interface = FuzzyIndex(self.db)
        self.cache = MongoValidationCache()


    def build_image_result_dict(self, image_check_result):
        result_dict = {}
        for result in image_check_result:
            if not result.get('model_id'):
                continue
            model_id = str(result['model_id'])
            if model_id not in result_dict:
                result_dict[model_id] = 0
            result_dict[model_id] += 1
        result_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}
        return result_dict
    

    def check_fuzzy_vs_image(self, fuzzy_result, image_result_dict):
        image_result_keys = [key for key in image_result_dict.keys()]
        for model in fuzzy_result:
            if model['model_id'] in image_result_keys:
                return model
        return None
    

    
    def validate(self, url, comp_vec, make, model):
        try:
            if self.cache.get(url):
                return self.cache.get(url)
            comp_vec = comp_vec
            index_result = self.fuzzy_index_interface.check_make_model(make, model)
            if not index_result:
                self.cache.set(url, {
                    'valid': False
                })
                return {
                    'valid': False
                }

            image_check_result = image_check(self.db, comp_vec)
            image_result_dict = self.build_image_result_dict(image_check_result)
            result = self.check_fuzzy_vs_image(index_result, image_result_dict)
            if result:
                result['valid'] = True
                self.cache.set(url, result)
                return result
            else:
                self.cache.set(url, {
                    'valid': False
                })
                return {
                    'valid': False
                }
        except Exception as e:
            print(e)
            return {
                'valid': False
            }
    

 
MODEL_VALIDATION_MANAGER = ValidationManager(get_atlas_search_engine_db())