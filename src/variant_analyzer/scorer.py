import json
import os
from gevent.pywsgi import WSGIServer

from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests as requests

from src.variant_analyzer.weights import get_weights_by_entry

with open('../config.json') as config_file:
    config = json.load(config_file)
    annotation_location = config["nextprot_data"]["location"]
    default_entries = config["default_entries"]
    nextprot_urls = config["nextprot_urls"]

score_table = dict()

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

def download_file(url, local_filename):
    response = requests.get(url)
    with open(local_filename, 'wb') as file:
        file.write(response.content)

def get_file(url, local_filename):
    if os.path.exists(local_filename):
        print(f"The file '{local_filename}' already exists.")
    else:
        print(f"The file '{local_filename}' does not exist. Downloading...")
        download_file(url, local_filename)
        print(f"Download complete.")

# Initializes by loading the variant data for the entries
create_folder(annotation_location)
annotation_data = dict()
for entry in default_entries:
    score_table[entry] = dict()
    entry_path = f'{annotation_location}{entry}'
    create_folder(entry_path)

    # Call nextprot API if data file does not exist
    # For all annotations
    annotations_url = f'{nextprot_urls["annotations"].replace("entry_accession", entry)}'
    get_file(annotations_url, f'{entry_path}/annotations.json')

    # For mutagenesis
    mutagenesis_url = f'{nextprot_urls["mutagenesis"].replace("entry_accession", entry)}'
    get_file(mutagenesis_url, f'{entry_path}/mutagenesis.json')

    # For phenotypic-variations
    phenotypic_url = f'{nextprot_urls["phenotypic_variation"].replace("entry_accession", entry)}'
    get_file(phenotypic_url, f'{entry_path}/phenotypic-variations.json')

    # Build scoring tables
    with open(f'{entry_path}/annotations.json') as annotation_file:
        entry_data = json.load(annotation_file)["entry"]

        print("Construct the feature tables for the entries")
        annotation_data[entry] = {
            isoform["isoformAccession"]: {
                'sequence': isoform["sequence"],
                'annotations': []
            } for isoform in entry_data["isoforms"]
        }

        feature_weights = get_weights_by_entry(entry)
        if feature_weights is not None:
            for annotation_category in entry_data['annotationsByCategory']:
                if annotation_category in feature_weights["features"]:
                    for annotation in entry_data['annotationsByCategory'][annotation_category]:
                        for isoform in list(annotation['targetingIsoformsMap'].keys()):
                            annotation_data[entry][isoform]['annotations'].append({
                                'start':  annotation['targetingIsoformsMap'][isoform]["firstPosition"],
                                'end': annotation['targetingIsoformsMap'][isoform]["lastPosition"],
                                'type': annotation_category
                            })

            for feature in feature_weights:
                score_table[entry][feature] = feature_weights[feature]


def score_variant(isoform, variant):
    start = variant["nextprotPosition"]
    end = variant["nextprotPosition"]

    entry = isoform.split('-')[0]
    annotation_data_by_isoform = annotation_data[entry][isoform]
    # Get the features covering the variant position
    relevant_features = filter(lambda f: start >= f['start']  and end <= f['end'], annotation_data_by_isoform["annotations"])
    feature_types = set(r['type'] for r in list(relevant_features))

    # Calculate the score
    # Just add the weights if the variant happen to occur on or between a given feature
    score = 0
    for feature_type in feature_types:
        if feature_type in score_table[entry]["features"]:
            score += score_table[entry]["features"][feature_type]

    return score


app = Flask(__name__)
@app.route('/score', methods=['POST'])
@cross_origin()
def get_variant_score():
    data = request.get_json()
    isoform = data['isoform']
    variants = data['variantData']

    variant_scores = dict()
    variant_scores['isoform'] = isoform
    variant_scores['variants'] = list()
    for variant in variants:
        score = score_variant(isoform, variant)
        variant["score"] = score
        variant_scores['variants'].append(variant)

    # VEP

    return json.dumps(variant_scores)


@app.route('/features/<entry>', methods=['GET'])
def get_features_for_entry(entry):
    weights = get_weights_by_entry(entry)
    if weights is not None:
        return json.dumps(["mutagenesis"].extend(weights["features"].keys()))
    else:
        return json.dumps([])


if __name__ == '__main__':
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Serve the src with gevent
    http_server = WSGIServer(('127.0.0.1', 9001), app)
    print("Server started at 9001")
    http_server.serve_forever()