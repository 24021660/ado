import Vue from 'vue'
import Router from 'vue-router'
import ADo from '@/components/ADo'
import login from '@/components/login/login'
import project_deploy from '@/components/project_deploy/project_deploy'
import deploy_list from '@/components/project_deploy/deploy_list'
import images_list from '@/components/docker_manager/images_list'
import images_manager from '@/components/docker_manager/images_manager'
import target_list from '@/components/target_manager/target_list'
import chart_manager from '@/components/target_manager/chart_manager'
import chart_list from '@/components/target_manager/chart_list'
import dashboard from '@/components/dashboard/dashboard'
import computer_list from '@/components/computer_manager/computer_list'
import computer_agent from '@/components/computer_manager/computer_agent'
import target_center from '@/components/target_manager/target_center'
import task from '@/components/automation/task'
import ado_service from '@/components/automation/ado_service'
import ado_workflow from '@/components/automation/ado_workflow'
import test_page from '@/components/test/test_page'
import { path } from 'chromedriver'

Vue.use(Router)





export default new Router({
  routes: [
    {
      path: '/',
      name: 'ADo',
      component: ADo,
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          component: dashboard,
        }
        , {
          path: '/project_deploy/project_deploy',
          name: 'project_deploy',
          component: project_deploy,
        },
        {
          path: '/project_deploy/deploy_list',
          name: 'deploy_list',
          component: deploy_list,
        },
        {
          path: '/docker_manager/images_list',
          name: 'deploy_list',
          component: images_list,
        }, {
          path: '/docker_manager/images_manager',
          name: 'images_manager',
          component: images_manager,
        }, {
          path: '/target_manager/target_list',
          name: 'target_list',
          component: target_list,
        }, {
          path: '/target_manager/chart_manager',
          name: 'chart_manager',
          component: chart_manager,
        }, {
          path: '/target_manager/chart_list',
          name: 'chart_list',
          component: chart_list,
        },
        {
          path: '/computer_manager/computer_list',
          name: 'computer_list',
          component: computer_list,
        }, {
          path: '/computer_manager/computer_agent',
          name: 'computer_agent',
          component: computer_agent,
        },
        {
          path: '/target_manager/target_center',
          name: 'target_center',
          component: target_center,
        },
        {
          path: '/automation/ado_service',
          name: 'ado_service',
          component: ado_service,
        },
        {
          path: '/automation/task',
          name: 'task',
          component: task,
        },{
          path: '/automation/ado_workflow',
          name: 'ado_workflow',
          component: ado_workflow,
        },
        {path: '/test/test_page',
        name: 'test_page',
        component: test_page,}
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
}
)
