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

    <b-modal
      ref="login-modal"
      title="Login"
      :ok-disabled="haveErr"
      @ok.prevent="submit"
      @hide="checkLogin"
    >
      <b-form-group
        id="usernameInputGroup"
        :label="$t('Username:')"
        label-for="usernameInput"
      >
        <b-form-input
          id="usernameInput"
          v-model="form.username"
          autofocus
          type="text"
          required
        />
      </b-form-group>
      <b-form-group
        id="passwordInputGroup"
        :label="$t('Password:')"
        label-for="passwordInput"
        :state="!haveErr"
      >
        <b-form-input
          id="passwordInput"
          v-model="form.password"
          type="password"
          required
          @keydown.enter.prevent="!haveErr && submit()"
        />
        <template #invalid-feedback>
          <div v-if="haveErr">
            {{ $t('Mobile or password is wrong') }}!
          </div>
        </template>
      </b-form-group>
    </b-modal>

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
  data () {
    return {
      form: {
        username: '',
        password: '',
      },
      haveErr: false,
      resolve: null,
      reject: null,
    }
  },
  watch: {
    'form.username' () {
      this.haveErr = false
    },
    'form.password' () {
      this.haveErr = false
    }
  },
  created() {
    // this.$store.commit('setLoginFunc', this.login)
  },
  methods: {
    async submit(event) {
      // event.preventDefault()
      try {
        const res = await this.axios.post('/api/auth/login/', {
          username: this.form.username,
          password: this.form.password
        })
        this.$store.commit('setUserState', {
          user: this.form.username,
          key: res.data.key
        })
        this.$refs['login-modal'].hide()
        this.resolve()
        // await this.checkUserActivation()
        // if (window.history.length > 1) {
        //   this.$router.back()
        // } else {
        //   this.$router.push('/')
        // }
      } catch (err) {
        if (err.response.status == 400) {
          this.haveErr = true
        } else {
          console.log(err.response)
          this.reject('Unknown Error')
        }
      }
    },
    checkLogin() {
      if (!this.$store.state.user) {
        this.reject('User cancelled')
      }
    },
    login() {
      this.form.username = this.form.password = ''
      this.haveErr = false
      this.$refs['login-modal'].show()
      return new Promise((resolve, reject) => {
        this.resolve = resolve
        this.reject = reject
      })
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
</style>
