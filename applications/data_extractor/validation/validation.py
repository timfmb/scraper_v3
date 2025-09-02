from applications.data_extractor.validation import validation_funcs



DEFAULT_VALIDATION = [
    validation_funcs.title,
    validation_funcs.status,
    validation_funcs.length,
    validation_funcs.year,
    validation_funcs.price,
    validation_funcs.currency,
    validation_funcs.country,
    validation_funcs.make,
    validation_funcs.model,
    validation_funcs.description,
    validation_funcs.image_urls_exists,
    validation_funcs.image_download_urls_not_none
]




def validate_listing(listing, required_validation=DEFAULT_VALIDATION):
    errors = []
    for validation_func in required_validation:
        if not validation_func(listing):
            errors.append(validation_func.__name__)
    errors = sorted(errors)
    return errors




    
