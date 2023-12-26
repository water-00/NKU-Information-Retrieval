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
        style="margin-bottom: 10px;"
      />通配查询
      <a-input-search
        v-focus
        v-model="searchText"
        size="large"
        @search="searchResult"
      />
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
      isPhraseSearch: false
    };
  },
  components: {
    SearchResult,
  },
  methods: {
    toggleWildcard(value) {
      this.isWildcardSearch = value;
      console.log(this.isWildcardSearch)
    },
    goHome() {
      this.$router.push("/").catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    searchResult() {
      // const currentQuery = this.$route.query.q;
      if (this.searchText !== "") {
        this.$router.push({ 
            path: `/search`, 
            query: { 
              q: this.searchText, 
              wildcard: this.isWildcardSearch, 
              phrase: this.isPhraseSearch 
            }
          })
          .catch((err) => {
            if (err.name !== "NavigationDuplicated") {
              throw err;
            }
          });
      }

      const path = `http://localhost:5000/search?q=${encodeURIComponent(this.searchText)}&wildcard=${this.isWildcardSearch}&phrase=${this.isPhraseSearch}`;

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
    this.searchText = this.$route.query.q || '';
    this.isWildcardSearch = this.$route.query.wildcard === 'true';
    this.isPhraseSearch = this.$route.query.phrase === 'true';
    this.searchResult();
  },
  watch: {
    '$route.query'(newQuery) {
      this.searchText = newQuery.q || '';
      this.isWildcardSearch = newQuery.wildcard === 'true';
      this.isPhraseSearch = newQuery.phrase === 'true';
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

</style>
