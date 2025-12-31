<template>
  <div>
      <v-container>
        <h1 class="mb-4">{{ $t('modules.core.customers') }}</h1>
        <v-card>
          <v-card-text class="pa-0">
            <exp-data-table
              uuid="table-customer"
              :endpoint="`${endpoint}/customer`"
              :drawRefresh="drawRefresh"
              :headers="headers"
              :extraMenuItems="[
                { title: 'modules.auth.password', action: 'password', icon: 'mdi-lock' },
                { title: 'modules.core.history_sos_alert', action: 'sos', icon: 'mdi-bell' },
                { title: 'modules.core.history_location', action: 'locations', icon: 'mdi-map-marker' },
              ]"
              :menuItems="['edit', 'delete', 'password', 'sos', 'locations']"
              :labelNew="'modules.core.new_customer'"
              :showFilters="true"
              @onClickNew="clickNew"
              @onClickEdit="clickEdit"
              @onClickDelete="clickDelete"
              @onClickAction="clickAction"
              :extraParameters="extraParams"
            >
              <template #extra-filters>
                <v-row>
                  <v-col>
                    <v-autocomplete
                      v-model="selectedCompany"
                      :items="companies"
                      item-title="name"
                      item-value="id"
                      :label="$t('commons.common.company')"
                      clearable
                      hide-details
                    ></v-autocomplete>
                  </v-col>
                  <v-col v-if="false">
                    <v-select
                      v-model="selectedGender"
                      :items="genders"
                      item-title="label"
                      item-value="id"
                      :label="$t('commons.common.gender')"
                      clearable
                      hide-details
                    ></v-select>
                  </v-col>
                </v-row>
              </template>
              <template #item.name="{ item }">
                {{ item.first_name }} {{ item.last_name }}
              </template>
              <template #item.image="{ item }">
                <v-avatar size="40" variant="outlined">
                  <v-img :src="uUtils.getUrlImg(item.customer_info.image)" />
                </v-avatar>
              </template>
              <template #item.birth_date="{ item }">
                {{ item.customer_info.birth_date }}
              </template>
              <template #item.phone="{ item }">
                {{ item.customer_info.phone }}
              </template>
              <template #item.company="{ item }">
                {{ item.customer_info.company_name }}
              </template>
            </exp-data-table>
          </v-card-text>
        </v-card>
      </v-container>
      <exp-modal-form
        :title="$t('modules.core.new_customer')"
        :width="800"
        v-model="formModal"
        @fnSave="saveBooking"
      >
        <v-card-text>
          <v-row>
            <v-col cols="7">
              <exp-dynamic-form
                v-model="formData"
                :schema="(formSchemaCalculated as any)"
                :errors="combinedErrors"
                variant="outlined"
                density="compact"
                hide-details="true"
              >
              </exp-dynamic-form>
            </v-col>
            <v-col cols="5">
              <div>
                <exp-crop
                  v-model="formData.url_image"
                  :width="300"
                  :height="300"
                />
              </div>
              <div v-if="!((formData as any).id > 0)" class="mt-12">
                <exp-password v-model="passwordData" />
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </exp-modal-form>
      <exp-modal-form
        :title="$t('modules.core.history_sos_alert')"
        :width="1100"
        v-model="formModalSos"
        :btn-save="false"
      >
        <history-sos :userId="userId" />
      </exp-modal-form>
      <exp-modal-form
        :title="$t('modules.core.history_location')"
        :width="1100"
        v-model="formModalLocation"
        :btn-save="false"
      >
        <history-locations :userId="userId" />
      </exp-modal-form>
      <exp-modal-form
        :title="$t('modules.auth.password')"
        :width="550"
        v-model="passwordModal"
        @fnSave="onUpdatePassword"
        :btnSaveEnabled="!(passwordData?.valid !== true)"
      >
        <expPassword v-model="passwordData" />
      </exp-modal-form>
      <exp-modal-form
        v-if="deleteModal"
        v-model="deleteModal"
        :title="$t('commons.forms.are_sure')"
        :btnSaveText="$t('commons.forms.delete')"
        @fnSave="confirmDelete"
        size="400"
      >
        <p>{{ $t('commons.common.confirm_delete') }} <strong>{{ itemToDelete.first_name }}</strong>?</p>
      </exp-modal-form>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useVuelidate } from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";
import { useLoading } from "vue-loading-overlay";
import dayjs from "dayjs";

const endpoint = "/api/1.0/core";

