import json
import sys
import os.path as path

from flask import render_template, jsonify, request
from app import app

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))
import engine
import metrics

optimisation_functions = {'Maximise': max, 'Minimise': min}
metric_functions = {'weighted phonetic product': metrics.weighted_phonetic_product,
                    'phonetic product': metrics.phonetic_product,
                    'Word Complexity Measure': metrics.word_complexity_measure,
                    'number of syllables': metrics.number_of_syllables,
                    'number of consonant clusters': metrics.number_of_consonant_clusters,
                    'random value': metrics.random_value}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def sanitise(string):
    '''Remove all whitespace from a string and lowercase it.'''
    banned_characters = "'.-–—‒ \u02C8"

    return ''.join([c for c in string.strip().lower() if c not in
                    banned_characters])


def format_transcriptions(transcriptions):
    '''Split the raw string of transcriptions into
    the correct tuple rules.'''
    clean_transcriptions = transcriptions.strip().lower()

    if len(clean_transcriptions) == 0:
        return []
    else:
        return [(sanitise(pair.split(':')[0]), sanitise(pair.split(':')[1]))
                for pair in clean_transcriptions.split('\n')]


@app.route('/evolve')
def evolve():
    words = [sanitise(word) for word in request.args['words'].split()]

    try:
        transcriptions = format_transcriptions(request.args['transcriptions'])
    except IndexError:
        return jsonify({'error': 'Transcription seperator must be a colon'})

    try:
        generations = int(request.args['generations'])
    except ValueError:
        return jsonify({'error': 'Generations must be an integer'})

    if request.args['direction'] == 'Reverse':
        reverse = True
    else:
        reverse = False

    optimisation_function = optimisation_functions[request.args['optimisationFunction']]
    metric = metric_functions[request.args['metric']]

    try:
        words, rules = engine.run_engine(words, generations, transcriptions,
                                         reverse, metric, optimisation_function)
    except Exception as e:
        return jsonify({'error': str(e)})

    return jsonify({'rules': rules, 'words': words, 'error': 0})


@app.route('/apply')
def apply():
    '''Evolves the language according to the given rules, specified by:

        words: list [strings]
        rules: list [Rules]
        reverse: if True, apply in reverse order (used when applying rules
                 created by reverse evolution)
    '''
    words = [sanitise(word) for word in request.args['words'].split()]
    rules = json.loads(request.args['rules'])

    if request.args['direction'] == 'Reverse':
        reverse = True
    else:
        reverse = False

    try:
        transcriptions = format_transcriptions(request.args['transcriptions'])
    except IndexError:
        return jsonify({'error': 'Transcription seperator must be a colon'})

    try:
        evolved_words = engine.apply_rules(words, rules, transcriptions,
                                           reverse)
    except Exception as e:
        return jsonify({'error': str(e)})

    return jsonify({'words': evolved_words, 'error': 0})
