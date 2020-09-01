<template>
  <div id="app">
    <div class="navbar-div">
      <transition
        name="nav-fade"
        mode="out-in"
      >
        <NavBar v-show="$route.name != 'Editor'"/>
      </transition>
    </div>
    <transition
      name="fade"
      mode="out-in"
    >
      <keep-alive>
        <router-view />
      </keep-alive>
    </transition>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
  name: 'App',
  components: {
    NavBar
    // Footer
  },
}
</script>

<style lang="scss">
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
// }

// #nav {
//   padding: 30px;

//   a {
//     font-weight: bold;
//     color: #2c3e50;

//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }

/* 可以设置不同的进入和离开动画 */
/* 设置持续时间和动画函数 */
.nav-fade-enter-active, .nav-fade-leave-active {
  transition: all .8s ease;
  // #nav {
  //   transition: all .8s ease;
  // }
}
.nav-fade-enter, .nav-fade-leave-to {
  // transform: translateY(-100px);
  top: -5rem !important;
  // opacity: 0;
}

.navbar-div {
  margin-bottom: 5rem;
}
</style>
