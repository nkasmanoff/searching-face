# clean up descriptions and tags
def clean_up_tags(tags_list):
    tags_cleaned = []
    for tag in tags_list: 
        if ':' in tag:
            tag = tag.split(':')[1]
        
        tags_cleaned.append(tag)

    return ", ".join(tags_cleaned)

