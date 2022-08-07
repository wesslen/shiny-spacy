"""
Example of a Streamlit app for an interactive Prodigy dataset viewer that also lets you
run simple training experiments for NER and text classification.
Requires the Prodigy annotation tool to be installed: https://prodi.gy
"""
import imp
from shiny import App, reactive, ui, render
from prodigy.components.db import connect
from prodigy import serve
#from prodigy.models.ner import EntityRecognizer, merge_spans, guess_batch_size
#from prodigy.models.textcat import TextClassifier
import pandas as pd
from spacy.tokens import Doc
from spacy import displacy
from spacy.util import filter_spans, minibatch

SPACY_MODEL_NAMES = ["en_core_web_sm"]
EXC_FIELDS = ["meta", "priority", "score"]
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
COLOR_ACCEPT = "#93eaa1"
COLOR_REJECT = "#ff8f8e"


def guess_dataset_type(first_eg):
    if "image" in first_eg:
        return "image"
    if "arc" in first_eg:
        return "dep"
    if "options" in first_eg or "label" in first_eg:
        return "textcat"
    if "spans" in first_eg:
        return "ner"
    return "other"


def get_answer_counts(examples):
    result = {"accept": 0, "reject": 0, "ignore": 0}
    for eg in examples:
        answer = eg.get("answer")
        if answer:
            result[answer] += 1
    return result


def format_label(label, answer="accept"):
    # Hack to use different colors for the label (by adding zero-width space)
    return f"{label}\u200B" if answer == "reject" else label


def summary(examples):
    return get_answer_counts(examples)


db = connect()


app_ui = ui.page_fluid(
    ui.tags.style(),
    ui.h2("Prodigy Data Explorer: Shiny Python"),
    ui.markdown(
    """
    Example of a Python Shiny app for an interactive Prodigy dataset viewer.
    Requires the Prodigy annotation tool to be installed: https://prodi.gy
    """
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(    
            ui.input_select(id = "dataset", label = "Choose dataset", choices = db.datasets),
            ui.input_action_button("view", "View dataset!"),
            ui.input_action_button("delete", "Delete dataset!"),
        ),
        ui.panel_main(
            ui.output_ui("result", placeholder=True),
            ui.output_ui("delete", placeholder=True),
        ),
    )
)


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.view) # Take a dependency on the button
    async def result():
        examples = db.get_dataset(input.dataset())
        count = len(examples)
        return f"The dataset {input.dataset()} has {count} records.", examples[0]

    @output
    @render.text
    @reactive.event(input.delete) # Take a dependency on the button
    async def delete():
        db.drop_dataset(input.dataset())
        return f"Deleted the {input.dataset()} dataset!"

app = App(app_ui, server)