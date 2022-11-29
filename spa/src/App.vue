<template>
  <div>
    <div class="headblock">Picture Store - K8s Example App</div>
    <div class="main_btn_frame">
      <img src="./assets/icon_upload.png" alt="upload picture" />
    </div>
    <Thumbs />
    <Image v-if="$store.state.image_show!==null" />
  </div>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
</template>

<script>
import Thumbs from './components/Thumbs.vue'
import Image from './components/Image.vue'

export default {
  name: 'App',
  components: {
    Thumbs,
    Image
  },
  mounted(){
    this.$store.dispatch("call_thumbs_from_api");
    this.$store.dispatch("call_pictures_from_api");
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
  padding-top: 70px;
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
  padding-top: 10px;
  z-index: 2;
}
.main_btn_frame{
  width: 100%;
  text-align: right;
  /* background-color: #2c3e50; */
}
.main_btn_frame img{
  height: 40px;
  margin: 0 10px 0 10px;
  padding-bottom: 4px;
  cursor: pointer;
  border-bottom: 2px solid rgba(90, 110, 123, 0);
}
.main_btn_frame img:hover{
  border-bottom: 2px solid rgb(90, 110, 123);
}


/* rgb(90, 110, 123); */
</style>
