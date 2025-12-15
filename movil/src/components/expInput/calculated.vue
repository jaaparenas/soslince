<template>
  <div class="custom-input is-focused">
    <label :class="`custom-input-label active ${customClass}`">{{ label }}</label>
    <input
      type="text"
      ref="el"
      :readonly="true"
      :value="value"
      :class="`custom-input-field ${customClass}`"
      :style="`text-align: ${align}`"
    />
  </div>
</template>

<script setup lang="ts">
  const props = defineProps({
    label: {
      type: String,
      default: "",
    },
    value: {
      type: [String, Number],
      default: "",
    },
    align: {
      type: String,
      default: "right",
    },
    customClass: {
      type: String,
      default: "",
    },
  });
</script>

<style scoped>
.custom-input {
  position: relative;
}

.custom-input-label {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  background-color: white;
  padding-left: 4px;
  padding-right: 4px;
  cursor: text;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80%;
}

.custom-input-label.active {
  top: 0;
  font-size: 0.75rem;
  color: #7a7a7a;
  background: linear-gradient(180deg, hsla(0, 0%, 100%, 0.25) 50%, #f1f1f1 0);
}

.custom-input-field {
  width: 100%;
  padding: 9px 9px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.42);
  transition: border-color 0.3s ease;
  background-color: #f1f1f1;
}
</style>