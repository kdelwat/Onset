import json
import sys
import os.path as path

from flask import render_template, jsonify, request
from app import app

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))
import engine

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def format_transcriptions(transcriptions):
    '''Split the raw string of transcriptions into
    the correct tuple rules.'''
    clean_transcriptions = transcriptions.strip().lower()

    if len(clean_transcriptions) == 0:
        return []
    else:
        return [(pair.split(':')[0], pair.split(':')[1]) for pair in clean_transcriptions.split('\n')]


@app.route('/evolve')
def evolve():
    words = request.args['words'].split()

    try:
        transcriptions = format_transcriptions(request.args['transcriptions'])
    except IndexError:
        return jsonify({'error': 'Error: Transcription seperator must be a colon'})

    direction = request.args['direction']

    if direction == 'Reverse':
        reverse = True
    else:
        reverse = False

    try:
        generations = int(request.args['generations'])
    except ValueError:
        return jsonify({'error': 'Error: Generations must be an integer'})

    words, rules = engine.run_engine(words, generations, transcriptions,
                                     reverse)

    return jsonify({'rules': rules, 'words': words, 'error': 0})


@app.route('/apply')
def apply():
    '''Evolves the language according to the given rules, specified by:

        words: list [strings]
        rules: list [Rules]
    '''
    words = request.args['words'].split()
    rules = json.loads(request.args['rules'])

    evolved_words = applier.apply_loaded_rules(words, rules)

    return jsonify({'words': evolved_words, 'error': 0})
