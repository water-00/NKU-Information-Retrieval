<template>
  <div class="home">
    <LogoComponent class="ha"></LogoComponent>
    <div class="search-input">
      <a-input-search
        size="large"
        placeholder="在 Haogle 上搜索新闻"
        v-focus
        v-model="searchText"
        @search="onSearch"
      />
      <div class="buttons">
        <a-button @click="onPhraseSearch">短语查询</a-button>
        <a-button :class="{active: isWildcardSearch}" @click="onWildcardSearch">通配查询</a-button>
      </div>
      <p v-if="isWildcardSearch" class="wildcard-description">
        通配查询可以使用 * 代表任意字符，? 代表一个字符。
      </p>
    </div>
  </div>
</template>

<script>
// 子组件
import LogoComponent from "@/components/LogoComponent.vue";
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      searchText: "",
      isWildcardSearch: false, // 新增状态，用于跟踪通配查询是否激活
      isPhraseSearch: false
    };
  },
  components: {
    LogoComponent,
  },
  methods: {
    onSearch() {
      // 如果通配查询激活，则调用通配查询函数，否则执行正常搜索
      if (this.isWildcardSearch) {
        this.wildcardSearch();
      } else {
        if (this.searchText !== "") {
          this.$router
            .push({ path: `/search`, query: { q: this.searchText } })
            .catch((err) => {
              if (err.name !== "NavigationDuplicated") {
                throw err;
              }
            });
          console.info("home router q  :" + this.searchText);
        }
      }
    },
    onPhraseSearch() {
      // 处理短语查询的逻辑
      console.info("Performing phrase search for: " + this.searchText);
      // 如果当前是通配查询模式，则关闭它
      this.isWildcardSearch = false;
    },
    onWildcardSearch() {
      this.isPhraseSearch = false;
      this.isWildcardSearch = !this.isWildcardSearch;
    },
    wildcardSearch() {
      // 通配查询的逻辑
      console.info("Performing wildcard search for: " + this.searchText);

      // 检查搜索文本是否为空
      if (this.searchText.trim() === '') {
        console.warn("Search text is empty.");
        return;
      }

      // 构造通配符查询的URL
      const path = `http://localhost:5000/search?wildcard=true&q=${encodeURIComponent(this.searchText)}`;

      // 发送GET请求到后端服务
      axios.get(path)
        .then((res) => {
          // 将结果赋值给result数据属性以更新显示结果
          this.result = res.data;
        })
        .catch((error) => {
          // 打印错误到控制台
          if (error.name !== "NavigationDuplicated") {
            throw error;
          }
          console.error("Error during wildcard search: ", error);
        });
    },
  },
  directives: {
    focus: {
      inserted: function (el) {
        el.focus();
      },
    },
  },
};
</script>

<style scoped>
.home {
  position: absolute;
  left: 50%;
  top: 40%;
  transform: translate(-50%, -50%);
}

.search-input {
  width: 600px;
  text-align: center;
}

.ha {
  text-align: center;
  margin-bottom: 20px;
}

.buttons {
  margin-top: 20px;
}

a-button {
  margin: 0 10px;
}

a-button.active {
  background-color: #1890ff; /* 按钮激活时的背景色 */
  color: white;
}

.wildcard-description {
  margin-top: 10px; /* 在说明文字和按钮之间添加空间 */
  color: #666; /* 说明文字的颜色 */
}
</style>
