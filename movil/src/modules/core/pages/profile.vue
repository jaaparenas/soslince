<template>
  <div v-if="isLoaded">
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col></v-col>
          <v-col cols="6" class="mb-8">
            <div>
              <exp-crop
                v-model="formData.url_image"
                :width="300"
                :height="300"
              />
            </div>
          </v-col>
          <v-col></v-col>
        </v-row>
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="formData.first_name"
          :label="$t('modules.auth.first_name')"
          variant="outlined"
          density="compact"
          hide-details
          :error="hasError('first_name')"
        />
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="formData.last_name"
          :label="$t('modules.auth.last_name')"
          variant="outlined"
          density="compact"
          hide-details
          :error="hasError('last_name')"
        />
      </v-col>
      <v-col cols="6">
        <exp-date-time
          v-model="formData.birth_date"
          :label="$t('commons.common.birth_date')"
          type="date"
        ></exp-date-time>
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="formData.blood_type"
          :label="$t('commons.common.blood_type')"
          :items="listBloodType"
          item-title="label"
          item-value="id"
          variant="outlined"
          density="compact"
          hide-details
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="formData.phone"
          :label="$t('commons.common.phone')"
          variant="outlined"
          density="compact"
          hide-details
          :error="hasError('phone')"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="formData.company"
          :label="$t('commons.common.company')"
          variant="outlined"
          density="compact"
          hide-details
          :error="hasError('company')"
        />
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="formData.secret_word"
          :label="$t('commons.common.secret_word')"
          variant="outlined"
          density="compact"
          hide-details
          :error="hasError('secret_word')"
        />
      </v-col>
      <v-col cols="12">
        <quill-editor theme="snow"
          v-model:content="formData.details"
          contentType="html"
          :options="editorOption"
          style="height: 175px;"
        ></quill-editor>
      </v-col>
      <v-col cols="12">
        <v-btn class="btn-update" color="#20282d" :disabled="!isLoaded" @click="updateData">
          {{ $t('commons.common.update_profile') }}
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { toast } from 'vue3-toastify';

import { useRouter } from "vue-router";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";

import expDateTime from '@/components/expInput/dateTime.vue';
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import useAuth from "@/modules/auth/composables/useAuth";
import useCore from "@/modules/core/composables/useCore";
import useUtils from "@/composables/useUtils";
import expCrop from "@/components/expCrop/expCrop.vue";

const { t } = useI18n();
const uUtils = useUtils();
const uCore = useCore();
const uRouter = useRouter();
const uAuth = useAuth();

const isLoaded = ref(false);
const listBloodType = [
  { id: "1", label: "A+" },
  { id: "2", label: "A-" },
  { id: "3", label: "B+" },
  { id: "4", label: "B-" },
  { id: "5", label: "AB+" },
  { id: "6", label: "AB-" },
  { id: "7", label: "O+" },
  { id: "8", label: "O-" },
  { id: "9", label: "Unknown" },
];

const editorOption = {
  placeholder: '',
  modules: {
    toolbar: [
      [{ header: [1, 2, 3, 4, 5, 6, false] }],
      ['bold', 'italic', 'underline'],
      [{ 'color': [] as any[] }, { background: [] as any[] }],
      [{ 'align': [] as any[] }],
      [{ 'list': 'ordered' }, { list: 'bullet' }],
      [{ 'indent': '-1' }, { indent: '+1' }],
      ['clean'],
    ]
  }
}

const formData = ref();
const rules = {
  first_name: { required, minLength: minLength(2) },
  last_name: { required, minLength: minLength(2) },
  phone: { required, minLength: minLength(2) },
  company: { required, minLength: minLength(5) },
  secret_word: { required, minLength: minLength(5) },
};

const v$ = useVuelidate(rules, formData);
const hasError = (field: any) => {
  const error = v$.value[field].$error;
  return error ? v$.value[field].$invalid : false;
};

onMounted(async () => {
  const userData: any = await uCore.getUserData();
  formData.value = {
    ...userData.data,
    url_image: uUtils.getUrlImg(userData.data.image ?? '')
  };
  isLoaded.value = true;
});

const updateData = async () => {
  v$.value.$touch();
  if (v$.value.$invalid) return;

  const data: any = await uCore.updateUserData(formData.value);
  if (data.data.mgs === "OK") {
    toast.success('Profile updated');
    setTimeout(async () => {
      await uAuth.authData();
      uRouter.push({ name: 'core-index' })
    }, 1000);
  }
};
</script>

<style lang="scss">
.btn-update {
  width: 100%;
  height: 50px !important;
}
</style>
