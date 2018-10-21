<template>
  <div>
    <div class="text-center mt-4">
      <img src="../assets/logo.svg" width="70" height="70" alt="logo">
      <h2>HoneyBadgers</h2>
    </div>
     <b-form class="form-signin" @submit="onSubmit"> 
      <b-alert show 
               variant="danger" 
               v-for="(error, index) in form.non_field_errors"
               v-bind:key="index">{{ error }}</b-alert>
      <b-form-group label="Email address:"
                    label-for="exampleInput1">
        <b-form-input id="exampleInput1"
                      type="email"
                      v-model="form.email"
                      required
                      placeholder="Enter email">
        </b-form-input>
      </b-form-group>
      <b-form-group label="Password:"
                    label-for="exampleInput2">
        <b-form-input id="exampleInput2"
                      type="password"
                      v-model="form.password"
                      required
                      placeholder="Enter password">
        </b-form-input>
      </b-form-group>
      <!--<b-form-group>
        <b-form-checkbox-group v-model="form.checked" id="exampleChecks">
          <b-form-checkbox value="remember">Remember me</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>-->
      <b-button type="submit" variant="primary" block>Login</b-button>
    </b-form>
    <p class="text-center text-muted">Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      form: {
        email: "",
        password: "",
        checked: [],
        non_field_errors: []
      }
    };
  },
  methods: {
    onSubmit() {
      this.$axios
        .post("/user/login/", {
          username: this.form.email,
          password: this.form.password
        })
        .then(response => {
          localStorage.setItem("token", response.data.token);
          this.$root.$data.token = response.data.token;
          this.$router.push("/dashboard");
          //alert(JSON.stringify(response.data));
        })
        .catch(error => {
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            if (error.response.data["non_field_errors"]) {
              this.form.non_field_errors =
                error.response.data["non_field_errors"];
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
