<template>
  <div class="bg-grey">
    <NavigationBar/>

    <b-container>
      <b-row>
        <b-col>
          <h2>My Text Annotations</h2>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col>
          <b-card no-body class="border-0 shadow">
            <b-list-group flush>
              <b-list-group-item :key="anno.id" v-for="anno in textAnnotations">
                <div><strong>Annotation:</strong></div>
                <!-- ql-snow and ql-editor is necessary for quill editor styling -->
                <div class="unique2 ql-snow" :style="{'max-height':'60vh','overflow-y':'auto'}">
                  <div class="ql-editor" v-html="anno.body.value"></div>
                </div>
                <router-link :to="removeBaseUrl(anno.target.source)">Go to annotated page</router-link>
              </b-list-group-item>
            </b-list-group>
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
  name: "MyTextAnnotations",
  components: {
    NavigationBar,
    MyFooter
  },
  data() {
    return {
      textAnnotations: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios
        .get(`/annotation/textannotation/?user__id=${this.$root.$data.user_id}`)
        .then(response => {
          this.textAnnotations = response.data;
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    removeBaseUrl(url) {
      /*
       * Replace base URL in given string, if it exists, and return the result.
       *
       * e.g. "http://localhost:8000/api/v1/blah/" becomes "/api/v1/blah/"
       *      "/api/v1/blah/" stays "/api/v1/blah/"
       */
      let baseUrlPattern = /^https?:\/\/[a-z:0-9.]+/;
      let result = "";

      let match = baseUrlPattern.exec(url);
      if (match != null) {
        result = match[0];
      }

      if (result.length > 0) {
        url = url.replace(result, "");
      }

      return url;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
