<template>
  <div class="home">
    <h1>{{ user }}'s configured stores:</h1>
    {{ stores }}
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
    var url = 'https://salesreporter.ns1.mooo.com/api/users/' + this.id + '/stores/';
    console.log(url);

    this.$http.get(url).then(function(data){
        this.stores = data.body.user_stores;
        console.log(data.body.user_stores);
        console.log(data);
        // console.log(this.stores);
      });
  },
  beforeMount() {
    //do something before mounting vue instance
    alert('beforMount');
  },
  mounted() {
    //do something after mounting vue instance
    alert('mounted');
  }

}
</script>
