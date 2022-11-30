import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    picture_base_path: "/api/dl/picture/",
    thumb_base_path: "/api/dl/thumb/",
    thumbs: [],
    pictures: [],
    meta: [],
    view: "thumbs",
    loader_show: false,
    upload_show: false,
    image_show: null,
    meta_edit_show: null,
  },
  getters: {
    thumbs(state){
      return state.thumbs
    },
    pictures(state){
      return state.pictures
    },
    meta(state){
      return state.meta
    }
  },
  mutations: {
    set_view_thumbs(state){
      state.view = "thumbs";
    },
    set_view_table(state){
      state.view = "table";
    },

    set_loader_show(state){
      state.loader_show = true;
    },
    reset_loader_show(state){
      state.loader_show = false;
    },

    apply_thumbs(state, data){
      state.thumbs = data
    },
    apply_pictures(state, data){
      state.pictures= data
    },
    apply_meta(state, data){
      state.meta= data
    },

    add_thumb(state, data){
      state.thumbs.push(data)
    },
    add_picture(state, data){
      state.pictures.push(data)
    },
    add_meta(state, data){
      state.meta.push(data)
    },

    set_image_show(state, idx){
      state.image_show = idx;
    },
    reset_image_show(state){
      state.image_show = null;
    },

    set_meta_edit_show(state, idx){
      state.meta_edit_show = idx;
    },
    reset_meta_edit_show(state){
      state.meta_edit_show = null;
    },

    set_upload_show(state){
      state.upload_show = true;
    },
    reset_upload_show(state){
      state.upload_show = false;
    },

    delete_image(state, idx){
      state.meta.splice(idx, 1);
      state.thumbs.splice(idx, 1);
      state.pictures.splice(idx, 1);
    },

    edit_meta(state, item){
      state.meta[state.meta_edit_show] = item
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
    },
    call_meta_from_api(context){
      axios.get("/api/meta")
      .then((response)=>{
        context.commit("apply_meta", response.data)
      })
      .catch((err)=>{
        console.log(err)
      })
    }

  },
  modules: {
  }
})
