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
// import axios from "axios";

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
      if (this.searchText !== "") {
        this.$router.push({ 
            path: `/search`, 
            query: { 
              q: this.searchText, 
              wildcard: this.isWildcardSearch, 
              phrase: this.isPhraseSearch 
            }
          }).catch((err) => {
          if (err.name !== "NavigationDuplicated") {
            throw err;
          }
        });
        console.info("home router q  :" + this.searchText);
      }
    },
    onPhraseSearch() {
      this.isWildcardSearch = false;
      this.isPhraseSearch = !this.isPhraseSearch
    },
    onWildcardSearch() {
      this.isPhraseSearch = false;
      this.isWildcardSearch = !this.isWildcardSearch;
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
