<template>
   <div :id="data.title" style="width: 600px; height: 400px" ></div>
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
        let myChart = echarts.init(document.getElementById(chart_data.title))
            //let myChart = echarts.init(document.getElementById(chart_data[i]._id.$oid));
            myChart.setOption({
        title: {
          text: chart_data.title,
          left: 'center'
        },
        tooltip: {
    trigger: 'item'
  },
        legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '',
      type: 'pie',
      radius: '50%',
      data: chart_data.data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
      });
        
    },
  },
};
</script>