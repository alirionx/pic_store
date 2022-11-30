<template>
  <div>
    <div class="thumb" v-for="(item, idx) in $store.getters.thumbs" :key="idx" 
      v-bind:style="{'background-image':'url('+get_img_path(item.filename)+')'}" 
      @click="set_image_show(idx)"></div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'Thumbs',
  props: {
  },
  data(){
    return {

    }
  },
  methods:{
    ...mapMutations([ "set_image_show", "reset_image_show" ]),

    get_img_path(filename){
      let url_path = this.$store.state.thumb_base_path + filename
      return url_path
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.thumb{
  display: inline-block;
  height: 180px;
  width: 180px;
  margin: 20px;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  cursor: pointer;
  border-radius: 4px;
  border: 8px solid #fff;
  box-shadow: 1px 4px 8px #444;
}
.thumb:hover{
  box-shadow: 1px 5px 10px #222;
}

</style>
