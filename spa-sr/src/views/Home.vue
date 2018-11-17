<template>
  <div class="home">
    <h1>This is an home page of {{ user }}</h1>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {

  },
  data: () => ({
      user: this.$route.paarams.id//prendere i dati dall'url più chiamata
  }),

}
</script>
