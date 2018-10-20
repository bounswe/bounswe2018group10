<template>
  <div>
    <div class="text-center">
      <h1>HoneyBadgers</h1>
    </div>
     <b-form class="form-signin" @submit="onSubmit">
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
        checked: []
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
          alert(JSON.stringify(response.data));
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
.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
</style>
