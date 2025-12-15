<template>
  <v-list-group>
    <template v-slot:activator="{ props }">
      <v-list-item v-bind="props" :title="item?.title ? $t(item?.title) : ''"
        :prepend-icon="item?.icon ? item.icon : ''"></v-list-item>
    </template>
    <exp-item v-for="(child, index) in getChildren(item.children)" :key="index" :item="child" />
  </v-list-group>
</template>

<script setup lang="ts">
import { computed } from "vue";
import useAuth from "@/modules/auth/composables/useAuth";
import expItem from "./expItem.vue";

const uAuth = useAuth();

const props = defineProps({
  item: {
    type: Object,
    default: () => ({})
  }
});

const userData = uAuth.getUserData();
const getChildren = (children: any) => {
  if (children == null)
    return [];

  let _itemsFiltered: any = []
  children.forEach((itm: any) => {
    if ('roles' in itm) {
      if ((itm.roles as Array<number>).includes(userData.role)) {
        _itemsFiltered.push(itm)
      }
    } else {
      _itemsFiltered.push(itm)
    }
  });
  return _itemsFiltered;
}
</script>