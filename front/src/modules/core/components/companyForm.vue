<template>
  <exp-modal-form
    :title="$t('modules.core.company')"
    :width="600"
    v-model="modelValue"
    @fnSave="clickSave"
    :btnSaveEnabled="!validate.$invalid"
  >
    <v-card-text>
      <exp-dynamic-form
        v-model="formData"
        :schema="(formSchema as any)"
        variant="outlined"
        density="compact"
        hide-details="true"
      >
      </exp-dynamic-form>
    </v-card-text>
  </exp-modal-form>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useVuelidate } from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";

import useCrud from "@/composables/useCrud";
import useUtils from "@/composables/useUtils";
import expModalForm from "@/components/expModalForm";
import expDynamicForm from "@/components/expDynamicForm";

const endpoint = "/api/1.0/core";
const uCrud = useCrud(`${endpoint}/company`);
const uUtils = useUtils();
const { t } = useI18n();

const modelValue = defineModel<boolean>();
const props = defineProps({
  id: {
    type: Number,
    default: null,
  },
});

const formDataDefault = {
  name: "",
  address: "",
  phone: "",
  email: "",
  NIT: "",
  is_active: true,
};
const formData = ref({ ...formDataDefault });

const formSchema = [
  { key: "is_active", type: "switch", col:"md-12", title: t("modules.auth.active"), required: true },
  { key: "name", type: "text", col:"md-6", title: t("commons.common.name"), required: true },
  { key: "NIT", type: "text", col:"md-6", title: t("commons.common.nit"), required: true },
  { key: "address", type: "text", col:"md-6", title: t("commons.common.address"), required: true },
  { key: "phone", type: "text", col:"md-6", title: t("commons.common.phone"), required: true },
  { key: "email", type: "email", col:"md-12", title: t("commons.common.email"), required: true },
];

const rules = {
  name: { required, minLength: minLength(2) },
  email: { required, email },
};
const validate = useVuelidate(rules, formData);

onMounted(async () => {
  if (props.id != null) {
    await uCrud
      .retrieve(props.id)
      .then((item: any) => {
        Object.assign(formData.value, { ...item });
      });
  } else {
    Object.assign(formData.value, { id: null, ...formDataDefault });
  }
});

const clickSave = async () => {
  validate.value.$touch();
  if (!validate.value.$invalid) {
    let data = { ...formData.value };
    await uCrud
      .save(data)
      .then((resp: any) => {
        emit("onSave", `${uUtils.createUUID()}`);
        modelValue.value = false;
      });
  }
};

const emit = defineEmits(["onSave"]);
</script>

<style lang="scss">

</style>
