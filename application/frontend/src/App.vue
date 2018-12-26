<template>
  <div id="app" @mouseup="mouseup" @mousedown="mousedown">
    <router-view></router-view>
    <Annotation ref="annotation"/>
  </div>
</template>

<script>
import Annotation from './components/Annotation.vue';

export default {
  name: 'App',
  components: {
    Annotation
  },
  methods: {
    mouseup(e) {
      this.$refs.annotation.onTextSelect(e);
    },
    mousedown(e) {
      this.$refs.annotation.mousedown(e);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

<style>
.bg-grey {
  background-color: #efefef;
  min-height: 100vh;
}
</style>