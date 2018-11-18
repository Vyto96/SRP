<template>
  <div id="show-records">
    <ul>
      <li v-for="record in records" class="single-record">

        <h2>Date: {{ record.date }}</h2>
        <h3>Total views: {{ record.tot_views }}</h3>
        <h3>Transactions: {{ record.transactions }}</h3>
        <h3>Sales Conversion Rate: {{ record.scr }}</h3>

      </li>
    </ul>
  </div>
</template>
<script>
export default {
  props: ['records'],
  data: () => ({

  })
}
</script>
<style lang="scss" scoped>

#show-records{
    max-width: 800px;
    margin: 0px auto;
}
.single-record{
    padding: 20px;
    margin: 20px 0;
    box-sizing: border-box;
    background: #eee;
}
</style>
