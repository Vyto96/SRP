<template>
  <div>
      <h1>Show report for store {{ store }} with id = {{ id }}</h1>
      <div v-show="!show_report">
        <b-form @submit="onSubmit">
          <!-- START DATE -->
          <b-form-group id="startDateGroup"
                        label="Report start date:"
                        label-for="startDate"
                        >
            <b-form-input v-model="start_date"
                         type="date"
                         placeholder="Enter date"
                         required
                         >
           </b-form-input>
          </b-form-group>
          <!-- END-DATE -->
          <b-form-group id="endDateGroup"
                        label="Report end date:"
                        label-for="endDate"
                        >
            <b-form-input v-model="end_date"
                         type="date"
                         placeholder="Enter date"
                         required
                         >
           </b-form-input>
          </b-form-group>

         <b-button type="submit" variant="primary">Submit</b-button>
        </b-form>
      </div>
      <div v-show="show_report">
          <show-records v-bind:records="records"> </show-records>
          <b-button  variant="primary" v-on:click="show_report=false">
              get another report
          </b-button>
      </div>


  </div>
</template>
<script>
import ShowRecords from '@/components/ShowRecords.vue'


export default {
  props: ['id', 'store'],
  components: {
    'show-records': ShowRecords,
  },
  data: () => ({
    start_date: '',
    end_date: '',
    records: [],
    show_report: false,
  }),

  methods: {
    parseDate(){
      var d = this.start_date.slice(8, 10);
      var m = this.start_date.slice(5, 7);
      var y = this.start_date.slice(0, 4);
      this.start_date = y + m + d;

      d = this.end_date.slice(8, 10);
      m = this.end_date.slice(5, 7);
      y = this.end_date.slice(0, 4);
      this.end_date = y + m + d;
    },
    onSubmit (evt) {
      evt.preventDefault();

      this.parseDate();

      var url = 'https://salesreporter.ns1.mooo.com/api/get_report/' + this.id;
      console.log(url);

      this.$http.get(url,
        {params: {start_date: this.start_date,
                  end_date: this.end_date}, } //headers: {'X-Custom': '...'}},
        ).then(function(data){

          alert('chiamata fatta');
          console.log(data.body.report.report);
          this.records = data.body.report.report;
          this.show_report = true;
        });
    },
  },



}
</script>
<style lang="scss" scoped>
</style>
