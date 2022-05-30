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
              <span v-else-if="header_info.class == 'text'">{{ scope.row[header_info.header_data] }}</span>
              <span v-else-if="header_info.class == 'tag'">
                <el-tag :type="scope.row[header_info.header_data]" effect="dark" size="mini">{{ status_map.info }}
                </el-tag>
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
            <el-button size="mini" type="primary" @click="add_step_data(scope.$index, scope.row)"
              v-if="scope.row.isset == true">新增step数据</el-button>
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
    <el-row>
      <el-dialog :title="dialog_data.title" :visible.sync="dialog_data.visible" width="50%" center>
        <span>
          <el-table :data="dialog_data.info_list">
            <el-table-column type="index" label="步骤" width="50">
            </el-table-column>
            <el-table-column label="service选择" width="180" prop="service_id">
              <template slot-scope="scope">
                <el-select size="mini" v-model="scope.row.service_id" filterable>
                  <el-option v-for="item in dialog_data.step_list_data['service_data']" :key="item.value"
                    :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </template>

            </el-table-column>
            <el-table-column prop="host" label="主机选择" width="500">
              <template slot-scope="scope">
                <el-select v-model="scope.row.host" multiple placeholder="请选择" size="mini">
                  <el-option v-for="item in dialog_data.step_list_data['host']" :key="item.value" :label="item.label"
                    :value="item.value">
                  </el-option>
                </el-select>
              </template>
            </el-table-column>

          </el-table>
        </span>
        <el-row>
      <el-col :span="2">
        <el-button size="mini" type="success" @click="add_step()">新增</el-button>
      </el-col>
    </el-row>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialog_data.visible = false">取 消</el-button>
          <el-button type="primary" @click="save_step_data()">确 定</el-button>
        </span>
      </el-dialog>
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
      table_name: "workflow_manage",
      table_service: "service_manage",
      host_ip_table: 'computer_manager',
      table_header: [
        {
          header_data: "workflow_name",
          header_label: "workflow名称",
          placeholder: "",
        },
        {
          header_data: "workflow_detail",
          header_label: "workflow详情",
          placeholder: "shell",
          class: "cascader"
        },


      ],
      one_edit: false,
      tableData: [],
      dialog_data: {
        title: '',
        visible: false,
        data_index: 0,
        info_list: [{ service_id: '123', host: [123] }, { service_id: '234', host: [234] },{ service_id: '345', host: [345] }],
        step_list_data: { service_data: [], host: [] }
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
          edit_class: 'add',
          workflow_detail: [{ service_id: '',host:[] }]
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


    }, get_step_list_data() {
      var that = this
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: this.table_service, query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            this.dialog_data.step_list_data.service_data = res.data[1].map((i) => {
              return { value: i._id.$oid, label: i.service_name }
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
            this.dialog_data.step_list_data.host = res.data[1].map((i) => {
              return { value: i.ip, label: i.ip }
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });

    },
    add_step_data(index, row_data) {
      this.dialog_data.title = row_data.workflow_name
      this.dialog_data.info_list = row_data.workflow_detail
      this.dialog_data.data_index = index
      this.get_step_list_data()
      this.dialog_data.visible = true
    },
    save_step_data(){
      this.tableData[this.dialog_data.data_index].workflow_detail=this.dialog_data.info_list
      this.dialog_data.visible = false
    },
    add_step(){
      this.dialog_data.info_list.push({ service_id: '',host:[] })
    }
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