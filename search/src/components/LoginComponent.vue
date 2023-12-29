<template>
  <div class="login-container">
    <form @submit.prevent="onLogin">
      <div class="form-item">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-item">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="login-button">登录</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginComponent',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    onLogin() {
      // 发送请求到后端进行验证
      const loginCredentials = {
        username: this.username,
        password: this.password
      };
      // 在这里调用后端的登录API
      // axios.post('/api/login', loginCredentials)
      //   .then(response => {
      //     const token = response.data.token;
      //     localStorage.setItem('user-token', token); // 存储token
      //     this.$router.push('/'); // 导航到首页或其他页面
      //   })
      //   .catch(error => {
      //     console.error('登录失败:', error);
      //   });
      console.log('登录凭证:', loginCredentials);
      alert('请连接后端API进行登录');
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding-top: 50px;
}

.form-item {
  margin-bottom: 15px;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
