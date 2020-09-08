<template>
  <div>
    <b-overlay :show="status === 'Initializing'">
      <b-button id="return-button" pill variant="outline-dark" to="/" style="z-index: 20">
        <b-icon icon="arrow-left"></b-icon>
        Home
      </b-button>
      <b-button id="sidebar-button" pill variant="outline-dark" v-b-toggle.editor-note-detail style="z-index: 20">
        <b-icon icon="card-list"></b-icon>
        Note Details
      </b-button>
      <b-button id="status-button" pill :variant="statusStyle[status].variant" style="z-index: 20" @click="save">
        <b-icon :icon="statusStyle[status].icon"></b-icon>
        {{ status }}
      </b-button>
      <div id="editor-wrapper" class="editor" @keydown="keydownHandler">
        <div ref="editor"></div>
      </div>
      <NoteDetailSidebar id="editor-note-detail" :document="this.document" />
    </b-overlay>
    <input type="file" ref="file-input" @change="fileInputCallback" v-show="false"/>
  </div>
</template>

<script>
import Muya from '@/muya/lib'
import TablePicker from '@/muya/lib/ui/tablePicker'
import QuickInsert from '@/muya/lib/ui/quickInsert'
import CodePicker from '@/muya/lib/ui/codePicker'
import EmojiPicker from '@/muya/lib/ui/emojiPicker'
import ImagePathPicker from '@/muya/lib/ui/imagePicker'
import ImageSelector from '@/muya/lib/ui/imageSelector'
import FormatPicker from '@/muya/lib/ui/formatPicker'
import FrontMenu from '@/muya/lib/ui/frontMenu'
// import '@/muya/themes/default.css'
import '@/muya/themes/editor.scss'

import NoteDetailSidebar from '@/components/NoteDetailSidebar.vue'

const example = "# Muya Example\n\n## English Text\n\n#### Sponsor Mark Text Development\n\nMark Text is an MIT licensed open source project, you will always be able to download the latest version from [GitHub release page](https://github.com/marktext/marktext/releases). Mark Text is still in development, and its development is inseparable from all sponsors. I hope you join them:\n\n## Chinese Text\n\n9月1日，外交部发言人华春莹主持例行记者会。有记者就中印边境最新事态提问。\n\n华春莹表示，关于边界等历史遗留的问题，中方历来主张通过和平友好协商，找到公平合理和双方都能接受的解决方案。一段时间以来，双方在各个层级进行了多次接触和会谈，作出积极的努力来寻求和平解决边界的一些分歧或争端，共同维护中印边境地区的和平与稳定。\n\n但是在8月31日，印军破坏了前期双方多层级会谈会晤达成的共识，在中印边界的西段班公湖以南地区以及热钦山口附近再次非法越线，公然挑衅，造成边境局势再度紧张。印方的行径严重侵犯了中方的领土主权，也严重违反了两国相关的协定、协议和重要的共识，破坏了边境地区的和平与安宁。这与双方一段时间以来推动现地局势缓和降温的努力是背道而驰的，中方对此坚决反对并且已经向印方提出了严正交涉，要求印方停止一切挑衅行为，立即撤回非法越线的人员，立即停止任何导致局势紧张、升级和复杂化的举动。\n\n(本文来自澎湃新闻，更多原创资讯请下载“澎湃新闻”APP)\n\n![](https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=3604977702,2490965591&fm=173&app=49&f=JPEG?w=312&h=208&s=EF924781C4C074FC9499958A0300E091)\n\n## Code Block\n\n```js\nconst arr1 = [1,2,3,[1,2,3,4, [2,3,4]]]function flatten(input) { // flatten deep using a stack  const stack = [...input]  const res = []  while (stack.length) {    const next = stack.pop()    if (Array.isArray(next)) {      stack.push(...next)    } else {      res.push(next)    }  }  return res.reverse()}flatten(arr1)// [1, 2, 3, 1, 2, 3, 4, 2, 3, 4]\n```\n\n## Table\n\n```\n| 标题1 | 标题2 | 标题3 || :--  | :--: | ----: || 左对齐 | 居中 | 右对齐 || ---------------------- | ------------- | ----------------- |\n```\n\n| 标题1                    | 标题2           | 标题3               |\n| ---------------------- | ------------- | ----------------- |\n| 左对齐                    | 居中            | 右对齐               |\n| ---------------------- | ------------- | ----------------- |\n\n## Flowchart\n\n```flowchart\nstart=>start: start\noperation1=>operation: operation1\nisSuccess=>condition: success?\noperation2=>operation: operation2\noperation3=>operation: operation3\noperation4=>operation: operation4\nend=>end: 结束\nstart->operation1->isSuccess\nisSuccess(yes)->operation2->end\nisSuccess(no)->operation3->operation4(right)->operation1\n```\n\n## Katex Formula\n\n$$\n1 +  \\frac{q^2}{(1-q)}+\\frac{q^6}{(1-q)(1-q^2)}+\\cdots=\\prod_{j=0}^{\\infty}\\frac{1}{(1-q^{5j+2})(1-q^{5j+3})},\\text{ for }\\lvert q\\rvert < 1.\n$$\n"
const cursor = {
  anchor: {line: 0, ch: 0},
  focus: {line: 0, ch: 0}
}

