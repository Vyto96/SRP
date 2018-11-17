<template>
  <div class="home">
    <h1>{{ user }}'s configured stores:</h1>

  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
// import axios from 'axios';

export default {
  name: 'home',
  components: {

  },
  data() {
      return {
        user: this.$route.params.user,
        id: this.$route.params.id,
        stores : [],
      }
  },
  created() {
    //do something after creating vue instance
    var url = 'https://salesreporter.ns1.mooo.com/api/users/' + this.id + '/stores/'
    this.$http.get(url).then(function(data){
        this.stores = data.user_stores;
        console.log(this.stores);
      });
  }

}
</script>
