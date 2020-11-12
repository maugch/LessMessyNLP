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
        <b-card-text v-if="filedata && filedata.words">
          words:
          <div v-for="(w,i) in filedata.words" :key="i">{{w[0]}} = {{w[1]}}</div>
        </b-card-text>
      </b-card-body>
    </b-collapse>
  </b-card>
</template> 

<script>

export default {
  name: 'SidebarWords',
  props: ['id','isOpened','title', 'filedata'],
};
</script>
