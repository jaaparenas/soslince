<template>
  <loading v-model:active="isLoading">
    <div class="text-center">
      <v-progress-circular
        :model-value="valueProgress"
        :size="70"
        :width="2"
        v-if="valueProgress < 100"
      >
        {{ valueProgress }}%
      </v-progress-circular>
      <v-progress-circular
        indeterminate
        :size="70"
        :width="2"
        v-else
      />
      <h1 class="mt-6">{{ $t(labelProgress) }}<span v-if="valueProgress < 100">: {{ valueProgress }}%</span></h1>
    </div>
  </loading>
  <v-card class="mx-auto">
    <v-toolbar class="text-center">
      <v-toolbar-title class="ma-0">{{ $t(title) }}</v-toolbar-title>
      <v-btn
        icon="mdi-file-image-remove-outline"
        class="mr-1"
        color="red"
        @click="clearImage"
        :disabled="!imageUrl && !imagePreview"
      ></v-btn>
    </v-toolbar>
    <div class="wrap-uploader">
      <div>
        <div v-if="!imageUrl">
          <v-img
            :src="imagePreview"
            :style="{ margin: 'auto', width: props.width + 'px', height: props.height + 'px' }"
            v-if="imagePreview != '' && imagePreview != null"
          />
          <template v-else>
            <input
              ref="fileInput"
              type="file"
              style="display: none"
              @change="handleFileChange"
              accept="image/jpeg,image/png"
            />
            <div
              class="click-wrap"
              :style="{ width: props.width + 'px', height: props.height + 'px' }"
            >
              <div class="click-area" @click="openFileInput">
                {{ $t("commons.forms.click_choose_image") }}
              </div>
            </div>
          </template>
        </div>
        <div class="image-area" v-else :style="{ margin: 'auto', width: props.width + 'px', height: props.height + 'px' }">
          <v-img
            :src="imageUrl"
            aspect-ratio="3/4"
            :width="'100%'"
          />
        </div>
      </div>
    </div>
  </v-card>
  <expAlert
    v-model="alertStatus"
    type="alert"
    :text="alertMessage"
    @fn-ok="alertStatus = false"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import expAlert from "@/components/expAlert/expAlert.vue";
import axios from "axios";
import loading from 'vue-loading-overlay';

const props = defineProps({
  width: {
    type: Number,
    default: 300
  },
  height: {
    type: Number,
    default: 400
  },
  preview: {
    default: null
  },
  title: {
    type: String,
    default: "commons.common.image"
  }
})

onMounted(() => {
  setTimeout(() => {
    imagePreview.value = props.preview
  }, 10)
})

const endpoint = "bum/image/upload";
const fileInput = ref();
const imageUrl = ref();
const imagePreview = ref();
const binaryFile = ref();
const alertStatus = ref(false);
const alertMessage = ref("");
const isLoading = ref(false);
const valueProgress = ref(0);
const labelProgress = ref("commons.forms.uploading_file");

const openFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = (event:any ) => {
  const file = event.target.files[0];
  const extension = file.name.split(".").slice(-1)[0];
  let extensions = ["jpg", "jpeg", "png"];
  if (extensions.indexOf(extension) === -1) {
    fileInput.value.value = "";
    alertStatus.value = true;
    alertMessage.value = 'commons.forms.extensions_allow'
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    imageUrl.value = reader.result;
  };
  reader.readAsDataURL(file);
  binaryFile.value = file;
};

const clearImage = () => {
  imagePreview.value = "";
  imageUrl.value = "";
};

const exeUpload = async (folder: string, preview:boolean = false) => {
  return new Promise((resolve, reject) => {
    isLoading.value = true;
    if ((imageUrl.value === undefined || imageUrl.value === "") && (props.preview !== "" && props.preview === imagePreview.value)) {
      isLoading.value = false;
      resolve({"image": null, "path": null});
    } else if (props.preview === "" && imageUrl.value === "") {
      isLoading.value = false;
      resolve({"image": "", "path": ""});
    } else if ((imageUrl.value === undefined || imageUrl.value === "") && (props.preview !== "" && props.preview !== imagePreview.value)) {
      isLoading.value = false;
      resolve({"image": "", "path": ""});
    } else {
      try {
        valueProgress.value = 0;
        labelProgress.value = "commons.forms.uploading_file";

        let formData = new FormData();
        formData.append("type", "binary");
        formData.append("file", binaryFile.value);
        formData.append("folder", folder);
        formData.append("preview", preview ? "1" : "0");
        axios
          .post(`${endpoint}/`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            onUploadProgress: (progressEvent) => {
              const progressValue = (progressEvent.loaded / progressEvent.total) * 100;
              valueProgress.value = progressValue;
              if (progressValue > 0.99) {
                labelProgress.value = "commons.forms.processing_file";
              }
            },
          })
          .then((resp: any) => {
            isLoading.value = false;
            resolve(resp.data); // Url image
          })
          .catch(() => {
            isLoading.value = false;
            reject(null);
          });
      } catch {
        isLoading.value = false;
        reject(null);
      }
    }
  });
}

defineExpose({ exeUpload });
</script>

<style scoped lang="scss">
  .click-wrap {
    display: flex;
    padding: 5px;
    margin: auto;
    .click-area {
      border: 2px dotted #ccc;
      width: 100%;
      cursor: pointer;
      padding: 20px;
      font-size: 20px;
      text-align: center;
    }
  }
  .image-area {
    display: flex;
    width: 100%;
    justify-content: center;
  }
</style>








