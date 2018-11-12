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

          <h6><font-awesome-icon icon="map-marker-alt" fixed-width />Location <span class="text-muted">(Optional)</span></h6>
          <div><small class="text-muted">You can select a location by clicking to the map or searching via search box. You can change the selected location by clicking again. You can remove location by reset button.</small></div>
          <b-button class="mb-1" size="sm" @click="deleteMarkerAndClearInput">Reset location</b-button>
          <b-form-input id="pac-input" class="controls mb-1" type="text" placeholder="Search location"></b-form-input>
          <div class="embed-responsive mb-2">
            <div id="map"></div>
          </div>

          <b-button type="submit" variant="primary" block>Post Project</b-button>
        </b-form>
      </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import "@voerro/vue-tagsinput/dist/style.css";
import GoogleMapsLoader from "google-maps";

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
      map: null,
      mapMarkers: [],
      mapSearchBox: null
    };
  },
  created() {
    this.setToday();
    this.fetchData();
  },
  mounted() {
    this.googleMapsFontFix();
    this.googleMapsInit();
  },
  beforeDestroy() {
    GoogleMapsLoader.release(function() {});
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
      if(this.mapMarkers.length > 0){
        postBody["latitude"] = this.mapMarkers[0].getPosition().lat().toFixed(7);
        postBody["longitude"] = this.mapMarkers[0].getPosition().lng().toFixed(7);
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
    googleMapsFontFix(){
      /* to prevent google maps from replacing the default
       * font with Roboto. */
      let head = document.getElementsByTagName("head")[0];

      // Save the original method
      let insertBefore = head.insertBefore;

      // Replace it!
      head.insertBefore = function(newElement, referenceElement) {
        if (
          newElement.href &&
          newElement.href.indexOf("//fonts.googleapis.com/css?family=Roboto") > -1
        ) {
          console.info("Prevented Roboto from loading!");
          return;
        }
        insertBefore.call(head, newElement, referenceElement);
      };
    },
    googleMapsInit(){
      GoogleMapsLoader.KEY = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;
      GoogleMapsLoader.VERSION = '3.34';
      GoogleMapsLoader.LIBRARIES = ['places'];

      GoogleMapsLoader.load((google) => {
        this.map = new google.maps.Map(document.getElementById("map"), {
          zoom: 1,
          center: {lat:0, lng:0},
        });
        
        // Create the search box and link it to the UI element.
        let input = document.getElementById('pac-input');
        google.maps.event.addDomListener(input, 'keydown', function(event) { 
          if (event.keyCode === 13) { 
              event.preventDefault();
          }
        });
        this.mapSearchBox = new google.maps.places.SearchBox(input);
        //this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        this.map.addListener('bounds_changed', () => {
          this.mapSearchBox.setBounds(this.map.getBounds());
        });

        this.mapSearchBox.addListener('places_changed', () => {
          let places = this.mapSearchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          this.deleteMarkers();

          // For each place, get the icon, name and location.
          let bounds = new google.maps.LatLngBounds();
          places.forEach((place) => {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }
            /*
            let icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };*/

            // Create a marker for each place.
            this.mapMarkers.push(new google.maps.Marker({
              map: this.map,
              //icon: icon,
              title: place.name,
              position: place.geometry.location
            }));

            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
          });
          this.map.fitBounds(bounds);
        });


        
        this.map.addListener('click', (event) => {
          this.deleteMarkers();
          document.getElementById('pac-input').value = "";
          this.addMapMarker(event.latLng);
        });
      });
    },
    addMapMarker(location){
      // Adds a marker to the map and push to the array.
      GoogleMapsLoader.load((google) => {
        let marker = new google.maps.Marker({
          position: location,
          map: this.map
        });
        this.mapMarkers.push(marker);
      });
    },
    deleteMarkers() { 
      // Deletes all markers in the array by removing references to them.
      this.clearMarkers();
      this.mapMarkers = [];
    },
    clearMarkers() {
      // Removes the markers from the map, but keeps them in the array.
      this.setMapOnAll(null);
    },
    setMapOnAll(map) {
      // Sets the map on all markers in the array.
      for (var i = 0; i < this.mapMarkers.length; i++) {
        this.mapMarkers[i].setMap(map);
      }
    },
    deleteMarkerAndClearInput(){
      this.deleteMarkers();
      document.getElementById('pac-input').value = "";
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
#map {
  height: 400px;
}
</style>
