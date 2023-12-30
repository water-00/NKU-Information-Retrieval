<template>
  <div class="login-container">
    <form @submit.prevent="onLogin">
      <div class="form-item">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-item">
        <label for="password">密码: </label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="login-button">登录</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginComponent",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    onLogin() {
      // 发送请求到后端进行验证
      const loginCredentials = {
        username: this.username,
        password: this.password,
      };

      const url = `http://localhost:5000/login`;

      // 在这里调用后端的登录API
      axios
        .post(url, loginCredentials)
        .then((response) => {
          // 处理登录成功
          alert(response.data.message); // 显示登录成功的消息
          this.$emit("login-success", this.username); // 发出登录成功的事件

          // this.$router.push("/admin"); // 导航到首页或其他页面
        })
        .catch((error) => {
          // 登录失败时，处理错误
          if (error.response && error.response.data) {
            // 显示后端返回的错误消息
            alert(error.response.data.error);
          } else {
            // 显示通用错误消息
            console.error("登录失败:", error);
            alert("登录失败，请稍后再试。");
          }
        });
    },
  },
};
</script>
<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding-top: 50px;
}

.form-item {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  margin-bottom: 15px;
}

.form-item label {
  width: 70px; /* 设置标签宽度，确保它们宽度一致 */
  text-align: center; /* 标签文字居中对齐 */
  margin-right: 10px; /* 与输入框之间的间隔 */
}

.form-item input {
  flex: 1; /* 输入框填充剩余空间 */
}

.login-button {
  width: calc(100% - 80px); /* 减去标签宽度和间隔宽度 */
  padding: 10px;
  background-color: #42b983;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
