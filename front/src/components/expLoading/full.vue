<template>
  <div class="ore-loading">
    <div class="ore-loading-wrap">
      <v-progress-circular
        :size="30"
        :width="4"
        color="blue"
        indeterminate
        class="ore-loading-progress"
      />
    </div>
    <div class="ore-loading-title">
      <slot name="title">{{ $t('core.common.loading') }}</slot>
    </div>
    <div class="ore-loading-message">
      <slot name="message">{{ $t('core.common.loading') }}</slot>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
.ore-loading {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 9999;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  text-align: center;
  background-image: url("/img/loadingbg.png");
  background-size: cover;
  background-position: bottom;

  .ore-loading-wrap {
    position: absolute;
    width: 100%;
    bottom: 115px;

    @media only screen and (max-width: 599px) {
      bottom: 150px;
    }
  }

  .ore-loading-title {
    position: absolute;
    width: 100%;
    bottom: 50px;
    text-align: center;
    font-size: 40px;
    font-weight: bold;

    @media only screen and (max-width: 599px) {
      font-size: 30px;
      bottom: 70px;
    }
  }

  .ore-loading-message {
    position: absolute;
    width: 100%;
    bottom: 5px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    height: 50px;

    @media only screen and (max-width: 599px) {
      font-size: 15px;
      bottom: 15px;
      padding: 5px;
    }
  }
}
</style>