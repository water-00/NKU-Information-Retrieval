<template>
  <div>
    <a-card hoverable>
      <a-card-meta
        :title="info._source.title"
        :description="info._source.ctime"
      >
        <!-- 修改为长方形头像，可以通过调整width和height的值来改变长方形的尺寸 -->
        <template #avatar>
          <a-avatar shape="square" style="background-color: #d04713; width: 50px; height: 30px;">{{ info._source.media_name || '新闻' }}</a-avatar>
        </template>
      </a-card-meta>
      <!-- 修改描述部分，使其左对齐-->
      <div class="describe">{{info._source.content.slice(0, 200) + '...' }}</div>
      <!-- 显示Elasticsearch返回的_score值 -->
      <div class="score">{{ info._score }}</div>
    </a-card>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: ["info"],
};
</script>

<style scoped>
div {
  margin-top: 12px;
}

.describe {
  padding: 12px 0 0 0;
  text-align: left; /* 左对齐文本 */
  color: #d04713;
}

.score {
  text-align: right;
}
</style>
