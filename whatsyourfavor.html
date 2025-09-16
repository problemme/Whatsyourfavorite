<template>
  <!--给div标签(最外层容器)加上选择器--> 
  <div class="chat-container">
    <!--vue指令遍历results字典列表,每个元素都有自己的区域;:key负责给这个元素增加标识--> 
    <div v-for="item in results" :key="item.title.text">
      <!--超链接标签,用户点击后跳转到results字典元素中的作品链接--> 
      <a :href="item.title.url" target="_blank">{{ item.title.text }}</a>
      <!--文本标签，显示"by"--> 
      <span>by</span>
      <!--href后跟链接,{{}}表示文本--> 
      <a :href="item.author.url" target="_blank">{{ item.author.text }}</a>
      <!--作品标签区域--> 
      <div class="tags">
        <a v-for="t in item.tags" :key="t.text" :href="t.url" target="_blank">
        {{ t.text }}
        </a>
      </div>
    </div>
    <!--v-model用于双向绑定,输入框的值与userinput同步:--> 
    <!-- @keyup.enter表示按下回车键时触发sendQuery方法-->
    <input v-model="userInput" @keyup.enter="sendQuery" placeholder="Whatsyourfavorite"/>
  </div>
</template>

<script setup>
  // ref用来自动更新视图变量，onMounted表示组件挂载完成后执行
import { ref, onMounted } from 'vue'
// const定义的变量不会改变，但如果是ref或对象则可以改变
const userInput = ref('')
// 保存爬取函数返回的数据列表
const results = ref([])
// let声明的变量可以被重新赋值，这里存放了websocket实例
let socket

// vue首次渲染完成时执行
onMounted(() => {
  socket = new WebSocket('ws://localhost:8000/ws')
  socket.onmessage = (e) => {
    // 监听后端消息
    const msg = JSON.parse(e.data)
    if (msg.type === 'result') results.value = msg.data
  }
})

function sendQuery() {
  // 将用户输入的消息格式化后发送到后端
  socket.send(JSON.stringify({ type: 'search', query: userInput.value }))
}
</script>
