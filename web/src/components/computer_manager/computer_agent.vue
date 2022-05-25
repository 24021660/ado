<template>
  <div>
    <el-row>
      <el-table
        :data="tableData"
        border
        style="width: 100%"
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
              >重启主机</el-button
            >
            
          </template>
        </el-table-column>
        <el-table-column label="登录">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="save_data(scope.$index, scope.row)"
              >ssh登录</el-button
            >
          </template></el-table-column
        >
      </el-table>
    </el-row>
  </div>
</template>

<script>
import { url, computer_agent_url, data_del_url,data_commit_url } from "@/data_interface/url";
import axios from "axios";
export default {
  data() {
    return {
      get_data_url: url + computer_agent_url,
      del_data_url: url + data_del_url,
      commit_data_url:url+data_commit_url,
      table_name:'target_manager',
      table_header: [
         {
          header_data: "name",
          header_label: "实例名称",
          placeholder: "生成方式",
        } ,
        {
          header_data: "ip",
          header_label: "IP地址",
          placeholder: "生成方式",
        } ,
        {
          header_data: "cpu_rate",
          header_label: "cpu使用率",
          placeholder: "生成方式",
        },
        {
          header_data: "memory_rate",
          header_label: "内存使用率",
          placeholder: "生成方式",
        },
        {
          header_data: "disk_rate",
          header_label: "磁盘占用率",
          placeholder: "请输入种类",
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
        data: { table: this.table_name, query: {} },
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
        data: { table: this.table_name, del_id: row_data._id.$oid },
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
    cancel_data(list_index){
        this.one_edit=false
        this.tableData.splice(list_index,1)

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
      if (table_row.edit_class!='normal'){
          axios({
        url: this.commit_data_url,
        method: "post",
        data: { table: this.table_name, commit_data: table_row  },
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
        });}
      

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