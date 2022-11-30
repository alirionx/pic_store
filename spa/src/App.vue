<template>
  <div>
    <div class="headblock">Picture Store - K8s Example App</div>
    <div class="main_btn_frame">
      <img src="./assets/icon_thumbs.png" alt="thumbs view" @click="set_view_thumbs" v-if="$store.state.view=='table'" />
      <img src="./assets/icon_table.png" alt="table view" @click="set_view_table" v-if="$store.state.view=='thumbs'" />
      <img src="./assets/icon_upload.png" alt="upload picture" @click="set_upload_show"  />
    </div>
    <Thumbs v-if="$store.state.view=='thumbs'" />
    <MetaTable v-if="$store.state.view=='table'" />
    <Image v-if="$store.state.image_show!==null" />
    <Upload v-if="$store.state.upload_show" />
    <MetaEdit v-if="$store.state.meta_edit_show!==null" />

    <Loader v-if="$store.state.loader_show" />

  </div>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
</template>

<script>
import Loader from './components/Loader.vue'
import Thumbs from './components/Thumbs.vue'
import MetaTable from './components/MetaTable.vue'
import Upload from './components/Upload.vue'
import Image from './components/Image.vue'
import MetaEdit from './components/MetaEdit.vue'

import { mapMutations } from 'vuex'

export default {
  name: 'App',
  components: {
    Loader,
    Thumbs,
    MetaTable,
    Upload,
    MetaEdit,
    Image
  },
  methods:{
    ...mapMutations([ "set_upload_show", "reset_upload_show", "set_view_table", "set_view_thumbs" ]),

  },
  mounted(){
    this.$store.dispatch("call_thumbs_from_api");
    this.$store.dispatch("call_pictures_from_api");
    this.$store.dispatch("call_meta_from_api");
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 6px;
  padding-top: 80px;
}
.headblock{
  position: fixed;
  left:0;
  top:0;
  width: 102%;
  margin: -1%;
  background-color: rgb(90, 110, 123);
  color: #fff;
  font-weight: bold;
  font-size: 22px;
  line-height: 70px;
  text-align: center;
  padding-top: 16px;
  z-index: 2;
  box-shadow: 0px 2px 4px #222;
}
.main_btn_frame{
  width: 100%;
  text-align: right;
  /* background-color: #2c3e50; */
}
.main_btn_frame img{
  height: 44px;
  margin: 0 20px 0 0;
  padding-bottom: 4px;
  cursor: pointer;
  border-bottom: 2px solid rgba(90, 110, 123, 0);
}
.main_btn_frame img:hover{
  border-bottom: 2px solid #000;
}


.Form{
  display: inline-block;
  margin: 15vh auto 2vh auto;
  min-width: 500px;
  width: 60%;
  max-width: 600px;
  min-height: 50px;
  padding:22px 22px 26px 22px; 
  background-color: #eee;
  color: #000;
  border: 1px solid #aaa;
  border-radius: 0px;
  box-shadow: 1px 8px 16px #222; 
  text-align: left;
}
.Form .scroll_box{
  max-height: 58vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding:20px;
}

.Form .Hl{
  font-size: 18px;
  font-weight: bold;
  text-align: right;
  color: #000;
  padding: 0 0 12px 0;
}
.Form .File{
  padding:20px;
  font-size: 20px;
  text-align: center;
  color: #000;
  background-color: #fff;
  border: 1px solid #aaa;
  min-height: 20px;
  cursor: pointer;
}


.Form .ipt_hl{
  font-size: 14px;
  font-weight: bold;
  text-align: left;
  color: #000;
  padding: 12px 10px 0px 0px;
}
.Form ::placeholder {
  color: #bbb;
}
.Form input[type=text], input[type=number], input[type=email], input[type=password]{
  display: block;
  padding:10px;
  font-size: 15px;
  margin: 4px 0 4px 0;
  background-color: #fff;
  border: 1px solid #bbb;
  box-shadow: 1px 1px 2px #666; 
}
.Form input[type=text], input[type=email], input[type=password]{
  width: 96%;
}
.Form input[type=number]{
  width: 40%;
}
.Form input[type=checkbox]{
  transform: scale(1.5);
  margin: 10px;
}
.Form label{
  font-size: 14px;
  font-weight: bold;
  text-align: left;
  color: #000;
  padding: 8px;
}
.Form input[disabled]{
  background-color: #eee;
}

.Form select{
  display: block;
  padding:10px;
  font-size: 15px;
  margin: 4px 0 12px 0;
  background-color: #fff;
  border: 1px solid #bbb;
  box-shadow: 1px 1px 2px #666; 
  width: 50%;
}


.Form .BtnFrame{
  padding-top: 32px;
  text-align: center;
}
.Form .BtnFrame button{
  min-width: 120px;
  padding: 6px 12px 6px 12px;
  margin: 0 10px 0 10px;
  border: none;
  text-align: center;
  background-color: #444;
  color:#fff;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 1px 1px 2px #333; 
  cursor: pointer;
}
.Form .BtnFrame button:hover{
  background-color: #333;
}


</style>
