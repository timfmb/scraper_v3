


def clean_images(images: list[str]) -> list[str]:
    if not images:
        return []
    
    cleaned = []
    for image in images:
        if image != None:
            cleaned.append(image)
    
    return cleaned




