<template>
  <v-app v-show="isAuthenticated">
    <exp-menu v-model="drawer"></exp-menu>
    <v-app-bar app color="white" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>&nbsp;</v-toolbar-title>
      <v-menu min-width="100px" rounded>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" class="mr-2">
            <v-avatar size="42" v-if="user?.image != ''">
              <v-img
                :alt="user.initials"
                :src="user.image"
              ></v-img>
            </v-avatar>
            <v-avatar size="42" color="primary" v-else>
              {{ user.initials }}
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-card-text>
            <v-list>
              <v-list-item
                :subtitle="user?.email"
                :title="user?.fullName"
              >
                <template v-slot:prepend>
                  <v-avatar size="42" v-if="user.image != ''">
                    <v-img
                      :alt="user.initials"
                      :src="user.image"
                    ></v-img>
                  </v-avatar>
                  <v-avatar size="42" color="primary" v-else>
                    {{ user.initials }}
                  </v-avatar>
                </template>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-list :lines="false" density="compact" nav>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
                :value="item"
                @click="item.fn"
              >
                <template v-slot:prepend v-if="item.text != '-'">
                  <v-icon :icon="item.icon"></v-icon>
                </template>
                <v-list-item-title v-text="$t(item.text)" v-if="item.text != '-'"></v-list-item-title>
                <v-divider v-if="item.text == '-'"></v-divider>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-menu>
    </v-app-bar>
    <v-main>
      <v-card elevation="0" class="ma-auto" max-width="1600">
        <v-card-text>
          <router-view />
        </v-card-text>
      </v-card>
    </v-main>
  </v-app>

  <profileForm
    v-if="profileModal"
    v-model="profileModal"
    :id="staffId"
  />
  <passwordForm
    v-if="passwordModal"
    v-model="passwordModal"
    :id="staffId"
  />
</template>

<script setup lang="ts">
import { watch, computed, onMounted, ref } from "vue";

import { useRouter } from "vue-router";
import useAuth from "@/modules/auth/composables/useAuth";
import useUtils from "@/composables/useUtils";
import useGlobalState from "@/stores/global";
import expMenu from "@/components/expMenu";

import profileForm from "@/modules/core/components/profile.vue";
import passwordForm from "@/modules/core/components/password.vue";

const uRouter = useRouter();
const uAuth = useAuth();
const sGlobalState = useGlobalState();
const uUtils = useUtils();

const drawer = ref(true);

const staffId = ref();
const profileModal = ref(false);
const passwordModal = ref(false);

const isAuthenticated = computed(() => {
  if (uAuth.isAuthenticated() && sGlobalState.value.auth) {
    return true;
  } else {
    sGlobalState.value.auth = false;
    return false;
  }
});

onMounted(() => {
  if (!isAuthenticated.value)
    uRouter.push({ name: "auth-login" });
});

const data = computed(() => {
  return uAuth.getUserData();
});

const logOut = () => {
  uAuth.authLogOut();
    uRouter.push({ name: "auth-login" });
};

const myProfile = () => {
  staffId.value = uAuth.getUserData().id;
  profileModal.value = true;
};

const myPassword = () => {
  staffId.value = uAuth.getUserData().id;
  passwordModal.value = true;
};

const items = [
  { text: "modules.auth.profile", icon: "mdi-account", fn: myProfile },
  { text: "modules.auth.password", icon: "mdi-lock", fn: myPassword },
  { text: "-" },
  { text: "modules.auth.logout", icon: "mdi-logout", fn: logOut },
]

const user = computed(() => {
  return {
    fullName: data.value.first_name + " " + data.value.last_name,
    email: data.value.email,
    initials: data.value.first_name?.substring(0, 1) + data.value.last_name?.substring(0, 1),
    image: uUtils.getUrlImg(data.value.image ?? "")
  };
})

watch(isAuthenticated, () => {
  if (!isAuthenticated.value)
    uRouter.push({ name: "auth-login" });
});
</script>

<style lang="scss">
.vuejs3-datepicker {
  width: 100% !important;

  label {
    position: absolute !important;
    top: 0 !important;
    font-size: 12px;
  }

  .vuejs3-datepicker__value {
    padding-left: 0;
    padding-right: 0;
    border: 0 !important;
    border-bottom: 1px solid #ababab !important;
    border-radius: 0;
    width: 100%;
    padding-top: 16px !important;
    padding-bottom: 2px !important;
  }

  .vuejs3-datepicker__calendar {
    position: fixed !important;

    .selected {
      background: #1867c0 !important;
    }

    .vuejs3-datepicker__calendar-topbar {
      display: none !important;
    }

    .cell:hover {
      border-color: #1867c0 !important;
    }
  }
}
</style>