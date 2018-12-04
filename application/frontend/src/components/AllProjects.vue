<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>All Projects</h2>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-list-group>
            <b-list-group-item :key="project.id" v-for="project in projects">
              <router-link :to="`/project/${project.id}`">{{project.title}}</router-link>
              <div>{{project.description | shortDescription}}</div>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "AllProjects",
  components: {
    NavigationBar
  },
  data() {
    return {
      projects: [],
      freelancerProjects: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/project/create/`)
        .then(response => {
          this.projects = response.data;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
