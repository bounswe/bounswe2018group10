<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>My Wallet</h2>
        </b-col>
      </b-row>

      <b-row class="mb-2">
        <b-col><h5><strong class="mr-1">Balance:</strong>{{balance}}</h5></b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-button variant="primary" to="/deposit">Deposit Money</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "Wallet",
  components: {
    NavigationBar
  },
  data() {
    return {
      balance: null,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/payment/wallet/?search=${this.$root.$data.user_id}`)
        .then(response => {
          this.balance = response.data[0].budget;
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
</style>
