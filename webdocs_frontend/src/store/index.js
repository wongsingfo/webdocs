import Vue from 'vue'
import Vuex from 'vuex'
import IndexedDBP from 'indexeddbp'

Vue.use(Vuex)

const readLocalStorage = store => {
  if (window.localStorage && window.localStorage.user) {
    store.commit('setUserState', {
      user: window.localStorage.user,
      key: window.localStorage.token
    })
    // store.commit('setUserActivation', true)
  }
}

export default new Vuex.Store({
  state: {
    user: null,
    userActivated: false,
    userToken: null,
    isLoading: false,
    loginFunc: null,
    db: null,
  },
  mutations: {
    setUserState (state, userState) {
      if (userState !== null) {
        state.user = userState.user
        state.userActivated = true
        state.userToken = userState.key
        if (window.localStorage) {
          window.localStorage.user = state.user
          window.localStorage.token = userState.key
        }
      } else {
        state.user = null
        state.userActivated = false
        state.userToken = null
        if (window.localStorage) {
          window.localStorage.user = ''
          window.localStorage.token = ''
        }
      }
    },
    // setUserActivation (state, activated) {
    //   state.userActivated = activated
    // },
    setLoading (state, isLoading) {
      state.isLoading = isLoading
    },
    setLoginFunc (state, func) {
      state.loginFunc = func
    },
    clearUserToken (state) {
      state.userToken = null
    },
    setDB(state, db) {
      state.db = db
    }
  },
  actions: {
    async initDB({ commit, state }) {
      if (state.db !== null) {
        return
      }
      const db = new IndexedDBP({ name: 'webdocs' })
      await db.init()
      await db.useObjectStore('note', { keyPath: 'id' })
      commit('setDB', db)
    }
  },
  plugins: [ readLocalStorage ],
  strict: process.env.NODE_ENV !== 'production'
})
