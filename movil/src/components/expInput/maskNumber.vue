<template>
  <div class="custom-input" :class="{ 'is-focused': isFocused || localValue, 'disabled': disabled }">
    <label class="custom-input-label" :class="{ 'active': isFocused || localValue }" @click="sendFocus">{{ label }}</label>
    <mask-input
      :id="idControl"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :value="localValue"
      :mask="mask.mask"
      :radix="mask.radix"
      :thousands-separator="mask.thousandsSeparator"
      :min="mask.min"
      :max="mask.max"
      :scale="mask.scale"
      @focus="handleFocus"
      @blur="handleBlur"
      @accept:masked="onAccept"
      @accept:unmasked="onAcceptUnmasked"
      class="custom-input-field"
      :class="customClass"
    />
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, watch } from 'vue';
  import { IMaskComponent as MaskInput } from 'vue-imask';

  const emit = defineEmits(["change"]);
  const props = defineProps({
    value: {
      type: [String, Number],
      default: "",
    },
    mask: {
      type: Object,
      default: () => ({
        mask: Number,
        radix: ".",
        thousandsSeparator: ",",
        min: 0,
        max: 999999999,
        scale: 2,
      })
    },
    label: {
      type: String,
      default: ""
    },
    placeholder: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    customClass: {
      type: String,
      default: ""
    },
  });

  const isFocused = ref(false);
  const localValue = ref("");
  const idControl = ref("");
  const firstParse = ref(true);

  onMounted(() => {
    let dt = new Date().getTime();
    const uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
      /[xy]/g,
      function (c) {
        const r = (dt + Math.random() * 16) % 16 | 0;
        dt = Math.floor(dt / 16);
        return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
      }
    );

    idControl.value = uuid;
    localValue.value = props.value?.toString() ?? "0";
  });

  const handleFocus = () => {
    isFocused.value = true;
    const input = (document.getElementById(idControl.value) as HTMLInputElement);
    input.setSelectionRange(0, input.value.length);
  }
  const handleBlur = () => {
    if (!localValue.value) {
      isFocused.value = false;
    }
  }
  const sendFocus = () => {
    const input = (document.getElementById(idControl.value) as HTMLInputElement);
    input.focus();
  }

  const onAccept = (value:any) => {
    //console.log({ value });
  }

  const onAcceptUnmasked = (unmaskedValue:any) => {
    if (firstParse.value) {
      localValue.value = unmaskedValue;
      firstParse.value = false;
    } else {
      emit("change", unmaskedValue);
    }
  }

  watch(() => props.value, (newVal: any, oldVal: any) => {
    if (typeof newVal === "number") {
      newVal = newVal.toString();
    }
    if (newVal === oldVal) {
      return;
    }
    localValue.value = newVal;
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
  transition: top 0.1s, font-size 0.1s, color 0.1s;
  background-color: white;
  padding-left: 4px;
  padding-right: 4px;
  cursor: text;
}

.custom-input-label.active {
  top: 0;
  font-size: 0.75rem;
  color: #7a7a7a;
}

.custom-input-field {
  width: 100%;
  padding: 8px;
  padding-left: 16px;
  padding-right: 16px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.42);
  transition: border-color 0.3s ease;
  font-size: 16px;
  min-height: 40px;
  text-align: right;
}

.custom-input-field:focus {
  outline: none;
  border: 2px solid #000;
}

.custom-input.is-focused .custom-input-label {
  top: 0;
  font-size: 0.75rem;
  color: #7a7a7a;
}
.custom-input.disabled {
  input, label {
    color: #d4d4d4;
    border-color: #d4d4d4 !important;
  }
}
</style>