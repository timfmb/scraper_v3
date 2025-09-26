def remove_all_html_attributes(container):
    container.attrs.clear()
    for tag in container.find_all(True):
        tag.attrs.clear()
    return container