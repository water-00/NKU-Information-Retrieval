<template>
  <div>
    <!-- 单独的 div 用于固定登录按钮 -->
    <div class="fixed-header">
      <a-button class="login-button" @click="showLoginModal">登录</a-button>
      <LoginComponent v-if="showLogin" @close="showLogin = false" />
    </div>

    <div class="home">
      <LogoComponent class="ha"></LogoComponent>
      <!-- 登录组件或对话框 -->

      <div class="search-input">
        <a-input-search
          size="large"
          placeholder="在 Haogle 上搜索新闻"
          v-focus
          v-model="searchText"
          @search="onSearch"
        />
        <div class="buttons">
          <a-button :class="{ active: isPhraseSearch }" @click="onPhraseSearch"
            >短语查询</a-button
          >
          <a-button
            :class="{ active: isWildcardSearch }"
            @click="onWildcardSearch"
            >通配查询</a-button
          >
        </div>
        <p v-if="isWildcardSearch" class="wildcard-description">
          通配查询可以使用 * 代表任意字符，? 代表一个字符。
        </p>
        <!-- 短语查询表单 -->
        <div v-if="isPhraseSearch" class="phrase-search-form">
          <div class="form-item">
            <label>必须包含的关键词：</label>
            <a-input placeholder="关键词..." v-model="keywords" />
          </div>
          <div class="form-item">
            <label>起始日期：</label>
            <a-input placeholder="YYYY-MM-DD" v-model="startDate" />
          </div>
          <div class="form-item">
            <label>截止日期：</label>
            <a-input placeholder="YYYY-MM-DD" v-model="endDate" />
          </div>
          <div class="form-item">
            <label>来源媒体：</label>
            <a-input placeholder="媒体..." v-model="media" />
          </div>
          <div class="form-item">
            <label>不包含以下内容：</label>
            <a-input placeholder="不包含的内容..." v-model="excludedContent" />
          </div>
          <div class="form-item">
            <a-button type="primary" @click="onSearch">搜索</a-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 子组件
import LogoComponent from "@/components/LogoComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";

export default {
  name: "HomePage",
  data() {
    return {
      searchText: "",
      isWildcardSearch: false,
      isPhraseSearch: false,
      keywords: "",
      startDate: "",
      endDate: "",
      media: "",
      excludedContent: "",
      showLogin: false, // 控制登录组件的显示
    };
  },
  components: {
    LogoComponent,
    LoginComponent, // 注册登录组件
  },
  methods: {
    onSearch() {
      if (this.searchText !== "") {
        this.$router
          .push({
            path: `/search`,
            query: {
              q: this.searchText,
              wildcard: this.isWildcardSearch,
              phrase: this.isPhraseSearch,
              keywords: this.keywords,
              startDate: this.startDate,
              endDate: this.endDate,
              media: this.media,
              excludedContent: this.excludedContent,
            },
          })
          .catch((err) => {
            if (err.name !== "NavigationDuplicated") {
              throw err;
            }
          });
        console.info("home router q  :" + this.searchText);
      }
    },
    onPhraseSearch() {
      this.isWildcardSearch = false;
      this.isPhraseSearch = !this.isPhraseSearch;
    },
    onWildcardSearch() {
      this.isPhraseSearch = false;
      this.isWildcardSearch = !this.isWildcardSearch;
    },
    showLoginModal() {
      this.showLogin = !this.showLogin; // 显示登录组件
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
.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  padding: 20px;
}

.login-button {
  position: absolute; /* 使用 fixed 而不是 absolute，以便按钮固定在视口的右上角 */
  top: 20px; /* 距离顶部的距离 */
  right: 20px; /* 距离右侧的距离 */
}

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

.phrase-search-form {
  background: #fff;
  padding: 20px;
  margin-top: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.form-item label {
  min-width: 130px;
  text-align: right;
  margin-right: 10px;
}
</style>
