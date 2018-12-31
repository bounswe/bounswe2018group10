<template>
  <div>
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>Deposit Money</h2>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <b-form @submit="deposit">
            <b-form-row>
              <b-col>
                <b-form-group label-for="inputAmount">
                  <template slot="label">
                    <font-awesome-icon icon="money-bill" fixed-width />
                    Amount
                  </template>
                  <b-form-input id="inputAmount"
                                type="number"
                                v-model="form.amount"
                                min="0"
                                required
                                placeholder="Amount">
                  </b-form-input>
                </b-form-group> 
              </b-col>
            </b-form-row>
            <!--<b-form-row>
              <b-col>
                <b-form-group label-for="inputAmount">
                  <template slot="label">
                    <font-awesome-icon icon="money-bill" fixed-width />
                    Credit Card Number
                  </template>
                  <b-form-input id="inputAmount"
                                type="text"
                                v-model="form.creditCardNumber"
                                required
                                placeholder="Credit Card Number">
                  </b-form-input>
                </b-form-group> 
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-col>
                <b-form-group label-for="inputAmount">
                  <template slot="label">
                    <font-awesome-icon icon="money-bill" fixed-width />
                    Expiration Date
                  </template>
                  <b-form-input id="inputAmount"
                                type="text"
                                v-model="form.expirationDate"
                                required
                                placeholder="MM / YY">
                  </b-form-input>
                </b-form-group> 
              </b-col>
              <b-col>
                <b-form-group label-for="inputAmount">
                  <template slot="label">
                    <font-awesome-icon icon="money-bill" fixed-width />
                    CVV
                  </template>
                  <b-form-input id="inputAmount"
                                type="text"
                                v-model="form.cvv"
                                required
                                placeholder="CVV">
                  </b-form-input>
                </b-form-group> 
              </b-col>
            </b-form-row>-->

            <b-button type="submit" variant="primary" block>
              Deposit
            </b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  name: "Deposit",
  components: {
    NavigationBar
  },
  data() {
    return {
      wallet: null,
      form: {
        amount: null,
        creditCardNumber: null,
        expirationDate: null,
        cvv: null
      }
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
          this.wallet = response.data[0];
        })
        .catch(err => {
          console.log(err);
        });
    },
    deposit(evt) {
      evt.preventDefault();
      this.$axios
        .put(`/payment/wallet/${this.wallet.id}/`, {
          budget: Number(this.form.amount) + Number(this.wallet.budget)
        })
        .then(response => {
          this.$router.push("/settings");
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
