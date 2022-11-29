<template>
  <div class="ShowBoxBlocker">
    <img :src="get_picture_url()" />
  </div>
</template>

<script>
export default {
  name: 'Thumbs',
  props: {
  },
  data(){
    return {}
  },
  methods:{
    get_picture_url(){ 
      let url = "/api/picture/" + this.$store.getters.pictures[this.$store.state.image_show].filename;
      return url;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.ShowBoxBlocker{
  position: absolute;
  top:2px;
  left:2px;
  width: 99%;
  height:99%;
  background-color: rgba(255, 255, 255, 0.85);
  text-align:center;
  /* padding-top: 180px; */
}
.ShowBoxBlocker img{
  max-width:60%;
  max-height: 80vh;
  display: table;
  margin: 140px auto auto auto;
}

</style>
