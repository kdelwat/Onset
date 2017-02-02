<template>
  <div class="card rule">
    <header class="card-header">
      <p class="card-header-title" style="font-weight: 400">{{ rule.name }}</p>
      <a @click="toggleExpansion" class="card-header-icon">
        <span class="icon">
          <i class="fa fa-angle-down"></i>
        </span>
      </a>
    </header>
    <div v-if="expanded" class="card-content">
      <p>{{ rule.description }}</p>

      <div class="rule-definition">
        <span v-if="ruleConditions.length !== 0" class="feature-matrix">
          <div v-for="feature in ruleConditions">
            {{feature}}
          </div>
        </span>

        <span class="rule-definition-separator">&rarr;</span>

        <span v-if="ruleApplies.length !== 0" class="feature-matrix">
          <div v-for="feature in ruleApplies">
            {{feature}}
          </div>
        </span>

        <span class="rule-definition-separator">/</span>

        <span v-if="ruleBefore.length !== 0" class="feature-matrix">
          <div v-for="feature in ruleBefore">
            {{feature}}
          </div>
        </span>

        <span class="rule-definition-separator">__</span>

        <span v-if="ruleAfter.length !== 0" class="feature-matrix">
          <div v-for="feature in ruleAfter">
            {{feature}}
          </div>
        </span>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'rule',
  props: ['rule'],
  data() {
    return {
      expanded: false,
    };
  },
  computed: {
    ruleConditions() {
      return this.formatFeatures(this.rule.conditions);
    },
    ruleApplies() {
      return this.formatFeatures(this.rule.applies);
    },
    ruleBefore() {
      return this.formatFeatures(this.rule.before);
    },
    ruleAfter() {
      return this.formatFeatures(this.rule.after);
    },
  },
  methods: {
    toggleExpansion() {
      if (this.expanded) {
        this.expanded = false;
      } else {
        this.expanded = true;
      }
    },
    formatFeatures(featureObject) {
      const features = featureObject || {};
      const negative = features.negative || [];
      const positive = features.positive || [];

      if (positive.includes('deletion')) {
        return ['Ø'];
      }

      return negative.map(x => `–${x}`).concat(positive.map(x => `+${x}`));
    },
  },
};
</script>

<style scoped>
.rule {
    width: inherit;
    box-shadow: none;
    border-top: 1px solid rgba(10,10,10,.1);
}

.rule-definition {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1em;

}

.rule-definition-separator {
  font-size: 1.5em;
  margin-right: 10px;

}

.feature-matrix {
  border-left: 2px solid rgba(10,10,10,.7);
  border-right: 2px solid rgba(10,10,10,.7);
  padding: 5px;
  margin-right: 10px;
}

</style>

