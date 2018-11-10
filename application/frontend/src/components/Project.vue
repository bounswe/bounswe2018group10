<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row class="mb-2">
        <b-col>
          <h2 class="mb-0">{{project.title}}</h2>
        </b-col>
        <b-col cols="auto" class="ml-auto">
          <b-button v-b-toggle.collapse1 variant="primary">Bid for Project</b-button>
        </b-col>
      </b-row>

      <b-collapse id="collapse1">
        <b-row class="mb-4">
          <b-col>
            <b-card>
              <b-form>
                <b-form-row>
                  <b-col cols="12" md="6">
                    <b-form-group label="Bid Amount"
                                  label-for="inputBid"
                                  description="Your bid should be within the budget range.">
                      <b-form-input id="inputBid"
                                    type="number"
                                    v-model="bidForm.amount"
                                    :min="project.budget_min"
                                    :max="project.budget_max"
                                    required>
                      </b-form-input>
                    </b-form-group>
                  </b-col>
                  <b-col cols="12" md="6">
                    <b-form-group label="Deliver In"
                                  label-for="inputDeliver">
                      <b-input-group append="Days">
                        <b-form-input id="inputDeliver"
                                      type="number"
                                      v-model="bidForm.deliverIn"
                                      min="1"
                                      required>
                        </b-form-input>
                      </b-input-group>
                    </b-form-group>
                  </b-col>
                </b-form-row>

                <h6><strong>Milestones</strong></h6>

                <b-form-row :key="index" v-for="(milestone,index) in bidForm.milestones">
                  <b-col cols="12" md="6">
                    <b-form-group :label="`Milestone ${index+1} Name`"
                                  label-for="inputMilestone">
                      <b-form-input id="inputMilestone"
                                    type="text"
                                    maxlength="200"
                                    v-model="milestone.name"
                                    required>
                      </b-form-input>
                    </b-form-group>
                  </b-col>
                  <b-col cols="12" md="6">
                    <b-form-group :label="`Milestone ${index+1} Amount`"
                                  label-for="inputMileBud">
                      <b-form-input id="inputMileBud"
                                    type="number"
                                    v-model="milestone.amount"
                                    min="1"
                                    required>
                      </b-form-input>
                    </b-form-group>
                  </b-col>
                </b-form-row>

                <b-form-row class="mb-2">
                  <b-col>
                    <b-button class="mr-1" @click="addMilestone" variant="primary" size="sm">Add a Milestone</b-button>
                    <b-button @click="removeMilestone" variant="primary" size="sm">Remove a Milestone</b-button>
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
          <b-card>
              <b-row>
                <b-col>
                  <strong>Budget</strong>
                  <div>
                    {{project.budget_min}} - {{project.budget_max}}
                  </div>
                </b-col>
                <b-col>
                </b-col>
                <b-col>
                  <strong>Deadline</strong>
                  <div>
                    {{deadline}}
                  </div>
                </b-col>
              </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card title="Project Description">
              <p class="card-text">{{project.description}}</p>
              <div>Category: <router-link :to="`/search/${projectCategory.title}`">{{projectCategory.title}}</router-link></div>
              <div>
                <span>Tags: </span>
                <b-badge class="mr-1" 
                         variant="primary"
                         :to="`/search/${tag.title}`" 
                         :key="tag.id" 
                         v-for="tag in projectTags">{{tag.title}}</b-badge>
              </div>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-list-group>
            <b-list-group-item>
              <b-row>
                <b-col>
                  <strong>Freelancer</strong>
                </b-col>
                <b-col>
                  <strong>Rating</strong>
                </b-col>
                <b-col>
                  <strong>Bid</strong>
                </b-col>
              </b-row>
            </b-list-group-item>
            <b-list-group-item :key="index" v-for="(bidder,index) in bidders">
              <b-row>
                <b-col class="clearfix">
                  <b-img left 
                         :src="bidder.picture" 
                         fluid 
                         rounded 
                         width="96" 
                         class="m-1"/>
                  {{bidder.name}}
                </b-col>
                <b-col>
                  {{bidder.rating}}
                </b-col>
                <b-col>
                  {{bidder.bid}}
                </b-col>
              </b-row>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-list-group>
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
      bidders: [
        {
          name: "John",
          picture: "https://randomuser.me/api/portraits/men/44.jpg",
          bid: 100,
          rating: 4.5
        },
        {
          name: "Johnny",
          picture: "https://randomuser.me/api/portraits/men/18.jpg",
          bid: 200,
          rating: 4.5
        }
      ],
      comments: [
        {
          name: "John",
          picture: "https://randomuser.me/api/portraits/men/44.jpg",
          text: "Sounds like a good project !!",
          date: "2018-11-1"
        },
      ],
      newCommentText: "",
      bidForm: {
        amount: null,
        deliverIn: null,
        milestones: [
          {
            name: "",
            amount: null,
          }
        ],
      },
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
          this.deadline = this.project.deadline.replace(/[TZ]/g, " ");
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
    },
    addMilestone() {
      this.bidForm.milestones.push({name:"",amount: null});
    },
    removeMilestone() {
      if(this.bidForm.milestones.length > 1){
        this.bidForm.milestones.pop();
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
