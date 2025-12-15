<template>
  <v-list-item v-if="!hasChild" :title="item?.title ? $t(item.title) : ''" :prepend-icon="item?.icon ? item.icon : ''"
    @click="openRoute(item?.url ? item.url : '')"></v-list-item>
  <exp-group class="expMenu-Group" v-else :item="item" />
</template>

<script setup lang="ts">
import { computed } from "vue";

import { useRouter } from "vue-router";
import expGroup from "./expGroup.vue";

const router = useRouter();

const props = defineProps({
  item: {
    type: Object,
    default: () => ({})
  }
});

const hasChild = computed({
  get() {
    return props.item?.children?.length > 0 ? true : false;
  },
  set(value) {
    return value;
  }
});

const openRoute = (url: string) => {
  router.push(url);
}
</script>

<style lang="scss">
.expMenu-Group .v-list-group__items .v-list-item {
  padding-inline-start: calc(16px + var(--indent-padding)/5) !important;
}
</style>