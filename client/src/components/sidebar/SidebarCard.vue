<template>
  <b-card no-body class="mb-1">
    <b-card-header header-tag="header" class="p-1" role="tab">
      <b-button block v-b-toggle="id">
        {{title }}
        <span class="when-opened">
          <i class="fa fa-chevron-down float-right" aria-hidden="true"></i>
        </span>
        <span class="when-closed">
          <i class="fa fa-chevron-left float-right" aria-hidden="true"></i>
        </span>
      </b-button>
    </b-card-header>
    <b-collapse :id="id" :visible="isOpened" :accordion="id" role="tabpanel">
      <b-card-body>
        <b-card-text>
          <p v-if="!contentList" v-html="htmlDescription"></p>
          <br />
          <job-component :job="wp" v-for="(wp,i) in contentList" v-bind:key="i"></job-component>
        </b-card-text>
      </b-card-body>
    </b-collapse>
  </b-card>
</template> 

<script>
import JobComponent from '@/components/Job.vue';

export default {
  name: 'SidebarCard',
  props: ['id','isOpened','title','htmlDescription','contentList'],
  components: {
    JobComponent,
  },
  watch: {
    'contentList': {
      handler() {
        console.log('contentList changed',this.contentList.length, this.contentList);
        //this.isOpened = true;
      },
      deep: true,
    },
  },
  methods: {},
};
</script>
