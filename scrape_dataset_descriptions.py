import datasets
import requests
import json
from tqdm import tqdm


def scrape_dataset(dataset_metadata_file: str = 'data/responses.json') -> list:
    """
    Scrape metadata of all public datasets available on Hugging Face's Datasets Hub.

    Args:
        dataset_metadata_file (str): The path to the file where the dataset metadata will be saved in JSON format.
                                     Default value is 'data/responses.json'.

    Returns:
        list: A list of dictionaries containing metadata of all public datasets available on Hugging Face's Datasets Hub.

    Raises:
        Exception: Any exceptions that occur while making requests or saving dataset metadata to a file will be caught
                   and suppressed.

    """
    all_datasets = datasets.list_datasets()
    responses = []

    for dataset_id in tqdm(all_datasets):
        api_url = f"https://huggingface.co/api/datasets/{dataset_id}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                response_json = response.json()
                # only keep id, private, tags, description, downloads, likes, pretty_name
                keys_to_keep = ['id', 'private', 'tags', 'description', 'downloads', 'likes', 'pretty_name']
                response_saved = {}
                for key in keys_to_keep:
                    if key in response_json:
                        response_saved[key] = response_json[key]

                responses.append(response_saved)

                with open(dataset_metadata_file, 'w') as f:
                    json.dump(responses, f)
            else:
                # some invalid response. Ignore for now
                pass
        except Exception as e:
            print(e)

    return responses
