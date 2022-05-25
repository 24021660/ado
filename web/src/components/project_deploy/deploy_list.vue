<template>
  <el-table :data="tableData" border style="width: 100%">
    <el-table-column
      v-for="(header_info, key) in table_header"
      :key="key"
      :prop="header_info.header_data"
      :label="header_info.header_label"
    >
    </el-table-column>
    <el-table-column label="状态">
      <template slot-scope="scope">
        <el-tag
          :type="scope.row.status === '更新完毕' ? 'success' : scope.row.status === '生成中' ? 'warning':'danger'"
          disable-transitions
          >{{ scope.row.status }}</el-tag
        >
      </template></el-table-column
    >
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="danger"
          @click="del_data(scope.$index, scope.row)"
          >删除</el-button
        >
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { url, data_query_url, data_del_url} from "@/data_interface/url";
import axios from "axios";
export default {
  data() {
    return {
      get_data_url: url+data_query_url,
      del_data_url: url+data_del_url,
      table_header: [
        { header_data: "project_name", header_label: "项目名称" },
        { header_data: "project_no", header_label: "项目编号" },
        { header_data: "version_no", header_label: "版本号" },
        { header_data: "update_time", header_label: "更新日期" },
      ],

      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1517 弄",
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
        },
      ],
    };
  },
  methods: {
    get_data() {
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: "deploy_config", query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            this.tableData = res.data[1];
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    del_data(list_index, row_data){
        this.tableData.splice(list_index,1)
        axios({
        url: this.del_data_url,
        method: "post",
        data: { table: "deploy_config", del_id: row_data._id.$oid },
      })
        .then((res) => {
          console.log(row_data._id.$oid)
        })
        .catch((err) => {
          console.log(err);
        });
        
    }
  },
  mounted() {
    this.get_data();
  },
};
</script>