import useAuth from "@/modules/auth/composables/useAuth";
import useCrud from "@/composables/useCrud";
import useUtils from "@/composables/useUtils";
import expDataTable from "@/components/expDataTable";
import expModalForm from "@/components/expModalForm";
import expDynamicForm from "@/components/expDynamicForm";
import expPassword from "@/modules/auth/components/password.vue";
import expCrop from "@/components/expCrop/expCrop.vue";

import historyLocations from "../components/history_locations.vue";
import historySos from "../components/history_sos.vue";
import useCustomer from "../composables/useCustomer";
import useToast from "@/composables/useToast";

const uCrud = useCrud(`${endpoint}/customer`);
const companyCrud = useCrud(`${endpoint}/company`);
const { t } = useI18n();
const uUtils = useUtils();
const uCustomer = useCustomer();
const uLoading = useLoading();
const uAuth = useAuth();

const headers: any[] = [
  { key: 'id', visible: false },
  { key: 'is_active', title: t("modules.auth.active"), width: "80px", type: "check", align: "start", sortable: false, },
  { key: 'first_name', visible: false },
  { key: 'last_name', visible: false },
  { key: 'name', title: t("commons.common.name"), virtual: true, width: "auto", align: "start", sortable: false, },
  { key: 'customer_info', visible: false },
  { key: 'image', title: t("commons.common.image"), virtual: true, width: "auto", align: "start", sortable: false, },
  { key: 'birth_date', title: t("commons.common.birth_date"), virtual: true, width: "auto", align: "start", sortable: false, },
  { key: 'email', title: t("commons.common.email"), width: "auto", align: "start", sortable: false, },
  { key: 'phone', virtual: true, title: t("commons.common.phone"), width: "auto", align: "start", sortable: false, },
  { key: 'company', virtual: true, title: t("commons.common.company"), width: "auto", align: "start", sortable: false, },
  { key: "actions", title: t("commons.common.actions"), width: "130px", type: "actions", sortable: false, },
];
const drawRefresh = ref("");

const filters = ref({});
const formModalSos = ref(false);
const formModalLocation = ref(false);
const userId = ref(0);
const formModal = ref(false);
const passwordModal = ref(false);
const deleteModal = ref(false);
const itemToDelete = ref();
const companies = ref([]);
const selectedCompany = ref(null);
const selectedGender = ref(null);
const companyItems = ref([]);

const extraParams = computed(() => {
  const params = {};
  if (selectedCompany.value) {
    params['customer__company'] = selectedCompany.value;
  }
  if (selectedGender.value) {
    params['customer__gender'] = selectedGender.value;
  }
  return params;
});

const formDataDefault = {
  is_active: false,
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  url_image: "",
  image: "",
  birth_date: dayjs().format("YYYY-MM-DD"),
  blood_type: "1",
  gender: "",
  company: "",
  secret_word: "",
  details: "",
};
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

const genders = [
  { id: 'M', label: 'Male' },
  { id: 'F', label: 'Female' }
];

const formData = ref({ id: null, ...formDataDefault });
const passwordData = ref();
const formSchema = computed(() => [
  { key: "is_active", type: "switch", title: t("modules.auth.active"), required: true },
  { key: "first_name", type: "text", col:"md-6", title: t("modules.auth.first_name"), required: true },
  { key: "last_name", type: "text", col:"md-6", title: t("modules.auth.last_name"), required: true },
  { key: "email", type: "email", title: t("commons.common.email"), required: true },
  { key: "phone", type: "phone", col:"md-6", title: t("commons.common.phone"), required: true },
  { key: "birth_date", type: "date", col:"md-6", title: t("commons.common.birth_date"), required: true },
  { key: "gender", type: "select", items: genders, col:"md-6", title: t("commons.common.gender"), required: true },
  { key: "blood_type", type: "select", items: listBloodType, col:"md-6", title: t("commons.common.blood_type"), required: true },
  { key: "company", type: "select", items: companyItems.value, col:"md-6", title: t("commons.common.company"), required: true },
  { key: "secret_word", type: "text", title: t("commons.common.secret_word"), required: true },
  { key: "details", type: "editor", title: t("commons.common.details"), required: true },
]);
const rules = {
  first_name: { required, minLength: minLength(2) },
  last_name: { required, minLength: minLength(2) },
  email: { required, email, minLength: minLength(5) },
};
const validate = useVuelidate(rules, formData);

const uToast = useToast();
const backendErrors = ref<any[]>([]);
const combinedErrors = computed(() => {
  try {
    return [...(validate.value.$errors || []), ...backendErrors.value];
  } catch (e) {
    return [...backendErrors.value];
  }
});

