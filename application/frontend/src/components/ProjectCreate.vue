<template>
  <div>
      <NavigationBar/>

      <b-container class="form-narrow mb-5">
        <h2>Create Project</h2>
        <b-form @submit="onSubmit">
          <b-form-row>
            <b-col>
              <b-form-group label="Project Title"
                            label-for="inputTitle">
                <b-form-input id="inputTitle"
                              type="text"
                              v-model="form.title"
                              placeholder="e.g. Interior Desing for a Restaurant"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
          </b-form-row>
            
          <b-form-row>
            <b-col>
              <b-form-group label="Project Description"
                            label-for="inputDesc">
                <b-form-textarea id="inputDesc"
                          v-model="form.description"
                          placeholder="Describe your project"
                          :rows="4"
                          :max-rows="8"
                          required>
                </b-form-textarea>
              </b-form-group>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group label="Category"
                            label-for="inputCategory">
                <b-form-select v-model="form.categorySelected" 
                               :options="form.categoryOptions" 
                               required/>
              </b-form-group>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group label="Tags">
                <tags-input input-class="form-control"
                            :typeahead-max-results="6"
                            placeholder="Enter tags (e.g required skills)"
                            :only-existing-tags="true"
                            v-model="form.tags"
                            :existing-tags="form.tagOptions"
                            :typeahead="true"></tags-input>
              </b-form-group>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group label="Minimum Budget"
                            label-for="inputMinBudget">
                <b-form-input id="inputMinBudget"
                              type="number"
                              v-model="form.budget_min"
                              min="1"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
            <b-col>
              <b-form-group label="Maximum Budget"
                            label-for="inputMaxBudget">
                <b-form-input id="inputMaxBudget"
                              type="number"
                              v-model="form.budget_max"
                              :min="form.budget_min"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group label="Deadline Date"
                            label-for="inputDeadlineD">
                <b-form-input id="inputDeadlineD"
                              type="date"
                              v-model="form.deadlineDate"
                              :min="today"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
            <b-col>
              <b-form-group label="Deadline Time"
                            label-for="inputDeadlineT">
                <b-form-input id="inputDeadlineT"
                              type="time"
                              v-model="form.deadlineTime"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
          </b-form-row>

          <b-button type="submit" variant="primary" block>Post Project</b-button>
        </b-form>
      </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import "@voerro/vue-tagsinput/dist/style.css";

export default {
  name: "ProjectCreate",
  components: {
    NavigationBar
  },
  data() {
    return {
      today: "",
      form: {
        title: "",
        description: "",
        categorySelected: null,
        categoryOptions: [{ value: null, text: "Select a category" }],
        tagOptions: {},
        tags: [],
        budget_min: null,
        budget_max: null,
        deadlineDate: null,
        deadlineTime: "23:59"
      }
    };
  },
  created() {
    this.setToday();
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get("/project/category/")
        .then(response => {
          response.data.forEach(element => {
            this.form.categoryOptions.push({
              value: element.id,
              text: element.title
            });
          });
        })
        .catch(err => {
          console.log(err);
        });
      this.$axios
        .get("/project/tag/")
        .then(response => {
          response.data.forEach(element => {
            this.form.tagOptions[element.id] = element.title;
          });
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit() {
      this.$axios
        .post("/project/create/", {
          title: this.form.title,
          description: this.form.description,
          category: this.form.categorySelected,
          tags: this.form.tags,
          budget_min: this.form.budget_min,
          budget_max: this.form.budget_max,
          deadline:
            this.form.deadlineDate + "T" + this.form.deadlineTime + ":00Z"
        })
        .then(response => {
          this.$router.push(`/project/${response.data.id}`);
        })
        .catch(err => {
          console.log(err);
        });
    },
    setToday() {
      let today = new Date();
      let dd = today.getDate();
      let mm = today.getMonth() + 1; //January is 0!
      let yyyy = today.getFullYear();

      if (dd < 10) {
        dd = "0" + dd;
      }

      if (mm < 10) {
        mm = "0" + mm;
      }
      this.today = yyyy + "-" + mm + "-" + dd;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.form-narrow {
  width: 100%;
  max-width: 660px;
  margin: auto;
}
</style>
