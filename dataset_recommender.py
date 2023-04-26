from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from vectorize_dataset import load_descriptions_data, create_db
from helpers import clean_up_tags, get_dataset_metadata



class DatasetRecommender:
    def __init__(self, llm_backbone = OpenAI(), embeddings_backbone = OpenAIEmbeddings()):
        self.llm_backbone = llm_backbone
        self.embeddings_backbone = embeddings_backbone
        self.hf_df = load_descriptions_data()
        self.db = create_db(self.hf_df, self.embeddings_backbone)
        self.datasets_url_base = "https://huggingface.co/datasets/"
        # expose this index in a retriever interface
        self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k":2})
        # create a chain to answer questions 
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm_backbone, chain_type="stuff", retriever=self.retriever, return_source_documents=True)

    def recommend_based_on_text(self, query):
        result = self.qa({"query": query})
        response_text = result['result']
        source_documents = result['source_documents']
        linked_datasets = [f"{self.datasets_url_base}{x.metadata['id']}" for x in source_documents]
        return {'message': response_text, 'datasets': linked_datasets}

    def get_similar_datasets(self, query_url):
        retrieved_metadata = get_dataset_metadata(query_url)
        if 'description' not in retrieved_metadata:
            return {'error': 'no description found for this dataset.'}
        cleaned_description = retrieved_metadata['description'] + clean_up_tags(retrieved_metadata['tags'])
        similar_documents = self.db.similarity_search(cleaned_description)
        similar_datasets = [f"{self.datasets_url_base}{x.metadata['id']}" for x in similar_documents if x.metadata['id'] not in query_url]       
        return {'datasets': similar_datasets} 