<template>
    <textarea ref="input" rows=20 v-bind:value="value" v-on:input="updateValue($event.target.value)"></textarea>
</template>

<script>
export default {
  name: 'words',
  props: ['value'],
  methods: {
    updateValue(value) {
      this.$refs.input.value = value;
      this.$emit('input', value);
    },
  },
};

</script>
