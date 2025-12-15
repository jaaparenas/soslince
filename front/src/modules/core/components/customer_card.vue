<template>
  <v-img class="mx-auto" height="200" width="200" :src="uUtils.getUrlImg(item.customer.image)"></v-img>
  <v-card-item>
    <v-card-title>{{ item.customer.user.first_name }} {{ item.customer.user.last_name }}</v-card-title>
    <v-card-subtitle>
      <table class="text-left">
        <tr>
          <th width="80px">{{ $t('commons.common.active') }}</th>
          <td>
            <v-icon v-if="item.customer.user.is_active == false" color="red">mdi-close-circle</v-icon>
            <v-icon v-else color="green">mdi-check-circle</v-icon>
          </td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.email') }}</th>
          <td>{{ item.customer.user.email }}</td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.birth_date') }}</th>
          <td>{{ item.customer.birth_date }}</td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.blood_type') }}</th>
          <td>{{ getBloodType(item.customer.blood_type) }}</td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.phone') }}</th>
          <td>{{ item.customer.phone }}</td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.company') }}</th>
          <td>{{ item.customer.company }}</td>
        </tr>
        <tr>
          <th>{{ $t('commons.common.secret_word') }}</th>
          <td><div>{{ item.customer.secret_word }}</div></td>
        </tr>
      </table>
    </v-card-subtitle>
  </v-card-item>
</template>

<script lang="ts" setup>
import useUtils from "@/composables/useUtils";

const uUtils = useUtils();

defineProps({
  item: {
    type: Object,
    default: null,
  },
});

const getBloodType = (id: string) => {
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
  return listBloodType.filter((item: any) => item.id == id)[0].label;
}

</script>