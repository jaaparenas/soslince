<template>
  <v-text-field
    v-model="formData.password"
    :label="$t('modules.auth.new_password')"
    type="password"
    variant="outlined"
    density="compact"
    @keyup="modelValue=getReturnData()"
  ></v-text-field>
  <ul v-if="passwordValidations.length > 0" class="ml-8 mb-5">
    <li v-for="(error, index) in passwordValidations" :key="index" style="color: #b00020;">
      {{ error }}
    </li>
  </ul>
  <v-text-field
    v-model="formData.confirmPassword"
    :label="$t('modules.auth.confirm_password')"
    type="password"
    :hide-details="true"
        variant="outlined"
    density="compact"
    @keyup="modelValue=getReturnData()"
  ></v-text-field>
</template>

<script lang="ts" setup>
import { toRefs, reactive, computed, ref } from "vue";
import { required, email, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

const modelValue = defineModel();

const hasLetter = (value:any) =>
  /[a-z]/.test(value) || "Must contain at least one lower letter";
const hasUppercase = (value:any) =>
  /[A-Z]/.test(value) || "Must contain at least one capital letter";
const hasNumber = (value:any) =>
  /\d/.test(value) || "Must contain at least one number";
const hasSpecialChar = (value:any) =>
  /[!@#%^&*()_+\-=|;':",./?]/.test(value) ||
  "Must contain one special character (!@#%^&*()_+-=|;':\",./?)";
const passwordsMatch = (password:any, confirm:any) =>
  password === confirm || "Passwords must match";

const rules = {
  password: {
    required,
    minLength: minLength(10),
    hasLetter,
    hasUppercase,
    hasNumber,
    hasSpecialChar,
  },
  confirmPassword: {
    required,
    passwordsMatch: (value:any) => passwordsMatch(formData.password, value),
  },
};

const formData = reactive({
  password: "",
  confirmPassword: "",
});
const validate = useVuelidate(rules, toRefs(formData));

const isValid = computed(() => {
  return validate.value != null && !validate.value.$invalid;
});

const passwordValidations = computed(() => {
  let errors = [];

  if (formData.password.length < 10)
    errors.push("Must be at least 10 characters");

  if ((validate.value as any).password.hasLetter["$response"] !== true)
    errors.push((validate.value as any).password.hasLetter["$response"]);

  if ((validate.value as any).password.hasUppercase["$response"] !== true)
    errors.push((validate.value as any).password.hasUppercase["$response"]);

  if ((validate.value as any).password.hasNumber["$response"] !== true)
    errors.push((validate.value as any).password.hasNumber["$response"]);

  if ((validate.value as any).password.hasSpecialChar["$response"] !== true)
    errors.push((validate.value as any).password.hasSpecialChar["$response"]);

  if ((validate.value as any).confirmPassword.passwordsMatch["$response"] !== true)
    errors.push((validate.value as any).confirmPassword.passwordsMatch["$response"]);

  return errors;
});

const getReturnData = () => {
  return {
    valid: isValid.value && passwordValidations.value.length == 0,
    password: formData.password
  }
}
</script>
