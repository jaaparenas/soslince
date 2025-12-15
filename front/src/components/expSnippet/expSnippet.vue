<template>
  <div class="exp-snippet">
    <div>
      <exp-calculated
        :label="title"
        :customClass="'white-background text-left'"
        :value="snippetText"
      /></div>
    <div class="exp-snippet-btn"><v-btn block @click="modalTable = true"><v-icon>mdi-table-search</v-icon></v-btn></div>
  </div>
  <exp-modal-form
    v-model="modalTable"
    :width="width"
    :title="title"
    :btnSave="false"
  >
    <exp-data-table
      :endpoint="endpoint"
      :headers="headers"
      :labelNew="'modules.appointment.new_booking'"
    >
      <template v-slot:header>&nbsp;</template>
      <template v-for="(header, index) in headers" :key="index" v-slot:[`item.${header.key}`]="{ item }">
        <div style="cursor:pointer" @click="fnOnSelect(item)">{{ item[header.key] }}</div>
      </template>
    </exp-data-table>
  </exp-modal-form>
</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue";
  import { useI18n } from "vue-i18n";

  import useCrud from "@/composables/useCrud";
  import expModalForm from "@/components/expModalForm";
  import expDataTable from "@/components/expDataTable";
  import expCalculated from "@/components/expInput/calculated.vue";

  const { t } = useI18n();

  const modelValue = defineModel<number>();

  const props = defineProps({
    title: {
      type: String,
      default: ""
    },
    width: {
      type: Number,
      default: 700
    },
    endpoint: {
      type: String,
      default: ""
    },
    fields: {
      type: Array
    },
  });

  const modalTable = ref(false);
  const snippetText = ref("");

  const headers: any[] = props.fields.map((field: any) => {
    return { key: field.key, title: (field.title), width: "auto", align: "start", sortable: false, searchable: true }
  });

  onMounted(async () => {
    if (modelValue && modelValue.value &&modelValue.value > 0) {
      const uCrud = useCrud(props.endpoint);
      uCrud.retrieve(modelValue.value).then((item: any) => {
        snippetText.value = item.first_name + " " + item.last_name;
      });
    }
  });

  const fnOnSelect = (item: any) => {
    modelValue.value = item.id;
    snippetText.value = item.first_name + " " + item.last_name;
    modalTable.value = false;
  };

  const emit = defineEmits(["onSelect"]);
</script>

<style scoped lang="scss">
.exp-snippet {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  .exp-snippet-btn {
    padding-left: 5px;
    width: 40px;
  }
}
</style>