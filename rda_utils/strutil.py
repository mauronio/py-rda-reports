def get_enclosed_text(text, start_tag, end_tag):

    start_index = text.index(start_tag) 
    end_index = text.rfind(end_tag) + len(end_tag) + 1

    return text[start_index:end_index]