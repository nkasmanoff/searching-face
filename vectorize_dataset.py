from datasets import load_dataset
from helpers import clean_up_tags
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader


def load_descriptions_data():
    hf_datasets = load_dataset('nkasmanoff/huggingface-datasets')
    hf_df = hf_datasets['train'].to_pandas()
    hf_df['tags_cleaned'] = hf_df['tags'].apply(clean_up_tags)
    hf_df.dropna(subset=['description'],inplace=True)
    hf_df['description_full'] = hf_df['description'].fillna('') + ' ' + hf_df['tags_cleaned']
    hf_df = hf_df[hf_df['description_full'] != ' ']
    hf_df = hf_df[['id','description_full']]

    return hf_df


def create_db(hf_df, embeddings):
    loader = DataFrameLoader(hf_df, page_content_column="description_full")
    documents = loader.load()
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    # select which embeddings we want to use
    # create the vectorestore to use as the index
    db = Chroma.from_documents(texts, embeddings)    
    return db