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
    onSubmit (evt) {
      evt.preventDefault();
      alert('start date: ' + this.start_date.year + '_' + this.start_date.month + '_'+ this.start_date.day );
      console.log(this.end_date);
      // alert('end date: ' + this.end_date);

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
