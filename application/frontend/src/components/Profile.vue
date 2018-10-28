<template>
  <div>
      <NavigationBar/>

      <b-container>
        <b-row>
          <b-col>
            <h2>My Profile</h2>
          </b-col >
          <b-col cols="auto">
            <b-button variant="primary" to="/profile-edit">Edit Profile</b-button>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" sm="2">
            <b-img :src="avatar" thumbnail fluid rounded alt="img" class="m-1" />
            <!-- width="150" height="150"  -->
          </b-col>
          <b-col cols="12" sm="7">
            <h4>{{name}}</h4>
            <p>{{body}}</p>
            <p>Rating: {{rating}}</p>
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
      </b-container>
      
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue'

export default {
  name: "Profile",
  components: {
    NavigationBar
  },
  data () {
    return {
      name: '',
      avatar: require('../assets/blank-profile-picture.svg'),
      body: '',
      rating: 0,
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData(){
      this.$axios
        .get("/user/profile/")
        .then(response => {
          let profiles = response.data.filter(profile => profile.user_id == this.$root.$data.user_id );
          if(profiles.length == 0){ // if user has not created a profile before
            this.$router.replace('/profile-edit');
          }
          let profileData = profiles[0];
          this.name = profileData.name;
          if(profileData.avatar){
            this.avatar = profileData.avatar;
          }
          this.body = profileData.body;
          this.rating = profileData.rating;
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
