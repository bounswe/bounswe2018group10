<template>
  <div>
    <NavigationBar/>

    <b-container>
      <h2>Edit Profile</h2>
      <b-form @submit="onSubmit">
        <b-form-row>
          <b-col cols="12" md="6">
            <div>Current Profile Picture</div>
            <b-img :src="avatar" rounded width="160" blank-color="#777" alt="img" class="m-1" />
            <b-form-group label="New Profile Picture"
                          label-for="inputAvatar">
              <b-form-file id="inputAvatar"
                            accept="image/*"
                            v-model="form.file" 
                            placeholder="Choose an image file...">
              </b-form-file>
            </b-form-group>    
          </b-col>
          <b-col cols="12" md="6">
            <b-form-group label="Name"
                          label-for="inputName">
              <b-form-input id="inputName"
                            type="text"
                            maxlength="255"
                            v-model="form.name"
                            placeholder="Enter name"
                            required>
              </b-form-input>
            </b-form-group>
            <b-form-group label="Profile Body"
                          label-for="inputBody">
              <b-form-textarea id="inputBody"
                        v-model="form.body"
                        placeholder="Tell us about yourself"
                        :rows="4"
                        :max-rows="8"
                        required>
              </b-form-textarea>
            </b-form-group>
          </b-col>
        </b-form-row>
        
        
        <b-button type="submit" variant="primary" block>Save changes</b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "ProfileEdit",
  components: {
    NavigationBar
  },
  data() {
    return {
      avatar: require("../assets/blank-profile-picture.svg"),
      form: {
        name: "",
        file: null,
        body: ""
      },
      profileId: null,
      firstProfile: false // if it is true the user does not have a profile, we should create a new one
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get("/user/profile/")
        .then(response => {
          let profiles = response.data.filter(
            profile => profile.user_id == this.$root.$data.user_id
          );
          if (profiles.length != 0) {
            let profileData = profiles[0];
            this.profileId = profileData.id;
            this.form.name = profileData.name;
            if (profileData.avatar) {
              this.avatar = profileData.avatar;
            }
            this.form.body = profileData.body;
          } else {
            this.firstProfile = true;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      let formData = new FormData();
      formData.append("name", this.form.name);
      formData.append("body", this.form.body);
      if (this.form.file) {
        formData.append("avatar", this.form.file, this.form.file.name);
      }

      let method;
      let url;
      if (this.firstProfile) {
        method = "post";
        url = "/user/profile/";
      } else {
        method = "patch";
        url = `/user/profile/${this.profileId}/`;
      }

      this.$axios({
        method: method,
        url: url,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          this.$router.push("/profile");
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
