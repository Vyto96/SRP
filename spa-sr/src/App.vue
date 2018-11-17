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
      user: 'vyto' //prendere i dati dall'url più chiamata
  }),
}

</script>

<style lang="scss">

</style>
