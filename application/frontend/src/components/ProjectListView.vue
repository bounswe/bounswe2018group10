<template>
  <b-list-group class="border-0 shadow">
    <b-list-group-item :key="project.id" v-for="project in projects">
      <router-link v-if="!accepted" :to="`/project/${project.id}`">{{project.title}}</router-link>
      <router-link v-if="accepted" :to="`/accepted-project/${project.id}`">{{project.title}}</router-link>
      <div>{{project.description | striphtml | shortDescription}}</div>
      <span v-if="!accepted" class="mb-1 mr-3">
        <b-badge
          class="mr-1"
          variant="dark"
          :to="`/search/${tags[tagId-1].title}`"
          :key="tagId"
          v-for="tagId in project.tags"
        >{{tags[tagId-1].title}}</b-badge>
      </span>
      <span class="text-success mr-4">
        <font-awesome-icon icon="money-bill" fixed-width/>
        {{project.price || `${project.budget_min}-${project.budget_max}`}}
      </span>
      <small
        class="text-muted"
        v-b-tooltip.hover.bottom="$moment(project.deadline).format('LLLL')"
      >Deadline {{project.deadline | moment("from")}}</small>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
export default {
  name: "ProjectListView",
  props: ["projects", "accepted", "tags"]
};
</script>
