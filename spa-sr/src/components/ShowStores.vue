<template>
  <div id="show-stores">
    <ul>
      <li v-for="store in stores" class="single-store">
        <h2>{{ store.store_name }}</h2>
        <h3>{{ store.reference_ecommerce_name }}</h3>
        <h3>{{ store.id }}</h3>
        <b-button  variant="primary" v-on:click="getReport(store.id)">
            GET REPORT
        </b-button>
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  props: ['stores'],
  data () {
      return {

      }
  },
  methods: {
    getReport: function(store_id) {
      this.$emit('selectID', store_id);
    }
  }


}

</script>



<style>
#show-stores{
    max-width: 800px;
    margin: 0px auto;
}
.single-store{
    padding: 20px;
    margin: 20px 0;
    box-sizing: border-box;
    background: #eee;
}
</style>
