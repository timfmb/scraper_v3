from rapidfuzz import process, fuzz
from diskcache import Cache
import re

class FuzzyIndex:
    def __init__(self, db):
        self.db = db
        self.makes_collection = self.db['makes']
        self.models_collection = self.db['models']

        self.make_cache = Cache('applications/data_extractor/caches/fuzzy_index/make_cache', size_limit=10000000000000000, eviction_policy='none')
        self.make_model_cache = Cache('applications/data_extractor/caches/fuzzy_index/make_model_cache', size_limit=10000000000000000, eviction_policy='none')

        self.build_indices()
        

    def build_make_index(self):
        makes = self.makes_collection.find({})
        make_list = []
        for make in makes:
            make_list.append({'make':make['make'], 'make_id':str(make['_id'])})
            if make.get('alt_names'):
                for alt_name in make['alt_names']:
                    make_list.append({'make':alt_name, 'make_id':str(make['_id'])})
        self.make_cache['makes'] = make_list
        return make_list
        

    def build_make_model_cache(self, makes):
        models = self.models_collection.find({}, {'make':1, 'model':1, '_id':1, 'make_id':1})
        make_models_dict = {make['make_id']: [] for make in makes}
        errors = 0
        for model in models:
            try:
                make_models_dict[str(model['make_id'])].append({'model':model['model'], 'model_id':str(model['_id'])})
            except KeyError:
                errors += 1
                continue
        for make in make_models_dict.keys():
            self.make_model_cache[make] = make_models_dict[make]

        return make_models_dict
    

    def build_indices(self):
        self.make_cache.clear()
        self.make_model_cache.clear()
        makes = self.build_make_index()
        self.build_make_model_cache(makes)
        return 


    def load_makes(self):
        makes = self.make_cache['makes']
        make_id_dict = {make['make']: make['make_id'] for make in makes}
        return make_id_dict
    

    def load_models(self, make, make_id):
        models = self.make_model_cache[make_id]
        model_dict = {model['model']: {'make': make, 'model': model, 'model_id': model['model_id']} for model in models}
        return model_dict
    

    def find_exact_make(self, make):
        make_id_dict = self.load_makes()
        make_id = make_id_dict.get(make)
        if not make_id:
            return None, None
        return make_id, make
    

    def find_fuzzy_make(self, make):
        make_id_dict = self.load_makes()
        results  = process.extract(make, make_id_dict.keys(), scorer=fuzz.ratio)
        if not results:
            return None, None
        make, score, idx = results[0]
        if score < 90:
            return None, None
        return make_id_dict[make], make    
    

    def find_exact_model(self, make, make_id, model):
        model_dict = self.load_models(make, make_id)
        model_data = model_dict.get(model)
        if not model_data:
            return None
        
        return model_data.get('model')
    

    def extract_numeric(self, model):
        numeric_characters = re.findall(r'\d+\.?\d*', model)
        result = ' '.join(numeric_characters)
        return result
    

    def check_numeric_match(self, model, comp_models):
        model_numeric = self.extract_numeric(model)
        results = []
        for comp_model in comp_models:
            comp_model_numeric = self.extract_numeric(comp_model[0])
            if comp_model_numeric == model_numeric:
                results.append(comp_model)
        return results
    

    def split_alpha_numeric(self, input_string):
        split_string = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', input_string)  # Splits letters followed by numbers
        split_string = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', split_string)  # Splits numbers followed by letters
        return split_string



    def find_potential_models(self, make, make_id, model, threshold=90):
        model_dict = self.load_models(make, make_id)

        model_tokens_dict = {}
        for model_name in model_dict.keys():
            model_tokens_dict[self.split_alpha_numeric(model_name)] = model_name

        results = process.extract(self.split_alpha_numeric(model), model_tokens_dict.keys(), scorer=fuzz.partial_token_sort_ratio, limit=30)
        results = [result for result in results if result[1] > threshold]

        return results, model_tokens_dict, model_dict



    def find_fuzzy_model_token_sort(self, make, make_id, model, threshold=85):
        results, model_tokens_dict, model_dict = self.find_potential_models(make, make_id, model, threshold)
        if not results:
            return None
        
        results = self.check_numeric_match(model, results)
        if not results:
            return None
        
        best_score = 0

        best_results = []
        for result in results:
            model, score, idx = result
            if score > best_score:
                best_score = score
            
            if score == best_score:
                best_results.append(result)


        longest_model = 0
        final_model = None

        for result in best_results:
            model, score, idx = result
            if len(model) > longest_model:
                longest_model = len(model)
                final_model = model

        if not final_model:
            return None

        model = model_tokens_dict[final_model]
        model_data = model_dict.get(model)
        if not model_data:
            return None
        
        return model_data.get('model')
    

    def find_fuzzy_model(self, make, make_id, model):
        model_dict = self.load_models(make, make_id)
        results = process.extract(model, model_dict.keys())
        if not results:
            return None

        results = self.check_numeric_match(model, results)
        if not results:
            return None
        
        model, score, idx = results[0]

        model_data = model_dict.get(model)
        
        if not model_data:
            return None
        
        return model_data.get('model')
    

    def find_make_match(self, make):
        make_id, matched_make = self.find_exact_make(make)
        if make_id:
            return make_id, matched_make
        
        make_id, matched_make = self.find_fuzzy_make(make)
        return make_id, matched_make


    def find_model_match(self, make_id, make, model):
        model_data = self.find_exact_model(make, make_id, model)
        if model_data:
            return model_data
        
        model_data = self.find_fuzzy_model_token_sort(make, make_id, model)
        return model_data


    def check_make_model(self, make, model):
        make = make.lower()
        model = model.lower()
        make_id, matched_make = self.find_make_match(make)
        if not make_id:
            return []
        
        model_data = self.find_model_match(make_id, matched_make, model)
        if not model_data:
            return []
        
        model_data['make'] = matched_make
        return [model_data]
    


    def get_potential_models(self, make, model):
        make = make.lower()
        model = model.lower()
        make_id, matched_make = self.find_make_match(make)
        if not make_id:
            return []
        
        result, model_tokens_dict, model_dict = self.find_potential_models(matched_make, make_id, model, threshold=30)
        #result = self.check_numeric_match(model, result)
        results = []
        for result in result:
            model, score, idx = result
            model_data = model_dict.get(model_tokens_dict[model])
            model_data['make'] = matched_make
            model_data['model'] = model_data['model']['model']
            results.append(model_data)

        return results            











    

