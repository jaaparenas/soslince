<template>
  <RouterView />
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import useAuth from "@/modules/auth/composables/useAuth";
import useGlobalState from "@/stores/global";

const uAuth = useAuth();
const sGlobalState = useGlobalState();

onMounted(async () => {
  if (uAuth.isAuthenticated()) {
    sGlobalState.value.auth = true;
    await uAuth.authData();
  }
});
</script>