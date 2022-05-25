<template>
  <div>
    <el-row>
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
              <el-input
                size="mini"
                :placeholder="header_info.placeholder"
                v-model="scope.row[header_info.header_data]"
                @change="is_edit(scope.row)"
              >
              </el-input
            ></span>
            <span v-else>{{ scope.row[header_info.header_data] }}</span>
          </template>
        </el-table-column>
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
    </el-row>
    <el-row>
      <el-col :span="2"
        ><el-button size="mini" type="success" @click="add_data()"
          >新增</el-button
        ></el-col
      >
    </el-row>
  </div>
</template>

<script>
import { url, data_query_url, data_del_url,data_commit_url } from "@/data_interface/url";
import axios from "axios";
export default {
  data() {
    return {
      get_data_url: url + data_query_url,
      del_data_url: url + data_del_url,
      commit_data_url:url+data_commit_url,
      table_header: [
        {
          header_data: "chart_name",
          header_label: "图表名称",
          placeholder: "生成方式",
        },
        {
          header_data: "time_range",
          header_label: "时间长度",
          placeholder: "请输入种类",
        },
        {
          header_data: "time_class",
          header_label: "单位",
          placeholder: "请输入镜像名称",
        },{
          header_data: "unit_class",
          header_label: "表格单位",
          placeholder: "请输入镜像名称",
        },
      ],
      one_edit: false,
      tableData: [],
    };
  },
  methods: {
    get_data() {
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: "chart_manager", query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            console.log(res.data[1]);
            this.tableData = res.data[1].map((i) => {
              i.isset = false;
              i.edit_class='normal'
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
        data: { table: "chart_manager", del_id: row_data._id.$oid },
      })
        .then((res) => {
          console.log(row_data._id.$oid);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    add_data() {
      if (this.one_edit == false) {
        var init_data = {
          isset: true,
          edit_class:'add'
        };
        this.tableData.push(init_data);
        this.one_edit = true;
      }
    },
    change_edit(row, column, cell, index) {
      if (column.label != "操作" &&this.one_edit==false) {
        row.isset = true;
        console.log(row);
        console.log(column);
        console.log(cell);
        console.log(index);
        this.one_edit=true
      }
    },
    is_edit(row_data){
        if (row_data.edit_class!='add'){
            row_data.edit_class='edit'
        }
    },
    save_data(table_index, table_row) {
      table_row.isset = false;
      this.one_edit=false
      console.log(table_row)
      axios({
        url: this.commit_data_url,
        method: "post",
        data: { table: "chart_manager", commit_data: table_row  },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            console.log(res.data[1]);
            //this.add_data={chart_name:'',chart_time_range:'',}
            //this.get_data(target_url)
          }
        })
        .catch((err) => {
          console.log(err);
        });

    },
  },
  mounted() {
    this.get_data();
  },
};
</script>

<style>
.el-row {
  margin-bottom: 10px;
}
</style>