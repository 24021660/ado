<template>
  <div>
    <el-row>
      <el-table :data="tableData" border style="width: 100%" @cell-click="change_edit">
        <el-table-column v-for="(header_info, key) in table_header" :key="key" :prop="header_info.header_data"
          :label="header_info.header_label">
          <template slot-scope="scope">
            <span v-if="scope.row.isset">
              <span v-if="header_info.class == 'dropdownlist'">
                <el-select size="mini" v-model="scope.row[header_info.header_data]"
                  :placeholder="header_info.placeholder" filterable>
                  <el-option v-for="item in dropdownlist_data[header_info.header_data]" :key="item.value"
                    :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </span>
              <span v-else>
                <el-input size="mini" :placeholder="header_info.placeholder"
                  v-model="scope.row[header_info.header_data]" @change="is_edit(scope.row)">
                </el-input>
              </span>
            </span>
            <span v-else>{{ scope.row[header_info.header_data] }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="danger" @click="del_data(scope.$index, scope.row)"
              v-if="scope.row.isset == false">删除</el-button>
            <el-button size="mini" type="success" @click="save_data(scope.$index, scope.row)"
              v-if="scope.row.isset == true">保存</el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-row>
    <el-row>
      <el-col :span="2">
        <el-button size="mini" type="success" @click="add_data()">新增</el-button>
      </el-col>
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
import axios from "axios";
export default {
  data() {
    return {
      ssh_data_url: url + ssh_check_url,
      get_data_url: url + data_query_url,
      del_data_url: url + data_del_url,
      commit_data_url: url + data_commit_url,
      table_name: "service_manage",
      host_ip_table: 'computer_manager',
      table_header: [
        {
          header_data: "service_name",
          header_label: "service名称",
          placeholder: "",
          class: "input",
        },
        {
          header_data: "service_class",
          header_label: "service种类",
          placeholder: "shell",
          class: "dropdownlist",


        },
        {
          header_data: "host_ip",
          header_label: "主机ip",
          placeholder: "请选择",
          class: "dropdownlist",

        },
        {
          header_data: "service_shell",
          header_label: "执行语句",
          placeholder: "",
        },
        {
          header_data: "upload_file",
          header_label: "上传脚本",
          placeholder: "",
        },

      ],
      one_edit: false,
      tableData: [],
      dropdownlist_data: {
        service_class: [{
          value: 'shell',
          label: 'shell'
        }, {
          value: '脚本',
          label: '脚本'
        }], host_ip: []
      }
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
              i.edit_class = 'normal'
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
          edit_class: 'add'
        };
        this.tableData.push(init_data);
        this.one_edit = true;
      }
    },
    cancel_data(list_index) {
      this.one_edit = false
      this.tableData.splice(list_index, 1)

    },
    change_edit(row, column, cell, index) {
      if (column.label != "操作" && this.one_edit == false) {
        row.isset = true;
        console.log(row);
        console.log(column);
        console.log(cell);
        console.log(index);
        this.one_edit = true
      }
    },
    is_edit(row_data) {
      if (row_data.edit_class != 'add') {
        row_data.edit_class = 'edit'
      }
    },
    save_data(table_index, table_row) {
      table_row.isset = false;
      this.one_edit = false
      console.log(table_row)
      if (table_row.edit_class != 'normal') {
        axios({
          url: this.commit_data_url,
          method: "post",
          data: { table: this.table_name, commit_data: table_row },
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
      }


    },
    get_drop_list_data() {
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: this.host_ip_table, query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            console.log(res.data[1]);
            this.dropdownlist_data.host_ip = res.data[1].map((i) => {
              return { value: i.ip, label: i.ip }
            });
            console.log(this.dropdownlist_data.host_ip);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    this.get_data();
    this.get_drop_list_data();
  },
};
</script>

<style>
.el-row {
  margin-bottom: 10px;
}
</style>