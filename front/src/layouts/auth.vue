<template>
  <v-app>
    <v-main v-show="!isAuthenticated">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed, watch, onMounted } from "vue";

import { useRouter } from "vue-router";
import useAuth from "@/modules/auth/composables/useAuth";
import useGlobalState from "@/stores/global";

const sGlobalState = useGlobalState();
const router = useRouter();
const auth = useAuth();

const isAuthenticated = computed(() => {
  if (auth.isAuthenticated() && sGlobalState.value.auth) {
    return true;
  } else {
    sGlobalState.value.auth = false;
    return false;
  }
});

watch(isAuthenticated, (currentValue) => {
  if (currentValue)
    router.push({ name: "core-index" });
});

onMounted(async () => {
  if (isAuthenticated.value)
    router.push({ name: "core-index" });
});
</script>