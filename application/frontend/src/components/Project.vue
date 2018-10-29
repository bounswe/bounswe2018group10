<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>{{project.title}}</h2>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card class="mb-4">
              <b-row>
                <b-col>
                  <div>Budget</div>
                  <div>
                    {{project.budget_min}} - {{project.budget_max}}
                  </div>
                </b-col>
                <b-col>
                </b-col>
                <b-col>
                  <div>Deadline</div>
                  <div>
                    {{deadline}}
                  </div>
                </b-col>
              </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-card title="Project Description">
              <p class="card-text">{{project.description}}</p>
              <div>Category: {{projectCategory.title}}</div>
              <div>
                    <span>Tags: </span>
                    <b-badge class="mr-1" 
                             variant="primary" 
                             :key="tag.id" 
                             v-for="tag in projectTags">{{tag.title}}</b-badge>
                  </div>
          </b-card>
        </b-col>
      </b-row>
      
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "Project",
  components: {
    NavigationBar
  },
  data() {
    return {
      project: {},
      projectTags: [],
      projectCategory: {},
      deadline: "",
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/project/create/${this.$route.params.id}/`)
        .then(response => {
          this.project = response.data;
          this.deadline = this.project.deadline.replace(/[TZ]/g,' ');
          this.$axios
            .get("/project/category/")
            .then(response => {
              this.projectCategory = response.data.filter(
                categoryObj => categoryObj.id == this.project.category
              )[0];
            })
            .catch(err => {
              console.log(err);
            });
          this.$axios
            .get("/project/tag/")
            .then(response => {
              this.projectTags = response.data.filter(tag =>
                this.project.tags.includes(tag.id)
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
