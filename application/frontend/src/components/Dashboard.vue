<template>
  <div>
      <NavigationBar/>

      <b-container>
        <b-button v-if="this.$root.$data.role == 'client'" class="mr-2" variant="primary" to="/project-create">Create Project</b-button>
        <b-button variant="primary" to="/my-projects">My Projects</b-button>
      </b-container>
      <!--<p>Role: {{this.$root.$data.role}}</p>-->
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
