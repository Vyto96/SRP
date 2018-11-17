<template>
  <div id="app" class="container-fluid">
<!-- NAVBAR -->
    <sr-header v-bind:user="user"></sr-header>
<!--ROUTER VIEW -->
    <router-view/>
  </div>
</template>

<script>

export default {
  data: () => ({
    
  }),
}

</script>

<style lang="scss">

</style>
