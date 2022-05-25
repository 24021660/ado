<template>
  <div id="target_center">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="主机指标" name="1">
        <template slot="title">
          <p>主机指标</p>
        </template>
        <el-row
          align="middle"
          type="flex"
          style="margin: 10px"
          v-for="(key, target_name) in target_center_res.computer_target"
          :key="key"
        >
          <el-col :span="6"
            ><el-form
              :inline="true"
              class="demo-form-inline"
              label-position="left"
              ><el-form-item :label="'指标项：' + target_name">
              </el-form-item></el-form
          ></el-col>
          <el-col :span="10">
            <el-row
              v-for="(target_detail_name, key2) in target_center_res
                .computer_target[target_name]"
              :key="key2"
            >
              <el-form :inline="true" class="demo-form-inline">
                <el-form-item label="阈值：">
                  <el-select v-model="value" placeholder=">=">
                    <el-option :value="target_detail_name.value_range">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-input
                    style="width: 100px"
                    v-model="target_detail_name.value"
                  ></el-input>
                </el-form-item>
                <el-form-item label="级别：">
                  <el-select
                    v-model="target_detail_name.level"
                    placeholder="警告"
                  >
                    <el-option v-for="item in target_alarm_level_list"
                      :key="item.level"
                      :label="item.level_label"
                      :value="item.level"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
            </el-row>
          </el-col>
        </el-row>
        <el-button type="primary" size="mini">保存</el-button>
      </el-collapse-item>

      <el-collapse-item title="服务指标" name="2">
        <template slot="title">
          <p>服务指标</p>
        </template>
      </el-collapse-item>
      <el-collapse-item title="定制化指标" name="3">
        <template slot="title">
          <p>定制化指标</p>
        </template>
        <div>简化流程：设计简洁直观的操作流程；</div>
        <div>
          清晰明确：语言表达清晰且表意明确，让用户快速理解进而作出决策；
        </div>
        <div>
          帮助用户识别：界面简单直白，让用户快速识别而非回忆，减少用户记忆负担。
        </div>
      </el-collapse-item>
    </el-collapse>
    
  </div>
</template>

<style>
.el-collapse-item__header {
  background-color: #fafafa;
}
p {
  margin-left: 10px;
}
.relationContainer {
  display: flex;
  justify-content: center; /*主轴上居中*/
  align-items: center; /*侧轴上居中*/
}
#target_center .el-input {
  width: 100px;
}
el-row {
  margin: 20px;
}
</style>


<script>
export default {
  data() {
    return {
      activeNames: ["1"],
      test: 0,
      target_center_res: {
        computer_target: {
          cpu_rate: [
            {
              value_range: ">=",
              value: 0.9,
              level: "1",
            },
            {
              value_range: ">=",
              value: 0.8,
              level: "0",
            },
          ],
          memory_rate: [
            { value_range: ">=", value: 0.9, level: "1" },
            { value_range: ">=", value: 0.8, level: "0" },
          ],
          disk_rate: [
            { value_range: ">=", value: 0.9, level: "1" },
            { value_range: ">=", value: 0.8, level: "0" },
          ],
        },
        business_target: {},
      },
      target_alarm_level_list: [
        {
          level: "1",
          level_label: "严重",
        },
        {
          level: "0",
          level_label: "警告",
        },
      ],
    };
  },
  methods: {
    handleChange(val) {
      console.log(val);
    },
  },
};
</script>