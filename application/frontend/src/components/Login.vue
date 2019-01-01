<template>
  <div class="my-gradient py-4">
    <b-card class="bg-light-grey narrow-card border-0 shadow">
      <div class="text-center my-4">
        <img src="../assets/logo.svg" width="70" height="70" alt="logo">
        <h2>HoneyBadgers</h2>
      </div>
      <b-form @submit="onSubmit"> 
        <b-alert show 
                variant="danger" 
                v-for="(error, index) in form.non_field_errors"
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
            <font-awesome-icon icon="lock" fixed-width />
            Password
          </template>
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
      <p class="text-center text-muted mt-2">Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
    </b-card>
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
    onSubmit(evt) {
      evt.preventDefault();
      this.$axios
        .post("/user/login/", {
          username: this.form.email,
          password: this.form.password
        })
        .then(response => {
          this.$axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
          sessionStorage.setItem('token',`Token ${response.data.token}`);
          this.$axios
            .get("/user/register/", {
              params: {
                search: this.form.email
              }
            })
            .then(responseForUserID => {
              this.$root.$data.user_id = responseForUserID.data[0].id;
              sessionStorage.setItem('user_id',responseForUserID.data[0].id);
              this.$router.push("/dashboard");
            })
            .catch(err => {
              // eslint-disable-next-line
              console.log(err);
            });
        })
        .catch(error => {
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            if (error.response.data["non_field_errors"]) {
              this.form.non_field_errors =
                error.response.data["non_field_errors"];
            }
            // eslint-disable-next-line
            console.log(error.response.data);
            // eslint-disable-next-line
            console.log(error.response.status);
            // eslint-disable-next-line
            console.log(error.response.headers);
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            // eslint-disable-next-line
            console.log(error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            // eslint-disable-next-line
            console.log("Error", error.message);
          }
          // eslint-disable-next-line
          console.log(error.config);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/*.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}*/
.narrow-card {
  max-width: 330px;
  margin: auto;
}
.bg-light-grey {
  background-color: #f7f7f7;
}
.my-gradient {
  background-image: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
  min-height: 100vh;
}
</style>
