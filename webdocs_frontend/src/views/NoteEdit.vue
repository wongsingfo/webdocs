<template>
  <Editor ref="editor" />
</template>

<script>
import Editor from '@/components/Editor.vue'

export default {
  name: 'NoteEdit',
  components: {
    Editor
  },
  beforeRouteUpdate(...args) {
    this.$refs.editor.beforeRouteUpdate(...args)
  },
  beforeRouteLeave(...args) {
    this.$refs.editor.beforeRouteLeave(...args)
  }
}
</script>
