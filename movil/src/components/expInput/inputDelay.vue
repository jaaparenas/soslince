<template>
  <v-text-field
    v-bind="$attrs"
    v-model="searchImput"
  ></v-text-field>
</template>

<script lang="ts" setup>
import { watch, ref } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  delay: {
    type: Number,
    default: 1000,
  },
});

const searchImput = ref('')

const emit = defineEmits(["update:modelValue"])

watch(() => props.modelValue, () => {
  searchImput.value = props.modelValue;
});

let searchDelay = Object();
watch(searchImput, (currentValue, oldValue) => {
  if (currentValue == oldValue)
    return
  clearTimeout(searchDelay);
  searchDelay = setTimeout(() => {
    emit("update:modelValue", currentValue);
  }, props.delay);
});
</script>