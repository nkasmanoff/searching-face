from datasets import load_dataset
from helpers import clean_up_tags

def load_descriptions_data():
    hf_datasets = load_dataset('nkasmanoff/huggingface-datasets')
    hf_df = hf_datasets['train'].to_pandas()
    hf_df['tags_cleaned'] = hf_df['tags'].apply(clean_up_tags)
    hf_df.dropna(subset=['description'],inplace=True)
    hf_df['description_full'] = hf_df['description'].fillna('') + ' ' + hf_df['tags_cleaned']
    hf_df = hf_df[hf_df['description_full'] != ' ']
    hf_df = hf_df[['id','description_full']]

    return hf_df