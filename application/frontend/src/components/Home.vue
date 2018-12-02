<template>
  <div>
    <b-navbar toggleable="md" type="light" variant="light">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="#">
        <img
          src="../assets/logo.svg"
          width="30"
          height="30"
          class="d-inline-block align-top"
          alt="logo"
        >
        HoneyBadgers
      </b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">
        <!--<b-navbar-nav>
            <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#">Link 2</b-nav-item>
        </b-navbar-nav>-->
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-button class="mb-1 mb-md-0 mr-md-2" variant="outline-primary" to="/signup">Sign Up</b-button>
          <b-button variant="outline-primary" to="/login">Login</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-jumbotron
      fluid
      header="Hire the best freelancers"
      header-level="4"
      lead="We bring together clients and freelancers and make it easy to do business."
    >
      <!--<p>For more information visit website</p>-->
      <b-btn class="mr-2" variant="primary" to="/signup">Create a project</b-btn>
      <b-btn variant="primary" to="/signup">Start working</b-btn>
    </b-jumbotron>

    <b-container fluid>
      <b-row class="text-center my-5">
        <b-col>
          <font-awesome-icon icon="users" size="3x" class="text-info"/>
          <h3>Flexible</h3>
          <p class="mb-1">Choose among various freelancers with different skills</p>
          <p class="mb-1">Compare the prior work of freelancers</p>
          <p>Read others client's comments about the freelancers</p>
        </b-col>
        <b-col>
          <font-awesome-icon icon="handshake" size="3x" class="text-success"/>
          <h3>Trustworthy</h3>
          <p class="mb-1">Monitor the progress of your project</p>
          <p>Pay after each milestone not before</p>
        </b-col>
        <b-col>
          <font-awesome-icon icon="bolt" size="3x" class="text-warning"/>
          <h3>Fast</h3>
          <p class="mb-1">Save time and money</p>
          <p>Reach a wide range of freelancers with one click</p>
        </b-col>
      </b-row>

      <b-row class="text-center bg-dark text-white my-5">
        <b-col>
          <b-row class="mt-5 mb-3">
            <b-col>
              <h2>How it works</h2>
            </b-col>
          </b-row>

          <b-row class="mb-5">
            <b-col>
              <h4>1. Post Your Project</h4>
              <font-awesome-icon icon="file-import" size="2x"/>
            </b-col>
            <b-col>
              <h4>2. Wait For Bids</h4>
              <font-awesome-icon icon="clock" size="2x"/>
            </b-col>
            <b-col>
              <h4>3. Choose a Bid</h4>
              <font-awesome-icon icon="list-ul" size="2x"/>
            </b-col>
            <b-col>
              <h4>4. Monitor Progress</h4>
              <font-awesome-icon icon="file-medical-alt" size="2x"/>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>

    <b-jumbotron fluid class="my-gradient text-white" header="Start Now">
      <b-btn variant="light" to="/signup" size="lg">Create a project</b-btn>
    </b-jumbotron>

    <footer class="text-center mb-4">
      Build by team
      <b-link
        href="https://github.com/bounswe/bounswe2018group10"
        target="_blank"
        rel="noopener noreferrer"
      >HoneyBadgers</b-link>
    </footer>
  </div>
</template>

<script>
export default {
  name: "Home",
  beforeMount() {
    if (this.$axios.defaults.headers.common["Authorization"] != null) {
      this.$router.replace("/dashboard");
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.my-gradient {
  background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
