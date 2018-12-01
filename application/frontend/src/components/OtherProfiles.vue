<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>{{name}}'s {{isClientProfile ? "Client":"Freelancer"}} Profile</h2>
        </b-col>
        <b-col cols="auto">
          <span>Profile type:</span>
          <b-form-radio-group
            buttons
            button-variant="outline-secondary"
            size="sm"
            v-model="role"
            name="radioBtnOutline"
          >
            <b-form-radio value="client">Client</b-form-radio>
            <b-form-radio value="freelancer">Freelancer</b-form-radio>
          </b-form-radio-group>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col cols="12" sm="2">
          <b-img
            v-if="isFreelancerProfile"
            :src="freelancer.avatar"
            fluid
            rounded
            alt="img"
            class="m-1"
          />
          <b-img v-if="isClientProfile" :src="client.avatar" fluid rounded alt="img" class="m-1"/>
        </b-col>
        <b-col cols="12" sm="7">
          <p v-if="isFreelancerProfile">{{freelancer.body}}</p>
          <p v-if="isClientProfile">{{client.body}}</p>
          <!--<p>Rating: {{rating}}</p>-->
        </b-col>
        <b-col cols="12" sm="3">
          <!--<b-card no-body header="<b>Skills</b>">
              <b-list-group flush>
                <b-list-group-item href="#">Java</b-list-group-item>
                <b-list-group-item href="#">Python</b-list-group-item>
                <b-list-group-item href="#">Javascript</b-list-group-item>
              </b-list-group>
          </b-card>-->
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-list-group v-show="isClientProfile">
            <b-list-group-item>
              <b-row>
                <b-col>
                  <h5 class="mb-0">Comments ({{clientComments.length}})</h5>
                </b-col>
              </b-row>
            </b-list-group-item>
            <b-list-group-item>
              <b-form @submit="submitCommentForClient" ref="clientForm">
                <b-form-row>
                  <b-col>
                    <b-form-group label label-for="inputComment">
                      <b-form-textarea
                        id="inputComment"
                        v-model="commentForClient"
                        placeholder="Write your comment here"
                        :rows="2"
                        :max-rows="8"
                        required
                      ></b-form-textarea>
                    </b-form-group>
                  </b-col>
                </b-form-row>

                <b-button type="submit" variant="primary">Submit Comment</b-button>
              </b-form>
            </b-list-group-item>
            <b-list-group-item :key="index" v-for="(comment,index) in clientComments">
              <b-row>
                <b-col md=2 lg=1>
                  <b-img left :src="comment.commenter_avatar" fluid rounded width="96" class="m-1"/>
                </b-col>
                <b-col md="10" lg="11">
                  <b-row>
                    <b-col>
                      <div>
                        <router-link :to="`/profile/${comment.user_id.id}`">
                          <strong>{{comment.user_id.name}}</strong>
                        </router-link>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <p class="mb-0">{{comment.description}}</p>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <small class="text-muted" v-b-tooltip.hover.bottom="$moment(comment.created_at).format('LLLL')">
                        {{comment.created_at | moment("from") }}
                      </small>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </b-list-group-item>
          </b-list-group>

          <b-list-group v-show="isFreelancerProfile">
            <b-list-group-item>
              <b-row>
                <b-col>
                  <h5 class="mb-0">Comments ({{freelancerComments.length}})</h5>
                </b-col>
              </b-row>
            </b-list-group-item>
            <b-list-group-item>
              <b-form @submit="submitCommentForFreelancer" ref="freelancerForm">
                <b-form-row>
                  <b-col>
                    <b-form-group label label-for="inputComment">
                      <b-form-textarea
                        id="inputComment"
                        v-model="commentForFreelancer"
                        placeholder="Write your comment here"
                        :rows="2"
                        :max-rows="8"
                        required
                      ></b-form-textarea>
                    </b-form-group>
                  </b-col>
                </b-form-row>

                <b-button type="submit" variant="primary">Submit Comment</b-button>
              </b-form>
            </b-list-group-item>
            <b-list-group-item :key="index" v-for="(comment,index) in freelancerComments">
              <b-row>
                <b-col md=2 lg=1>
                  <b-img left :src="comment.commenter_avatar" fluid rounded width="96" class="m-1"/>
                </b-col>
                <b-col md="10" lg="11">
                  <b-row>
                    <b-col>
                      <div>
                        <router-link :to="`/profile/${comment.user_id.id}`">
                          <strong>{{comment.user_id.name}}</strong>
                        </router-link>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <p class="mb-0">{{comment.description}}</p>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <small class="text-muted" v-b-tooltip.hover.bottom="$moment(comment.created_at).format('LLLL')">
                        {{comment.created_at | moment("from") }}
                      </small>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>

    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "OtherProfiles",
  components: {
    NavigationBar
  },
  data() {
    return {
      role: this.$route.params.role || "freelancer",
      profileId: this.$route.params.id,
      freelancer: {
        body: "",
        avatar: require("../assets/blank-profile-picture.svg")
      },
      client: {
        body: "",
        avatar: require("../assets/blank-profile-picture.svg")
      },
      name: "",
      //rating: 0,
      freelancerComments: [],
      clientComments: [],
      commentForClient: "",
      commentForFreelancer: ""
    };
  },
  created() {
    this.fetchData();
  },
  beforeRouteUpdate(to, from, next) {
    this.profileId = to.params.id;
    this.role = to.params.role || "freelancer";
    this.freelancer = {
      body: "",
      avatar: require("../assets/blank-profile-picture.svg")
    };
    this.client = {
      body: "",
      avatar: require("../assets/blank-profile-picture.svg")
    };
    this.name = "";
    this.freelancerComments = [];
    this.clientComments = [];
    this.commentForClient = "";
    this.commentForFreelancer = "";
    this.$refs.freelancerForm.reset();
    this.$refs.clientForm.reset();
    //this.fetchData();
    window.scrollTo(0, 0);
    next();
  },
  watch: {
    // call again the method if the route changes
    '$route': function(newRoute,oldRoute) {
      this.fetchData();
    }
  },
  computed: {
    isClientProfile: function() {
      return this.role == "client";
    },
    isFreelancerProfile: function() {
      return this.role == "freelancer";
    }
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/user/freelancerprofile/?search=${this.profileId}`)
        .then(response => {
          let profile = response.data[0];
          this.freelancer.body = profile.body;
          if (profile.avatar) {
            this.freelancer.avatar = profile.avatar;
          }
          this.name = profile.user.name;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/user/clientprofile/?search=${this.profileId}`)
        .then(response => {
          let profile = response.data[0];
          this.client.body = profile.body;
          if (profile.avatar) {
            this.client.avatar = profile.avatar;
          }
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/comment/client/?search=${this.profileId}`)
        .then(response => {
          let comments = response.data;
          comments.forEach((comment) => {
            if(comment.commenter_avatar){
            }else{
              comment.commenter_avatar = require("../assets/blank-profile-picture.svg");
            }
            this.clientComments.push(comment);
          });
          //this.clientComments.description = comment.description;
          //this.clientComments.date = comment.created_at;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
      this.$axios
        .get(`/comment/freelancer/?search=${this.profileId}`)
        .then(response => {
          let comments = response.data;
          comments.forEach((comment) => {
            if(comment.commenter_avatar){
            }else{
              comment.commenter_avatar = require("../assets/blank-profile-picture.svg");
            }
            this.freelancerComments.push(comment);
          });
          //this.freelancerComments.description = comment.description;
          //this.freelancerComments.date = comment.created_at;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    submitCommentForClient(evt) {
      evt.preventDefault();
      this.$axios
        .post("/comment/client/", {
          description: this.commentForClient,
          profile_id: this.profileId
        })
        .then(response => {
          this.reloadDataAndResetForm();
        })
        .catch(err => {
          console.log(err);
        });
    },
    submitCommentForFreelancer(evt) {
      evt.preventDefault();
      this.$axios
        .post("/comment/freelancer/", {
          description: this.commentForFreelancer,
          profile_id: this.profileId
        })
        .then(response => {
          this.reloadDataAndResetForm();
        })
        .catch(err => {
          console.log(err);
        });
    },
    reloadDataAndResetForm() {
      this.commentForClient = "";
      this.commentForFreelancer = "";
      this.$refs.freelancerForm.reset();
      this.$refs.clientForm.reset();
      this.freelancerComments = [];
      this.clientComments = [];
      this.fetchData();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
