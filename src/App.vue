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
                        <p>Onset is a (mostly) linguistically-accurate language evolution simulator. Enter a list of words to evolve to the right, tweak the settings, and hit <emph>Evolve!</emph> to see it in action.</p>
                      </div>
                    </div>
                    <footer class="card-footer">
                        <a class="card-footer-item">Evolve</a>
                        <a class="card-footer-item is-disabled">Save</a>
                        <a class="card-footer-item">Load</a>
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
                <p>Words: {{ transcriptions }}, {{ words }}</p>
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
    <div v-if="evolvedWords.length >= 1">
    <div class="columns">
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

export default {
  name: 'app',
  components: {},
  data() {
    return {
      wordString: '',
      generations: 5,
      transcriptionString: '',
      evolvedWords: ['a', 'b', 'c'],
    };
  },
  computed: {
    words() {
      return this.wordString.split('\n').filter(x => x !== '');
    },
    transcriptions() {
      const pairs = this.transcriptionString.split('\n').map(pair => pair.split(':'));
      return pairs.filter(x => x.length !== 1);
    },
  },
};
</script>

<style>
.is-disabled {
    opacity: 0.5;
}

textarea {
}
</style>
