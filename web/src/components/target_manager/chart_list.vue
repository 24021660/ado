<template>
<div >
    <el-row >
        <el-col :span="6" v-for="(chart_info,key) in chart_data" :key="key">
            <div><chart_line :data='chart_info'/></div>
        </el-col>
    </el-row>
    
  </div>
  
</template>

<script>
import {url,chart_query_url} from '@/data_interface/url';
import axios from 'axios'
import chart_line from '@/components/target_manager/chart_line.vue'
export default {
    components:{chart_line},
     data(){
        return{
get_chart_url:url+chart_query_url,
           chart_data:[]
        }
    }
,
  // 基于准备好的dom，初始化echarts实例
  mounted(){
      this.get_data()
      //this.charts_init(this.chart_data)
  },
  methods: {
      get_data(){
          axios({
        url: this.get_chart_url,
        method: "post",
        data: { query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            this.chart_data = res.data[1];
            
          }
        })
        .catch((err) => {
          console.log(err);
        });

      },}
};
</script>