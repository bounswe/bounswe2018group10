import Vue from 'vue';

// used this to make this functions global
Vue.mixin({
  computed: {
    isClient: function () {
      return this.$root.$data.role == 'client';
    },
    isFreelancer: function () {
      return this.$root.$data.role == 'freelancer';
    }
  }
});