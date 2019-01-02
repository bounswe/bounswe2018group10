<template>
  <div>
      <NavigationBar/>

      <b-container>
        <b-button v-if="isClient" class="mr-2" variant="primary" to="/project-create">
          <font-awesome-icon icon="plus" fixed-width />Create Project
        </b-button>
        <b-button class="mr-2" variant="primary" to="/my-projects">My Projects</b-button>
        <b-button class="mr-2" variant="primary" to="/my-accepted-projects">My Accepted Projects</b-button>
        <b-button variant="primary" to="/all-projects">All Projects</b-button>

        <h2>Current Projects</h2>
          <b-card-group class="h-25">

            <swiper :options="swiperOption" class="pl-4 pr-4 w-100" style="height:250px;">
              <swiper-slide v-for="project in projects" :key="project.id">
                <b-card v-if="isClient" :title="project.title" class="h-100">
                  <div class="card-text"> 
                    {{project.description.substring(0,40) + "..."}}
                  </div>
                  <b-badge pill variant="dark" style="position:absolute;  bottom:60px; right:20px;">
                    <span v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')">
                      {{project.deadline | moment("from") }}
                    </span>
                  </b-badge>
                  <b-button variant="link" style="position:absolute;  bottom:30px;">
                    <router-link :to="`/project/${project.id}`">
                      Go to project
                    </router-link>
                  </b-button>
                </b-card>
                <b-card v-if="isFreelancer" :title="project.title" class="h-100">
                  <div class="card-text"> 
                    {{project.description.substring(0,40) + "..."}}
                  </div>
                  <b-badge pill variant="dark" style="position:absolute;  bottom:60px; right:20px;">
                    <span v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')">
                      {{project.deadline | moment("from") }}
                    </span>
                  </b-badge>
                  <b-button variant="link" style="position:absolute;  bottom:30px;">
                    <router-link :to="`/project/${project.id}`">
                      Go to project
                    </router-link>
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
import NavigationBar from './NavigationBar.vue';
import MyFooter from "./MyFooter.vue";

export default {
  name: "Dashboard",
  components: {
    NavigationBar,
    MyFooter
  },
  data () {
    return {
      projects: [],
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
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData(){
      this.$axios
        .get(`/project/create/?search=${this.$root.$data.user_id}`)
        .then(response => {
          // CURRENT PROJECTS
          this.projects = response.data.filter(p => {var d = new Date(p.deadline); return d.getTime() > Date.now() });
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
