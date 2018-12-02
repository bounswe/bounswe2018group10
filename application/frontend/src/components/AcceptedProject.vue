<template>
  <div class="bg-light">
    <NavigationBar/>

    <b-container>
      <b-row class="mb-2">
        <b-col>
          <h2 class="mb-0">{{project.title}}</h2>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card class="shadow" title="Project Details">
            <p class="card-text">{{project.description}}</p>
            <p>Budget: {{project.price}}</p>
            <div v-if="project.file">File:
              <b-link :href="project.file" :target="'_blank'" :rel="'noopener noreferrer'">
                <font-awesome-icon icon="file"/>
                {{project.file.split('/').pop()}}
              </b-link>
            </div>
            <div class="mt-2" v-if="position.lat!=0&&position.lng!=0">
              <h6>Location</h6>
              <div class="embed-responsive">
                <GmapMap :center="position" :zoom="15" style="height: 400px">
                  <GmapMarker
                    :key="index"
                    v-for="(m, index) in markers"
                    :position="m.position"
                    :clickable="true"
                    :draggable="false"
                  />
                </GmapMap>
              </div>
            </div>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card class="shadow" title="Project Progress">
            <b-progress class="mt-1" :max="milestones.length">
              <b-progress-bar
                :key="index"
                v-for="(milestone,index) in milestones"
                :value="milestone.is_done ? 1 : 0"
                variant="success"
                :label="`Milestone ${index+1}`"
              ></b-progress-bar>
            </b-progress>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card class="shadow" title="Project Milestones">
            <div :key="index" v-for="(milestone,index) in milestones">
              <hr v-if="index != 0">
              <b-row>
                <b-col>
                  <h5>
                    <strong class="mr-2">Milestone {{(index+1)}}</strong>
                    <span v-if="milestone.is_done" class="badge badge-success">
                      <font-awesome-icon icon="check"/>Completed
                    </span>
                    <span v-if="!milestone.is_done" class="badge badge-secondary">Not Completed</span>
                  </h5>
                </b-col>
                <b-col cols="auto">
                  <span class="text-muted">Deadline: {{milestone.deadline}}</span>
                </b-col>
              </b-row>
              <p>
                <strong>Description:</strong>
                {{milestone.description}}
              </p>
              <p>
                <strong>Budget:</strong>
                {{milestone.amount}}
              </p>

              <div v-if="milestone.file"><strong class="mr-1">File:</strong>
                <b-link :href="milestone.file" :target="'_blank'" :rel="'noopener noreferrer'">
                  <font-awesome-icon icon="file"/>
                  {{milestone.file.split('/').pop()}}
                </b-link>
              </div>

              <b-button
                v-if="isProjectFreelancer && !milestone.is_done"
                v-b-modal="`modal${index}`"
                variant="primary"
              >Complete</b-button>
              
              <!-- Modal Component -->
              <b-modal
                :id="`modal${index}`"
                :title="`Complete Milestone ${index+1}`"
                ok-title="Complete"
                @ok="completeMilestone(milestone.id,index)"
              >
                <b-form>
                  <b-form-row>
                    <b-col>
                      <b-form-group
                        label="Milestone File Upload"
                        label-for="inputFile"
                        description="You can drag and drop your file to this input box."
                      >
                        <b-form-file
                          id="inputFile"
                          accept="*"
                          v-model="files[index]"
                          placeholder="Choose a file..."
                          ref="fileinput"
                        ></b-form-file>
                      </b-form-group>
                      <b-form-group>
                        <b-button @click="$refs.fileinput[index].reset()" size="sm">Clear file input</b-button>
                      </b-form-group>
                    </b-col>
                  </b-form-row>
                </b-form>
              </b-modal>
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
  name: "AcceptedProject",
  components: {
    NavigationBar
  },
  data() {
    return {
      projectID: this.$route.params.id,
      project: {},
      milestones: [],
      position: { lat: 0, lng: 0 },
      markers: [],
      files: []
      //projectTags: [],
      //projectCategory: {},
      //deadline: "",
      //newCommentText: "",
      //bidForm: {
      //  amount: null,
      //  deliverIn: null,
      //  description: "",
      //  milestones: []
      //},
      //bids: []
    };
  },
  created() {
    this.fetchData();
  },
  beforeRouteUpdate(to, from, next) {
    this.projectID = to.params.id;
    this.fetchData();
    window.scrollTo(0, 0);
    next();
  },
  computed: {
    isProjectCreator: function() {
      return this.$root.$data.user_id == this.project.user_id;
    },
    isProjectFreelancer: function() {
      return this.$root.$data.user_id == this.project.freelancer_id;
    }
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/acceptedproject/create/${this.projectID}/`)
        .then(response => {
          this.project = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/acceptedproject/milestone/?search=${this.projectID}`)
        .then(response => {
          this.milestones = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    completeMilestone(id,fileIndex) {
      let formData = new FormData();
      formData.append("is_done", true);
      if (this.files[fileIndex]) {
        formData.append("file", this.files[fileIndex], this.files[fileIndex].name);
      }
      this.$axios({
        method: "patch",
        url: `/acceptedproject/milestone/${id}/`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          this.fetchData();
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
