<template>
  <el-table
    :data="tableData"
    border
    style="width: 100%"
    @cell-click="change_edit"
  >
    <el-table-column
      v-for="(header_info, key) in table_header"
      :key="key"
      :prop="header_info.header_data"
      :label="header_info.header_label"
    >
     <template slot-scope="scope">
       <span v-if="scope.row.isset">
         
         
         
         <el-input size="mini"   :placeholder="header_info.placeholder" v-model="scope.row[header_info.header_data]">
                                </el-input></span>
       <span v-else>{{scope.row[header_info.header_data]}}</span>
     </template>
    </el-table-column>

    <el-table-column label="状态">
      <template slot-scope="scope">
        <el-tag
          :type="
            scope.row.status === '更新完毕'
              ? 'success'
              : scope.row.status === '生成中'
              ? 'warning'
              : 'danger'
          "
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
          v-if="scope.row.isset == false"
          >删除</el-button
        >
        <el-button
          size="mini"
          type="success"
          @click="save_data(scope.$index, scope.row)"
          v-if="scope.row.isset == true"
          >保存</el-button
        >
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { url, data_query_url, data_del_url } from "@/data_interface/url";
import axios from "axios";
export default {
  data() {
    return {
      get_data_url: url + data_query_url,
      del_data_url: url + data_del_url,
      table_header: [

        { header_data: "create_mode", header_label: "生成方式" ,placeholder:'生成方式'},
        { header_data: "class", header_label: "分类" ,placeholder:'请输入种类'},
        { header_data: "image_name", header_label: "镜像名称" ,placeholder:'请输入镜像名称'},
        { header_data: "image_version", header_label: "版本号" ,placeholder:'请输入版本号'},
        { header_data: "port", header_label: "默认映射端口" ,placeholder:'宿主机端口：容器端口，多个端口空格分割'},
        { header_data: "v", header_label: "默认映射目录" ,placeholder:'宿主机目录：容器目录，多个目录空格分割'},
        { header_data: "update_time", header_label: "更新日期" ,placeholder:'无需填写'},
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
        data: { table: "docker_image_manage", query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            console.log(res.data[1]);
            this.tableData = res.data[1].map((i) => {
              i.isset = false;
              return i;
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    del_data(list_index, row_data) {
      this.tableData.splice(list_index, 1);
      axios({
        url: this.del_data_url,
        method: "post",
        data: { table: "docker_image_manage", del_id: row_data._id.$oid },
      })
        .then((res) => {
          console.log(row_data._id.$oid);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    add_data(){
      var init_data={
    create_mode: "",
    image_name: "",
    image_version: "",
    v: "",
    port: "",
    class: "",
    status: "",
    update_time: "",
    download: "",
    install_array: "",
    isset: true
}
      this.tableData.push()
    },
    save_data(table_index, table_row) {
      table_row.isset = false;
    },
    change_edit(row, column, cell, index) {
      if (column.label != "操作") {
        row.isset = true;
        console.log(row);
        console.log(column);
        console.log(cell);
        console.log(index);
      }
    },
    test(selection) {
      console.log(selection);
    },
  },
  mounted() {
    this.get_data();
  },
};
</script>