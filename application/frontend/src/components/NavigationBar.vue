<template>
  <b-navbar class="mb-3 border-bottom shadow-sm" toggleable="md" type="light" variant="light">

  <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

  <b-navbar-brand to="/">
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

        <!--<b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
          <b-button size="sm" class="my-2 my-sm-0 mr-sm-3" type="submit">Search</b-button>
        </b-nav-form>

        <b-nav-form>
            <b-form-radio-group buttons
                                button-variant="outline-primary"
                                size="sm"
                                v-model="selected"
                                :options="options"
                                name="radioBtnOutline" />
        </b-nav-form>-->

        <b-nav-item-dropdown right>
            <template slot="text">
            Settings
            </template>
            <b-dropdown-item to="/profile">Profile</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item @click="logout">Log out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: "NavigationBar",
  data () {
    return {
      selected: this.$root.$data.role,
      options: [
        { text: 'Client', value: 'client' },
        { text: 'Freelancer', value: 'freelancer' }
      ]
    }
  },
  watch: {
    selected: function (newSelected, oldSelected) {
      this.$root.$data.role = newSelected;
      localStorage.setItem('role',newSelected);
    }
  },
  methods: {
    logout(){
      delete this.$axios.defaults.headers.common["Authorization"];
      this.$router.push('/');
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
