<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="dark">

          <b-nav-toggle target="nav_collapse"></b-nav-toggle>

      <b-link class="navbar-brand" to="#">
        <span>SalesReporter</span>
      </b-link>

      <b-collapse is-nav id="nav_collapse">
        <!-- COLLAPSE ITEM -->
        <b-navbar-nav>
          <b-nav-item>
            <router-link to="/">Home</router-link>
          </b-nav-item>
          <b-nav-item>Link
            <router-link to="/about">About SR</router-link>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>



<script>
export default {
  data: () => ({
  })
}
</script>

<style lang="scss" scoped>
</style>
