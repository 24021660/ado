<template>
    <div>
        <el-row>
            <el-col>71</el-col>
            <el-col>81</el-col>
            <el-col>91</el-col>
            <el-col>100</el-col>

        </el-row>

    </div>





</template>


<script>
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
            res_data: {
                total_num_host: 2,
                total_num_task: 1,
                total_service: 3,
                total_num_workflow: 2,
                class_num: [
                    {
                        title: 'task',
                        data: [
                            { value: 1048, name: 'single' },
                            { value: 735, name: 'interval' },
                            { value: 580, name: 'cron' },
                        ]
                    },
                    {
                        title: 'service',
                        data: [
                            { value: 1048, name: 'shell' },
                            { value: 735, name: '脚本' },
                        ]
                    },
                ]
            }

        }
    },
    methods: {}

}

</script>