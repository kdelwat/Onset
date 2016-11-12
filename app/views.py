from flask import render_template, jsonify, request
from app import app
from app import evolver


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
    print(request.args['words'])

    words = request.args['words'].split()

    try:
        transcriptions = format_transcriptions(request.args['transcriptions'])
    except IndexError:
        return jsonify({'error': 'Error: Transcription seperator must be a colon'})

    try:
        generations = int(request.args['generations'])
    except ValueError:
        return jsonify({'error': 'Error: Generations must be an integer'})

    words, rules = evolver.evolve(words, generations, transcriptions)

    return jsonify({'rules': rules, 'words': words, 'error': 0})
