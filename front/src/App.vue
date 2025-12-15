<template>
  <RouterView />
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import useAuth from "@/modules/auth/composables/useAuth";
import useEncode from "@/composables/useEncode";
import useGlobalState from "@/stores/global";

const encode = useEncode();
const auth = useAuth();
const sGlobalState = useGlobalState();

onMounted(async () => {
  if (auth.isAuthenticated()) {
    sGlobalState.value.auth = true;
    await auth.authData();
  }
});
</script>