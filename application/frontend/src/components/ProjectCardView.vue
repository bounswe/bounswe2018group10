<template>
  <b-row>
    <b-col
      class="mb-4"
      cols="12"
      sm="6"
      md="4"
      lg="3"
      :key="project.id"
      v-for="project in projects"
    >
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
        <b-button block v-if="!accepted" variant="primary" :to="`/project/${project.id}`">Go to project</b-button>
        <div slot="footer">
          <small
            class="text-muted"
            v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
          >Deadline {{project.deadline | moment("from")}}</small>
        </div>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "ProjectCardView",
  props: ["projects", "accepted", "tags"]
};
</script>