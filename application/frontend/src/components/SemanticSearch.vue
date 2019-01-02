<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>Semantic Search Results for "{{this.query}}"</h2>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-list-group class="border-0 shadow">
            <b-list-group-item v-if="projects.length == 0">
              <p class="mb-0">No project found. 😞</p>
            </b-list-group-item>
          </b-list-group>
          <b-list-group class="border-0 shadow">
            <b-list-group-item :key="project.id" v-for="project in projects">
              <router-link :to="`/project/${project.id}`">{{project.title}}</router-link>
              <div>{{project.description | striphtml | shortDescription}}</div>
              <span class="text-success mr-4">
                <font-awesome-icon icon="money-bill" fixed-width/>
                {{`${project.budget_min}-${project.budget_max}`}}
              </span>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
      <MyFooter/>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import MyFooter from "./MyFooter.vue";

export default {
  name: "SemanticSearch",
  components: {
    NavigationBar,
    MyFooter
  },
  data() {
    return {
      projects: [],
      query: this.$route.params.query
    };
  },
  created() {
    this.fetchData();
  },
  beforeRouteUpdate(to, from, next) {
    this.query = to.params.query;
    this.fetchData();
    next();
  },
  methods: {
    fetchData() {
      this.$axios({
        url: "/project/semantic",
        method: "post",
        data: {
          keyword: this.query
        },
        responseType: "text"
      })
        .then(response => {
          //console.log(JSON.parse(response.data));
          this.projects = JSON.parse(response.data);
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
