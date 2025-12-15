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

import { useLoading } from "vue-loading-overlay";
import expModalForm from "@/components/expModalForm";
import expPassword from "@/modules/auth/components/password.vue";
import useCore from "@/modules/core/composables/useCore";
import { toast } from 'vue3-toastify';
import { useI18n } from "vue-i18n";

const uLoading = useLoading();
const uCore = useCore();
const { t } = useI18n();

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
  try {
    await uCore.updateUserPassword({
      id: props.id,
      password: passwordData.value.password
    });
    toast.success(t('modules.auth.password_updated'));
    modelValue.value = false;
  } catch { }
  loader.hide();
};
</script>

<style lang="scss">

</style>