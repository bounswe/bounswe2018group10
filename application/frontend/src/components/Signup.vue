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
      <b-form-group label="Name:"
                    label-for="exampleInput2">
        <b-form-input id="exampleInput2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-form-group label="Password:"
                    label-for="exampleInput3">
        <b-form-input id="exampleInput3"
                      type="password"
                      v-model="form.password"
                      required
                      placeholder="Enter password">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary" block>Sign Up</b-button>
    </b-form>
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
        name: ""
      }
    };
  },
  methods: {
    onSubmit() {
      this.$axios
        .post("/user/register/", {
          email: this.form.email,
          password: this.form.password,
          name: this.form.name
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
