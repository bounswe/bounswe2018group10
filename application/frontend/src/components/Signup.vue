<template>
  <div class="my-gradient py-4">
    <b-card class="bg-light-grey narrow-card border-0 shadow">
      <div class="text-center my-4">
        <img src="../assets/logo.svg" width="70" height="70" alt="logo">
        <h2>HoneyBadgers</h2>
      </div>
      <b-form @submit="onSubmit">
        <b-alert
          show
          variant="danger"
          v-for="(error, index) in form.errors"
          v-bind:key="index"
        >{{ error }}</b-alert>
        <b-form-group label-for="exampleInput1">
          <template slot="label">
            <font-awesome-icon icon="envelope" fixed-width/>Email address
          </template>
          <b-form-input
            id="exampleInput1"
            type="email"
            v-model="form.email"
            required
            placeholder="Enter email"
          ></b-form-input>
        </b-form-group>
        <b-form-group label-for="exampleInput2">
          <template slot="label">
            <font-awesome-icon icon="user" fixed-width/>Name
          </template>
          <b-form-input
            id="exampleInput2"
            type="text"
            v-model="form.name"
            required
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>
        <b-form-group label-for="exampleInput4">
          <template slot="label">
            <font-awesome-icon icon="user" fixed-width/>Username
          </template>
          <b-form-input
            id="exampleInput4"
            type="text"
            v-model="form.username"
            required
            placeholder="Enter username"
          ></b-form-input>
        </b-form-group>
        <b-form-group label-for="exampleInput3">
          <template slot="label">
            <font-awesome-icon icon="lock" fixed-width/>Password
          </template>
          <b-form-input
            id="exampleInput3"
            type="password"
            v-model="form.password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-group description="You will be able to change your role later.">
          <template slot="label">
            <font-awesome-icon icon="user-cog" fixed-width/>Role
          </template>
          <b-form-radio-group v-model="form.selectedRole" name="radioSubComponent" required>
            <b-form-radio value="freelancer">Freelancer</b-form-radio>
            <b-form-radio value="client">Client</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
        <b-button type="submit" variant="primary" block>Sign Up</b-button>
      </b-form>
      <p class="text-center text-muted mt-2">Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </b-card>
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
        username: "",
        selectedRole: "freelancer",
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
          name: this.form.name,
          username: this.form.username,
          role: this.form.selectedRole=="freelancer" ? 0 : 1
        })
        .then(response => {
          this.$root.$data.role = this.form.selectedRole;
          sessionStorage.setItem("role", this.form.selectedRole);
          this.$root.$data.user_id = response.data.id;
          sessionStorage.setItem("user_id", response.data.id);
          this.$axios
            .post("/user/login/", {
              username: this.form.email,
              password: this.form.password
            })
            .then(responseForLogin => {
              this.$axios.defaults.headers.common["Authorization"] = `Token ${
                responseForLogin.data.token
              }`;
              sessionStorage.setItem(
                "token",
                `Token ${responseForLogin.data.token}`
              );
              this.$router.push("/profile-edit");
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
            for (let key in error.response.data) {
              if (error.response.data[key].constructor === Array) {
                error.response.data[key].forEach(errorString => {
                  this.form.errors.push(errorString);
                });
              }
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
