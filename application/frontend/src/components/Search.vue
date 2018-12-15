<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>Search Results for "{{this.query}}"</h2>
        </b-col>
        <b-col cols="auto">
          <b-dropdown right>
            <template slot="text">Show: {{filter.orderingLabel}} first</template>
            <b-dropdown-item-button @click="setSorting(0)">Newest</b-dropdown-item-button>
            <b-dropdown-item-button @click="setSorting(1)">Oldest</b-dropdown-item-button>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item-button @click="setSorting(2)">Highest Price</b-dropdown-item-button>
            <b-dropdown-item-button @click="setSorting(3)">Lowest Price</b-dropdown-item-button>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item-button @click="setSorting(4)">Closest Deadline</b-dropdown-item-button>
            <b-dropdown-item-button @click="setSorting(5)">Farthest Deadline</b-dropdown-item-button>
          </b-dropdown>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12" md="3">
          <b-card title="Filter">
            <b-form>
              <b-form-row>
                <b-col>
                  <b-form-group>
                    <template slot="label">Minimum Price</template>
                    <b-form-input
                      id="inputMinBudget"
                      type="number"
                      v-model="filter.budget_min"
                      :min="0"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group>
                    <template slot="label">Maximum Price</template>
                    <b-form-input
                      id="inputMaxBudget"
                      type="number"
                      v-model="filter.budget_max"
                      :min="filter.budget_min"
                      max="10000"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-button @click="resetFilters" size="sm">Reset filters</b-button>
            </b-form>
          </b-card>
        </b-col>
        <b-col cols="12" md="9">
          <b-list-group>
            <b-list-group-item v-if="projects.length == 0"><p class="mb-0">No project found. 😞</p></b-list-group-item>
            <b-list-group-item :key="project.id" v-for="project in projects">
              <router-link :to="`/project/${project.id}`">
                {{project.title}}
              </router-link>
              <div>{{project.description | striphtml | shortDescription}}</div>
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
import debounce from "lodash.debounce";

export default {
  name: "Search",
  components: {
    NavigationBar,
    MyFooter
  },
  data() {
    return {
      projects: [],
      query: this.$route.params.query,
      filter: {
        budget_min: 0,
        budget_max: 10000,
        ordering: "id",
        orderingLabel: "Oldest"
      },
      orderingOptions: [
        "-id",
        "id",
        "-budget_max",
        "budget_max",
        "deadline",
        "-deadline"
      ],
      orderingLabelOptions: [
        "Newest",
        "Oldest",
        "Highest Price",
        "Lowest Price",
        "Closest Deadline",
        "Farthest Deadline"
      ]
    };
  },
  watch: {
    'filter.ordering' : function(newOrdering, oldOrdering) {
      this.fetchData();
    },
    'filter.budget_min' : function(newBudget_min, oldBudget_max) {
      this.debouncedFetchData();
    },
    'filter.budget_max' : function(newBudget_max, oldBudget_max) {
      this.debouncedFetchData();
    }
  },
  beforeRouteLeave(to, from, next) {
    sessionStorage.setItem("filterMinPrice",this.filter.budget_min);
    sessionStorage.setItem("filterMaxPrice", this.filter.budget_max);
    next();
  },
  created() {
    this.setSorting(Number(sessionStorage.getItem("sortByIndex") || "1"));
    if(sessionStorage.getItem("filterMinPrice")){
      this.filter.budget_min = Number(sessionStorage.getItem("filterMinPrice"));
    }else{
      this.filter.budget_min = 0;
    }
    if(sessionStorage.getItem("filterMaxPrice")){
      this.filter.budget_max = Number(sessionStorage.getItem("filterMaxPrice"));
    }else{
      this.filter.budget_max = 10000;
    }
    this.debouncedFetchData = debounce(this.fetchData, 500);
    this.fetchData();
  },
  beforeRouteUpdate(to, from, next) {
    this.query = to.params.query;
    this.fetchData();
    next();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/project/create/`, {
          params: {
            search: this.query,
            ordering: this.filter.ordering,
            budget_min__gt: this.filter.budget_min,
            budget_max__lt: this.filter.budget_max
          }
        })
        .then(response => {
          this.projects = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    setSorting(index) {
      this.filter.ordering = this.orderingOptions[index];
      this.filter.orderingLabel = this.orderingLabelOptions[index];
      sessionStorage.setItem("sortByIndex",index);
    },
    resetFilters(){
      this.filter.budget_min = 0;
      this.filter.budget_max = 10000;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
