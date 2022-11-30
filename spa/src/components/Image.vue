<template>
  <div class="ShowBoxBlocker">
    <div class="img_box">
      <img class="picture" :src="get_picture_url()" @click="stats_show=!stats_show" />
      <table v-if="stats_show">
        <tr>
          <th>Filename:</th>
          <td>{{$store.getters.pictures[$store.state.image_show].filename}}</td>
        </tr>
        <tr>
          <th>Uploaded:</th>
          <td>{{get_datetime($store.getters.pictures[$store.state.image_show].uploaded)}}</td>
        </tr>
        <tr>
          <th>Size:</th>
          <td>{{get_size_in_kb($store.getters.pictures[$store.state.image_show].size)}}</td>
        </tr>
      </table>
      <img class="xbtn" src="../assets/icon_close.png" @click="reset_image_show" />
    </div>
    
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Image',
  props: {
  },
  data(){
    return {
      stats_show:false
    }
  },
  methods:{
    ...mapMutations([ "set_image_show", "reset_image_show" ]),

    get_picture_url(){ 
      let url = this.$store.state.picture_base_path + this.$store.getters.pictures[this.$store.state.image_show].filename;
      return url;
    },

    get_datetime(unix_timestamp){
      let date = new Date(unix_timestamp * 1000);
      return date.toLocaleString()
    },
    get_size_in_kb(size){
      let res = (size / 1024).toFixed().toString() + " kb"
      return res 
    }

  }
}
</script>

<style scoped>


.ShowBoxBlocker{
  position: fixed;
  top:0;
  left:0;
  width: 100%;
  height: 100%;
  background-color: rgba(80, 80, 80, 0.80);
  text-align:center;
  /* padding-top: 180px; */
}
.ShowBoxBlocker .img_box{
  display: table;
  position: relative;
  margin: 140px auto auto auto;
  /* background-color: aqua; */
}
.ShowBoxBlocker .img_box .xbtn{
  position: absolute;
  right: -20px;
  top: -20px;
  height: 40px;
  cursor: pointer;
}

.ShowBoxBlocker .picture{
  max-height: 75vh;
  box-shadow: 0px 8px 16px #222;
}

.ShowBoxBlocker .img_box table{
  position: absolute;
  bottom: 2px;
  width:100%;
  background-color: #555;
  color:#fff;
  font-size: 12px;
  padding:2px;
  opacity: 0.9;
}
.ShowBoxBlocker .img_box table th{
  font-weight: bold;
  text-align: left;
  background-color: #222;
}
.ShowBoxBlocker .img_box table td{
  text-align: left;
  background-color: #444;
}
.ShowBoxBlocker .img_box table th, .ShowBoxBlocker .img_box table td{
  padding:4px;
}

</style>
