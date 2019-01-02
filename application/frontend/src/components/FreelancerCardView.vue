<template>
  <b-row>
    <b-col
      class="mb-4"
      cols="12"
      sm="6"
      md="4"
      lg="3"
      :key="freelancer.id"
      v-for="freelancer in freelancers"
    >
      <b-card no-body class="border-0 shadow" :title="``">
        <b-card-img v-if="freelancer.avatar" :src="freelancer.avatar"></b-card-img>
        <b-card-img v-if="!freelancer.avatar" :src="blankAvatar"></b-card-img>
        <b-card-body>
          <div class="card-text mb-1">{{freelancer.body}}</div>
          <div class="mb-1">
            <b-badge
              class="mr-1"
              variant="dark"
              :to="`/search/${tags[tagId-1].title}`"
              :key="tagId"
              v-for="tagId in freelancer.tags"
            >{{tags[tagId-1].title}}</b-badge>
          </div>
          <b-button block variant="primary" :to="`/profile/${freelancer.id}`">Go to Profile</b-button>
        </b-card-body>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "FreelancerCardView",
  props: ["freelancers", "tags", "blankAvatar"]
};
</script>