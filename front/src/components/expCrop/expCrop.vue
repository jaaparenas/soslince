<template>
  <input
    ref="uploadInput"
    type="file"
    accept="image/jpg, image/jpeg, image/png, image/gif"
    @change="selectFile"
    style="display: none;"
  />

  <div class="wrap-crop" :style="`width: 100%; aspect-ratio: ${ratio};`">
    <v-row>
      <v-col class="text-left">{{ $t('commons.common.image') }}</v-col>
      <v-col class="text-right">
        <v-icon @click="clearImage" color="red">mdi-delete</v-icon>
      </v-col>
    </v-row>
    <div class="img-container">
      <template v-if="modelValue">
        <img :src="modelValue" class="img" />
      </template>
      <template v-else>
        <div class="icon" :style="`aspect-ratio: ${ratio};`">
          <v-icon>mdi-image</v-icon>
        </div>
      </template>
    </div>
    <div class="uploadTrigger" :style="`aspect-ratio: ${ratio};`" @click="triggerFileUpload"></div>
  </div>
  <exp-modal-form
    v-model="modalCrop"
    :width="'370px'"
    :title="'commons.common.image'"
    :btnSaveNew="false"
    :btnSaveLabel="'commons.form.crop'"
    @fnSave="cropImage"
  >
    <div class="modal-content" :style="`width: 340px; height: 340px`">
      <VuePictureCropper
        :boxStyle="{
          width: '100%',
          height: '100%',
          backgroundColor: '#f8f8f8',
          margin: 'auto'
        }"
        :img="pic"
        :options="{
          viewMode: 1,
          dragMode: 'crop',
          aspectRatio: ratio
        }"
        :presetMode="{
          mode: 'fixedSize',
          width: props.width,
          height: props.height
        }"
      />
    </div>
  </exp-modal-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import VuePictureCropper, { cropper } from 'vue-picture-cropper';
import expModalForm from "@/components/expModalForm";

const modelValue = defineModel<string>();
const modalCrop = ref(false);

const props = defineProps({
  width: {
    type: Number,
    default: 300
  },
  height: {
    type: Number,
    default: 300
  }
});

const ratio = ref(props.width / props.height);

const triggerFileUpload = () => {
  (uploadInput.value as any).click();
};

const uploadInput = ref<HTMLInputElement | null>(null);
const pic = ref<string>('');

function selectFile(e: Event) {
  pic.value = '';

  const { files } = e.target as HTMLInputElement;
  if (!files || !files.length) return;

  const file = files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
    pic.value = String(reader.result);
    modalCrop.value = true;
    if (!uploadInput.value) return;
    uploadInput.value.value = '';
  };
}

const cropImage = async () => {
  if (!cropper) return;
  const base64Str = cropper.getDataURL();
  modelValue.value = base64Str;
  modalCrop.value = false;
};

const clearImage = () => {
  modelValue.value = '';
};
</script>


<style scoped lang="scss">
.wrap-crop {
  display: block;
  position: relative;

  .img-container {
    position: absolute;
    width: 100%;

    .icon {
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;

      i {
        font-size: 100px;
      }
    }

    .img {
      width: 100%;
      height: 100%;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
  }

  .uploadTrigger {
    position: absolute;
    width: 100%;
    cursor: pointer;
    border-radius: 5px;
    border: 1px solid #ccc;
  }

  .uploadTrigger:hover {
    background-color: rgba(0, 0, 0, 0.5);
  }
}
</style>