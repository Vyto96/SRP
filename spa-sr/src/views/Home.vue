<template>
  <div class="home">
    <h1>{{ user }}'s configured stores:</h1>
    <show-stores v-bind:stores="stores"
  </div>
</template>

<script>
// @ is an alias to /src
import ShowStores from '@/components/ShowStores.vue'
// import axios from 'axios';

export default {
  name: 'home',
  components: {
    show-stores: ShowStores,
  },
  data() {
      return {
        user: this.$route.params.user,
        id: this.$route.params.id,
        stores : [],
      }
  },
  methods: {
    methodName() {

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


}
</script>
