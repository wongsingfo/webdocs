<template>
  <div>
    <b-overlay :show="status === 'Initializing'">
      <div
        class="button-area"
        @mouseleave="showButtons = false"
        @mousemove="showButtons = true"
      >
        <transition name="fade">
          <div v-show="showButtons">
            <b-button
              id="return-button"
              class="left-side-button"
              pill
              variant="outline-dark"
              @click="handleBackButton"
            >
              <b-icon icon="arrow-left"></b-icon>
              {{ this.historyLength > 1 ? 'Back' : 'Home' }}
            </b-button>
            <b-button
              id="detail-button"
              v-b-toggle.editor-note-detail
              class="left-side-button"
              pill
              variant="outline-dark"
            >
              <b-icon icon="card-list"></b-icon>
              Note Details
            </b-button>
            <b-button
              id="toc-button"
              v-b-toggle.toc-sidebar
              class="left-side-button"
              pill
              variant="outline-dark"
            >
              <b-icon icon="bar-chart-steps"></b-icon>
              Table of Contents
            </b-button>
            <b-button
              id="refresh-button"
              class="left-side-button"
              pill
              variant="outline-dark"
              @click="fetchData"
            >
              <b-icon icon="arrow-clockwise"></b-icon>
              Refresh
            </b-button>
          </div>
        </transition>
      </div>
      <b-button
        id="status-button"
        pill
        :variant="statusStyle[status].variant"
        style="z-index: 20"
        v-b-tooltip.hover
        title="Click to save!"
        @click="save"
      >
        <b-icon :icon="statusStyle[status].icon"></b-icon>
        {{ status }}
      </b-button>
      <div id="editor-wrapper" class="editor" @keydown="keydownHandler">
        <div ref="editor"></div>
      </div>
      <NoteDetailSidebar id="editor-note-detail" :document="document"/>
      <TOCSidebar id="toc-sidebar" :toc="toc" />
    </b-overlay>
    <input
      v-show="false"
      ref="file-input"
      type="file"
      accept="image/*"
      @change="fileInputCallback"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'

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
import TOCSidebar from '@/components/TOCSidebar.vue'

// const example = "# Muya Example\n\n## English Text\n\n#### Sponsor Mark Text Development\n\nMark Text is an MIT licensed open source project, you will always be able to download the latest version from [GitHub release page](https://github.com/marktext/marktext/releases). Mark Text is still in development, and its development is inseparable from all sponsors. I hope you join them:\n\n## Chinese Text\n\n9月1日，外交部发言人华春莹主持例行记者会。有记者就中印边境最新事态提问。\n\n华春莹表示，关于边界等历史遗留的问题，中方历来主张通过和平友好协商，找到公平合理和双方都能接受的解决方案。一段时间以来，双方在各个层级进行了多次接触和会谈，作出积极的努力来寻求和平解决边界的一些分歧或争端，共同维护中印边境地区的和平与稳定。\n\n但是在8月31日，印军破坏了前期双方多层级会谈会晤达成的共识，在中印边界的西段班公湖以南地区以及热钦山口附近再次非法越线，公然挑衅，造成边境局势再度紧张。印方的行径严重侵犯了中方的领土主权，也严重违反了两国相关的协定、协议和重要的共识，破坏了边境地区的和平与安宁。这与双方一段时间以来推动现地局势缓和降温的努力是背道而驰的，中方对此坚决反对并且已经向印方提出了严正交涉，要求印方停止一切挑衅行为，立即撤回非法越线的人员，立即停止任何导致局势紧张、升级和复杂化的举动。\n\n(本文来自澎湃新闻，更多原创资讯请下载“澎湃新闻”APP)\n\n![](https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=3604977702,2490965591&fm=173&app=49&f=JPEG?w=312&h=208&s=EF924781C4C074FC9499958A0300E091)\n\n## Code Block\n\n```js\nconst arr1 = [1,2,3,[1,2,3,4, [2,3,4]]]function flatten(input) { // flatten deep using a stack  const stack = [...input]  const res = []  while (stack.length) {    const next = stack.pop()    if (Array.isArray(next)) {      stack.push(...next)    } else {      res.push(next)    }  }  return res.reverse()}flatten(arr1)// [1, 2, 3, 1, 2, 3, 4, 2, 3, 4]\n```\n\n## Table\n\n```\n| 标题1 | 标题2 | 标题3 || :--  | :--: | ----: || 左对齐 | 居中 | 右对齐 || ---------------------- | ------------- | ----------------- |\n```\n\n| 标题1                    | 标题2           | 标题3               |\n| ---------------------- | ------------- | ----------------- |\n| 左对齐                    | 居中            | 右对齐               |\n| ---------------------- | ------------- | ----------------- |\n\n## Flowchart\n\n```flowchart\nstart=>start: start\noperation1=>operation: operation1\nisSuccess=>condition: success?\noperation2=>operation: operation2\noperation3=>operation: operation3\noperation4=>operation: operation4\nend=>end: 结束\nstart->operation1->isSuccess\nisSuccess(yes)->operation2->end\nisSuccess(no)->operation3->operation4(right)->operation1\n```\n\n## Katex Formula\n\n$$\n1 +  \\frac{q^2}{(1-q)}+\\frac{q^6}{(1-q)(1-q^2)}+\\cdots=\\prod_{j=0}^{\\infty}\\frac{1}{(1-q^{5j+2})(1-q^{5j+3})},\\text{ for }\\lvert q\\rvert < 1.\n$$\n"

