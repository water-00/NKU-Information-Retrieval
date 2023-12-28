<template>
  <div class="news-detail-container">
    <div class="header">
      <h1>{{ title }}</h1>
      <p class="meta">
        <span>{{ ctime }}</span> <span>{{ media_name }}</span>
      </p>
    </div>
    <div class="content">
      <p>{{ content }}</p>
    </div>
    <div class="keywords">
      <p>
        <strong>关键字：</strong
        ><span class="keyword" v-for="keyword in keywordsList" :key="keyword">{{
          keyword
        }}</span>
      </p>
    </div>
    <button @click="goBack" class="back-button">返回</button>
    <button @click="openSnapshot" class="snapshot-button">网页快照</button>
    <div class="footer">
      <p>© 2023 Haogle</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DetailedPage",

  data() {
    return {
      id: "",
      title: "",
      ctime: "",
      media_name: "",
      content: "",
      keywords: "",
      keywordsList: [],
    };
  },

  created() {
    if (this.$route.query) {
      this.id = this.$route.query.id;
      this.title = this.$route.query.title;
      this.ctime = this.$route.query.ctime;
      this.media_name = this.$route.query.media_name;
      this.content = this.$route.query.content;
      this.keywords = this.$route.query.keywords;
      this.keywordsList = this.keywords.split(","); // 假设关键字是以逗号分隔的
    }
  },

  methods: {
    goBack() {
      this.$router.go(-1);
    },
    openSnapshot() {
      const imageName = this.formatTitleToFilename(this.title);
      const url = `http://localhost:5000/open-snapshot?image_name=${imageName}`;

      axios.get(url)
        .then(response => {
          console.log('Snapshot opened:', response.data);
        })
        .catch(error => {
          console.error('There has been a problem with your axios operation:', error);
        });
    },
    formatTitleToFilename(title) {
      // 替换掉标题中所有非法的文件名字符，例如空格替换为下划线
      return title.replace(/[\s]+/g, '_');
    }
  },
};
</script>

<style scoped>
.news-detail-container {
  padding: 30px 50px; /* 页面左右边距 */
  font-family: "Arial", sans-serif;
  position: relative;
  padding-bottom: 50px; /* 为返回按钮留出空间 */
}

.back-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  margin: 10px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.snapshot-button {
  background-color: #008CBA; /* 蓝色背景 */
  color: white;
  padding: 10px 20px;
  margin: 10px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px; /* 和返回按钮保持一定间距 */
}

h1 {
  color: #333;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.meta {
  font-size: 14px;
  color: #888;
  margin-bottom: 20px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
}

.keywords {
  margin-top: 20px;
  color: #555;
}

.keyword {
  background-color: #ddd;
  padding: 5px;
  margin-right: 5px;
  border-radius: 5px;
}

.footer {
  margin-top: 40px;
  text-align: center;
  color: #888;
}

@media screen and (max-width: 768px) {
  .news-detail-container {
    padding: 0 20px; /* 移动设备上的页面左右边距 */
  }

  .back-button {
    left: 20px; /* 移动设备上返回按钮的位置 */
  }
}
</style>
