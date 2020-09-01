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
              <em>{{ note.lastModified.toLocaleDateString()}}, {{ note.lastModified.toLocaleTimeString() }}</em>
            </div>
            <p
              class="mb-2"
              style="text-align: left"
            >
              {{ 'Here is abstract.' }}
            </p>
            <hr>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  // components: {
  //   HelloWorld
  // }
  data() {
    return {
      recentNotes: [
        {
          id: 1,
          title: 'Hello',
          lastModified: new Date(),
        }
      ],
    }
  }
}
</script>
