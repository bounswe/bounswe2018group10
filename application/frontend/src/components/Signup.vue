<template>
  <div>
    <div class="text-center mt-4">
      <img src="../assets/logo.svg" width="70" height="70" alt="logo">
      <h2>HoneyBadgers</h2>
    </div>
    <b-form class="form-signin" @submit="onSubmit">
      <b-alert show 
               variant="danger" 
               v-for="(error, index) in form.errors"
               v-bind:key="index">{{ error }}</b-alert>
      <b-form-group label-for="exampleInput1">
        <template slot="label">
          <font-awesome-icon icon="envelope" fixed-width />
          Email address
        </template>
        <b-form-input id="exampleInput1"
                      type="email"
                      v-model="form.email"
                      required
                      placeholder="Enter email">
        </b-form-input>
      </b-form-group>
      <b-form-group label-for="exampleInput2">
        <template slot="label">
          <font-awesome-icon icon="user" fixed-width />
          Name
        </template>
        <b-form-input id="exampleInput2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-form-group label-for="exampleInput3">
        <template slot="label">
          <font-awesome-icon icon="lock" fixed-width />
          Password
        </template>
        <b-form-input id="exampleInput3"
                      type="password"
                      v-model="form.password"
                      required
                      placeholder="Enter password">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary" block>Sign Up</b-button>
    </b-form>
    <p class="text-center text-muted">Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
export default {
  name: "Signup",
  data() {
    return {
      form: {
        email: "",
        password: "",
        name: "",
        errors: [],
      }
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.$axios
        .post("/user/register/", {
          email: this.form.email,
          password: this.form.password,
          name: this.form.name
        })
        .then(response => {
          this.$root.$data.user_id = response.data.id;
          this.$axios
            .post("/user/login/", {
              username: this.form.email,
              password: this.form.password
            })
            .then(responseForLogin => {
              this.$axios.defaults.headers.common['Authorization'] = `Token ${responseForLogin.data.token}`;
              this.$router.push("/profile-edit");
            })
            .catch(err => {
              console.log(err);
            });
        })
        .catch(error => {
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            for(let key in error.response.data){
              if(error.response.data[key].constructor === Array){
                error.response.data[key].forEach((errorString) => {
                  this.form.errors.push(errorString);
                });
              }
            }
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            console.log(error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            console.log("Error", error.message);
          }
          console.log(error.config);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
</style>
