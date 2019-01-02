<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>My Accepted Projects</h2>
          <h6 v-if="isClient" class="text-muted">Projects that I created and choose a freelancer for it</h6>
          <h6 v-if="isFreelancer" class="text-muted">Projects that I bid for and choosen as a freelancer</h6>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <ProjectListView v-if="isClient" :projects="projects" :accepted="true"/>
          <ProjectListView v-if="isFreelancer" :projects="freelancerProjects" :accepted="true"/>
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
  name: "MyAcceptedProjects",
  components: {
    NavigationBar,
    ProjectListView,
    MyFooter
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
        .get(`/acceptedproject/create/`, {
          params: {
            user_id__id: this.$root.$data.user_id
          }
        })
        .then(response => {
          this.projects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/acceptedproject/create/`, {
          params: {
            freelancer_id__id: this.$root.$data.user_id
          }
        })
        .then(response => {
          this.freelancerProjects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
