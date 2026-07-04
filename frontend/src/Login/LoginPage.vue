<template>
  <div class="login-page noise-texture">
    <div class="left-section">
      <div class="logo-section">
        <a href="/" class="logo-link">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span>TMP</span>
        </a>
      </div>

      <div class="characters-section">
        <AnimatedCharacters
          :isTyping="isTyping"
          :showPassword="showPassword"
          :passwordLength="password.length"
          :loginFailed="loginFailed"
          :loginSuccess="loginSuccess"
        />
      </div>

      <div class="footer-links">
        <a href="/privacy-policy" class="footer-link">隐私政策</a>
        <a href="/terms" class="footer-link">服务条款</a>
      </div>

      <div class="deco-grid"></div>
      <div class="deco-blob deco-blob-1"></div>
      <div class="deco-blob deco-blob-2"></div>
      <div class="deco-blob deco-blob-3"></div>
    </div>

    <div class="right-section">
      <div class="form-wrapper">
        <div class="mobile-logo">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span>HBNU-TMP</span>
        </div>

        <div class="form-header">
          <div class="header-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
            Secure Access
          </div>
          <h1 class="form-title">欢迎回来</h1>
          <p class="form-subtitle">请输入您的账户信息以继续</p>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="email" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              邮箱地址
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="you@example.com"
              class="form-input"
              autocomplete="off"
              required
              @focus="isTyping = true"
              @blur="isTyping = false"
            />
            <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">
              <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              密码
            </label>
            <div class="password-wrapper">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="form-input"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                <svg v-if="showPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                  <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                  <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                  <line x1="2" x2="22" y1="2" y2="22"/>
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" class="checkbox" />
              <span class="checkbox-custom"></span>
              <span>记住我 30 天</span>
            </label>
            <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
          </div>

          <div v-if="errorMessage" class="error-alert">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            class="submit-button"
            :disabled="isLoading"
          >
            <span class="button-text">{{ isLoading ? '登录中...' : '登录' }}</span>
            <svg class="button-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/>
              <path d="m12 5 7 7-7 7"/>
            </svg>
          </button>
        </form>

        <div class="social-login">
          <button
            type="button"
            @click="handleGitHubSignIn"
            class="github-button"
          >
            <svg class="github-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span>使用 GitHub 登录</span>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AnimatedCharacters from './AnimatedCharacters.vue'
import { authAPI } from '../api/index.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isTyping = ref(false)
const isLoading = ref(false)
const loginFailed = ref(false)
const loginSuccess = ref(false)
const errorMessage = ref('')
const errors = ref({
  email: '',
  password: ''
})

const validateForm = () => {
  errors.value = { email: '', password: '' }
  let isValid = true

  if (!email.value) {
    errors.value.email = '请输入邮箱地址'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = '请输入有效的邮箱地址'
    isValid = false
  }

  if (!password.value) {
    errors.value.password = '请输入密码'
    isValid = false
  } else if (password.value.length < 6) {
    errors.value.password = '密码长度至少为 6 位'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  loginFailed.value = false
  loginSuccess.value = false

  try {
    const response = await authAPI.login(email.value, password.value)
    
    if (rememberMe.value) {
      localStorage.setItem('token', response.data.token)
    } else {
      sessionStorage.setItem('token', response.data.token)
    }
    
    localStorage.setItem('user_info', JSON.stringify(response.data.user_info))
    
    loginSuccess.value = true
    
    setTimeout(() => {
      router.push('/dashboard')
    }, 500)
    
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '邮箱或密码错误，请重试。'
    loginFailed.value = true
    setTimeout(() => {
      loginFailed.value = false
    }, 3000)
  } finally {
    isLoading.value = false
  }
}

const handleGitHubSignIn = async () => {
  try {
    console.log('GitHub Sign In')
    alert('GitHub 登录功能待实现')
  } catch (error) {
    errorMessage.value = 'GitHub 登录失败，请重试。'
  }
}
</script>

<style scoped>
.login-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}

.left-section {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: var(--space-2xl);
  color: white;
  background: 
    radial-gradient(ellipse at 20% 30%, rgba(232, 93, 4, 0.15), transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(20, 184, 166, 0.12), transparent 45%),
    radial-gradient(ellipse at 50% 50%, rgba(244, 63, 94, 0.08), transparent 40%),
    linear-gradient(145deg, var(--ink-primary) 0%, var(--ink-deep) 50%, #0a0f1a 100%);
  overflow: hidden;
}

.logo-section {
  position: relative;
  z-index: 20;
  display: inline-block;
  width: auto;
}

.logo-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 1.125rem;
  font-weight: 700;
  text-decoration: none;
  color: inherit;
  padding: var(--space-sm);
  margin: calc(var(--space-sm) * -1);
  border-radius: var(--radius-md);
  transition: all 0.3s var(--ease-smooth);
}

