<template>
  <div class="home">
    <h1>This is an home page of {{ $route.params.id }}</h1>
    <h1>user {{ user }}</h1>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {

  },
  data() {
      return {
        user: this.$route.params.id,//prendere i dati dall'url più chiamata
      }
  },

}
</script>
