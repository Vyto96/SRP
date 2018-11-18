<template>
  <div id="show-report">
      <h1>Show report for store with id = {{ id }}</h1>

      <div>
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">
          <b-form-group id="startDateGroup"
                        label="Report start date:"
                        label-for="startDate"
                        description="Insert Start date of report.">
            <b-form-input v-model="start-date"
                         type="date"
                         placeholder="Enter date"
                         >
           </b-form-input>

           <b-button type="submit" variant="primary">Submit</b-button>
           <b-button type="reset" variant="danger">Reset</b-button>
          </b-form-group>
        </b-form>
      </div>



  </div>
</template>
<script>
export default {
  props: ['id'],
  data: () => ({

  })
}
</script>
<style lang="scss" scoped>
</style>
