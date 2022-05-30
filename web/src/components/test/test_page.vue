<template><div>
 <el-cascader :props="props" v-model="test_data" clearable></el-cascader>
    <el-button @click="get_test_data()">123</el-button>
</div>
   
</template>


<script>
let id = 0;
import {
    url,
    data_query_url,
    data_del_url,
    data_commit_url,
    ssh_check_url
} from "@/data_interface/url";
import { task_status_map } from "@/data_interface/map";
import axios from "axios";
export default {
    data() {
        return {
            ssh_data_url: url + ssh_check_url,
            get_data_url: url + data_query_url,
            del_data_url: url + data_del_url,
            commit_data_url: url + data_commit_url,
            status_map: task_status_map,
            host_ip_table: 'computer_manager',
            table_workflow: "workflow_manage",
            table_service: "service_manage",
            test_data: [['step1', '62931e503f3b6e0fab65dd44', '1.116.94.231'],['step3', '62931e503f3b6e0fab65dd44', '1.116.94.231']],
            props: {
                multiple: true,
                step_len: 10,
                step_list_data: { service_data: [], host_data: [] },
                lazy: true,
                lazyLoad(node, resolve) {
                    const { level } = node;
                    setTimeout(() => {
                        console.log(level)
                        //console.log(this.get_step_list_data)
                        var nodes = []
                        if (level == 0) {
                            let id = 0
                            nodes = Array.from({ length: this.step_len }).map(item => ({
                                value: `step${++id}`,
                                label: `step${id}`
                            })

                            )
                        }
                        else if (level == 1) { nodes = this.step_list_data['service_data'] }
                        else { nodes = this.step_list_data['host_data'] }
                        // 通过调用resolve将子节点数据返回，通知组件数据加载完成
                        resolve(nodes);
                    }, 1000);
                }
            }
        };
    },
    methods: {
        get_test_data(){
            console.log(this.test_data)
        },
        get_step_list_data() {
            var that = this
            axios({
                url: this.get_data_url,
                method: "post",
                data: { table: this.table_service, query: {} },
            })
                .then((res) => {
                    if (res.data[0] == 0) {
                        that.props.step_list_data.service_data = res.data[1].map((i) => {
                            return { value: i._id.$oid, label: i.service_name, leaf: false }
                        });

                    }
                })
                .catch((err) => {
                    console.log(err);
                });
            axios({
                url: this.get_data_url,
                method: "post",
                data: { table: this.host_ip_table, query: {} },
            })
                .then((res) => {
                    if (res.data[0] == 0) {
                        that.props.step_list_data.host_data = res.data[1].map((i) => {
                            return { value: i.ip, label: i.ip, leaf: true }
                        });
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
    },
    mounted() {
        this.get_step_list_data();
    },

};
</script>