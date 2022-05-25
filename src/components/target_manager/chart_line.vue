<template>
   <div :id="data._id.$oid" style="width: 300px; height: 200px" ></div>
</template>

<script>
import * as echarts from "echarts";
export default {
    props:{data:Object},
    data(){
        return{
           
        }
    }
,
  // 基于准备好的dom，初始化echarts实例
  mounted(){
      //this.get_data()

      this.charts_init(this.data)
  },
  methods: {
    charts_init(chart_data) {
        let myChart = echarts.init(document.getElementById(chart_data._id.$oid))
            //let myChart = echarts.init(document.getElementById(chart_data[i]._id.$oid));
            myChart.setOption({
        title: {
          text: chart_data.chart_name,
        },
        tooltip: {
    trigger: 'axis'
  },
        xAxis: {
            type: 'category',
    boundaryGap: false,
          data: chart_data.time_array,
        },
        yAxis: {type: 'value'},
        series: chart_data.data
      });
        
    },
  },
};
</script>