<template>
  <v-container>
    <h1 class="mb-4">{{ $t('modules.core.staff') }}</h1>
    <v-card>
      <v-card-text class="pa-0">
        <exp-data-table
          uuid="table-staff"
          :endpoint="`${endpoint}/staff`"
          :drawRefresh="drawRefresh"
          :headers="headers"
          :extraMenuItems="[
            { title: 'modules.auth.password', action: 'password', icon: 'mdi-lock' },
          ]"
          :menuItems="['edit', 'delete', 'password']"
          :labelNew="'modules.core.new_staff'"
          @onClickNew="clickNew"
          @onClickEdit="clickEdit"
          @onClickDelete="clickDelete"
          @onClickAction="clickAction"
        >
          <template v-slot:item.is_superuser="{item}">
            <v-icon v-if="item.is_superuser" color="blue" class="mr-2">
              mdi-account-tie
            </v-icon>
            <v-icon v-else color="green" class="mr-2">
              mdi-account-hard-hat
            </v-icon>
          </template>
        </exp-data-table>
      </v-card-text>
    </v-card>
    <profileForm
      v-if="profileModal"
      v-model="profileModal"
      :id="staffId"
      @onSave="onSaveProfile"
    />
    <passwordForm
      v-if="passwordModal"
      v-model="passwordModal"
      :id="staffId"
    />
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
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";

import expDataTable from "@/components/expDataTable";
import profileForm from "@/modules/core/components/profile.vue";
import passwordForm from "@/modules/core/components/password.vue";
import expModalForm from "@/components/expModalForm/expModalForm.vue";
import useCrud from "@/composables/useCrud";
import useUtils from "@/composables/useUtils";

const endpoint = "/api/1.0/core";
const { t } = useI18n();
const uCrud = useCrud(`${endpoint}/staff`);
const uUtils = useUtils();

const headers: any[] = [
  { key: 'id', title: t("commons.common.id"), width: "auto", align: "start", sortable: true },
  { key: 'first_name', title: t("modules.auth.first_name"), width: "auto", align: "start",  searchable: true, sortable: true, },
  { key: 'last_name', title: t("modules.auth.last_name"), width: "auto", align: "start", sortable: true, },
  { key: 'email', title: t("commons.common.email"), width: "auto", align: "start", sortable: false, },
  { key: 'phone', title: t("commons.common.phone"), width: "auto", align: "start", sortable: false, },
  { key: 'is_superuser', title: t("modules.auth.role"), width: "auto", align: "start", sortable: false, },
  { key: 'is_active', title: t("modules.auth.active"), width: "auto", align: "center", type: "check", sortable: false, },
  { key: "actions", title: t("commons.common.actions"), width: "90px", type: "actions", sortable: false, },
];
const drawRefresh = ref("");
const staffId = ref();
const deleteModal = ref(false);
const itemToDelete = ref();

const profileModal = ref(false);
const passwordModal = ref(false);

onMounted(async () => {});

const clickNew = () => {
  staffId.value = null;
  profileModal.value = true;
};

const clickEdit = async (item: any) => {
  staffId.value = item.id;
  profileModal.value = true;
};

const clickAction = (item: any, action: string) => {
  staffId.value = item.id;
  passwordModal.value = true;
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

const onSaveProfile = (uuid: string) => {
  drawRefresh.value = uuid;
  profileModal.value = false;
}
</script>

<style lang="scss">

</style>