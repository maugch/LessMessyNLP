<template>
  <footer id="footer_id" class="container-fluid overflow-auto flex-shrink-0 flex-grow-0">
    <template v-for="(line,i) in loglines">
      {{line}}
      <br v-bind:key="i" />
    </template>
  </footer>
</template>

<script>
export default {
  name: 'FooterLogger',
  props: ['loglines'],
  watch: {
    loglines: function () {
      //scroll to bottom
      var obFooter = document.getElementById('footer_id');
      this.$nextTick(() => {
        obFooter.scrollTop = obFooter.scrollHeight;
      });
    },
  },
};
</script>
