<template>
  <div>
      <h1>Show report for store with id = {{ id }}</h1>
      <div>
        <b-form @submit="onSubmit" @reset="onReset">
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
         <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </div>



  </div>
</template>
<script>
export default {
  props: ['id'],
  data: () => ({
    start_date: '',
    end_date: '',
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

          // this.stores = data.body.;
          // console.log(data.body.user_stores);
          alert('chiamata fatta');
          console.log(data.body.report.report);
          // console.log(this.stores);

      // alert('start date:' + this.start_date);
      // alert('end date: ' + this.end_date);
        });
    },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      alert('reset');
    }
  },



}
</script>
<style lang="scss" scoped>
</style>
