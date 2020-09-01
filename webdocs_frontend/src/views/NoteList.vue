<template>
  <div class="home">
    这里打算放一个表格展示该用户的所有笔记
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
