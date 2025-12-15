<template>
  <div class="simple-loading" v-if="props.isLoading">
    <loading v-model:active="props.isLoading">
      <v-progress-circular indeterminate :size="70" :width="6" />
      <h1 class="mt-6">{{ $t(labelLoading) }}</h1>
    </loading>
  </div>
</template>

<script setup lang="ts">
import loading from "vue-loading-overlay";

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  labelLoading: {
    type: String,
    default: "commons.common.loading",
  },
});
</script>

<style scoped lang="scss">
.simple-loading {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
  text-align: center;
}
</style>
