<template>
  <b-sidebar
    :id="id"
    title="Note Detail"
    shadow
  >
    <div class="px-3 py-2" v-if="document.created">
      <h5>Title</h5>
      <p v-show="newTitle === null">
        {{ document.title }}
        <b-icon icon="pencil-square" @click="changeTitle" />
      </p>
      <b-input
        v-if="newTitle !== null"
        v-model="newTitle"
        @keydown.enter.prevent="keydownCallback()"
      />
      <h5>Author</h5>
      <p>{{ document.owner }}</p>
      <h5>Create Time</h5>
      <p>{{ document.created.toLocaleDateString() }}, {{ document.created.toLocaleTimeString() }}</p>
      <h5>Last Modified Time</h5>
      <p>{{ document.lastModified.toLocaleDateString() }}, {{ document.lastModified.toLocaleTimeString() }}</p>
    </div>
  </b-sidebar>
</template>

<script>


export default {
  name: 'NoteDetailSidebar',
  props: {
    id: String,
    // ['url', 'id', 'title', 'owner', 'body', 'created', 'last_modified']
    document: Object
  },
  data () {
    return {
      newTitle: null,
      keydownCallback: null,
    }
  },
  methods: {
    changeTitle() {
      this.newTitle = this.document.title
      this.keydownCallback = async () => {
        this.keydownCallback = null
        const res = await this.axios.patch(`/api/documents/${this.document.id}/`, {
          id: this.document.id,
          title: this.newTitle,
        })
        this.newTitle = null
        this.$emit('doc-change', res.data)
      }
    }
  }
}
</script>

<style>

</style>