Muya.use(TablePicker)
Muya.use(QuickInsert)
Muya.use(CodePicker)
Muya.use(EmojiPicker)
Muya.use(ImagePathPicker)
Muya.use(ImageSelector)
Muya.use(FormatPicker)
Muya.use(FrontMenu)

function cleanLine(line) {
  return line.replace(/^#+ /, '')
}

function cleanText(markdown) {
  return markdown
    .replace(/```.*```/g, '')
    .replace(/!\[([^\]]*)\]\(.[^\)]*\)/g, '')
    .replace(/\[([^\]]*)\]\(.[^\)]*\)/g, (...match) => match[1])
}

function getTitleAndAbstract(markdown) {
  const lines = markdown.split('\n').map(cleanLine)
  const title = cleanText(lines[0]) || undefined
  const plainText = cleanText(lines.slice(1).join(''))
  const abstract = plainText.slice(0, 200) + (plainText.length > 200 ? '...' : '')
  return { title, abstract }
}

export default {
  name: 'Editor',
  components: {
    NoteDetailSidebar,
    TOCSidebar,
  },
  async created () {
    await this.$nextTick()

    window.onbeforeunload = (event) => {
      return this.status == 'Unsaved' ? true : null
    }

    this.editor = new Muya(this.$refs.editor, {
      // markdown: `# 欢迎使用Webdocs`,
      markdown: '',
      imageAction: async (obj, id, name) => {
        // console.log('imageAction:', obj, ' ', id, ' ', name)
        if (obj instanceof File) {
          return await this.uploadImage(obj)
        } else {
          return obj
        }
      },
      imagePathPicker: async () => await this.uploadImage(await this.selectFile()),
    })

    this.editor.on('change', changes => {
      // console.log(changes, this.document)
      // TODO: fix muya import problem of \n
      if (this.status == 'Initializing' || !this.document ||
        changes.markdown.replace(/\n+$/, '') == this.document.body.replace(/\n+$/, '')) {
        return
      }
      this.toc = this.editor.getTOC()
      this.status = 'Unsaved'

      clearTimeout(this.saveHandler)
      this.saveHandler = setTimeout(this.save, 10000)
    })

    await this.$store.dispatch('initDB')
    await this.fetchData()
  },
  beforeDestroy() {
    window.onbeforeunload = this.savedOnbeforeunloadHandler
  },
  data () {
    return {
      status: 'Initializing',
      fileInputCallback: () => {},
      saveHandler: null,
      document: null,
      toc: [],
      statusStyle: {
        Saved: { variant: 'success', icon: 'cloud-check' },
        Saving: { variant: 'secondary', icon: 'cloud-upload' },
        'Saved Locally': { variant: 'info', icon: 'check' },
        Unsaved: { variant: 'warning', icon: 'exclamation' },
        Initializing: { variant: 'secondary', icon: 'cloud-download' },
      },
      showButtons: false,
      historyLength: window.history.length,
      savedOnbeforeunloadHandler: window.onbeforeunload,
    }
  },
  computed: mapState(['db']),
  methods: {
    handleBackButton() {
      if (this.historyLength > 1) {
        this.$router.go(this.historyLength - window.history.length - 1)
      } else {
        this.$router.replace('/')
      }
    },
    beforeRouteUpdate(to, from, next) {
      if (to.params.id != this.document.id) {
        this.confirmSave().then(ok => {
          if (ok) {
            this.fetchData()
            this.historyLength = window.history.length + 1
          }
        })
      }
    },
    beforeRouteLeave(to, from, next) {
      clearTimeout(this.saveHandler)
      this.confirmSave().then(ok => {
        if (ok) {
          next()
        }
      })
    },
    async confirmSave() {
      if (this.status != 'Unsaved') {
        return true
      }
      const ans = await this.$bvModal.msgBoxConfirm(this.$t('Save this note?'), {
        title: this.$t('Not saved yet'),
        centered: true,
        okTitle: this.$t('Yes'),
        cancelTitle: this.$t('No')
      })
      if (ans === true) {
        await this.save()
      }
      return this.status == 'Saved' || ans === false
    },
    async fetchData() {
      if (!await this.confirmSave()) {
        return
      }
      this.status = 'Initializing'
      // this.editor.setMarkdown('')
      const docId = Number(this.$route.params.id)
      let res
      try {
        res = await this.axios.get(`/api/documents/${docId}/`)
      } catch (err) {
        if (!err.repsonse) {
          await this.localLoad(docId)
          if (this.document) {
            this.editor.setMarkdown(this.document.body)
            this.toc = this.editor.getTOC()
            this.status = 'Saved Locally'
            return
          }
        }
        console.log(err)
        alert('Failed to load markdown, please retry...')
        return
      }
      await this.localLoad(docId)
      if (this.document && res.data.lastModified < this.document.lastModified) {
        // the local copy is newer, update server
        this.axios.patch(`/api/documents/${this.document.id}/`, {
          ...this.document,
          lastSync: undefined
        }).then(() => this.status = 'Saved', err => {
          console.log(err)
        })
      } else {
        res.data.lastSync = res.data.lastModified
        await this.localSave(res.data)
        this.status = 'Saved'
      }
      this.editor.setMarkdown(this.document.body)
      this.toc = this.editor.getTOC()
    },
    async localLoad(id) {
      const result = await this.db.$db.note.find(id)
      this.document = result.length > 0 ? result[0] : null
    },
    async localSave(doc) {
      this.document = doc
      await this.db.$db.note.update(doc.id, doc, { upsert: true })
      this.status = 'Saved Locally'
    },
    async save() {
      if (this.status == 'Saved' || this.status == 'Saving') {
        return
      }
      this.status = 'Saving'
      const markdown = this.editor.markdown
      const newDoc = {
        ...this.document,
        body: markdown,
        ...getTitleAndAbstract(markdown),
        lastSync: undefined
      }
      try {
        const res = await this.axios.patch(`/api/documents/${this.document.id}/`, newDoc)
        res.data.lastSync = res.data.lastModified
        await this.localSave(res.data)
        this.status = 'Saved'
      } catch (err) {
        console.log(err)
        this.status = 'Unsaved'
        await this.localSave({
          ...newDoc,
          lastModified: new Date(),
          lastSync: this.document.lastModified
        })
      }
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
    async uploadImage(image) {
      const form = new FormData()
      form.append('image', image, image.name)
      form.append('document', this.document.id)
      const res = await this.axios.post(`/api/images/`, form, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      let imageUrl = res.data.image
      if (window.location.hostname !== 'localhost' && imageUrl.startsWith('http://')) {
        imageUrl = 'https' + imageUrl.substring(4)
      }
      return imageUrl
      // read as base64 encoding
      // return await new Promise(resolve => {
      //   const reader = new FileReader()
      //   reader.onload = event => {
      //     resolve(event.target.result)
      //   }
      //   reader.readAsDataURL(obj)
      // })
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

.left-side-button {
  position: fixed;
  left: 2vw;
  z-index: 20;
}

#return-button {
  top: 4vh;
}

#detail-button {
  top: 12vh;
}

#toc-button {
  top: 20vh;
}

#refresh-button {
  top: 28vh;
}

#status-button {
  position: fixed;
  top: 4vh;
  right: 2vw;
}

.button-area {
  position: fixed;
  top: 0;
  left: 0;
  width: 20vw;
  height: 100vh;
  /* filter: blur(20px); */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
