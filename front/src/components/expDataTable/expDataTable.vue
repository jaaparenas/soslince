<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useLoading } from "vue-loading-overlay";
import useDataTable from "@/composables/useDataTable";
import expInputDelay from "@/components/expInput/inputDelay.vue";

const loading = useLoading();
const { t } = useI18n();

const props = defineProps({
  uuid: {
    type: String,
    default: "",
  },
  endpoint: {
    type: String,
    default: "",
  },
  drawRefresh: {
    type: String,
    default: "",
  },
  headers: {
    type: Array
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showFilters: {
    type: Boolean,
    default: true
  },
  itemsPerPage: {
    type: Number,
    default: 10,
  },
  defaultMenuItems: {
    type: Array,
    default: () => [
      { title: "commons.forms.view", action: "view", icon: "mdi-eye" },
      { title: "commons.forms.edit", action: "edit", icon: "mdi-pencil" },
      { title: "commons.forms.delete", action: "delete", icon: "mdi-delete" },
      { title: "commons.forms.print", action: "print", icon: "mdi-printer" },
    ],
  },
  extraMenuItems: {
    type: Array
  },
  extraParameters: {
    type: Object,
    default: () => ({}),
  },
  menuItems: {
    type: Array,
    default: () => ["view", "edit", "delete", "print"],
  },
  labelNew: {
    type: String,
    default: "commons.forms.new",
  },
});

const emit = defineEmits([
  "onClickNew",
  "onClickView",
  "onClickEdit",
  "onClickDelete",
  "onClickPrint",
  "onClickAction",
]);

const uDataTable = useDataTable(
  props.uuid,
  props.headers,
  props.endpoint
);

const search = ref("");
const serverItems = ref([]);
const paramsTable = ref();
const totalItems = ref(0);

const loadItems = ({
  page,
  itemsPerPage,
  sortBy,
  search,
  extra,
}: {
  page: number;
  itemsPerPage: number;
  sortBy: string;
  search: string;
  extra: null;
}) => {
  paramsTable.value = { page, itemsPerPage, sortBy, search, extra: props.extraParameters };
  let loader = loading.show({});

  uDataTable
    .getData(paramsTable.value)
    .then(({ items, total }) => {
      serverItems.value = items;
      totalItems.value = total;
    })
    .finally(() => {
      loader.hide();
    });
};

const activeMenuItems = computed(() => {
  let activeItems: any[] = [];
  const allMenuItems = [...props.defaultMenuItems, ...props.extraMenuItems];
  props.menuItems.forEach((menuItem: any) => {
    let item = allMenuItems.find((i: any) => i.action === menuItem);
    if (item) {
      activeItems.push(item);
    }
  });
  return activeItems;
});

const fnAction = (action: string, item: any) => {
  switch (action) {
    case "new":
      emit("onClickNew");
      break;
    case "view":
      emit("onClickView", item);
      break;
    case "edit":
      emit("onClickEdit", item);
      break;
    case "delete":
      emit("onClickDelete", item);
      break;
    case "print":
      emit("onClickPrint", item);
      break;
    default:
      emit("onClickAction", item, action);
  }
};

watch(() => props.drawRefresh, () => {
  loadItems(paramsTable.value);
});
</script>

<template>
  <v-card elevation="0" v-if="showHeader">
    <slot name="header">
      <v-card-text>
        <v-row>
          <v-col>
            <v-btn @click="fnAction('new', null)" color="primary">
              <v-icon class="mr-2">mdi-plus</v-icon>
              {{ $t(labelNew) }}
            </v-btn>
          </v-col>
          <v-col>
            <slot name="btns"></slot>
          </v-col>
        </v-row>
      </v-card-text>
    </slot>
  </v-card>
  <v-card>
    <v-card-text class="pa-0" >
      <slot name="filters" v-if="showFilters">
        <exp-input-delay
          v-model="search"
          :delay="500"
          label="Search"
          prepend-inner-icon="mdi-magnify"
          single-line
          hide-details
          variant="underlined"
          class="mx-4"
        />
      </slot>
      <v-data-table-server
        :items-per-page="itemsPerPage"
        :headers="headers.filter((x: any) => x.visible !== false)"
        :items-length="totalItems"
        :items="serverItems"
        :search="search"
        :hover="true"
        :show-current-page="true"
        class="elevation-1"
        @update:options="loadItems"
      >
        <template
          v-for="header in (headers as any).filter((x: any) => x.key != 'actions')"
          v-slot:[`item.${header.key}`]="{ item }"
        >
          <slot
            :name="`item.${(header as any).key}`"
            :item="item"
            :key="(header as any).key"
          >
            <template v-if="(header as any).type">
              <template v-if="(header as any).type == 'check'">
                <div class="text-center">
                  <v-icon
                    :icon="item[(header as any).key] ? 'mdi-check-circle' : 'mdi-close-circle'"
                    :color="item[(header as any).key] ? 'blue' : 'red'"
                  />
                </div>
              </template>
              <template v-else>
                {{ item[(header as any).key] }}
              </template>
            </template>
            <template v-else>
              {{ item[(header as any).key] }}
            </template>
          </slot>
        </template>
        <template v-slot:item.actions="{ item }">
          <slot :name="`actions`" :data="item">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon="mdi-menu" size="small" v-bind="props"></v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(action, index) in activeMenuItems"
                  :key="index"
                  :value="index"
                  :title="action?.title ? $t(action.title) : ''"
                  :prepend-icon="action?.icon ? action.icon : ''"
                  @click="fnAction(action.action, item)"
                />
              </v-list>
            </v-menu>
          </slot>
        </template>
      </v-data-table-server>
    </v-card-text>
  </v-card>
</template>
