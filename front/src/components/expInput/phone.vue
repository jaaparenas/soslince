<template>
  <div class="custom-input" @focusin="handleFocus" @focusout="handleBlur">
    <label :class="['custom-input-label', labelClasses, customClass]">{{ t(label) }}</label>
    <div class="phone-input-wrapper">
      <v-select
        v-model="countryCode"
        :items="countryCallingCodes"
        item-title="text"
        item-value="value"
        density="compact"
        hide-details
        variant="outlined"
        class="country-code-v-select"
      >
        <template #selection="{ item }">
          {{ item.raw.value }}
        </template>
      </v-select>
      <div class="divider"></div>
      <input
        type="tel"
        :value="numberPart"
        @input="handleNumberInput"
        class="phone-number-input"
        placeholder=" "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';
import { countryCallingCodes } from '@/data/countryCallingCodes';
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: 'commons.common.phone',
  },
  customClass: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);

const countryCode = ref('+57');
const numberPart = ref('');
const isFocused = ref(false);

const sortedCountryCodes = computed(() => {
  return [...countryCallingCodes].sort((a, b) => b.value.length - a.value.length);
});

const handleFocus = () => { isFocused.value = true; };
const handleBlur = () => { isFocused.value = false; };

const handleNumberInput = (event: Event) => {
  const input = event.target as HTMLInputElement;
  input.value = input.value.replace(/\D/g, ''); // Remove any non-digit characters
  numberPart.value = input.value;
};

const updateModelValue = () => {
  const fullNumber = `${countryCode.value}${numberPart.value}`; // Removed .replace(/\s+/g, '')
  if (props.modelValue !== fullNumber) {
    emit('update:modelValue', fullNumber);
  }
};

watch(countryCode, updateModelValue);
watch(numberPart, updateModelValue);

const parseModelValue = (value: string | null) => {
  if (!value) {
    numberPart.value = '';
    countryCode.value = '+57';
    return;
  }

  const foundCode = sortedCountryCodes.value.find(c => value.startsWith(c.value));
  if (foundCode) {
    countryCode.value = foundCode.value;
    numberPart.value = value.substring(foundCode.value.length);
  } else {
    numberPart.value = value;
    countryCode.value = '+57';
  }
};

watch(() => props.modelValue, (newValue) => {
  parseModelValue(newValue);
}, { immediate: true });

onMounted(() => {
    parseModelValue(props.modelValue);
});

const hasValue = computed(() => !!numberPart.value); // Only numberPart as countryCode always has a value
const isActive = computed(() => isFocused.value || hasValue.value);
const labelClasses = computed(() => ({ active: isActive.value }));

</script>

<style scoped>
.custom-input {
  display: block; /* Ensure it takes full width */
  width: 100%; /* Take full width of parent */
  box-sizing: border-box; /* Include padding and border in element's total width and height */
  position: relative;
}

.custom-input-label {
  position: absolute;
  top: 10px; /* Initial position for the label */
  left: 100px;
  transform: translateY(0); /* Initial transform */
  font-size: 1rem; /* Initial font size */
  color: rgba(0, 0, 0, 0.6);
  background-color: transparent; /* Transparent initially */
  padding-left: 4px;
  padding-right: 4px;
  cursor: text;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: calc(100% - 24px); /* Max width to prevent overflow */
  z-index: 1;
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1); /* Smooth transition */
  pointer-events: none; /* Allow clicks to pass through to input */
}

.custom-input-label.active {
  top: -8px; /* Floats above the border */
  font-size: 0.75rem; /* Smaller font size when active */
  color: #7a7a7a;
  background: #ffffff; /* Solid background to cover the border line */
  transform: translateY(0); /* Maintain position */
  max-width: 80%; /* Shrink width when floating */
}

.phone-input-wrapper {
  display: flex;
  align-items: center;
  height: 40px;
  padding: 0 9px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.42);
  background-color: #ffffff;
}

.custom-input:focus-within .phone-input-wrapper {
  border-color: #000000;
}

.country-code-v-select {
  width: 70px; /* Adjust width for v-select padding/arrow */
  min-width: 70px;
  max-width: 70px;
  flex: 0 0 70px; /* Prevent it from growing */
}

.country-code-v-select :deep(.v-field--variant-outlined .v-field__outline) {
  display: none;
}

.country-code-v-select :deep(.v-field) {
  height: 40px;
  align-items: center;
  padding-right: 0px;
}

.country-code-v-select :deep(.v-field__input) {
  padding: 0 4px;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.country-code-v-select :deep(.v-field__append-inner) {
  align-items: center;
}

.country-code-v-select:focus {
  outline: none;
}

.divider {
  width: 1px;
  background-color: rgba(0, 0, 0, 0.22);
  align-self: stretch;
  height: auto;
  margin: 0 6px;
}

.phone-number-input {
  flex-grow: 1;
  border: none;
  background: transparent;
  width: 100%;
  font-size: 1rem;
}

.phone-number-input:focus {
  outline: none;
}

.phone-number-input::placeholder {
  color: transparent;
}
</style>
