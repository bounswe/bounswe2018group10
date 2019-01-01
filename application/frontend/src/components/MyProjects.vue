<template>
  <div class="bg-grey">
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
          <ProjectListView v-if="isClient" :projects="projects" :tags="tags"/>
          <ProjectListView v-if="isFreelancer" :projects="freelancerProjects" :tags="tags"/>
        </b-col>
      </b-row>
      <MyFooter/>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import ProjectListView from "./ProjectListView.vue";
import MyFooter from "./MyFooter.vue";

export default {
  name: "MyProjects",
  components: {
    NavigationBar,
    ProjectListView,
    MyFooter
  },
  data() {
    return {
      projects: [],
      freelancerProjects: [],
      tags: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/project/create/?user_id__id=${this.$root.$data.user_id}`)
        .then(response => {
          this.projects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
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
              // eslint-disable-next-line
              console.log(err);
            });
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get("/project/tag/")
        .then(response => {
          this.tags = response.data;
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
