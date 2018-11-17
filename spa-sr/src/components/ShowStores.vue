<template>
  <div id="show-stores">
    <div v-for="store in stores" class="single-store">
      <h2>{{ store.store_name }}</h2>
      <b-button  variant="primary" href="">
          GET REPORT
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
    data () {
        return {
            stores: []
        }
    },
    
    props: ['username'],
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
