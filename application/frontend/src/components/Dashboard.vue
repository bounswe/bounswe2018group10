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

        <b-row>
          <b-col>
            <h2>Recommended Freelancers</h2>
          </b-col>
          <!--<b-col cols="auto">
            <router-link to="/my-projects">View all</router-link>
          </b-col>-->
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card
                  v-if="recommendedFreelancers.length == 0"
                  class="text-center border-0 shadow"
                >
                  <p class="card-text">We do not have any recommended freelancer for you.</p>
                </b-card>
              </b-col>
            </b-row>
            <FreelancerCardView
              :freelancers="recommendedFreelancers.slice(-4).reverse()"
              :tags="tags"
              :blankAvatar="blankAvatar"
            />
          </b-col>
        </b-row>
      </div>

      <div v-if="isFreelancer">
        <b-row>
          <b-col>
            <h2>Recommended Projects</h2>
          </b-col>
          <!--<b-col cols="auto">
            <router-link to="/my-projects">View all</router-link>
          </b-col>-->
        </b-row>

        <b-row class="mb-4">
          <b-col>
            <b-row>
              <b-col>
                <b-card v-if="recommendedProjects.length == 0" class="text-center border-0 shadow">
                  <p class="card-text">We do not have any recommended project for you.</p>
                </b-card>
              </b-col>
            </b-row>
            <ProjectCardView :projects="recommendedProjects.slice(-4).reverse()" :tags="tags"/>
          </b-col>
        </b-row>

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




      <h2>Current Projects</h2>
      <b-card-group class="h-25">
        <swiper :options="swiperOption" class="pl-4 pr-4 w-100" style="height:250px;">
          <swiper-slide v-for="project in projects" :key="project.id">
            <b-card v-if="isClient" :title="project.title" class="h-100">
              <div class="card-text">{{project.description.substring(0,40) + "..."}}</div>
              <b-badge pill variant="dark" style="position:absolute;  bottom:60px; right:20px;">
                <span
                  v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
                >{{project.deadline | moment("from") }}</span>
              </b-badge>
              <b-button variant="link" style="position:absolute;  bottom:30px;">
                <router-link :to="`/project/${project.id}`">Go to project</router-link>
              </b-button>
            </b-card>
            <b-card v-if="isFreelancer" :title="project.title" class="h-100">
              <div class="card-text">{{project.description.substring(0,40) + "..."}}</div>
              <b-badge pill variant="dark" style="position:absolute;  bottom:60px; right:20px;">
                <span
                  v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
                >{{project.deadline | moment("from") }}</span>
              </b-badge>
              <b-button variant="link" style="position:absolute;  bottom:30px;">
                <router-link :to="`/project/${project.id}`">Go to project</router-link>
              </b-button>
            </b-card>
          </swiper-slide>
          <swiper-slide>
            <b-button variant="primary" to="/my-projects" class="h-100">
              <h3 class="h-50 mt-4 pt-3" style="vertical-align:middle">All Projects</h3>
            </b-button>
          </swiper-slide>
          <div class="swiper-pagination" slot="pagination"></div>
          <div class="swiper-button-prev" slot="button-prev"></div>
          <div class="swiper-button-next" slot="button-next"></div>
        </swiper>
      </b-card-group>




      <MyFooter/>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import MyFooter from "./MyFooter.vue";
import ProjectCardView from "./ProjectCardView.vue";
import FreelancerCardView from "./FreelancerCardView.vue";

export default {
  name: "Dashboard",
  components: {
    NavigationBar,
    MyFooter,
    ProjectCardView,
    FreelancerCardView
  },
  data() {
    return {
      projects: [],
      freelancerProjects: [],
      acceptedProjects: [],
      acceptedFreelancerProjects: [],
      newProjects: [],
      tags: [],
      recommendedProjects: [],
      recommendedFreelancers: [],
      blankAvatar: require("../assets/blank-profile-picture.svg"),
      swiperOption: {
        slidesPerView: 7,
        spaceBetween: 10,
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        },
        breakpoints: {
          1904: {
            slidesPerView: 7
          },
          1440: {
            slidesPerView: 6
          },
          1024: {
            slidesPerView: 5
          },
          960: {
            slidesPerView: 4
          },
          768: {
            slidesPerView: 3
          },
          425: {
            slidesPerView: 2
          },
          320: {
            slidesPerView: 1
          }
        },
        watchOverflow: true,
        //freeMode: true
      }
    };
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.$root.$on("rolechange", this.changeRecommendation);
  },
  methods: {
    fetchData() {
      this.$axios
        .get("/project/tag/")
        .then(response => {
          this.tags = response.data;
          this.changeRecommendation();
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
            .get(
              `/acceptedproject/create/?user_id__id=${this.$root.$data.user_id}`
            )
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
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    changeRecommendation() {
      if (this.$root.$data.role == "freelancer") {
        this.$axios
          .get("/recommend/dashboard/")
          .then(response => {
            this.recommendedProjects = response.data;
          })
          .catch(err => {
            // eslint-disable-next-line
            console.log(err);
          });
      } else {
        this.$axios
          .get("/recommend/dashboard/")
          .then(response => {
            this.recommendedFreelancers = response.data;
          })
          .catch(err => {
            // eslint-disable-next-line
            console.log(err);
          });
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
