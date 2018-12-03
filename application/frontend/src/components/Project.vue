<template>
  <div class="bg-light">
    <NavigationBar/>

    <b-container>
      <b-row class="mb-2">
        <b-col>
          <h2 class="mb-0">{{project.title}}</h2>
        </b-col>
        <b-col cols="auto" class="ml-auto">
          <b-button
            v-if="isFreelancer && !placedBid"
            v-b-toggle.collapse1
            variant="primary"
          >Bid for Project</b-button>
        </b-col>
      </b-row>

      <b-collapse v-if="isFreelancer && !placedBid" id="collapse1">
        <b-row class="mb-4">
          <b-col>
            <b-card class="shadow">
              <b-form @submit="onBidSubmit">
                <b-form-row>
                  <b-col>
                    <b-form-group
                      label="Bid Amount"
                      label-for="inputBid"
                      description="Your bid should be within the budget range."
                    >
                      <b-form-input
                        id="inputBid"
                        type="number"
                        v-model="bidForm.amount"
                        :min="project.budget_min"
                        :max="project.budget_max"
                        required
                        placeholder="Amount"
                      ></b-form-input>
                    </b-form-group>
                  </b-col>
                  <!--<b-col cols="12" md="6">
                    <b-form-group label="Deliver In"
                                  label-for="inputDeliver">
                      <b-input-group append="Days">
                        <b-form-input id="inputDeliver"
                                      type="number"
                                      v-model="bidForm.deliverIn"
                                      min="1"
                                      >
                        </b-form-input>
                      </b-input-group>
                    </b-form-group>
                  </b-col>-->
                </b-form-row>
                <b-form-row>
                  <b-col>
                    <b-form-group label-for="inputDesc">
                      <template slot="label">
                        <!--<font-awesome-icon icon="align-left" fixed-width />-->
                        Description
                      </template>
                      <b-form-textarea
                        id="inputDesc"
                        v-model="bidForm.description"
                        placeholder="Describe why the client should choose you"
                        maxlength="1000"
                        :rows="2"
                        :max-rows="8"
                        required
                      ></b-form-textarea>
                    </b-form-group>
                  </b-col>
                </b-form-row>

                <h6>
                  <strong>Milestones</strong>
                </h6>
                <div :key="index" v-for="(milestone,index) in bidForm.milestones">
                  <p class="mb-0">Milestone {{index+1}}</p>
                  <b-form-row>
                    <b-col cols="12" md="12" lg="6">
                      <b-form-group :label="`Description`" label-for="inputMilestone">
                        <b-form-textarea
                          id="inputMilestone"
                          type="text"
                          placeholder="Description for milestone"
                          maxlength="200"
                          :rows="2"
                          :max-rows="4"
                          v-model="milestone.description"
                          required
                        ></b-form-textarea>
                      </b-form-group>
                    </b-col>
                    <b-col cols="12" md="4" lg="2">
                      <b-form-group :label="`Amount`" label-for="inputMileBud">
                        <b-form-input
                          id="inputMileBud"
                          type="number"
                          v-model="milestone.amount"
                          min="1"
                          required
                          placeholder="Amount"
                        ></b-form-input>
                      </b-form-group>
                    </b-col>
                    <b-col cols="12" sm="6" md="4" lg="2">
                      <b-form-group label-for="inputDeadlineD">
                        <template slot="label">
                          <!--<font-awesome-icon icon="calendar-alt" fixed-width />-->
                          Deadline Date
                        </template>
                        <b-form-input
                          id="inputDeadlineD"
                          type="date"
                          v-model="milestone.deadlineDate"
                          :min="today"
                          required
                        ></b-form-input>
                      </b-form-group>
                    </b-col>
                    <b-col cols="12" sm="6" md="4" lg="2">
                      <b-form-group label-for="inputDeadlineT">
                        <template slot="label">
                          <!--<font-awesome-icon icon="clock" fixed-width />-->
                          Deadline Time
                        </template>
                        <b-form-input
                          id="inputDeadlineT"
                          type="time"
                          v-model="milestone.deadlineTime"
                          required
                        ></b-form-input>
                      </b-form-group>
                    </b-col>
                  </b-form-row>
                </div>

                <b-form-row class="mb-2">
                  <b-col>
                    <b-button
                      class="mr-1"
                      @click="addMilestone"
                      variant="primary"
                      size="sm"
                    >Add a Milestone</b-button>
                    <b-button
                      @click="removeMilestone"
                      variant="primary"
                      size="sm"
                    >Remove a Milestone</b-button>
                  </b-col>
                </b-form-row>

                <b-button type="submit" variant="primary" block>Place Bid</b-button>
              </b-form>
            </b-card>
          </b-col>
        </b-row>
      </b-collapse>

      <b-row class="mb-4">
        <b-col>
          <b-card class="shadow">
            <b-row>
              <b-col>
                <strong>Bids</strong>
                <div>{{bids.length}}</div>
              </b-col>
              <b-col>
                <strong>Budget</strong>
                <div>{{project.budget_min}} - {{project.budget_max}}</div>
              </b-col>
              <b-col>
                <strong>Deadline</strong>
                <div>
                  <span
                    v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
                  >{{project.deadline | moment("from") }}</span>
                </div>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card class="shadow" title="Project Description">
            <p class="card-text">{{project.description}}</p>
            <div>Category:
              <router-link :to="`/search/${projectCategory.title}`">{{projectCategory.title}}</router-link>
            </div>
            <div>
              <span>Tags:</span>
              <b-badge
                class="mr-1"
                variant="primary"
                :to="`/search/${tag.title}`"
                :key="tag.id"
                v-for="tag in projectTags"
              >{{tag.title}}</b-badge>
            </div>
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

      <b-row v-if="isProjectCreator" class="mb-4">
        <b-col>
          <b-list-group class="shadow">
            <b-list-group-item>
              <b-row>
                <b-col>
                  <h5 class="mb-0">Bids ({{bids.length}})</h5>
                  <!--<strong>Freelancer</strong>-->
                </b-col>
                <!--<b-col>
                  <strong>Description</strong>
                </b-col>
                <b-col>
                  <strong>Bid</strong>
                </b-col>
                <b-col cols="2"></b-col>-->
              </b-row>
            </b-list-group-item>
            <b-list-group-item v-show="!bids.length">
              <p class="mb-0">There are no bids placed on this project.</p>
            </b-list-group-item>
            <b-list-group-item :key="index" v-for="(bid,index) in bids">
              <b-row>
                <b-col class="clearfix" cols="12" md="3" lg="2">
                  <b-img
                    left
                    :src="bid.avatar ? bid.avatar : blankProfilePic"
                    fluid
                    rounded
                    width="96"
                    class="m-1"
                  />
                </b-col>
                <b-col cols="12" md="7" lg="6">
                  <div>
                    <router-link :to="`/profile/${bid.user_id}/freelancer`">
                      <strong>{{bid.name}}</strong>
                    </router-link>
                  </div>
                  <p>
                    <strong>Description</strong>
                    {{bid.description}}
                  </p>
                  <b-btn
                    v-show="milestones.filter(m => m.bid_id == bid.id).length > 0"
                    v-b-toggle="`collapse${index}`"
                    variant="secondary"
                    size="sm"
                  >
                    <span class="when-opened">Hide</span>
                    <span class="when-closed">Show</span>
                    Milestones
                  </b-btn>
                  <b-collapse :id="`collapse${index}`" class="mt-2">
                    <b-card>
                      <div
                        :key="index"
                        v-for="(milestone,index) in milestones.filter(m => m.bid_id == bid.id)"
                      >
                        <hr v-if="index != 0">
                        <p>
                          <strong>{{"Milestone "+(index+1)}}</strong>
                        </p>
                        <p>Description: {{milestone.description}}</p>
                        <p>Amount: {{milestone.amount}}</p>
                        <p>Deadline: {{$moment(milestone.deadline).format("LLL")}}</p>
                      </div>
                    </b-card>
                  </b-collapse>
                </b-col>
                <b-col cols="12" md="2" lg="2">
                  <strong>Bid</strong>
                  {{bid.amount}}
                </b-col>
                <b-col cols="12" lg="2">
                  <b-button
                    @click="chooseBid(bid.id)"
                    v-show="!project.accepted_bid && isClient"
                    variant="primary"
                  >Accept Bid</b-button>
                  <h5>
                    <b-badge
                      v-show="project.accepted_bid == bid.id && isClient"
                      variant="success"
                      class="p-2"
                    >Accepted Bid</b-badge>
                  </h5>
                </b-col>
              </b-row>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>

      <!--<b-row class="mb-4">
        <b-col>
          <b-list-group class="shadow">
            <b-list-group-item>
              <b-row>
                <b-col>
                  <h5 class="mb-0">Comments (1)</h5>
                </b-col>
              </b-row>
            </b-list-group-item>
            <b-list-group-item>
              <b-form>
                <b-form-row>
                  <b-col>
                    <b-form-group label=""
                                  label-for="inputComment">
                      <b-form-textarea id="inputComment"
                                       v-model="newCommentText"
                                       placeholder="Write your comment here"
                                       :rows="2"
                                       :max-rows="8"
                                       required>
                      </b-form-textarea>
                    </b-form-group> 
                  </b-col>
                </b-form-row>

                <b-button type="submit" variant="primary">Submit Comment</b-button>
              </b-form>
            </b-list-group-item>
            <b-list-group-item :key="index" v-for="(comment,index) in comments">
              <b-row>
                <b-col md=2 lg=1>
                  <b-img left :src="comment.picture" fluid rounded width="96" class="m-1"/>
                </b-col>
                <b-col md=10 lg=11>
                  <b-row>
                    <b-col>
                      <strong>{{comment.name}}</strong>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <p class="mb-0">{{comment.text}}</p>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <small class="text-muted">{{comment.date}}</small>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>-->
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
      today: "",
      blankProfilePic: require("../assets/blank-profile-picture.svg"),
      projectID: this.$route.params.id,
      project: {},
      projectTags: [],
      projectCategory: {},
      bidForm: {
        amount: null,
        deliverIn: null,
        description: "",
        milestones: [
          {
            description: "",
            amount: null,
            deadlineDate: null,
            deadlineTime: null
          }
        ]
      },
      bids: [],
      milestones: [],
      position: { lat: 0, lng: 0 },
      markers: []
    };
  },
  created() {
    this.setToday();
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
    placedBid: function() {
      return this.bids.some(bid => bid.user_id == this.$root.$data.user_id);
    }
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/project/create/${this.projectID}/`)
        .then(response => {
          this.project = response.data;
          this.position = {
            lat: Number(this.project.latitude),
            lng: Number(this.project.longitude)
          };
          this.markers.push({ position: this.position });
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
      this.$axios
        .get(`/project/bid/`, {
          params: {
            search: this.projectID
          }
        })
        .then(response => {
          let bids = response.data;
          this.bids = bids;
        })
        .catch(err => {
          console.log(err);
        });
      this.$axios
        .get(`/project/milestone/`)
        .then(response => {
          this.milestones = response.data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    addMilestone() {
      this.bidForm.milestones.push({
        description: "",
        amount: null,
        deadlineDate: null,
        deadlineTime: null
      });
    },
    removeMilestone() {
      if (this.bidForm.milestones.length > 1) {
        this.bidForm.milestones.pop();
      }
    },
    onBidSubmit(evt) {
      evt.preventDefault();
      this.$axios
        .post("/project/bid/", {
          project_id: this.projectID,
          description: this.bidForm.description,
          amount: this.bidForm.amount
        })
        .then(response => {
          let bidId = response.data.id;
          this.sendMilestone(0, bidId);
        })
        .catch(err => {
          console.log(err);
        });
    },
    sendMilestone(index, bidId) {
      if (index == this.bidForm.milestones.length) {
        this.fetchData();
        window.scrollTo(0, 0);
      } else {
        this.$axios
          .post("/project/milestone/", {
            bid_id: bidId,
            description: this.bidForm.milestones[index].description,
            amount: this.bidForm.milestones[index].amount,
            deadline:
              this.bidForm.milestones[index].deadlineDate +
              "T" +
              this.bidForm.milestones[index].deadlineTime +
              ":00Z"
          })
          .then(response => {
            this.sendMilestone(index + 1, bidId);
          })
          .catch(err => {
            console.log(err);
          });
      }
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
    isAcceptedBid(index) {
      return this.project.accepted_bid == index;
    },
    chooseBid(bidId) {
      this.$axios
        .patch(`/project/create/${this.projectID}/`, {
          accepted_bid: bidId
        })
        .then(response => {
          this.$axios
            .post(`/acceptedproject/accept`, {
              accepted_bid: bidId
            })
            .then(response => {
              this.fetchData();
              this.project.accepted_bid = bidId;
              this.$router.push(`/accepted-project/${response.data.id}`);
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
.collapsed > .when-opened,
:not(.collapsed) > .when-closed {
  display: none;
}
</style>
