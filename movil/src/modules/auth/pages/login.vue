<template>
  <div class="d-flex align-center justify-center wrap-login" style="height: 100vh">
    <v-sheet width="300" class="mx-auto sheet-login">
      <v-form fast-fail @submit.prevent="true">
        <v-card class="elevation-12 card-login">
          <h2 class="text-center bg-primary text-white">
            <v-img class="mx-auto" src="/src/assets/img/logo.png"></v-img>
          </h2>
          <v-card-text class="pa-4 text-center">
            Lince S.O.S. solicita acceso a tu ubicación
            para poder asistirte en situaciones de emergencia.
            Incluso si la app está cerrada, registramos tus
            movimientos para ayudarte en caso de desaparición.
            Este permiso garantiza una respuesta rápida y efectiva.
            Tu seguridad es nuestra prioridad y tu información
            se usa solo con este fin.
          </v-card-text>
          <v-card-text class="pa-4">
            <div v-if="loginMethod === 'username'">
              <v-text-field
                variant="outlined"
                density="compact"
                v-model="formData.username"
                :label="$t('modules.auth.username_email')"
                type="text"
              ></v-text-field>
            </div>
            <div v-else class="mb-4">
              <exp-input-phone
                v-model="formData.phone"
                label="commons.common.phone"
              ></exp-input-phone>
            </div>
            <v-text-field
              variant="outlined"
              density="compact"
              v-model="formData.password"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              :label="$t('modules.auth.password')"
              @click:append-inner="showPassword = !showPassword"
            />
             <div class="text-center mt-n2 mb-4">
              <a href="#" @click.prevent="toggleLoginMethod" class="toggle-link">
                <span v-if="loginMethod === 'username'">{{ $t('modules.auth.login_with_phone') }}</span>
                <span v-else>{{ $t('modules.auth.login_with_username') }}</span>
              </a>
            </div>
            <div class="mt-2 text-center">
              <v-btn
                type="submit"
                color="#20282d"
                size="large"
                block
                @click="onLogin"
                :disabled="!enableLogin"
                >{{ $t("modules.auth.sing_in") }}</v-btn
              >
            </div>
          </v-card-text>
        </v-card>
      </v-form>
    </v-sheet>
  </div>
</template>

<script lang="ts" setup>
import { toRefs, ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import useGlobal from "@/composables/useGobal";
import useAuth from "@/modules/auth/composables/useAuth";
import ExpInputPhone from '@/components/expInput/phone.vue';
import { Preferences } from '@capacitor/preferences';

import { useLoading } from "vue-loading-overlay";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";

const loading = useLoading({
  /* options */
});
const auth = useAuth();
const router = useRouter();
const uGlobal = useGlobal();
const uToast = uGlobal.useToast();
const uErrors = uGlobal.useErrors();

const loginMethod = ref('username'); // 'username' or 'phone'

const rules = {
  username: { },
  phone: { },
  password: { required, minLength: minLength(5) },
};
const showPassword = ref(false);
const formData = reactive({
  username: "",
  phone: "",
  password: "",
});

const validate = useVuelidate(rules, toRefs(formData));

const enableLogin = computed(() => {
  if (loginMethod.value === 'username') {
    return formData.username.length >= 2 && formData.password.length >= 5;
  } else {
    return formData.phone.length > 5 && formData.password.length >= 5;
  }
});

const toggleLoginMethod = async () => {
  if (loginMethod.value === 'username') {
    loginMethod.value = 'phone';
    formData.username = '';
  } else {
    loginMethod.value = 'username';
    formData.phone = '';
  }
  await Preferences.set({ key: 'loginMethod', value: loginMethod.value });
};

onMounted(async () => {
  const { value } = await Preferences.get({ key: 'loginMethod' });
  if (value && value === 'phone') {
    loginMethod.value = 'phone';
  }
});

const onLogin = async () => {
  validate.value.$touch();
  if (enableLogin.value) {
    let loader = loading.show({});

    const loginData = {
      username: loginMethod.value === 'phone' ? formData.phone : formData.username,
      password: formData.password
    };

    auth.authLogIn(loginData)
      .then(() => {
        router.push({ name: "core-index" });
      })
      .catch(() => {
        uToast.toastError(uErrors.byText("_BAD_USERNAME_PASSWORD"));
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

  .toggle-link {
    font-size: 0.8rem;
    text-decoration: none;
    color: #555;
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>