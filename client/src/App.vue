<template>
  <div class="d-flex flex-column h-100" id="app">
    <header class="container-fluid">
      <div class="row">
        <div class="col-12 p-0 bg-primary">
          <b-navbar type="light" variant="light">
            <b-navbar-nav>
              <b-navbar-brand href="#">LessMessy NLP Workbench</b-navbar-brand>
              <b-nav-item-dropdown text="Tools" right>
                <b-dropdown-item to="/">Home</b-dropdown-item>
                <b-dropdown-item to="/about">About</b-dropdown-item>
                <b-dropdown-item to="/json">Json Viewer</b-dropdown-item>
                <b-dropdown-item to="/manager">Workspace Manager</b-dropdown-item>
                <b-dropdown-item to="/log">Log Viewer</b-dropdown-item>
              </b-nav-item-dropdown>
              <b-nav-item-dropdown v-if="workspaceList" text="Workspaces" right>
                <b-dropdown-item
                  v-for="wp in workspaceList"
                  v-bind:key="wp"
                  :disabled="wp === storeState.workspace"
                  @click="changeWorkspace(wp)"
                >{{wp}}</b-dropdown-item>
              </b-nav-item-dropdown>
              <b-nav-item href="#">Current Workspace: {{storeState.workspace}}</b-nav-item>
            </b-navbar-nav>
          </b-navbar>
        </div>
      </div>
    </header>
    <main class="container-fluid flex-grow-1 overflow-hidden bg-light" >
      <div class="row h-100 overflow-auto">
        <div class="col">
          <div class="row h-100">
            <div id="mainContent" class="col-10 d-flex flex-column">
              <router-view />
            </div>
            <div id="sidebarContent" role="tablist" class="col-2">
              <SidebarCard
                id="a1"
                title="Description"
                :htmlDescription="storeState.sidebarDescription"
                :isOpened="true"
              />
              <SidebarFileInfo
                id="a2"
                title="Opened File"
                :filename="storeState.filename"
                :fileinfo="storeState.fileinfo"
                :filedata="storeState.jsonData"
                :isOpened="true"
              />
              <SidebarCard
                id="a3"
                title="Jobs"
                htmlDescription
                :contentList="jobList"
                :isOpened="true"
              />
              <SidebarWords
                id="a4"
                title="Words Alignment"
                :isOpened="true"
                :filedata="storeState.jsonData"
                v-if="storeState.jsonData && storeState.jsonData.words.length > 0"
              />
            </div>
          </div>
        </div>
      </div>
    </main>
    <FooterLogger v-bind:loglines="loglines" />
  </div>
</template>
<script>
import SidebarCard from '@/components/sidebar/SidebarCard.vue';
import SidebarFileInfo from '@/components/sidebar/SidebarFileInfo.vue';
import SidebarWords from '@/components/sidebar/SidebarWords.vue';
import FooterLogger from '@/components/FooterLogger.vue';
import commMixin from '@/mixins/commMixin.js';
import { store } from './store.js';

export default {
  data() {
    return {
      storeState: store.state,
      loglines: store.state.loglines,
      workspaceList: undefined,
      jobList: store.state.jobList,
    };
  },
  methods: {
    workspaceListFiller(data) {
      this.workspaceList = data;
    },
    changeWorkspace(wp) {
      this.storeState.workspace = wp;
      this.$router.replace({ query: { w: wp } });
    },
  },
  mounted() {
    console.log('mounted app, w:', this.$route.query.w);
    this.fetchWorkspaceList(this.workspaceListFiller);
    if (this.$route.query.w) {
      this.storeState.workspace = this.$route.query.w;
    }
  },
  watch: {
  	'$route': function(value) {
      if(value.name === 'About') {
      	//this.sidebarDescription = 'about';
      } else if (value.name === 'Json') {
      	//this.sidebarDescription = 'Json manager';
      } else if (value.name === 'Manager') {
      	//this.sidebarDescription = 'file manager';
      } else {
      	//this.sidebarDescription = 'xxxxx';
      }
    }
  },
  components: {
    SidebarCard,
    SidebarFileInfo,
    FooterLogger,
    SidebarWords,
  },
  mixins: [commMixin],
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body,
html {
  height: 100%;
}

.overflow-hidden {
  overflow: hidden;
}

.overflow-scroll {
  overflow: scroll;
}

footer {
  background: rgb(197, 202, 197);
  height: 100px;
  flex-basis: 100px;
}

.disableClick {
  pointer-events: none;
}

mark {
  background-color: azure;
}

.collapsed > .when-opened,
:not(.collapsed) > .when-closed {
  display: none;
}
</style>
