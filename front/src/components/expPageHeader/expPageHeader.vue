<template>
    <v-card>
      <v-card-text>
        <v-layout row wrap align-center>
          <div class="text-h4 font-weight-bold" v-if="props.title">
            <div class="title" v-if="props.translate_title">
              {{ $t(props.title) }}
            </div>
            <div class="title" v-else>
              {{ props.title }}
            </div>
          </div>
          <v-spacer/>
          <v-btn
            prepend-icon="mdi-plus-circle"
            color="primary"
            class="mx-1"
            @click="clickNew"
            v-if="props.btnNew"
          >
            {{ $t(props.labelAdd) }}
          </v-btn>
          <v-btn
            prepend-icon="mdi-file-export"
            color="primary"
            class="mx-1"
            @click="clickExport"
            v-if="props.btnExport"
          >
            {{ $t(props.labelExport) }}
          </v-btn>
          <slot name="right-buttons"></slot>
        </v-layout>
      </v-card-text>
    </v-card>
  </template>

  <script setup lang="ts">
    const props = defineProps({
      title: {
        type: String,
        default: ""
      },
      translate_title: {
        type: Boolean,
        default: true
      },
      btnNew: {
        type: Boolean,
        default: false
      },
      labelAdd: {
        type: String,
        default: "commons.forms.new"
      },
      btnExport: {
        type: Boolean,
        default: false
      },
      labelExport: {
        type: String,
        default: "commons.forms.export"
      }
    })

    const emit = defineEmits(["clickNew", "clickExport"]);

    const clickNew = () => {
      emit("clickNew");
    };

    const clickExport = () => {
      emit("clickExport");
    };
  </script>