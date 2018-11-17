import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// BOOTSTRAP STUFF
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// MY COMPONENTS
import SR-header from './components/Header.vue'


Vue.use(BootstrapVue)
Vue.config.productionTip = false

Vue.component('sr-header', SR-header);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
