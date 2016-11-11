<template>
    <div id="app">
        <div class="columns">
            <div class="column">
                <div class="card">
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
                <words v-model="wordString"></words>
                <p>Words: {{ wordString }}</p>
            </div>
            <div class="column">
            </div>
        </div>
  </div>
</template>

<script>
import Words from './components/Words';

export default {
  name: 'app',
  components: {
    Words,
  },
  data() {
    return {
      wordString: 'a',
    };
  },
};
</script>

<style>
#app {
}

.is-disabled {
    opacity: 0.5;
}
</style>
