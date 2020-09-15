<template>
  <div class="home">
    <b-container>
      <b-row>
        <b-col
          v-if="user !== null"
          cols="12"
          order="1"
          lg="4"
          order-lg="1"
          align="center"
        >
          <b-card
            no-body
            :header="$t('Your Recently Edited Notes')"
            class="mb-3"
            border-variant="dark"
            header-bg-variant="dark"
            header-text-variant="white"
          >
            <b-list-group flush>
              <b-list-group-item
                v-for="note in userRecentNotes"
                :key="'recent-note-' + note.id"
                :to="'/note/' + note.id"
                class="d-flex justify-content-between align-items-center"
              >
                {{ note.title }}
                <small>{{ note.lastModified.toLocaleString() }}</small>
              </b-list-group-item>
            </b-list-group>
          </b-card>

          <b-button
            v-b-modal.new-note-modal
            pill
            variant="outline-dark"
          >
            <b-icon icon="plus"></b-icon>
            New Note
          </b-button>
        </b-col>
        <b-col
          cols="12"
          order="1"
          lg="2"
          order-lg="1"
          v-else
        />

        <b-col
          cols="12"
          order="1"
          lg="8"
          order-lg="2"
        >
          <h3>{{ 'Recently Updated Notes' }}</h3>
          <div
            v-for="note in recentNotes"
            :key="'recent-note-' + note.id"
            no-body
            class="my-4"
          >
            <h4 class="mb-2">
              <b-link
                :to="`/note/${note.id}`"
                active-class=""
                exact-active-class=""
              >
                {{ note.title }}
              </b-link>
            </h4>
            <div class="d-flex w-100 justify-content-between">
              <p> by {{ note.owner.username }} </p>
              <em>last modified at {{ note.lastModified.toLocaleString() }}</em>
            </div>
            <p
              class="mb-2"
              style="text-align: left"
            >
              {{ note.abstract }}
            </p>
            <hr>
          </div>
        </b-col>
      </b-row>
    </b-container>

    <b-modal
      id="new-note-modal"
      title="New Note"
      @ok="newNote"
    >
      <b-form-group
        :label="'Title:'"
      >
        <b-form-input
          v-model="newNoteTitle"
          autofocus
          required
          @keydown.enter.prevent="newNote"
        />
      </b-form-group>
    </b-modal>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  data() {
    return {
      userRecentNotes: [],
      recentNotes: [],
      newNoteTitle: '',
    }
  },
  created () {
    this.fetchData()
  },
  watch: {
    user() {
      this.fetchData()
    }
  },
  methods: {
    async fetchData() {
      if (this.user !== null) {
        const res1 = await this.axios.get(`/api/documents/`, {
          params: {
            limit: 5,
            owner__username: this.user,
            ordering: '-last_modified'
          }
        })
        this.userRecentNotes = res1.data.results
      } else {
        this.userRecentNotes = []
      }
      const res = await this.axios.get(`/api/documents/`, {
        params: {
          ordering: '-last_modified'
        }
      })
      this.recentNotes = res.data.results
    },
    async newNote() {
      await this.needLogin()
      const res = await this.axios.post(`/api/documents/`, {
        title: this.newNoteTitle,
        body: '# ' + this.newNoteTitle + '\n\n'
      })
      this.$router.push(`/note/${res.data.id}`)
    }
  }
}
</script>
