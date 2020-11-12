<template>
  <div class="SequencesViewer">
    <div v-if="viewMode=='ta'">
      <b-form-textarea
        readonly
        rows="5"
        no-auto-shrink
        v-model="segmentsText"
        :wrap="dowrap3 ? 'soft' : 'off'"
      ></b-form-textarea>
      <b-form-checkbox v-model="dowrap3">Wrap</b-form-checkbox>
    </div>
    <div v-else>
      <b-button @click="splitSentence">Split [s]</b-button>
      <b-button :pressed.sync="toggleMerge" :variant="toggleMergeVariant">Merge sentences</b-button>
      <b-form-checkbox v-model="dowrap1">Wrap</b-form-checkbox>
      <p
        v-for="line in segments"
        v-bind:key="line.idx"
        class="mreadonly text-left"
        :class="[selectedP.includes(line.idx)?'selected':'', dowrap1?'text-wrap':'']"
        @click="selectForMerge(line.idx)"
        @mouseup="mouseUp(line.idx,$event)"
      >{{line.text}}</p>
    </div>
  </div>
</template>

<script>
import commMixin from '@/mixins/commMixin.js';
import loggingMixin from '@/mixins/loggingMixin.js';
import { store } from '../store.js';

export default {
  name: 'SegmentsViewer',
  // mixins: [commMixin, loggingMixin],
  props: ['segments', 'which', 'viewMode'],
  data() {
    return {
      myStore: store,
      segmentsText: '', // text for textarea
      paragraphSplit: { p_num: -1, offset: -1 },
      dowrap3: true,
      dowrap1: true,
      selectedP: [], //<p> selected for merging
      toggleMerge: false, //toggle button for merge.
    };
  },
  created() {
    window.addEventListener('keypress', this.onKeyPress);
  },
  destroyed() {
    window.removeEventListener('keypress', this.onKeyPress);
  },
  mounted() {
    this.fillSegmentText(this.segments);
  },
  methods: {

    splitSentence: function () {
      const p_num = this.paragraphSplit.p_num;
      const offset = this.paragraphSplit.offset;
      if (p_num == -1) return;

      console.log('split sentence');

      var data = this.segments[p_num].text;
      var data1 = data.substr(0, offset);
      var data2 = data.substr(offset, data.length);
      if (data2.length == 0) {
        return;
      }
      var d1 = { idx: p_num, text: data1 };
      var d2 = { idx: p_num, text: data2 };
      this.segments.splice(p_num, 1, d1, d2);

      //remake indexes
      this.rebuildIndex();
    },

    rebuildIndex() {
      var idx = 0;
      this.segments.forEach((element) => {
        element.idx = idx;
        idx++;
      });
    },

    selectForMerge(index) {
      if (this.toggleMerge) {
        var sel = this.selectedP;
        sel.includes(index)
          ? sel.splice(sel.indexOf(index), 1)
          : sel.push(index);

        if (sel.length == 2) {
          console.log('merging on ', this.which);
          this.toggleMerge = false;
          var idx1 = sel[0] < sel[1] ? sel[0] : sel[1];
          var idx2 = sel[1] > sel[0] ? sel[1] : sel[0];
          this.selectedP = [];
          var newElement = {
            idx: index,
            text: this.segments[idx1].text + ' ' + this.segments[idx2].text,
          };

          this.segments.splice(idx1, 2, newElement);
          this.rebuildIndex();
        }
      }
    },

    mouseUp(line_idx, ev) {
      if (this.toggleMerge) {
        return;
      }
      //experimental ? MDN says it's experimental (focusOffset etc.)
      //console.log('onselect',ev);
      var gs = window.getSelection();
      //console.log(gs.type);
      if (gs.type === 'Caret') {
        //clicks only
        return;
      }
      var startOffset =
        gs.anchorOffset < gs.focusOffset ? gs.anchorOffset : gs.focusOffset;

      this.paragraphSplit.p_num = line_idx;
      this.paragraphSplit.offset = startOffset + gs.toString().length;
      //console.log('mouseup',line_idx,startOffset,gs.toString().length,gs);
      //console.log('startoffset',gs.anchorOffset,gs.focusOffset);
    },

    onKeyPress: function (e) {
      if (this.$parent.$el.style.display === 'none') {
        //not visible. skip
      } else {
        //visible
        if (this.visibleTab == 0) {
          if (e.key == 's') {
            this.splitSentence();
            return;
          }
        }
        // console.log('keypress for', this.which, 'ignored', e.key);
      }
    },

    /** fill the object segmentText, used to show all segments together */
    fillSegmentText: function (segments) {
      var result = '';
      segments.forEach((element) => (result += element.text + '\n@@@@@\n'));
      this.segmentsText = result;
    },
  },
  computed: {
    toggleMergeVariant() {
      if (this.toggleMerge) return 'success';
      else return 'dark';
    },
  },
  watch: {
    segments: {
      handler: function (newVal, old) {
        console.log('SegmentsViewer watched.');
        this.fillSegmentText(newVal);
      },
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p.mreadonly {
  overflow-x: auto;
  white-space: nowrap;
  margin-bottom: 2px;
}
p:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.05);
}
p.selected {
  background-color: yellow;
}
</style>
