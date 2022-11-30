<template>
  <div class="MetaEditBlocker">
    <div class="Form">
      <div class="Hl">Edit Picture Meta Data</div>
      
      <form @submit.prevent="submit">
        <div class="scroll_box">  
          <div class="ipt_hl">Filename</div>
          <input type="text" disabled required v-model="meta_data.filename" />
          
          <div class="ipt_hl">Picture Format</div>
          <select v-model="meta_data.format" >
            <option :value="null">none</option>
            <option value="Landscape">Landscape</option>
            <option value="Portrait">Portrait</option>
            <option value="Square">Square</option>
          </select>

          <div class="ipt_hl">Picture Name</div>
          <input type="text" v-model="meta_data.name" />

          <div class="ipt_hl">Location</div>
          <input type="text" v-model="meta_data.location" />

          <div class="ipt_hl">Date</div>
          <input type="text" v-model="meta_data.date" />

          <div class="ipt_hl">Album</div>
          <input type="text" v-model="meta_data.album" />

          <div class="ipt_hl">Comment</div>
          <input type="text" v-model="meta_data.comment" />
        
        </div>
        <div class="BtnFrame">
          <button type="submit">submit</button>
          <button type="button" @click="reset_meta_edit_show">cancel</button>
        </div>
      </form>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex'

export default {
  name: 'MetaEdit',
  props: {
  },
  data(){
    return {
      meta_data: {}
    }
  },
  methods:{
    ...mapMutations([ "reset_meta_edit_show", "edit_meta" ]),

    submit(){
      axios.put('/api/meta/'+this.meta_data.filename, this.meta_data )
      .then((response)=>{ 
        // console.log(response.data)
        this.edit_meta(this.meta_data)
      })
      .catch((err)=>{
        console.log(err)
      })
      .finally(()=>{
        this.reset_meta_edit_show()
      })
    }
  },
  mounted(){
    
    this.meta_data = {... this.$store.getters.meta[this.$store.state.meta_edit_show] }
    // console.log(JSON.stringify(this.meta_data))
  }
}
</script>

<style scoped>


.MetaEditBlocker{
  position: fixed;
  top:0;
  left:0;
  width: 100%;
  height: 100%;
  background-color: rgba(80, 80, 80, 0.80);
  text-align:center;
  /* padding-top: 180px; */
}




</style>
