<template>
  <el-aside width="16rem">
    <el-row style="text-align: center;" >
      <div style="height: 60px">
        <h1>
          ADo Platform
          <el-button type="warning" round size="mini">v{{version_info}}</el-button>
        </h1>
      </div>
    </el-row>
    <el-row>
      <el-col :span="24">
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <div v-for="(nav_info, key) in nav_list" :key="key">
            <div v-if="nav_info.item_class == 'first_menu'">
              <el-submenu :index="key">
                <template slot="title">
                  <i :class="nav_info.icon_name"></i>
                  <span>{{ nav_info.name }}</span>
                </template>
                  <el-menu-item v-for="(second_item,key) in nav_info.children" :key="key"
                    ><router-link :to="nav_info.path+second_item.path"
                      > <i :class="second_item.icon_name"></i><a>{{second_item.name}}</a></router-link
                    ></el-menu-item
                  >
                
              </el-submenu>
            </div>
            <div v-if="nav_info.item_class != 'first_menu'">
              <el-menu-item>
                <i :class="nav_info.icon_name"></i>
                <span
                  ><router-link :to="nav_info.path">
                    {{ nav_info.name }}</router-link
                  ></span
                >
              </el-menu-item>
            </div>
          </div>
        </el-menu>
      </el-col>
    </el-row>
  </el-aside>
</template>


<script>
import config from '../../package.json'
import nav from "@/router/nav";
export default {
  data() {
    return {
      nav_list: nav,
      version_info:config.version
    };
  },
};
</script>


<style>
h1 {
  color: aliceblue;
}
a {
    text-decoration: none;
    color:#fff;
}

</style>