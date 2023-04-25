import gradio as gr

def predict(input_text, option):

    if option == "Semantic search":
        output = "Option 1 selected. Input text: " + input_text
    elif option == 'Dataset similarity':
        output = "Option 2 selected. Input text: " + input_text
    else:
        output = "Please select an option"
    return output

input_type = gr.inputs.Textbox(label="Input Text")
checkbox = gr.inputs.Radio(["Semantic search", "Dataset similarity"], label="Please select search type:")
iface = gr.Interface(fn=predict, inputs=[input_type, checkbox], outputs="text", title="SearchingFace")

iface.launch()
