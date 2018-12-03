<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>My Projects</h2>
          <h6 v-if="isClient" class="text-muted">Projects that I created</h6>
          <h6 v-if="isFreelancer" class="text-muted">Projects that I bid for</h6>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-list-group v-if="isClient">
            <b-list-group-item :key="project.id" v-for="project in projects">
              <router-link :to="`/project/${project.id}`">{{project.title}}</router-link>
              <div>{{project.description | shortDescription}}</div>
            </b-list-group-item>
          </b-list-group>
          <b-list-group v-if="isFreelancer">
            <b-list-group-item :key="project.id" v-for="project in freelancerProjects">
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
  name: "MyProjects",
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
        .get(`/project/create/?search=${this.$root.$data.user_id}`)
        .then(response => {
          this.projects = response.data;
        })
        .catch(err => {
          console.log(err);
        });
      this.$axios
        .get(`/project/bid/`)
        .then(response => {
          let projectList = response.data.filter(
            bid => bid.user_id == this.$root.$data.user_id
          ).map(bidList => bidList.project_id);
          this.$axios
            .get(`/project/create/`)
            .then(response => {
              this.freelancerProjects = response.data.filter(proj =>
                projectList.includes(proj.id)
              );
            })
            .catch(err => {
              console.log(err);
            });
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