export default {
  name: 'Editor',
  components: {
    NoteDetailSidebar,
  },
  created () {
    this.$nextTick(() => {
      const ele = this.$refs.editor

      Muya.use(TablePicker)
      Muya.use(QuickInsert)
      Muya.use(CodePicker)
      Muya.use(EmojiPicker)
      Muya.use(ImagePathPicker)
      Muya.use(ImageSelector)
      Muya.use(FormatPicker)
      Muya.use(FrontMenu)

      this.editor = new Muya(ele, {
        // markdown: `# 欢迎使用Webdocs`,
        markdown: this.document.body,
        imageAction: async (obj) => {
          if (obj instanceof File) {
            // 在这里把图片上传到服务器，返回服务器返回的路径
            const form = new FormData()
            form.append('image', obj, obj.name)
            let host = window.location.host
            let protocol = window.location.protocol
            // for dev
            if (host.search('localhost') !== -1) {
              host = 'localhost:8000'
            }
            form.append('document', `${protocol}//${host}/api/documents/${this.document.id}/`)
            const res = await this.axios.post(`/api/images/`, form, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
            return res.data.image
            // return res.data.image.match(/\/uploads\/images.*$/)[0]
            // return await new Promise(resolve => {
            //   const reader = new FileReader()
            //   reader.onload = event => {
            //     resolve(event.target.result)
            //   }
            //   reader.readAsDataURL(obj)
            // })
          } else {
            // console.log('imageAction:', obj)
            return obj
          }
          // await new Promise(r => setTimeout(r, 2000))
          // return 'https://i0.hdslb.com/bfs/archive/e62b6b095ef38dfb742687f11e4b570dde420b5d.png'
        },
        imagePathPicker: async () => { // return the src/path
          const file = await this.selectFile()
          return file
          // return await new Promise(resolve => {
          //   const reader = new FileReader()
          //   reader.onload = event => {
          //     resolve(event.target.result)
          //   }
          //   reader.readAsDataURL(file)
          // })
          // return 'https://i0.hdslb.com/bfs/archive/e62b6b095ef38dfb742687f11e4b570dde420b5d.png'
        }
      })

      const delaySave = () => {
        if (this.saveHandler != null) {
          clearTimeout(this.saveHandler)
        }
        this.saveHandler = setTimeout(this.save, 10000)
      }
      this.editor.on('change', changes => {
        // console.log(changes, this.document)
        // TODO: fix muya import problem of \n
        if (this.status == 'Initializing' || changes.markdown.replace(/\n+$/, '') == this.document.body.replace(/\n+$/, '')) {
          return
        }
        this.status = 'Unsaved'
        delaySave()
      })

      this.fetchData()
    })
  },
  data () {
    return {
      fileInputCallback: () => {},
      status: 'Saved',
      saveHandler: null,
      document: {
        id: null,
        body: ''
      },
      statusStyle: {
        Saved: { variant: 'success', icon: 'cloud-check' },
        Saving: { variant: 'secondary', icon: 'cloud-upload' },
        // 'Saved locally': { variant: 'info', icon: 'check2' },
        Unsaved: { variant: 'warning', icon: 'exclamation' },
        Initializing: { variant: 'secondary', icon: 'cloud-download' },
      }
    }
  },
  // watch: {
  //   '$route'() {
  //     if (this.$route.name == 'NoteEdit' && Number(this.$route.params.id) !== this.document.id) {
  //       this.fetchData()
  //     }
  //   }
  // },
  methods: {
    beforeRouteUpdate(to, from, next) {
      this.fetchData()
    },
    beforeRouteLeave(to, from, next) {
      if (this.status == 'Saved') {
        next()
      } else {
        clearTimeout(this.saveHandler)
        this.$bvModal.msgBoxConfirm(this.$t('Save this note?'), {
          title: this.$t('Not saved yet'),
          centered: true,
          okTitle: this.$t('Yes'),
          cancelTitle: this.$t('No')
        })
          .then(ans => {
            // 'ans' can be undefined
            if (ans === true) {
              this.save().then(() => {
                if (this.status == 'Saved') {
                  next()
                }
              })
            } else if (ans === false) {
              next()
            }
          })
      }
    },
    $t(a) {return a},
    async fetchData() {
      this.status = 'Initializing'
      // this.editor.setMarkdown('')
      const docId = this.$route.params.id
      try {
        const res = await this.axios.get(`/api/documents/${docId}/`)
        this.document = res.data
        this.status = 'Saved'
        this.editor.setMarkdown(this.document.body)
      } catch (err) {
        console.log(err)
        alert('Failed to load markdown, please retry...')
      }
    },
    async save() {
      if (this.status == 'Saved' || this.status == 'Saving') {
        return
      }
      this.status = 'Saving'
      console.log(this.editor.getTOC())
      // saved locally
      // send save request to the server
      try {
        const res = await this.axios.patch(`/api/documents/${this.document.id}/`, {
          id: this.document.id,
          body: this.editor.markdown
        })
        this.document = res.data
        this.status = 'Saved'
      } catch (err) {
        console.log(err)
        this.status = 'Unsaved'
      }
      // await new Promise(r => setTimeout(r, 1000))
      // let saved = Math.random() < 0.5
      // this.status = saved ? 'Saved' : 'Saved locally'
    },
    selectFile () {
      const fileInput = this.$refs['file-input']
      return new Promise((resolve, reject) => {
        this.fileInputCallback = (e) => {
          const file = fileInput.files[0]
          fileInput.value = ''
          resolve(file)
        }
        fileInput.click()
      })
      // console.log(this.$refs['file-input'].files)
    },
    keydownHandler (event) {
      if ((event.ctrlKey || event.metaKey) && event.keyCode == 83 && !event.altKey && !event.shiftKey) {
        // ctrl-s or command-s
        event.preventDefault()
        this.save()
      } else if ((event.ctrlKey || event.metaKey) && event.keyCode == 90 && !event.altKey && !event.shiftKey) {
        // ctrl-z or command-z
        event.preventDefault()
        this.editor.undo()
      } else if ((event.ctrlKey || event.metaKey) && event.keyCode == 89 && !event.altKey && !event.shiftKey) {
        // ctrl-y or command-y
        event.preventDefault()
        this.editor.redo()
      }
    },
  }
}
</script>

<style scoped>
#editor-wrapper {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  /* margin-top: 10px; */
}

#return-button {
  position: fixed;
  top: 4vh;
  left: 2vw;
}

#sidebar-button {
  position: fixed;
  top: 12vh;
  left: 2vw;
}

#status-button {
  position: fixed;
  top: 4vh;
  right: 2vw;
}
</style>
