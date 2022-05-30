/*
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-19 19:00:50
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-20 11:03:36
 */
import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ToolList from '../views/ToolList.vue'

const routes = [
  {
    path: '/',
    name: 'ToolList',
    component: ToolList
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
