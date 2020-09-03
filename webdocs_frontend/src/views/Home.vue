<template>
  <div class="home">
    <b-container>
      <b-row>
        <b-col
          cols="12"
          order="1"
          lg="2"
          order-lg="1"
        >
          <b-button pill variant="outline-dark" v-b-modal.new-note-modal>
            <b-icon icon="plus"></b-icon>
            New Note
          </b-button>
        </b-col>
        <b-col
          cols="12"
          order="1"
          lg="8"
          order-lg="2"
        >
          <h3>{{ 'Recent Notes' }}</h3>
          <div
            v-for="note in recentNotes"
            :key="'recent-note-' + note.id"
            no-body
            border-variant="white"
            class="my-4"
          >
            <div class="d-flex w-100 justify-content-between">
              <h4 class="mb-2">
                <b-link
                  :to="`/note/${note.id}`"
                  active-class=""
                  exact-active-class=""
                >
                  {{ note.title }}
                </b-link>
              </h4>
              <em>last modified at {{ note.lastModified.toLocaleDateString()}}, {{ note.lastModified.toLocaleTimeString() }}</em>
            </div>
            <p
              class="mb-2"
              style="text-align: left"
            >
              <!-- {{ 'Here is abstract.' }} -->
              by {{ note.owner }}
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
      recentNotes: [],
      newNoteTitle: '',
    }
  },
  async created () {
    const res = await this.axios.get(`/api/documents/`)
    this.recentNotes = res.data.results.map(note => {
      note.lastModified = new Date(note.lastModified)
      return note
    })
  },
  methods: {
    async newNote() {
      await this.needLogin()
      const res = await this.axios.post(`/api/documents/`, {
        title: this.newNoteTitle
      })
      this.$router.push(`/note/${res.data.id}`)
    }
  }
}
</script>
