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
              <span v-else-if="header_info.class=='text'">{{ scope.row[header_info.header_data] }}</span>
              <span v-else-if="header_info.class=='tag'"><el-tag :type="scope.row[header_info.header_data]" effect="dark" size="mini">{{status_map[scope.row[header_info.header_data]]}}</el-tag></span>
              <span v-else>
                <el-input size="mini" :placeholder="header_info.placeholder"
                  v-model="scope.row[header_info.header_data]" @change="is_edit(scope.row)">
                </el-input>
              </span></span>
            <span v-else>
              <span v-if="header_info.class=='tag'"><el-tag :type="scope.row[header_info.header_data]" effect="dark" size="mini">{{status_map[scope.row[header_info.header_data]]}}</el-tag></span>
              <span v-else>{{ scope.row[header_info.header_data] }}</span></span>
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
import {task_status_map} from "@/data_interface/map";
import axios from "axios";
export default {
  data() {
    return {
      ssh_data_url: url + ssh_check_url,
      get_data_url: url + data_query_url,
      del_data_url: url + data_del_url,
      commit_data_url: url + data_commit_url,
      status_map:task_status_map,
      table_name: "task_manage",
      table_workflow: "workflow_manage",
      table_service: "service_manage",
      table_header: [
        {
          header_data: "task_name",
          header_label: "任务名称",
          placeholder: "",
        },
        {
          header_data: "task_class",
          header_label: "定时种类",
          placeholder: "cron",
          class: "dropdownlist",
        },
        {
          header_data: "period",
          header_label: "周期",
          placeholder: "1",
        },
        {
          header_data: "unit",
          header_label: "单位",
          placeholder: "minutes",
          class: "dropdownlist",
        },
        {
          header_data: "task_detail",
          header_label: "任务内容",
          placeholder: "请选择",
          class: "dropdownlist",
        },
        {
          header_data: "last_run_time",
          header_label: "最近一次执行时间",
          placeholder: "暂无",
          class:"text",
        },
        {
          header_data: "last_run_status",
          header_label: "最近一次执行情况",
          placeholder: "暂无",
          class:"tag",
        },
      ],
      one_edit: false,
      tableData: [],
      dropdownlist_data: { task_class: [{ value: 'cron', label: 'cron' }, { value: 'interval', label: 'interval' },{ value: 'single', label: 'single' }], unit: [{ value: 'seconds', label: 'seconds' }, { value: 'minutes', label: 'minutes' }, { value: 'hours', label: 'hours' }, { value: 'days', label: 'days' }], task_detail_workflow: [], task_detail_service: [], task_detail: [] }

    };
  },
  methods: {
    get_data() {
      console.log(task_status_map)
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
          task_class: "single",
          unit: "seconds",
          last_run_status:'info',
          period:1
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
      var that=this
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: this.table_workflow, query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            that.dropdownlist_data.task_detail_workflow = res.data[1].map((i) => {
              return { value: 'workflow|' + i._id.$oid, label: "workflow:" + i.workflow_name }
            });
            this.dropdownlist_data.task_detail=this.dropdownlist_data.task_detail.concat(that.dropdownlist_data.task_detail_workflow)

          }
        })
        .catch((err) => {
          console.log(err);
        });
      axios({
        url: this.get_data_url,
        method: "post",
        data: { table: this.table_service, query: {} },
      })
        .then((res) => {
          if (res.data[0] == 0) {
            that.dropdownlist_data.task_detail_service = res.data[1].map((i) => {
              return { value: 'service|' + i._id.$oid, label: "service:" + i.service_name }
            });
            this.dropdownlist_data.task_detail=this.dropdownlist_data.task_detail.concat(that.dropdownlist_data.task_detail_service)

          }
        })
        .catch((err) => {
          console.log(err);
        });
      
    },
    
  },
  mounted() {
    this.get_data();
    this.get_drop_list_data()

  },
};
</script>

<style>
.el-row {
  margin-bottom: 10px;
}
</style>