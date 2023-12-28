<template>
  <div class="search">
    <div class="left">
      <img src="./../assets/haogle.png" @click="goHome" />
    </div>
    <div class="right">
      <!-- 添加通配查询的切换开关 -->
      <a-switch
        :checked="isWildcardSearch"
        @change="toggleWildcard"
        style="margin-bottom: 10px"
      />通配查询
      <a-switch
        :checked="isPhraseSearch"
        @change="togglePhrase"
        style="margin-bottom: 10px"
      />短语查询
      <a-input-search
        v-focus
        v-model="searchText"
        size="large"
        @search="searchResult"
      />
      <p v-if="isWildcardSearch" class="wildcard-description">
        通配查询可以使用 * 代表任意字符，? 代表一个字符。
      </p>
      <!-- 短语查询表单 -->
      <a-row v-if="isPhraseSearch" class="phrase-search-form" gutter="16">
        <a-col :span="24" class="phrase-search-keywords">
          <a-input placeholder="请输入关键词..." v-model="keywords" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="起始日期..." v-model="startDate" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="截止日期..." v-model="endDate" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="来源媒体..." v-model="media" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="排除内容..." v-model="excludedContent" />
        </a-col>
        <a-col :span="24" class="phrase-search-button">
          <a-button type="primary" @click="searchResult">短语搜索</a-button>
        </a-col>
      </a-row>
      
      <div v-for="item in result" :key="item.id">
        <SearchResult :info="item"></SearchResult>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SearchResult from "../components/SearchResult";

export default {
  name: "SearchPage",
  data() {
    return {
      searchText: "",
      result: [],
      isWildcardSearch: false,
      isPhraseSearch: false,
      keywords: "",
      startDate: "",
      endDate: "",
      media: "",
      excludedContent: "",
    };
  },
  components: {
    SearchResult,
  },
  methods: {
    toggleWildcard(value) {
      this.isWildcardSearch = value;
      if (value) {
        this.isPhraseSearch = false;
      }
    },
    togglePhrase(value) {
      this.isPhraseSearch = value;
      if (value) {
        this.isWildcardSearch = false;
      }
    },
    goHome() {
      this.$router.push("/").catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    searchResult() {
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
      }

      const path = `http://localhost:5000/search?q=${encodeURIComponent(
        this.searchText
      )}&wildcard=${this.isWildcardSearch}&phrase=${
        this.isPhraseSearch
      }&keywords=${this.keywords}&startDate=${this.startDate}&endDate=${
        this.endDate
      }&media=${this.media}&excludedContent=${this.excludedContent}`;
      axios
        .get(path)
        .then((res) => {
          this.result = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.searchText = this.$route.query.q || "";
    this.isWildcardSearch = this.$route.query.wildcard === "true";
    this.isPhraseSearch = this.$route.query.phrase === "true";
    this.keywords = this.$route.query.keywords;
    this.startDate = this.$route.query.startDate;
    this.endDate = this.$route.query.endDate;
    this.media = this.$route.query.media;
    this.excludedContent = this.$route.query.excludedContent;
    this.searchResult();
  },
  watch: {
    "$route.query"(newQuery) {
      this.searchText = newQuery.q || "";
      this.isWildcardSearch = newQuery.wildcard === "true";
      this.isPhraseSearch = newQuery.phrase === "true";
      this.keywords = this.$route.query.keywords;
      this.startDate = this.$route.query.startDate;
      this.endDate = this.$route.query.endDate;
      this.media = this.$route.query.media;
      this.excludedContent = this.$route.query.excludedContent;
      this.searchResult();
    },
  },
};
</script>

<style scoped>
.search {
  padding-top: 24px;
  overflow: hidden;
  zoom: 1;
}

.left {
  float: left;
  margin: 0 20px;
  text-align: center;
}

.right {
  width: 600px;
  overflow: hidden;
  zoom: 1;
}

img {
  padding-top: 4px;
  text-align: center;
}

/* 调整表单元素的宽度 */
.phrase-search-form .ant-input,
.phrase-search-form .ant-picker {
  width: 100%;
}

/* 单独为关键词输入框添加上方间隔 */
.phrase-search-keywords {
  margin-top: 10px; /* 调整这个值来增加或减少间隔 */
}

/* 单独为短语搜索按钮添加上方间隔 */
.phrase-search-button {
  margin-top: 5px; /* 调整这个值来增加或减少间隔 */
}

.wildcard-description {
  margin-top: 10px; /* 在说明文字和按钮之间添加空间 */
  color: #666; /* 说明文字的颜色 */
}
</style>
