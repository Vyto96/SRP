<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="dark">

      <b-nav-toggle target="nav_collapse"></b-nav-toggle>

      <b-link class="navbar-brand">
        <span>SalesReporter</span>
      </b-link>

      <b-collapse is-nav id="nav_collapse">
      </b-collapse>
    </b-navbar>
  </div>
</template>



<script>
export default {
  data: () => ({

  }),
  props: ['user']
}
</script>

<style lang="scss" scoped>
</style>
