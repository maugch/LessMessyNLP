<template>
  <div class="SentenceAlignViewer">
    <div v-if="viewMode == 'norm'">
      <b-button @click="connectSentences">Connect</b-button>
      <b-button @click="disconnectSentences">Disconnect</b-button>
      <b-button @click="drawAllArrows">Refresh</b-button>
      <b-container fluid>
        <b-row>
          <b-col class="firstc">
            <b-form-checkbox-group v-model="selected1">
              <p
                v-for="line in first.segments"
                v-bind:key="line.idx"
                class="mreadonly p_list1"
                ref="p_list1"
                align-v="center"
              >
                <span class="d-flex text-left text-wrap"
                  >{{ line.text }}
                  <b-form-checkbox
                    v-bind:key="line.idx"
                    :value="line.idx"
                    align-v="center"
                  ></b-form-checkbox>
                </span>
              </p>
            </b-form-checkbox-group>
          </b-col>
          <b-col cols="1" class="firstc secondc">
            <svg
              width="100%"
              height="100%"
              style="stroke-width: 0px; background-color: Gainsboro"
              ref="startpos"
              id="startpos"
            >
              <defs>
                <marker
                  id="arrowhead"
                  markerWidth="10"
                  markerHeight="7"
                  refX="0"
                  refY="3.5"
                  orient="auto"
                >
                  <polygon points="0 0, 10 3.5, 0 7" />
                </marker>
              </defs>
            </svg>
          </b-col>
          <b-col class="secondc">
            <b-form-checkbox-group v-model="selected2">
              <p
                v-for="line in second.segments"
                v-bind:key="line.idx"
                class="mreadonly p_list2"
                ref="p_list2"
              >
                <span class="d-flex text-left text-wrap">
                  <b-form-checkbox
                    v-bind:key="line.idx"
                    :value="line.idx"
                  ></b-form-checkbox>
                  {{ line.text }}
                </span>
              </p>
            </b-form-checkbox-group>
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div v-else>
      <p v-for="(line, i) in align" :key="i">{{ line }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SentenceAlignViewer',
  props: ['first', 'second', 'align', 'viewMode'],
  data() {
    return {
      selected1: [],
      selected2: [],
      dowrap: true, //unused. messy
      alignmentList: [],
    };
  },
  methods: {
    drawLine(index1, index2) {
      //var plist1 = this.$refs['p_list1'];
      //var plist2 = this.$refs['p_list2'];
      var plist1 = document.getElementsByClassName('p_list1');
      var plist2 = document.getElementsByClassName('p_list2');
      if (plist1.length == 0 && plist2.length == 0) return;
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      svg.setAttribute('stroke-width', '1px');
      svg.setAttribute('stroke', '#000000');
      svg.setAttribute('marker-end', 'url(#arrowhead)');

      //const start = this.$refs['startpos'].getBoundingClientRect().top;
      const start = document.getElementById('startpos').getBoundingClientRect()
        .top;
      const r1 = plist1[index1].getBoundingClientRect();
      const r2 = plist2[index2].getBoundingClientRect();
      const center1 = (r1.bottom - r1.top) / 2 + r1.top;
      const center2 = (r2.bottom - r2.top) / 2 + r2.top;
      //console.log('drawLine', start, r1.bottom, r1.top, r2.bottom, r2.top);
      svg.setAttribute('x1', 0);
      svg.setAttribute('y1', center1 - start); //this.$refs['myline']
      svg.setAttribute('x2', 100);
      svg.setAttribute('y2', center2 - start);
      svg.setAttribute('class', 'align-lines');

      return svg;
    },
    connectSentences() {
      console.log('connect sentences');
      console.log(this.selected1);
      console.log(this.selected2);
      this.selected1.forEach((index1) => {
        this.selected2.forEach((index2) => {
          var line = this.drawLine(index1, index2);
          this.$refs['startpos'].appendChild(line);
        });
      });
      this.alignmentList.push([this.selected1, this.selected2]);
      this.$emit('alignChanged', this.alignmentList);
      this.selected1 = [];
      this.selected2 = [];
    },
    disconnectSentences() {
      console.log('disconnect sentences');
      console.log(this.selected1);
      console.log(this.selected2);
      this.alignmentList.forEach((couple) => {
        if (this.selected1.length == 1 && this.selected2.length == 1) {
          if (
            couple[0].includes(this.selected1[0]) &&
            couple[1].includes(this.selected2[0])
          ) {
            var idx1 = couple[0].indexOf(this.selected1[0])
            var idx2 = couple[1].indexOf(this.selected2[0])
            if (couple[0].length == 1) {
              if (couple[1].length == 1) {
                couple[0].splice(idx1,1);
                couple[1].splice(idx2,1);
              } else 
                couple[1].splice(idx2,1);
            } else {
              if (couple[1].length == 1)
                couple[0].splice(idx1,1);
              else {
                couple[0].splice(idx1,1);
                couple[1].splice(idx2,1);
              }
            }
          }
        }
      });
      this.$emit('alignChanged', this.alignmentList);
      this.selected1 = [];
      this.selected2 = [];
      this.drawAllArrows();
      this.alignmentList.forEach((couple) => {
        //clean list
        if (couple[0].length == 0 && couple[1].length == 0) {
          var idx = this.alignmentList.indexOf(couple);
          this.alignmentList.splice(idx,1);
        }
      });
    },
    removeAllLines(myNode) {
      // drawn lines.
      var elements = myNode.getElementsByClassName('align-lines');

      while (elements[0]) {
        elements[0].parentNode.removeChild(elements[0]);
      }
    },
    drawAllArrows() {
      this.$nextTick(() => {
        if (this.align === undefined) {
          console.log('un align');
          this.alignmentList = [];
        } else {
          console.log('defined align'); //, this.align);
          this.alignmentList = this.align;
        }
        this.removeAllLines(this.$refs['startpos']);
        this.alignmentList.forEach((element) => {
          var first = element[0];
          var second = element[1];
          // console.log(first[0], second[0],this.$refs['startpos']);
          first.forEach((ff) => {
            second.forEach((ss) => {
              var line = this.drawLine(ff, ss);
              this.$refs['startpos'].appendChild(line);
              //console.log(ff, ss, this.$refs['startpos']);
            });
          });
        });
      });
    },
  },
  created() {
    // console.log('sentenceAlignViewer created',this.align.length);
    // this.drawAllArrows();
  },
  destroyed() {},
  updated() {
    // console.log('sentenceAlignViewer updated');
    if (this.viewMode != 'norm') {
      console.log('not norm');
      return;
    }
    this.drawAllArrows();
  },
  mounted() {
    // console.log('sentenceAlignViewer mounted');
    // get mounted at every tab change.
    if (this.viewMode != 'norm') {
      console.log('not norm');
      return;
    }
    this.drawAllArrows();
  },
  computed: {},
  watch: {
    align: function () {
      //console.log('sentenceAlignViewer watched');
      if (this.viewMode != 'norm') {
        console.log('not norm');
        return;
      }
      this.drawAllArrows();
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
.firstc {
  padding-right: 1px;
}
.secondc {
  padding-left: 1px;
}
span {
  align-items: center;
}
</style>
