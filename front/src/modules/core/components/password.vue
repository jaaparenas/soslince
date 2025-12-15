<template>
  <exp-modal-form
    :title="$t('modules.auth.password')"
    :width="550"
    v-model="modelValue"
    @fnSave="clickSave"
    :btnSaveEnabled="!(passwordData?.valid !== true)"
  >
    <exp-password v-model="passwordData" />
  </exp-modal-form>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const endpoint = "/api/1.0/core";

import { useLoading } from "vue-loading-overlay";
import expModalForm from "@/components/expModalForm";
import expPassword from "@/modules/auth/components/password.vue";

const uLoading = useLoading();

const modelValue = defineModel<boolean>();
const props = defineProps({
  id: {
    type: Number,
    default: null,
  },
});

const passwordData = ref();

onMounted(async () => { });

const clickSave = async () => {
  if (passwordData.value == undefined || passwordData.value.valid !== true)
    return;

  let loader = uLoading.show({});
  axios.patch(`${endpoint}/staff/${props.id}/password/`, { password: passwordData.value.password })
    .then(() => {
      modelValue.value = false;
    })
    .catch((err: any) => {
      modelValue.value = false;
    })
    .finally(() => {
      loader.hide();
    })
};
</script>

<style lang="scss">

</style>