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
          <b-card title="Filter" class="border-0 shadow">
            <b-form>
              <b-form-row>
                <b-col>
                  <b-form-group>
                    <template slot="label">
                      <font-awesome-icon icon="money-bill" fixed-width class="mr-1"/>Minimum Price
                    </template>
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
              <b-form-row>
                <b-col>
                  <b-form-group>
                    <template slot="label">
                      <font-awesome-icon icon="calendar-alt" fixed-width/>Deadline between
                    </template>
                    <v-date-picker mode="range" v-model="filter.date" show-caps>
                      <b-form-input
                        type="text"
                        slot-scope="{ inputValue, updateValue }"
                        :value="inputValue"
                        @change="updateValue($event.target.value, { formatInput: true, hidePopover: false })"
                      ></b-form-input>
                    </v-date-picker>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-form-row>
                <b-col>
                  <b-form-group>
                    <template slot="label">
                      <font-awesome-icon icon="tags" fixed-width/>Tags
                    </template>
                    <tags-input
                      input-class="form-control"
                      :typeahead-max-results="6"
                      placeholder="Filter tags"
                      :only-existing-tags="true"
                      v-model="filter.tags"
                      :existing-tags="filter.tagOptions"
                      :typeahead="true"
                    ></tags-input>
                  </b-form-group>
                </b-col>
              </b-form-row>
              <b-button @click="resetFilters" size="sm">Reset filters</b-button>
            </b-form>
          </b-card>
        </b-col>
        <b-col cols="12" md="9">
          <b-list-group class="border-0 shadow">
            <b-list-group-item v-if="projects.length == 0">
              <p class="mb-0">No project found. 😞</p>
            </b-list-group-item>
          </b-list-group>
          <ProjectListView :projects="projects" :tags="tags"/>
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
import ProjectListView from "./ProjectListView.vue";
import "@voerro/vue-tagsinput/dist/style.css";

export default {
  name: "Search",
  components: {
    NavigationBar,
    MyFooter,
    ProjectListView
  },
  data() {
    return {
      projects: [],
      query: this.$route.params.query,
      filter: {
        budget_min: 0,
        budget_max: 10000,
        ordering: "id",
        orderingLabel: "Oldest",
        date: {
          start: null,
          end: null
        },
        tagOptions: {},
        tags: []
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
      ],
      tags: []
    };
  },
  watch: {
    "filter.ordering": function(newOrdering, oldOrdering) {
      this.fetchData();
    },
    "filter.budget_min": function(newBudget_min, oldBudget_max) {
      this.debouncedFetchData();
    },
    "filter.budget_max": function(newBudget_max, oldBudget_max) {
      this.debouncedFetchData();
    },
    "filter.date": function(newDate, oldDate) {
      this.fetchData();
    },
    "filter.tags": function(newTags, oldTags) {
      this.fetchData();
    }
  },
  beforeRouteLeave(to, from, next) {
    sessionStorage.setItem("filterMinPrice", this.filter.budget_min);
    sessionStorage.setItem("filterMaxPrice", this.filter.budget_max);
    if (this.filter.date) {
      if (this.filter.date.start && this.filter.date.end) {
        sessionStorage.setItem("filterDeadlineStart", this.filter.date.start);
        sessionStorage.setItem("filterDeadlineEnd", this.filter.date.end);
      }
    }
    sessionStorage.setItem("filterTag", JSON.stringify(this.filter.tags));
    next();
  },
  created() {
    this.setSorting(Number(sessionStorage.getItem("sortByIndex") || "1"));
    const minPrice = sessionStorage.getItem("filterMinPrice");
    if (minPrice) {
      this.filter.budget_min = Number(minPrice);
    } else {
      this.filter.budget_min = 0;
    }
    const maxPrice = sessionStorage.getItem("filterMaxPrice");
    if (maxPrice) {
      this.filter.budget_max = Number(maxPrice);
    } else {
      this.filter.budget_max = 10000;
    }
    const deadlineStart = sessionStorage.getItem("filterDeadlineStart");
    if (deadlineStart) {
      const end = sessionStorage.getItem("filterDeadlineEnd");
      this.filter.date.start = new Date(deadlineStart);
      this.filter.date.end = new Date(end);
    }
    this.debouncedFetchData = debounce(this.fetchData, 500);
    this.fetchData();
    this.fetchTags();
  },
  beforeRouteUpdate(to, from, next) {
    this.query = to.params.query;
    this.fetchData();
    next();
  },
  methods: {
    fetchData() {
      let params = {
        ordering: this.filter.ordering,
        budget_min__gte: this.filter.budget_min,
        budget_max__lte: this.filter.budget_max
      };
      let tagStrings = this.filter.tags.map(
        index => this.filter.tagOptions[index]
      );
      let tagQuery = tagStrings.join(" ");
      params.search = this.query + " " + tagQuery;
      console.log(params.search);
      if (this.filter.date && this.filter.date.end && this.filter.date.start) {
        params.deadline__lte = this.$moment(this.filter.date.end).format(
          "YYYY-MM-DD"
        );
        params.deadline__gte = this.$moment(this.filter.date.start).format(
          "YYYY-MM-DD"
        );
      }
      this.$axios
        .get(`/project/create/`, {
          params
        })
        .then(response => {
          this.projects = response.data;
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
    },
    setSorting(index) {
      this.filter.ordering = this.orderingOptions[index];
      this.filter.orderingLabel = this.orderingLabelOptions[index];
      sessionStorage.setItem("sortByIndex", index);
    },
    resetFilters() {
      this.filter.budget_min = 0;
      this.filter.budget_max = 10000;
      this.filter.date = null;
      this.filter.tags = [];
    },
    fetchTags() {
      this.$axios
        .get("/project/tag/")
        .then(response => {
          response.data.forEach(element => {
            this.filter.tagOptions[element.id] = element.title;
          });
          const tagJson = sessionStorage.getItem("filterTag");
          if (tagJson) {
            this.filter.tags = JSON.parse(tagJson);
          }
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
