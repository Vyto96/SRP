<template>
  <div class="home">
    <h1>{{ user }}'s configured stores:</h1>
    <show-stores v-show="!report"
                v-bind:stores="stores"
                v-on:selectID="getReport($event)">
     </show-stores>

     <div v-show="report">
       <show-report v-bind:id="report_id">
       </show-report>
       <b-button  variant="primary" v-on:click="report=false">
           show user store
       </b-button>
     </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ShowStores from '@/components/ShowStores.vue'
import ShowReport from '@/components/ShowReport.vue'
// import axios from 'axios';

export default {
  name: 'home',
  components: {
    'show-stores': ShowStores,
    'show-report': ShowReport,
  },
  data() {
      return {
        user: this.$route.params.user,
        id: this.$route.params.id,
        stores : [],
        report: false,
        report_id: ''
      }
  },
  methods: {
    getReport: function(id_selected) {
      this.report_id = id_selected;
      this.report = true;


    }
  },

  created() {
    //do something after creating vue instance
    var url = 'https://salesreporter.ns1.mooo.com/api/users/' + this.id + '/stores/';
    // console.log(url);

    this.$http.get(url).then(function(data){
        this.stores = data.body.user_stores;
        console.log(data.body.user_stores);
        console.log(data);
        // console.log(this.stores);
      });
  },


}
</script>
