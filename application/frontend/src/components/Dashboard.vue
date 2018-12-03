<template>
  <div>
      <NavigationBar/>

      <b-container>
        <b-button v-if="isClient" class="mr-2" variant="primary" to="/project-create">
          <font-awesome-icon icon="plus" fixed-width />Create Project
        </b-button>
        <b-button variant="primary" to="/my-projects">My Projects</b-button>
        <b-button variant="primary" to="/my-accepted-projects">My Accepted Projects</b-button>
      </b-container>
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue'

export default {
  name: "Dashboard",
  components: {
    NavigationBar
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
