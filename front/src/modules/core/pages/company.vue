<template>
  <v-container>
    <h1 class="mb-4">{{ $t('modules.core.companies') }}</h1>
    <v-card>
      <v-card-text class="pa-0">
        <exp-data-table
          uuid="table-company"
          :endpoint="`${endpoint}/company`"
          :drawRefresh="drawRefresh"
          :headers="headers"
          :menuItems="['edit', 'delete']"
          :labelNew="'modules.core.new_company'"
          @onClickNew="clickNew"
          @onClickEdit="clickEdit"
          @onClickDelete="clickDelete"
        >
        </exp-data-table>
      </v-card-text>
    </v-card>
    <companyForm
      v-if="companyModal"
      v-model="companyModal"
      :id="companyId"
      @onSave="onSaveForm"
    />
    <exp-modal-form
      v-if="deleteModal"
      v-model="deleteModal"
      :title="$t('commons.forms.are_sure')"
      :btnSaveText="$t('commons.forms.delete')"
      @fnSave="confirmDelete"
      size="400"
    >
      <p>{{ $t('commons.common.confirm_delete') }} <strong>{{ itemToDelete.name }}</strong>?</p>
    </exp-modal-form>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";

import expDataTable from "@/components/expDataTable";
import companyForm from "@/modules/core/components/companyForm.vue";
import expModalForm from "@/components/expModalForm/expModalForm.vue";
import useCrud from "@/composables/useCrud";
import useUtils from "@/composables/useUtils";

const endpoint = "/api/1.0/core";
const { t } = useI18n();
const uCrud = useCrud(`${endpoint}/company`);
const uUtils = useUtils();

const headers: any[] = [
  { key: 'id', title: t("commons.common.id"), width: "auto", align: "start", sortable: true },
  { key: 'name', title: t("commons.common.name"), width: "auto", align: "start", searchable: true, sortable: true, },
  { key: 'address', title: t("commons.common.address"), width: "auto", align: "start", searchable: true, sortable: false, },
  { key: 'phone', title: t("commons.common.phone"), width: "auto", align: "start", searchable: true, sortable: false, },
  { key: 'email', title: t("commons.common.email"), width: "auto", align: "start", searchable: true, sortable: false, },
  { key: 'NIT', title: t("commons.common.nit"), width: "auto", align: "start", searchable: true, sortable: false, },
  { key: 'is_active', title: t("modules.auth.active"), width: "auto", align: "center", type: "check", sortable: false, },
  { key: "actions", title: t("commons.common.actions"), width: "90px", type: "actions", sortable: false, },
];
const drawRefresh = ref("");
const companyId = ref();
const companyModal = ref(false);
const deleteModal = ref(false);
const itemToDelete = ref();

onMounted(async () => {});

const clickNew = () => {
  companyId.value = null;
  companyModal.value = true;
};

const clickEdit = async (item: any) => {
  companyId.value = item.id;
  companyModal.value = true;
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

const onSaveForm = (uuid: string) => {
  drawRefresh.value = uuid;
  companyModal.value = false;
}
</script>

<style lang="scss">

</style>
