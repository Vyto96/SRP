<template>
  <div id="show-stores">
    <ul>
      <li v-for="store in stores" class="single-store">
        <h2>{{ store.store_name }}</h2>
        <h3>{{ store.reference_ecommerce_name }}</h3>
        <h3>{{ store.id }}</h3>
        <b-button  variant="primary" href="">
            GET REPORT
        </b-button>
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
    data () {
        return {

        }
    },

    props: ['stores'],

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
