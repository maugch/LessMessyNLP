<template>
  <div class="WordsAlignViewer">
    <b-button @click="alignWords">Connect</b-button>
    <b-button @click="refresh">Refresh</b-button>
    <b-button @click="test">test</b-button>
    {{ leftWord }} - {{ rightWord }}
    <b-container fluid>
      <b-row>
        <b-col>
          <p class="text-left first" @mouseup="onMouseUp('first')">
            <text-highlight :queries="queryFirst">
              {{ first.source }}
            </text-highlight>
          </p>
        </b-col>
        <b-col>
          <p class="text-left second" @mouseup="onMouseUp('second')">
            <text-highlight :queries="querySecond">
              {{ second.source }}
            </text-highlight>
          </p>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import TextHighlight from 'vue-text-highlight';

export default {
  name: 'WordsAlignViewer',
  props: ['first', 'second', 'words'],
  data() {
    return {
      queryFirst: [],
      querySecond: [],
      leftWord: '',
      rightWord: '',
      alignmentList: [],
    };
  },
  components: { TextHighlight },
  methods: {
    onMouseUp(where) {
      var s = window.getSelection().toString();
      if (where === 'first') {
        this.leftWord = s;
      } else {
        this.rightWord = s;
      }
    },
    alignWords() {
      console.log('align words');
      this.alignmentList.push([this.leftWord, this.rightWord]);
      this.$emit('alignChanged', this.alignmentList);
      this.leftWord = '';
      this.rightWord = '';
    },

    refresh() {
      console.log('refresh');
      this.alignmentList = this.words;
    },
    fillQueries() {
      this.queryFirst = [];
      this.querySecond = [];
      this.alignmentList.forEach((el) => {
        this.queryFirst.push(el[0]);
        this.querySecond.push(el[1]);
      });
    },
    test() {
      console.log('queryfirst,querysecond', this.queryFirst, this.querySecond);
    },
  },
  computed: {},
  created() {},
  destroyed() {},
  updated() {
    this.alignmentList = this.words;
  },
  mounted() {
    this.alignmentList = this.words;
  },
  watch: {
    alignmentList: {
      handler: function () {
        this.fillQueries();
      },
      deep: true,
    },
  },
};
</script>