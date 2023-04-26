import gradio as gr
from dataset_recommender import DatasetRecommender

db_lookup = DatasetRecommender()
def predict(input_text, option):

    if option == "Semantic search":

        response = db_lookup.recommend_based_on_text(input_text)
        output = f"Message: {response['message']} \n \n Datasets: {' \n '.join([x for x in response['datasets']])}"
    elif option == 'Dataset similarity':
        response = db_lookup.get_similar_datasets(input_text)
        if 'error' in response:
            output = response['error']
        else:
            output = f"Similar Datasets: {' \n '.join([x for x in response['datasets']])}"

    else:
        output = "Please select an option"
    return output

input_type = gr.inputs.Textbox(label="Input Text")
checkbox = gr.inputs.Radio(["Semantic search", "Dataset similarity"], label="Please select search type:")
iface = gr.Interface(fn=predict, inputs=[input_type, checkbox], outputs="text", title="SearchingFace")

iface.launch()