.logo-link:hover {
  background: rgba(255, 255, 255, 0.08);
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.3);
}

.characters-section {
  position: relative;
  z-index: 20;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  height: 500px;
}

.footer-links {
  position: relative;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: var(--space-xl);
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.footer-link {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s var(--ease-smooth);
}

.footer-link:hover {
  color: var(--ember-soft);
}

.deco-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

.deco-blob {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  transition: transform 0.8s var(--ease-smooth);
}

.deco-blob-1 {
  top: 10%;
  right: 15%;
  width: 250px;
  height: 250px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(232, 93, 4, 0.22) 0%, rgba(232, 93, 4, 0.14) 30%, rgba(232, 93, 4, 0.06) 50%, transparent 70%);
}

.deco-blob-2 {
  bottom: 20%;
  left: 10%;
  width: 200px;
  height: 200px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.18) 0%, rgba(20, 184, 166, 0.1) 30%, rgba(20, 184, 166, 0.04) 50%, transparent 70%);
}

.deco-blob-3 {
  top: 50%;
  right: 30%;
  width: 150px;
  height: 150px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.14) 0%, rgba(244, 63, 94, 0.08) 30%, rgba(244, 63, 94, 0.03) 50%, transparent 70%);
}

.left-section:hover .deco-blob-1 {
  transform: translate(12px, -12px);
}

.left-section:hover .deco-blob-2 {
  transform: translate(-8px, 8px);
}

.left-section:hover .deco-blob-3 {
  transform: translate(6px, -6px);
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  background: var(--paper-cream);
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.mobile-logo {
  display: none;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: var(--space-2xl);
  color: var(--ink-primary);
}

.form-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 1.75rem;
  padding: 4px 14px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  color: var(--ember-core);
  margin-bottom: var(--space-md);
}

.form-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin: 0 0 var(--space-sm) 0;
  color: var(--ink-primary);
}

.form-subtitle {
  font-size: 0.95rem;
  color: var(--ink-soft);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ink-secondary);
}

.label-icon {
  color: var(--ember-core);
}

.form-input {
  width: 100%;
  height: 3.25rem;
  padding: 0 var(--space-md);
  background: white;
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s var(--ease-smooth);
  outline: none;
  color: var(--ink-primary);
}

.form-input:focus {
  border-color: var(--ember-core);
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.1);
}

.form-input::placeholder {
  color: var(--slate-pale);
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: var(--space-md);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--ink-soft);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.3s var(--ease-smooth);
}

.password-toggle:hover {
  color: var(--ember-core);
}

.error-message {
  font-size: 0.85rem;
  color: var(--coral-primary);
  margin: 0;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.875rem;
  cursor: pointer;
  color: var(--ink-secondary);
}

.checkbox {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(232, 93, 4, 0.2);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s var(--ease-smooth);
}

.checkbox:checked + .checkbox-custom {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  border-color: transparent;
}

.checkbox:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-link {
  font-size: 0.875rem;
  color: var(--ember-core);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s var(--ease-smooth);
}

.forgot-link:hover {
  color: var(--ember-glow);
}

.error-alert {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md);
  font-size: 0.9rem;
  color: var(--coral-deep);
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.08), rgba(253, 164, 175, 0.06));
  border: 1px solid rgba(244, 63, 94, 0.2);
  border-radius: var(--radius-md);
}

.submit-button,
.github-button {
  position: relative;
  width: 100%;
  height: 3.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: 1rem;
  font-weight: 700;
  border-radius: var(--radius-md);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s var(--ease-smooth);
}

.submit-button {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  border: none;
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.2);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 0 30px rgba(232, 93, 4, 0.3);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.button-text {
  transition: transform 0.3s var(--ease-smooth);
}

.button-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s var(--ease-smooth);
}

.submit-button:hover:not(:disabled) .button-text {
  transform: translateX(-8px);
}

.submit-button:hover:not(:disabled) .button-icon {
  transform: translateX(8px);
}

.social-login {
  margin-top: var(--space-md);
}

.divider {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(232, 93, 4, 0.15), transparent);
}

.divider span {
  font-size: 0.8rem;
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.github-button {
  background: white;
  color: var(--ink-secondary);
  border: 2px solid rgba(232, 93, 4, 0.1);
}

.github-button:hover {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.04), rgba(250, 163, 7, 0.02));
  border-color: rgba(232, 93, 4, 0.2);
  transform: translateY(-2px);
}

.github-icon {
  width: 20px;
  height: 20px;
}

@media (max-width: 1024px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .left-section {
    display: none;
  }

  .mobile-logo {
    display: flex;
  }

  .right-section {
    padding: var(--space-xl);
  }
}

@media (max-width: 480px) {
  .right-section {
    padding: var(--space-lg);
  }

  .form-title {
    font-size: 1.75rem;
  }

  .form-options {
    flex-direction: column;
    gap: var(--space-md);
    align-items: flex-start;
  }
}
</style>
