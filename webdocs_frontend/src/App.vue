<template>
  <div id="app">
    <div class="navbar-div">
      <transition
        name="nav-fade"
        mode="out-in"
      >
        <NavBar v-show="$route.name != 'NoteEdit'"/>
      </transition>
    </div>
    <transition
      name="fade"
      mode="out-in"
    >
      <!-- <keep-alive include="NoteEdit"> -->
        <router-view />
      <!-- </keep-alive> -->
    </transition>

    <b-toast
      id="update-toast"
      title="Webdocs更新"
      auto-hide-delay="5000"
      solid
      variant="info"
    >
      Webdocs有更新！<br>
      点击
      <b-link @click="reload()">
        刷新
      </b-link>
      立刻更新， <br>
      或下次访问时自动更新。
    </b-toast>

    <LoginModal ref="login-modal" />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import LoginModal from '@/components/LoginModal.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    LoginModal,
  },
  methods: {
    login() {
      return this.$refs['login-modal'].login()
    },
    reload() {
      if('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations()
          .then((registrations) => {
              for(let registration of registrations) {
                console.log('unregister',registration);
                registration.unregister();
              }
          });
      }
      setTimeout(() => window.location.reload(true), 100);
    }
  }
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

.fade-enter-active, .fade-leave-active {
  transition: opacity .15s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
