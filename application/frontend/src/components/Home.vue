<template>
  <div>
      <b-navbar toggleable="md" type="light" variant="light">

        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

        <b-navbar-brand href="#">
          <img src="../assets/logo.svg" width="30" height="30" class="d-inline-block align-top" alt="logo">
          HoneyBadgers
        </b-navbar-brand>

        <b-collapse is-nav id="nav_collapse">

          <b-navbar-nav>
            <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#">Link 2</b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">

            <b-nav-form>
              <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
              <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>

            <b-nav-item-dropdown text="Lang" right>
              <b-dropdown-item href="#">EN</b-dropdown-item>
              <b-dropdown-item href="#">ES</b-dropdown-item>
              <b-dropdown-item href="#">RU</b-dropdown-item>
              <b-dropdown-item href="#">FA</b-dropdown-item>
            </b-nav-item-dropdown>

            <b-button class="mr-2" variant="outline-primary" to="/signup">Sign Up</b-button>
            <b-button variant="outline-primary" to="/login">Login</b-button>
          </b-navbar-nav>

        </b-collapse>
      </b-navbar>

      <b-jumbotron header="Hire the best freelancers" header-level="4" lead="Some slogan some slogan some slogan">
        <p>For more information visit website</p>
        <b-btn class="mr-2" variant="primary" to="/signup">Create a project</b-btn>
        <b-btn variant="primary" to="/signup">Start working</b-btn>
      </b-jumbotron>
      
  </div>
</template>

<script>
export default {
  name: "Home",
  beforeMount(){
    if(this.$axios.defaults.headers.common["Authorization"] != null){
      this.$router.replace('/dashboard')
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
