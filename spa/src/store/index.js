import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    thumbs: [],
    pictures: [],
    image_show: null
  },
  getters: {
    thumbs(state){
      return state.thumbs
    },
    pictures(state){
      return state.pictures
    }
  },
  mutations: {
    apply_thumbs(state, data){
      state.thumbs = data
    },
    apply_pictures(state, data){
      state.pictures= data
    },

    set_image_show(state, idx){
      state.image_show = idx;
    },
    reset_image_show(state){
      state.image_show = null;
    }
    
  },
  actions: {
    call_thumbs_from_api(context){
      axios.get("/api/thumbs")
      .then((response)=>{
        context.commit("apply_thumbs", response.data)
      })
      .catch((err)=>{
        console.log(err)
      })
    },
    call_pictures_from_api(context){
      axios.get("/api/pictures")
      .then((response)=>{
        context.commit("apply_pictures", response.data)
      })
      .catch((err)=>{
        console.log(err)
      })
    }

  },
  modules: {
  }
})
