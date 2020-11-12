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
        <b-card-text v-if="filedata">
          <div>{{filename}}</div>
          <div>{{fileinfo.creation}}</div>
          <div v-if="filedata && filedata.align && filedata.align.length > 0">Alignments {{filedata.align.length}}</div>
          <div v-if="filedata && filedata.words.length > 0">Words {{filedata.words.length}}</div>
          <div>
            <span class="when-opened" :class="visible ? null : 'collapsed'"
              :aria-expanded="visible ? 'true' : 'false'"
              aria-controls="collapse-4"
              @click="visible = !visible">
              <i class="fa fa-gear float-right" aria-hidden="true"></i>
            </span>
            <b-collapse id="collapse-4" v-model="visible" class="mt-2">
              <b-card>
                <div v-for="(p,i) in proplist" v-bind:key="i">{{p}}</div>
              </b-card>
            </b-collapse>
          </div>
        </b-card-text>
      </b-card-body>
    </b-collapse>
  </b-card>
</template> 

<script>
export default {
  name: 'SidebarFileInfo',
  props: ['id', 'isOpened', 'title', 'filename', 'filedata','fileinfo'],
  components: {},
  data() {
    return {
      visible: false,
    };
  },
  watch: {
    filedata: {
      handler() {
        console.log('filedata changed.');
        // console.log(this.filedata);
      },
      deep: true,
    },
  },
  computed: {
    proplist: function () {
      var keys = [];
      for (var key in this.filedata) {
        keys.push(key);
      }
      return keys;
    },
  },
  methods: {},
};
</script>
