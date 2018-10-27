<template>
  <div>
      <b-navbar toggleable="md" type="light" variant="light">

        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

        <b-navbar-brand href="#">
          <img src="../assets/logo.svg" width="30" height="30" class="d-inline-block align-top" alt="logo">
          HoneyBadgers
        </b-navbar-brand>

        <b-collapse is-nav id="nav_collapse">

          <!--<b-navbar-nav>
            <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#">Link 2</b-nav-item>
          </b-navbar-nav>-->

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-button class="mr-2" variant="outline-primary" to="/signup">Sign Up</b-button>
            <b-button variant="outline-primary" to="/login">Login</b-button>
          </b-navbar-nav>

        </b-collapse>
      </b-navbar>

      <b-jumbotron header="Hire the best freelancers" 
                   header-level="4" 
                   lead="We bring together clients and freelancers and make it easy to do business.">
        <!--<p>For more information visit website</p>-->
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
