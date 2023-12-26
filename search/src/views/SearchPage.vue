<template>
  <div class="search">
    <div class="left">
      <img src="./../assets/haogle.png" @click="goHome" />
    </div>
    <div class="right">
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
// 导入子组件，axios用于发起HTTP请求，SearchResult用于显示搜索结果
import axios from "axios";
import SearchResult from "../components/SearchResult";

export default {
  name: "SearchPage",
  data() {
    return {
      searchText: "",
      result: [],
    };
  },
  components: {
    SearchResult,
  },
  methods: {
    goHome() {
      this.$router.push("/").catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    searchResult() {
      const currentQuery = this.$route.query.q;
      if (this.searchText !== "" && this.searchText !== currentQuery) {
        this.$router
          .push({ path: `/search`, query: { q: this.searchText } })
          .catch((err) => {
            if (err.name !== "NavigationDuplicated") {
              throw err;
            }
          });
      }

      const path = "http://localhost:5000/search?q=" + currentQuery;
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
    this.searchResult();
  },
  watch: {
    '$route.query.q'(newQuery) {
      this.searchText = newQuery || '';
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