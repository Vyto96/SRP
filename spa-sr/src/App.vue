<template>
  <div id="app">

<!-- NAVBAR -->

      <b-navbar toggleable type="inverse" variant="success">

        <b-nav-toggle target="nav_collapse"></b-nav-toggle>

        <b-link class="navbar-brand" to="#">
          <span>SalesReporter</span>
        </b-link>

        <b-collapse is-nav id="nav_collapse">

          <!-- COLLAPSE ITEM -->

          <b-nav-item>
            <router-link to="/">Home</router-link> |
          </b-nav-item>
          <b-nav-item>Link
            <router-link to="/about">About SR</router-link>
          </b-nav-item>


          <!-- END COLLAPSE ITEM -->

        </b-collapse>

      </b-navbar>


<!--ROUTER VIEW -->

    <router-view/>


  </div>
</template>

<style lang="scss">
// #app {
//   font-family: 'Avenir', Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
// }
// #nav {
//   padding: 30px;
//   a {
//     font-weight: bold;
//     color: #2c3e50;
//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }
</style>
