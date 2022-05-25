<template>
  <el-row>
    <el-col :span="3" :offset="12"
      ><div class="grid-content bg-purple">主页</div></el-col
    >
    <el-col :span="3"><div class="grid-content bg-purple">设置</div></el-col>
    <el-col :span="2"
      ><div class="grid-content bg-purple-light">
        <i class="el-icon-bell"></i></div
    ></el-col>
    <el-col :span="2"
      ><div class="grid-content bg-purple-light">
        <i class="el-icon-message"></i></div
    ></el-col>
    <el-col :span="2"
      ><div style="line-height:55px">
          <el-avatar src="">user</el-avatar>
       </div
    ></el-col>
    
  </el-row>
</template>

<style>
.el-avatar{
  vertical-align: middle;
}

</style>