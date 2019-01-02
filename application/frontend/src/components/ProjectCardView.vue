<template>
  <b-row>
    <b-col class="mb-4">
      <swiper class="pl-4 pr-4 pb-4 pt-2">
        <swiper-slide v-for="project in projects" :key="project.id">
          <b-card class="border-0 shadow" :title="project.title">
            <div class="card-text mb-1">{{project.description | striphtml | shortDescription}}</div>
            <div v-if="!accepted" class="mb-1">
              <b-badge
                class="mr-1"
                variant="dark"
                :to="`/search/${tags[tagId-1].title}`"
                :key="tagId"
                v-for="tagId in project.tags"
              >{{tags[tagId-1].title}}</b-badge>
            </div>
            <div class="text-success mr-4 mb-1">
              <font-awesome-icon icon="money-bill" fixed-width/>
              {{project.price || `${project.budget_min}-${project.budget_max}`}}
            </div>
            <b-button
              block
              v-if="accepted"
              variant="primary"
              :to="`/accepted-project/${project.id}`"
            >Go to project</b-button>
            <b-button
              block
              v-if="!accepted"
              variant="primary"
              :to="`/project/${project.id}`"
            >Go to project</b-button>
            <div slot="footer">
              <small
                class="text-muted"
                v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
              >Deadline {{project.deadline | moment("from")}}</small>
            </div>
          </b-card>
        </swiper-slide>
        <div class="swiper-pagination" slot="pagination"></div>
        <div class="swiper-button-prev" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
      </swiper>

      <!--<b-card class="border-0 shadow" :title="project.title">
        <div class="card-text mb-1">{{project.description | striphtml | shortDescription}}</div>
        <div v-if="!accepted" class="mb-1">
          <b-badge
            class="mr-1"
            variant="dark"
            :to="`/search/${tags[tagId-1].title}`"
            :key="tagId"
            v-for="tagId in project.tags"
          >{{tags[tagId-1].title}}</b-badge>
        </div>
        <div class="text-success mr-4 mb-1">
          <font-awesome-icon icon="money-bill" fixed-width/>
          {{project.price || `${project.budget_min}-${project.budget_max}`}}
        </div>
        <b-button
          block
          v-if="accepted"
          variant="primary"
          :to="`/accepted-project/${project.id}`"
        >Go to project</b-button>
        <b-button block v-if="!accepted" variant="primary" :to="`/project/${project.id}`">Go to project</b-button>
        <div slot="footer">
          <small
            class="text-muted"
            v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
          >Deadline {{project.deadline | moment("from")}}</small>
        </div>
      </b-card>-->
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "ProjectCardView",
  props: ["projects", "accepted", "tags"]
};
</script>