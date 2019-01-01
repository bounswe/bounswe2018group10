<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <div class="mb-4">
        <b-button v-if="isClient" class="mr-2" variant="primary" size="lg" to="/project-create">
          <font-awesome-icon icon="plus" fixed-width/>Create Project
        </b-button>
        <b-button variant="primary" to="/all-projects">All Projects</b-button>
      </div>

      <div v-if="isClient">
        <b-row>
          <b-col>
            <h2>My Ongoing Projects</h2>
          </b-col>
          <b-col cols="auto">
            <router-link to="/my-accepted-projects">View all</router-link>
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card class="border-0 shadow" v-if="acceptedProjects.length == 0">
                  <p class="card-text text-center">You do not have any ongoing projects.</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="acceptedProjects.slice(-4).reverse()" :accepted="true"/>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <h2>My Projects</h2>
          </b-col>
          <b-col cols="auto">
            <router-link to="/my-projects">View all</router-link>
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card v-if="projects.length == 0" class="text-center border-0 shadow">
                  <p class="card-text">You do not have any projects.</p>
                  <b-button v-if="isClient" variant="primary" size="lg" to="/project-create">
                    <font-awesome-icon icon="plus" fixed-width/>Create Project
                  </b-button>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="projects.slice(-4).reverse()" :tags="tags"/>
          </b-col>
        </b-row>
      </div>

      <div v-if="isFreelancer">
        <b-row>
          <b-col>
            <h2>My Ongoing Projects</h2>
          </b-col>
          <b-col cols="auto">
            <router-link to="/my-accepted-projects">View all</router-link>
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card class="border-0 shadow" v-if="acceptedFreelancerProjects.length == 0">
                  <p class="card-text text-center">You do not have any ongoing projects.</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView
              :projects="acceptedFreelancerProjects.slice(-4).reverse()"
              :accepted="true"
            />
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <h2>Projects I Bid For</h2>
          </b-col>
          <b-col cols="auto">
            <router-link to="/my-projects">View all</router-link>
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card v-if="freelancerProjects.length == 0" class="text-center border-0 shadow">
                  <p
                    class="card-text"
                  >You do not have any projects. Search for new projects to bid for!</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="freelancerProjects.slice(-4).reverse()" :tags="tags"/>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <h2 class="text-danger">
              <font-awesome-icon icon="fire" fixed-width/>New Projects
            </h2>
          </b-col>
          <b-col cols="auto">
            <!--<router-link to="/my-projects">View all</router-link>-->
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card v-if="newProjects.length == 0" class="text-center border-0 shadow">
                  <p class="card-text">There are not any new projects.</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="newProjects.slice(-4).reverse()" :tags="tags"/>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <h2 class="text-primary">
              <font-awesome-icon icon="chart-line" fixed-width/>Trending Projects
            </h2>
          </b-col>
          <b-col cols="auto">
            <!--<router-link to="/my-projects">View all</router-link>-->
          </b-col>
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card v-if="newProjects.length == 0" class="text-center border-0 shadow">
                  <p class="card-text">There are not any trending projects.</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="newProjects.slice(-4).reverse()" :tags="tags"/>
          </b-col>
        </b-row>
      </div>

      <MyFooter/>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import MyFooter from "./MyFooter.vue";
import ProjectCardView from "./ProjectCardView.vue";

export default {
  name: "Dashboard",
  components: {
    NavigationBar,
    MyFooter,
    ProjectCardView
  },
  data() {
    return {
      projects: [],
      freelancerProjects: [],
      acceptedProjects: [],
      acceptedFreelancerProjects: [],
      newProjects: [],
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
        .get(`/acceptedproject/create/?user_id__id=${this.$root.$data.user_id}`)
        .then(response => {
          this.acceptedProjects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/project/bid/`)
        .then(response => {
          let projectList = response.data
            .filter(bid => bid.user_id == this.$root.$data.user_id)
            .map(bidList => bidList.project_id);
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
        .get(`/acceptedproject/create/`, {
          params: {
            freelancer_id__id: this.$root.$data.user_id
          }
        })
        .then(response => {
          this.acceptedFreelancerProjects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/project/create/`)
        .then(response => {
          this.newProjects = response.data;
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