const formSchemaCalculated = computed(() => {
  return formSchema.value;
});

onMounted(async () => {
  companyCrud.list().then((resp: any) => {
    companies.value = resp;
    companyItems.value = resp.map((c: any) => ({ id: c.id, label: c.name }));
  });
});

const isAdmin = computed(() => {
  try {
    return uAuth.getUserData().role == 1;
  } catch (error) {
    return false;
  }
});

const saveBooking = async () => {
  validate.value.$touch();
  if (validate.value.$invalid) {
    return false;
  }

  const data = {
    id: formData.value.id,
    is_active: formData.value.is_active,
    first_name: formData.value.first_name,
    last_name: formData.value.last_name,
    email: formData.value.email,
    password: passwordData.value?.password,
    customer_info: {
      phone: formData.value.phone,
      url_image: formData.value.url_image ?? "",
      birth_date: formData.value.birth_date,
      blood_type: formData.value.blood_type,
      gender: formData.value.gender,
      company: formData.value.company,
      secret_word: formData.value.secret_word,
      details: formData.value.details,
    }
  };
  try {
    await uCrud
      .save(data)
      .then(() => {
        drawRefresh.value = `${uUtils.createUUID()}`;
        formModal.value = false;
      })
      .finally(() => {});
  } catch (error) {
    
    // try to extract backend validation errors (axios typical shape: error.response.data)
    const respData = (error as any)?.response?.data ?? (error as any)?.data ?? (error as any);
    const errorsArray: any[] = [];

    const pushFieldError = (property: string, message: string) => {
      errorsArray.push({ $property: property, $message: message });
    };

    try {
      if (respData) {
        // If backend returns an object with `customer_info` nested errors
        if (respData.customer_info && typeof respData.customer_info === 'object') {
          for (const k in respData.customer_info) {
            const v = respData.customer_info[k];
            const msg = Array.isArray(v) ? v.join(', ') : String(v);
            pushFieldError(k, msg);
          }
        } else if (respData.email && typeof respData.email === 'object') {
          const v = respData.email;
          const msg = Array.isArray(v) ? v.join(', ') : String(v);
          pushFieldError('email', msg);
        }
      }
    } catch (e) {
      console.log('Error parsing backend errors', e);
    }

    // set backend errors for form and show toast(s)
    backendErrors.value = errorsArray;
    if (errorsArray.length > 0) {
      // build HTML list for toast
      const html = `<ul>${errorsArray.map((x: any) => `<li><strong>${x.$property}</strong>: ${x.$message}</li>`).join('')}</ul>`;
      uToast.toastHTML(html, { type: 'error' } as any);
    } else {
      // fallback generic message
      uToast.toastError('Error saving customer data.');
    }
  }
};

const clickNew = () => {
  backendErrors.value = [];
  formData.value = { id: null, ...formDataDefault };
  if (selectedCompany.value) {
    formData.value.company = selectedCompany.value;
  }
  formModal.value = true;
};

const clickEdit = async (item: any) => {
  backendErrors.value = [];
  await uCrud
    .retrieve(item.id)
    .then((item: any) => {
      formData.value = {
        ...item,
        gender: item.gender,
        ...item.customer_info,
        id: item.id,
        url_image: uUtils.getUrlImg(item.customer_info.image ?? '')
      };
      formModal.value = true;
    })
    .finally(() => {});
};

const clickDelete = (item: any) => {
  itemToDelete.value = item;
  deleteModal.value = true;
};

const confirmDelete = () => {
  uCrud.remove(itemToDelete.value.id).then(() => {
    drawRefresh.value = uUtils.createUUID();
    deleteModal.value = false;
  })
};

const clickAction = (item: any, action: string) => {
  userId.value = item.id;
  if (action === 'password') {
    passwordModal.value = true;
  } else if (action === 'sos') {
    formModalSos.value = true;
  } else if (action === 'locations') {
    formModalLocation.value = true;
  }
};

const onUpdatePassword = async () => {
  if (passwordData.value.valid) {
    let loader = uLoading.show({});
    await uCustomer.setPassword({
      id: userId.value,
      password: passwordData.value.password
    })
    .then(() => {
      passwordModal.value = false;
    })
    .finally(() => {
      passwordData.value.password = "";
      passwordData.value.valid = false;
      loader.hide();
    });
  }
}

const onChange = (filter: any) => {
  filters.value = filter;
}
</script>

<style lang="scss">

</style>
