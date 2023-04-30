import requests

def clean_up_tags(tags_list):
    tags_cleaned = []
    for tag in tags_list: 
        if ':' in tag:
            tag = tag.split(':')[1]
        
        tags_cleaned.append(tag)

    return ", ".join(tags_cleaned)



def check_api_url(url):
    """
    This function checks to see if "api" is present in the URL between ".co" and "/datasets". If not, it inserts "api" in the correct position.
    
    Args:
    url (str): A URL string
    
    Returns:
    str: A URL string with "api" inserted if necessary
    """
    # Split the URL into three parts based on the location of ".co" and "/datasets"
    parts = url.split(".co")
    first_part = parts[0] + ".co"
    last_part = parts[1]
    last_parts = last_part.split("/datasets")
    middle_part = ""
    if len(last_parts) > 1 and "/api" not in last_parts[0]:
        middle_part = "/api"
    # Concatenate the three parts to form the final URL
    new_url = first_part + middle_part + last_parts[0] + "/datasets" + last_parts[1]
    return new_url



def get_dataset_metadata(dataset_url):
    retrieved_metadata = {}
    dataset_url = check_api_url(dataset_url)
    keys_to_retrieve = ['id','description', 'tags']
    response = requests.get(dataset_url)
    if response.status_code == 200:
        response_json = response.json()
        for key in keys_to_retrieve:
            if key in response_json:
                retrieved_metadata[key] = response_json[key]

    return retrieved_metadata


def get_dataset_readme(dataset_url):
    retrieved_metadata = {}
    metadata_url = check_api_url(dataset_url)
    readme_url = dataset_url + '/raw/main/README.md'
    readme_response = requests.get(readme_url)
    metadata_response = requests.get(metadata_url)
    if readme_response.status_code == 200:
        response_text = readme_response.text
        dataset_id = metadata_response.json()['id']
        retrieved_metadata = {'id': dataset_id, 'README': response_text}

    return retrieved_metadata

