<template>
  <div class="d-flex align-center justify-center wrap-login" style="height: 100vh">
    <v-sheet width="350" class="mx-auto sheet-login">
      <v-form fast-fail @submit.prevent="true">
        <v-card class="elevation-12 card-login">
          <h2 class="text-center bg-primary text-white">
            <v-img class="mx-auto"src="/src/assets/img/logo.png"></v-img>
          </h2>
          <v-card-text class="pa-8">
            <v-text-field
              variant="outlined"
              density="compact"
              v-model="formData.username"
              :label="$t('modules.auth.username')"
              type="text"
            ></v-text-field>
            <v-text-field
              variant="outlined"
              density="compact"
              v-model="formData.password"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              :label="$t('modules.auth.password')"
              @click:append-inner="showPassword = !showPassword"
            />
            <div class="mt-2 text-center">
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                @click="onLogin"
                :disabled="!enableLogin"
                >{{ $t("modules.auth.sing_in") }}</v-btn
              >
            </div>
            <!-- <div class="mx-auto text-center mt-4">{{ $t('modules.auth.forgotten_password') }}</div> -->
          </v-card-text>
        </v-card>
      </v-form>
    </v-sheet>
  </div>
</template>

<script lang="ts" setup>
import { toRefs, ref, reactive, computed } from "vue";

import { useRouter } from "vue-router";
import useGlobal from "@/composables/useGobal";
import useAuth from "@/modules/auth/composables/useAuth";

import { useLoading } from "vue-loading-overlay";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";

const loading = useLoading({
  /* options */
});
const auth = useAuth();
const router = useRouter();
const UseGlobal = useGlobal();
const toast = UseGlobal.useToast();
const errors = UseGlobal.useErrors();

const rules = {
  username: { required, minLength: minLength(2) },
  password: { required, minLength: minLength(5) },
};
const showPassword = ref(false);
const formData = reactive({
  username: "",
  password: "",
});

const validate = useVuelidate(rules, toRefs(formData));

const enableLogin = computed(() => {
  return validate.value != null && !validate.value.$invalid;
});

const onLogin = async () => {
  validate.value.$touch();
  if (!validate.value.$invalid) {
    let loader = loading.show({});
    auth.authLogIn(formData)
      .then(() => {
        router.push({ name: "core-index" });
      })
      .catch((err) => {
        toast.toastError(errors.byText(err.response.data.msg));
      })
      .finally(() => {
        loader.hide();
      });
  }
};
</script>

<style scoped lang="scss">
.wrap-login {
  background-image: linear-gradient(140deg, #007d7e 0%,  #011432 75%);

  .sheet-login {
    border-radius: 16px;
  }

  .card-login {
    border-radius: 15px;
    background-color: #ffffff;
  }
}
</style>