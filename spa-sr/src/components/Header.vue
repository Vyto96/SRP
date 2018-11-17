<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="dark">

      <b-nav-toggle target="nav_collapse"></b-nav-toggle>

      <b-link class="navbar-brand" to="#">
        <span>SalesReporter</span>
      </b-link>

      <b-collapse is-nav id="nav_collapse">
        <!-- COLLAPSE ITEM -->
        <b-navbar-nav >
          <b-nav-item>
            <router-link to="/">Home</router-link>
          </b-nav-item>
          <b-nav-item>
            <router-link to="/about">About</router-link>
          </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">

          <b-nav-item>Hy {{user}}</b-nav-item>

          <b-nav-item>
            <a href="https://salesreporter.ns1.mooo.com/web_app">Logout</a>
          </b-nav-item>

        </b-navbar-nav>


      </b-collapse>
    </b-navbar>
  </div>
</template>



<script>
export default {
  data: () => ({
    user: 'vyto' //prendere i dati dall'url più chiamata 
  }),
  props: ['user']
}
</script>

<style lang="scss" scoped>
</style>
