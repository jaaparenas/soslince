<template>
  <v-dialog v-model="props.modelValue" :width="props.size" persistent>
    <v-card>
      <v-toolbar rounded="0" color="primary" elevation="0">
        <v-toolbar-title>{{ props.title }}</v-toolbar-title>
      </v-toolbar>
      <v-card-text :class="customClass">
        <slot></slot>
      </v-card-text>
      <v-card-text :class="customClass" v-if="btnSave || btnCancel">
        <v-row class="ma-0">
          <v-col class="pa-1 text-left" v-if="btnSave">
            <v-btn prepend-icon="mdi-content-save" color="green" @click="clickSave" :disabled="!btnSaveEnabled">
              {{ $t(btnSaveText) }}
            </v-btn>
          </v-col>
          <v-col class="pa-1 text-right" v-if="btnCancel">
            <v-btn prepend-icon="mdi-close-thick" color="red" @click="clickClose">
              {{ $t(btnCancelText) }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: "",
  },
  size: {
    type: [String, Number],
    default: "800",
  },
  btnSave: {
    type: Boolean,
    default: true,
  },
  btnSaveText: {
    type: String,
    default: "commons.forms.save",
  },
  btnSaveEnabled: {
    type: Boolean,
    default: true,
  },
  btnCancel: {
    type: Boolean,
    default: true,
  },
  btnCancelText: {
    type: String,
    default: "commons.forms.cancel",
  },
  customClass: {
    type: String,
    default: "",
  }
});

const emit = defineEmits(["fnClose", "fnSave", "update:modelValue"])

const clickClose= () => {
  emit("fnClose");
  emit("update:modelValue", false);
}

const clickSave = () => {
  emit("fnSave");
}
</script>