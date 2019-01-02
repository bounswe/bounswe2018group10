<template>
  <b-row>
    <b-col class="mb-4">
      <swiper class="pl-4 pr-4 pb-4 pt-2">
        <swiper-slide :key="freelancer.id" v-for="freelancer in freelancers">
          <b-card no-body class="border-0 shadow" :title="''">
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
        </swiper-slide>
        <div class="swiper-pagination" slot="pagination"></div>
        <div class="swiper-button-prev" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
      </swiper>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "FreelancerCardView",
  props: ["freelancers", "tags", "blankAvatar"]
};
</script>