<template>
  <div class="job">
    {{job.name}}
  </div>
</template> 

<script>
export default {
  name: 'job-component',
  props: ['job'],
  watch: {
    job: {
      handler: function () {
        console.log('job changed');
      },
      deep: true,
    },
  },
};
</script>
