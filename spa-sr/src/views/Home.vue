<template>
  <div class="home">
    <h1>{{ user }}'s configured stores:</h1>
    <p>{{ stores }}</p>
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
        this.stores = data.user_stores;
        console.log(data);
      });

    // const axios = require('axios');


// Make a request for a user with a given ID
    // axios.get(url)
      // .then(function (response) {
        // handle success
        // this.stores = response.data.user_stores;
        //     console.log(this.stores);
        // console.log(response.data.user_stores);
      // })
      // .catch(function (error) {
      //   // handle error
      //   console.log(error);
      // })
      // .then(function () {
      //   // always executed
      // });
  }

}
</script>
