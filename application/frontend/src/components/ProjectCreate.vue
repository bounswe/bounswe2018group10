<template>
  <div>
      <NavigationBar/>

      <b-container class="form-narrow mb-5">
        <h2>Create Project</h2>
        <b-form @submit="onSubmit">
          <b-form-row>
            <b-col>
              <b-form-group label-for="inputTitle">
                <template slot="label">
                  <font-awesome-icon icon="text-height" fixed-width />
                  Project Title
                </template>
                <b-form-input id="inputTitle"
                              type="text"
                              maxlength="200"
                              v-model="form.title"
                              placeholder="e.g. Interior Desing for a Restaurant"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
          </b-form-row>
            
          <b-form-row>
            <b-col>
              <b-form-group label-for="inputDesc">
                <template slot="label">
                  <font-awesome-icon icon="align-left" fixed-width />
                  Project Description
                </template>
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
              <b-form-group label-for="inputCategory">
                <template slot="label">
                  <font-awesome-icon icon="layer-group" fixed-width />
                  Category
                </template>
                <b-form-select v-model="form.categorySelected" 
                               :options="form.categoryOptions" 
                               required/>
              </b-form-group>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group>
                <template slot="label">
                  <font-awesome-icon icon="tags" fixed-width />
                  Tags
                </template>
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
              <b-form-group label-for="inputMinBudget">
                <template slot="label">
                  <font-awesome-icon icon="money-bill" fixed-width />
                  Minimum Budget
                </template>
                <b-form-input id="inputMinBudget"
                              type="number"
                              v-model="form.budget_min"
                              min="1"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
            <b-col>
              <b-form-group label-for="inputMaxBudget">
                <template slot="label">
                  <font-awesome-icon icon="money-bill" fixed-width />
                  Maximum Budget
                </template>
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
              <b-form-group label-for="inputDeadlineD">
                <template slot="label">
                  <font-awesome-icon icon="calendar-alt" fixed-width />
                  Deadline Date
                </template>
                <b-form-input id="inputDeadlineD"
                              type="date"
                              v-model="form.deadlineDate"
                              :min="today"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
            <b-col>
              <b-form-group label-for="inputDeadlineT">
                <template slot="label">
                  <font-awesome-icon icon="clock" fixed-width />
                  Deadline Time
                </template>
                <b-form-input id="inputDeadlineT"
                              type="time"
                              v-model="form.deadlineTime"
                              required>
                </b-form-input>
              </b-form-group> 
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group>
                <b-button class="mb-2" v-b-toggle.collapse1 variant="primary">Add Location</b-button>

                <b-collapse id="collapse1">
                  <h6><font-awesome-icon icon="map-marker-alt" fixed-width />Location <span class="text-muted">(Optional)</span></h6>
                  <div><small class="text-muted">You can select a location by clicking to the map or searching via search box. You can change the selected location by clicking again. You can remove location by reset button.</small></div>
                  <b-button class="mb-2" size="sm" @click="deleteMarkerAndClearInput">Reset location</b-button>

                  <GmapAutocomplete id="location-input" class="form-control mb-2" 
                                    placeholder="Search location" 
                                    @place_changed="setPlace"
                                    @keydown.native.enter.prevent
                                    :selectFirstOnEnter="true"></GmapAutocomplete>
                                    
                  <div class="embed-responsive mb-2">
                    <GmapMap :center="position"
                            :zoom="zoom"
                            style="height: 400px"
                            @click="mapClick"
                            ref="mapRef">
                      <GmapMarker :key="index"
                        v-for="(m, index) in markers"
                        :position="m.position"
                        :clickable="true"
                        :draggable="false"
                      />
                    </GmapMap>
                  </div>
                </b-collapse>

              </b-form-group>
            </b-col>
          </b-form-row>
          

          <b-button type="submit" size="lg" variant="primary" block>Post Project</b-button>
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
      },
      position: {lat:0, lng:0},
      markers: [],
      currentPlace: null,
      zoom: 1
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
    onSubmit(evt) {
      evt.preventDefault();
      let postBody = {
        title: this.form.title,
        description: this.form.description,
        category: this.form.categorySelected,
        tags: this.form.tags,
        budget_min: this.form.budget_min,
        budget_max: this.form.budget_max,
        deadline:
          this.form.deadlineDate + "T" + this.form.deadlineTime + ":00Z"
      };
      if(this.markers.length > 0){
        postBody["latitude"] = this.markers[0].position.lat.toFixed(7);
        postBody["longitude"] = this.markers[0].position.lng.toFixed(7);
      }
      this.$axios
        .post("/project/create/", postBody)
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
    },
    deleteMarkerAndClearInput(){
      this.markers = [];
      document.getElementById('location-input').value = "";
    },
    setPlace(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      this.currentPlace = place;
      this.markers = [{position: place.geometry.location}];
      this.position = place.geometry.location;

      let bounds = new google.maps.LatLngBounds();

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }

      this.$refs.mapRef.$mapPromise.then((map) => {
        map.fitBounds(bounds);
      });
    },
    mapClick(mouseArgs) {
      let position = {};
      position.lat = mouseArgs.latLng.lat();
      position.lng = mouseArgs.latLng.lng();

      this.markers = [{position: position}];
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
