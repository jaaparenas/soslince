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
  </v-container>
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
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";

import expDataTable from "@/components/expDataTable";
import profileForm from "@/modules/core/components/profile.vue";
import passwordForm from "@/modules/core/components/password.vue";

const endpoint = "/api/1.0/core";
const { t } = useI18n();

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
  //console.log(item);
};

const onSaveProfile = (uuid: string) => {
  drawRefresh.value = uuid;
  profileModal.value = false;
}
</script>

<style lang="scss">

</style>