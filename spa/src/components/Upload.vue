<template>
  <div class="UploadBoxBlocker">
    <div class="Form">
      <div class="Hl">Upload Picture</div>
      <div class="File" @click="call_file_select">{{get_selected()}}</div>
      <input type="file" @change="set_selected_image" id="image_input" />
      <div class="BtnFrame">
        <button v-if="selected_image" @click="submit">upload</button>
        <button @click="reset_upload_show">cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex'

export default {
  name: 'Upload',
  props: {
  },
  data(){
    return {
      selected_image: null
    }
  },
  methods:{
    ...mapMutations([ 
      "set_upload_show", "reset_upload_show", 
      "add_thumb", "add_picture", "add_meta",
      "set_loader_show", "reset_loader_show" ]),

    get_selected(){
      if(!this.selected_image){
        return "Click to select image"
      }
      else{
        return this.selected_image
      }
    },

    set_selected_image(){
      let elm = document.getElementById("image_input")
      console.log(elm.value)
      let str_split = elm.value.split("\\")
      this.selected_image = str_split[str_split.length - 1]
    },

    call_file_select(){
      document.getElementById("image_input").click()
    },

    submit(){
      this.set_loader_show()

      let elm = document.getElementById("image_input")
      let formData = new FormData()
      formData.append("file", elm.files[0])
      axios.post('/api/picture', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then((response)=>{ 
        this.add_thumb(response.data.thumb)
        this.add_picture(response.data.picture)
        this.add_meta({filename:response.data.picture.filename})
      })
      .catch((err)=>{
        console.log(err)
      })
      .finally(()=>{
        this.reset_loader_show()
        this.reset_upload_show()
      })
    }

  
  }
}
</script>

<style scoped>

.UploadBoxBlocker{
  position: fixed;
  top:0;
  left:0;
  width: 100%;
  height: 100%;
  background-color: rgba(80, 80, 80, 0.80);
  text-align:center;
  /* padding-top: 180px; */
}

#image_input{
  display: none;
}


</style>
