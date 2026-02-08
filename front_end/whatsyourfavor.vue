<template>
  <!--给div标签(最外层容器)加上选择器--> 
  <div class="chat-container">
    <div class="search-bar">
      <h2 class="search_title">Whatsyourfavorite</h2>
      <input
        v-model="userInput"
        @keyup.enter="sendQuery"
        class="search-input"
        placeholder="Search"
      />
    </div>
    <!--vue指令遍历results字典列表,每个元素都有自己的区域;:key负责给这个元素增加标识--> 
    <div v-if="mode === 'list'" class="result-list">
      <div class="results-area" v-for="item in results" :key="item.title.text">
      <!--超链接标签,用户点击后跳转到results字典元素中的作品链接；这里是后端爬取的正文链接展示于前端--> 
        <a class="title" href="#" @click.prevent="loadText(item.title.url)">
          {{ item.title.text }}
        </a>
        <div class="author">
          by
          <a href="#" @click.prevent="loadAuthor(item.author.url)">
            {{ item.author.text }}
          </a>
        </div>
        <div class="tags">
          <a
            v-for="t in item.tags"
            :key="t.text"
            href="#"
            @click.prevent="loadTag(t.url)"
          >
            #{{ t.text }}
          </a>
        </div>
      </div>
      <div v-if="mode === 'text'" class="text-view">
        <button class="back" @click="mode = 'list'">← Back</button>
        <h2 class="text-title">{{ currentTitle }}</h2>
          <article>
            <p v-for="(p, i) in fullText" :key="i">
            {{ p }}
            </p>
          </article>
      </div>
    </div>
  </div>
</template>

<script setup>
  // ref用来更新爬取内容，onMounted表示组件挂载完成后执行
import { ref, onMounted } from 'vue'
// 
const userInput = ref('')
// 保存爬取函数返回的数据列表
const results = ref([])
const fullText = ref([])
const mode = ref('list')
// let声明的变量可以被重新赋值，这里存放了websocket实例
let socket

// vue首次渲染完成时执行，
onMounted(() => {
  socket = new WebSocket('ws://localhost:8000/ws')
  socket.onmessage = (e) => {
    // 监听后端消息
    const msg = JSON.parse(e.data)
    if (msg.type === 'text_result') {
      fullText.value = msg.data
      mode.value = 'text'
    } else {
      results.value = msg.data
      mode.value = 'list'
    }
  }
})
function loadText(url){
  socket.send(JSON.stringify({type: 'text', url}))
}
function sendQuery() {
  // 传信给后端
  socket.send(JSON.stringify({ type: 'search', query: userInput.value }))
}
function loadAuthor(url) {
  socket.send(JSON.stringify({type: 'author', url: url }))
}
function loadTag(url) {
  socket.send(JSON.stringify({type: 'tag', url: url}))
}

</script>
