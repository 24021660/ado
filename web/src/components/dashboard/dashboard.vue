<template>
    <div>
        <el-row height="300px">
            <el-col :span="6" ><el-row ><div><font size="5" >host主机数量</font></div></el-row><el-row><div></div></el-row>
            <el-row><font size="3">{{chart_data.total_num_host}}</font></el-row></el-col>
            <el-col :span="6" ><el-row ><div><font size="5" >service数量</font></div></el-row><span> </span>
            <el-row><font size="3">{{chart_data.total_num_service}}</font></el-row></el-col>
            <el-col :span="6" ><el-row ><div><font size="5" >workflow数量</font></div></el-row><span> </span>
            <el-row><font size="3">{{chart_data.total_num_workflow}}</font></el-row></el-col>
            <el-col :span="6" ><el-row ><div><font size="5" >task数量</font></div></el-row><span> </span>
            <el-row><font size="3">{{chart_data.total_num_task}}</font></el-row></el-col>
        </el-row>
        <el-row height="1000px">
            <el-col :span="12" v-for="(chart_info, key) in chart_data.class_num" :key="key">
                <div>
                    <dashboard_chart_pie :data='chart_info' :index='key' />
                </div>
            </el-col>
        </el-row>

    </div>

</template>

<script>
import { url, dashboard_url } from '@/data_interface/url';
import axios from 'axios'
import dashboard_chart_pie from '@/components/dashboard/dashboard_chart_pie.vue'
export default {
    components: { dashboard_chart_pie },
    data() {
        return {
            get_dashboard_url: url + dashboard_url,
            chart_data: {}
        }
    }
    ,
    // 基于准备好的dom，初始化echarts实例
    mounted() {
        this.get_data()
        //this.charts_init(this.chart_data)
    },
    methods: {
        get_data() {
            axios({
                url: this.get_dashboard_url,
                method: "get",
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

        },
    }
};
</script>