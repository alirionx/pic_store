<template>
  <div>
    <table class="meta_table">
      <tr>
        <th>Thumb</th>
        <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign:col.align}">{{col.hl}}</th>
        <th>Action</th>
      </tr>
      <tr v-for="(item, row_idx) in $store.getters.meta" :key="row_idx">
        <td>
          <div class="table_thumb" 
            v-bind:style="{'background-image':'url('+get_img_path(item.filename)+')'}" 
            @click="set_image_show(row_idx)"></div>
        </td>
        <td v-for="(col, defi_idx) in defi" :key="defi_idx" :style="{textAlign:col.align}">{{item[col.key]}}</td>
        <td>
          <img class="table_btn" src="../assets/icon_edit.png" @click="set_meta_edit_show(row_idx)" />
          <img class="table_btn" src="../assets/icon_delete.png" @click="call_picture_delete(row_idx)" />
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import axios from 'axios'

export default {
  name: 'MetaTable',
  props: {
  },
  data(){
    return {
      defi:[
        {
          key: "filename",
          hl: "Filename",
          align: "left"
        },
        {
          key: "name",
          hl: "Name",
          align: "left"
        },
        {
          key: "location",
          hl: "Location",
          align: "left"
        },
        {
          key: "date",
          hl: "Date",
          align: "center"
        },
        {
          key: "album",
          hl: "Album",
          align: "left"
        },
        {
          key: "format",
          hl: "Format",
          align: "center"
        },
        {
          key: "comment",
          hl: "Comment",
          align: "left"
        }
      ]
    }
  },
  methods:{
    ...mapMutations([ "set_image_show", "reset_image_show", "set_meta_edit_show", "reset_meta_edit_show", "delete_image" ]),

    get_img_path(filename){
      let url_path = this.$store.state.thumb_base_path + filename
      return url_path
    },

    call_picture_delete(idx){

      axios.delete("/api/image/"+this.$store.getters.meta[idx].filename)
      .then((response)=>{
        this.delete_image(idx)
      })
      .catch((err)=>{
        console.log(err)
      })
    }
  }
}
</script>

<style scoped>

.meta_table{
  margin: 20px auto 20px auto;
  width: 90%;
  max-width: 1600px;
  font-size: 15px;
  padding:14px;
  box-shadow: 1px 4px 8px #444;
  background-color: #f6f6f6;
}
.meta_table th{
  border-bottom: 1px solid #222;
  background-color: #fff;
  padding:6px;
}
.meta_table td{
  background-color: #fff;
  padding:4px;
}
.meta_table tr:nth-child(2) td{
  padding-top: 8px;
}

.meta_table th:first-child, .meta_table td:first-child{
  text-align: center;
}
.meta_table .table_thumb{
  height: 38px;
  width: 38px;
  margin: -2px auto -2px auto;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  cursor: pointer;
  /* border-radius: 4px; */
  border: 1px solid #aaa;
  /* box-shadow: 1px 4px 8px #444; */
}
.meta_table .table_thumb:hover{
  border: 1px solid #000;
}

.meta_table .table_btn{
  height: 28px;
  margin: auto 4px auto 4px;
  cursor: pointer;
  border-bottom: 2px solid rgba(0, 0, 0, 0);
}
.meta_table .table_btn:hover{
  border-bottom: 2px solid rgba(0, 0, 0, 1);
}




</style>
