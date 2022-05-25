<template>
  <el-container>
    <appsidebar />
    <el-container>
      <el-header><appheader /></el-header>
      <el-divider></el-divider>
      <el-page-header @back="goBack" content="详情页面" style="margin:20px">
</el-page-header>
      <el-main><appmain /></el-main>
      <appfooter />
    </el-container>
  </el-container>
</template>

<script>
import appmain from "@/container/appmain.vue";
import appsidebar from "@/container/appsidebar.vue";
import appheader from "@/container/appheader.vue";
import appfooter from "@/container/appfooter.vue";
export default {
  name: "ADo",
  components: {
    appfooter,
    appmain,
    appheader,
    appsidebar,
    appmain,
  },
  data() {
    return {
      msg: "Welcome to Your Vue.js App",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.el-header,
.el-footer {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 60px;
  background: white;
}

.el-aside {
  background-color: #3c4b64;
  color: #333;
  text-align: left;
}

.el-main {
  text-align: center;
  background: whitesmoke;
}

body > .el-container {
  height: 100%;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
.el-divider--horizontal {
  margin: 0px 0;
}
</style>