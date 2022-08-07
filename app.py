from shiny import App, reactive, render, ui
import spacy
from spacy import displacy

SPACY_MODEL_NAMES = ["en_core_web_sm", "de_core_news_sm", "es_core_news_sm"]
DEFAULT_TEXT = "Tim Cook is the CEO of Apple."
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""

def load_model(name):
    return spacy.load(name)

def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text), nlp

def get_parser(doc, nlp):
    options = {
        "collapse_punct": True,
        "collapse_phrases": True,
        "compact": True,
    }
    docs = [span.as_doc() for span in doc.sents] if True else [doc]
    for sent in docs:
        html = displacy.render(sent, options=options)
        html = html.replace("\n\n", "\n")
        html = HTML_WRAPPER.format(html)
    return html

def get_ner(doc, nlp):
    labels = nlp.get_pipe("ner").labels
    html = displacy.render(doc, style="ent", options={"ents": labels})
    html = html.replace("\n", " ")
    html = HTML_WRAPPER.format(html)
    return html

def get_data(doc, nlp):
    labels = nlp.get_pipe("ner").labels
    attrs = ["text", "label_", "start", "end", "start_char", "end_char"]
    data = [
        [str(getattr(ent, attr)) for attr in attrs]
        for ent in doc.ents
        if ent.label_ in labels
    ]
    return data

app_ui = ui.page_fluid(
    ui.tags.style(),
    ui.h2("Interactive Python Shiny spaCy visualizer"),
    ui.markdown(
    """
Process text with [spaCy](https://spacy.io) models and visualize named entities,
dependencies and more. Uses spaCy's built-in
[displaCy](http://spacy.io/usage/visualizers) visualizer under the hood.
"""
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(    
            ui.input_select(id = "spacy_model", label = "Model name", choices = SPACY_MODEL_NAMES),
            ui.input_text_area(id = "text", label = "Text to analyze", value = DEFAULT_TEXT),
            ui.input_action_button("run", "Run doc!"),
        ),
        ui.panel_main(
            ui.output_ui("result", placeholder=True),
        ),
    )
)


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.run) # Take a dependency on the button
    async def result():
        doc, nlp = process_text(input.spacy_model(), input.text())
        if "parser" in nlp.pipe_names:
            html_parser = get_parser(doc, nlp)
        if "ner" in nlp.pipe_names:
            html_ner = get_ner(doc, nlp)
        return html_parser + html_ner

app = App(app_ui, server)