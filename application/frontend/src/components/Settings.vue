<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>Settings</h2>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card title="My Wallet" class="border-0 shadow">
            <b-row class="mb-2">
              <b-col>
                <h6>
                  <strong class="mr-1">Balance:</strong>
                  {{balance}}
                </h6>
              </b-col>
            </b-row>

            <b-row>
              <b-col>
                <b-button variant="primary" to="/deposit">Deposit Money</b-button>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card title="Annotations" class="border-0 shadow">
            <b-row class="mb-2">
              <b-col>
                <b-form inline>
                  <label class="mr-sm-2" for="radioBtnOutline">Annotations</label>
                  <b-form-radio-group
                    buttons
                    button-variant="outline-primary"
                    size="sm"
                    v-model="annoSetting"
                    :options="annoOptions"
                    name="radioBtnOutline"
                  />
                </b-form>
              </b-col>
            </b-row>

            <b-row>
              <b-col>
                <router-link to="/my-text-annotations">My Text Annotations</router-link>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <router-link to="/my-image-annotations">My Image Annotations</router-link>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>
      <MyFooter/>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";
import MyFooter from "./MyFooter.vue";

export default {
  name: "Settings",
  components: {
    NavigationBar,
    MyFooter
  },
  data() {
    return {
      balance: null,
      annoSetting: this.$root.$data.annoSetting,
      annoOptions: [
        { text: "Hide", value: "hide" },
        { text: "Show", value: "show" }
      ]
    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    annoSetting: function(newSet, oldSet) {
      this.$root.$data.annoSetting = newSet;
      sessionStorage.setItem("annoSetting", newSet);
    }
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/payment/wallet/?search=${this.$root.$data.user_id}`)
        .then(response => {
          this.balance = response.data[0].budget;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
