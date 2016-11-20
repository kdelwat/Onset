<template>
    <div id="app" class="container">
        <div class="columns">
            <div class="column">
                <div class="card is-fullwidth">
                    <header class="card-header">
                      <p class="card-header-title">Onset</p>
                    </header>
                    <div class="card-content">
                      <div class="content">
                        <p>Onset is a (mostly) linguistically-accurate language evolution simulator. Enter a list of words to evolve to the right, tweak the settings, and hit <em>Evolve!</em> to see it in action.</p>
                      </div>
                    </div>
                    <footer class="card-footer">
                        <a class="card-footer-item" v-on:click="evolve">Evolve</a>

                        <input v-model="filename" class="input" type="text" style="margin: 5px;" placeholder="filename"></input>

                        <a class="card-footer-item"
                           v-bind:class="{ disabled: !resultsPresent }"
                           v-on:click="saveLocal">
                           Save
                        </a>

                        <a class="card-footer-item"
                           v-on:click="loadLocal">
                           Load
                        </a>

                    </footer>
                </div>
            </div>
            <div class="column">
              <div class="card is-fullwidth">
                <header class="card-header">
                  <p class="card-header-title">Words</p>
                </header>
                  <div class="card-content">
                    <div class="content">
                      <p>Enter a list of words, one per line, which will be evolved.</p>
                      <textarea class="textarea" ref="input" rows=20 v-model="wordString"></textarea>
                    </div>
                  </div>
              </div>
            </div>
            <div class="column">
              <div class="card is-fullwidth">
                <header class="card-header">
                  <p class="card-header-title">Settings</p>
                </header>
                <div class="card-content">
                <form>
                  <label class="label">Generations</label>
                  <p class="control">
                    <input v-model="generations" type="number" class="input">
                  </p>
                  <label class="label">Transcriptions</label>
                  <p class="control">
                    <textarea v-model="transcriptionString" class="textarea" rows=5 placeholder="ng:ŋ"></textarea>
                  </p>
                </form>
                </div>
              </div>
            </div>
        </div>

    <div v-if="resultsPresent">
    <hr>
    <div class="columns">

      <div class="column">
        <div class="card is-fullwidth">
          <header class="card-header">
            <p class="card-header-title">Applied Rules</p>
          </header>
          <div class="card-content">
            <a class="panel-block" v-for="rule in evolutionRules">{{rule[0]}}: {{rule[1]}} -> {{rule[2]}}, {{rule[3]}}</a>
          </div>
        </div>
      </div>

      <div class="column">
        <div class="card is-fullwidth">
          <header class="card-header">
            <p class="card-header-title">Evolved Words</p>
          </header>
          <div class="card-content">
            <a class="panel-block" v-for="word in evolvedWords">{{word}}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'app',
  components: {},
  data() {
    return {
      wordString: '',
      generations: 5,
      transcriptionString: '',
      evolvedWords: [],
      evolutionRules: [],
      filename: '',
    };
  },
  computed: {
    resultsPresent() {
      return this.evolvedWords.length >= 1;
    },
  },
  methods: {
    // Call the backend to evolve the given words
    evolve() {
      const parameters = { words: this.wordString,
        generations: this.generations,
        transcriptions: this.transcriptionString };

      // Call the Flask API
      axios.get('http://127.0.0.1:5000/evolve',
                { params: parameters })
      // Handle a valid response
        .then((response) => {
          // Trigger API error display if necessary
          if (response.data.error !== 0) {
            this.showError(response.data.error);
          // Otherwise, update data from request result
          } else {
            this.evolvedWords = response.data.words;
            this.evolutionRules = response.data.rules;
            console.log(response.data.words);
          } })
      // Handle an invalid response
        .catch(error => console.log(error));
    },
    // Display an error
    showError(error) {
      console.log('Error', error);
    },
    // Save the current rules to localStorage, identified by the given filename
    saveLocal() {
      localStorage.setItem(this.filename, JSON.stringify(this.evolutionRules));
    },
    // Load rules from localStorage identified by the given filename
    loadLocal() {
      // Load and store the rules
      const loadedRules = JSON.parse(localStorage.getItem(this.filename));

      if (loadedRules === null) {
        this.showError('No rules are saved under that name');
      } else {
        this.evolutionRules = loadedRules;

        const parameters = { words: this.wordString,
          rules: JSON.stringify(this.evolutionRules) };

        // Call the Flask API
        axios.get('http://127.0.0.1:5000/apply',
                  { params: parameters })
        // Handle a valid response
          .then((response) => {
            // Trigger API error display if necessary
            if (response.data.error !== 0) {
              this.showError(response.data.error);
            // Otherwise, update words from request result
            } else {
              this.evolvedWords = response.data.words;
            } })
        // Handle an invalid response
          .catch(error => console.log(error));
      }
    },
  },
};
</script>

<style>
.disabled {
    opacity: 0.5;
}

textarea {
}
</style>
