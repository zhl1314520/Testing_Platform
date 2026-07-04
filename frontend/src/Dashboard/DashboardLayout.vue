<template>
  <div class="dashboard noise-texture gradient-mesh">
    <nav class="navbar glass-panel">
      <div class="nav-container">
        <div class="nav-brand" @click="router.push('/dashboard')">
          <div class="brand-logo">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="brand-info">
            <span class="brand-name">TMP</span>
            <span class="brand-slogan">Quality First</span>
          </div>
        </div>
        
        <div class="nav-menu">
          <router-link 
            v-for="item in navItems" 
            :key="item.path" 
            :to="item.path" 
            class="nav-item"
            :class="{ 'nav-item-active': isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span class="nav-label">{{ item.label }}</span>
            <span class="nav-indicator"></span>
          </router-link>
        </div>
        
        <div class="nav-actions">
          <div class="notification-bell">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E85D04" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 2L12 22M2 12L22 12M5 5L19 19M5 19L19 5M8 2L16 22M2 8L22 16M16 2L8 22M2 16L22 8" />
            </svg>
            <span class="notification-dot"></span>
          </div>
          
          <div class="user-menu-container" @click="toggleUserMenu">
            <div class="user-avatar">
              <span class="avatar-text">{{ userInfo?.username?.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="user-name">{{ userInfo?.username }}</span>
            <span class="user-role-badge">{{ userInfo?.role }}</span>
          </div>
          
          <Transition name="dropdown">
            <div v-if="showUserMenu" class="user-dropdown-menu glass-panel">
              <div class="dropdown-header">
                <div class="dropdown-avatar">{{ userInfo?.username?.charAt(0).toUpperCase() }}</div>
                <div class="dropdown-info">
                  <div class="dropdown-name">{{ userInfo?.username }}</div>
                  <div class="dropdown-role">{{ userInfo?.role }}</div>
                </div>
              </div>
              
              <div class="dropdown-section">
                <div class="dropdown-item" @click.stop="openProfileModal">
                  <svg class="dropdown-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <span>个人资料</span>
                  <svg class="dropdown-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"/>
                  </svg>
                </div>
              </div>
              
              <div class="dropdown-divider"></div>
              
              <div class="dropdown-item danger" @click="logout">
                <svg class="dropdown-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                <span>退出登录</span>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
    
    <Transition name="modal">
      <div v-if="showProfileModal" class="modal-overlay" @click="showProfileModal = false">
        <div class="modal-container glass-panel" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-ember">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <h2>个人资料</h2>
            </div>
            <button @click="showProfileModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <div class="modal-body">
            <div class="profile-section">
              <div class="section-title">基本信息</div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  用户 ID
                </label>
                <input 
                  v-model="profileForm.id" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  用户名
                </label>
                <input 
                  v-model="profileForm.username" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  密码
                </label>
                <input 
                  v-model="profileForm.password" 
                  type="password" 
                  disabled 
                  class="form-input disabled"
                  placeholder="••••••••"
                />
              </div>
              
              <div class="form-group">
                <button @click="openPasswordModal" class="btn-change-password">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
                  </svg>
                  修改密码
                </button>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                      <polyline points="22,6 12,13 2,6"/>
                    </svg>
                    邮箱
                  </label>
                  <input 
                    v-model="profileForm.email" 
                    type="email" 
                    class="form-input"
                    placeholder="example@email.com"
                  />
                </div>
                
                <div class="form-group">
                  <label class="form-label">
                    <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M12 8v8"/>
                      <path d="M8 12h8"/>
                    </svg>
                    角色
                  </label>
                  <select v-model="profileForm.role" class="form-select">
                    <option value="tester">测试工程师</option>
                    <option value="developer">开发工程师</option>
                  </select>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  创建时间
                </label>
                <input 
                  v-model="profileForm.created_at" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button @click="showProfileModal = false" class="btn-cancel">取消</button>
            <button @click="saveProfile" class="btn-submit">
              <span class="btn-spinner" v-if="loading"></span>
              <span v-else>保存修改</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
    
    <Transition name="modal">
      <div v-if="showPasswordModal" class="modal-overlay" @click="showPasswordModal = false">
        <div class="modal-container glass-panel" @click.stop>
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-icon-wrapper icon-wrapper-teal">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
                </svg>
              </div>
              <h2>修改密码</h2>
            </div>
            <button @click="showPasswordModal = false" class="btn-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <div class="modal-body">
            <div class="profile-section">
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                  当前邮箱
                </label>
                <input 
                  v-model="passwordForm.email" 
                  type="text" 
                  disabled 
                  class="form-input disabled"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  加密后的原密码
                </label>
                <input 
                  v-model="profileForm.password" 
                  type="password" 
                  disabled 
                  class="form-input disabled"
                  placeholder="••••••••"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  请输入原密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.oldPassword" 
                    :type="showOldPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请输入原密码"
                  />
                  <button
                    type="button"
                    @click="showOldPassword = !showOldPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showOldPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  请输入新密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.newPassword" 
                    :type="showNewPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请输入新密码"
                  />
                  <button
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showNewPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="label-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  请确认密码
                </label>
                <div class="password-wrapper">
                  <input 
                    v-model="passwordForm.confirmPassword" 
                    :type="showConfirmPassword ? 'text' : 'password'" 
                    class="form-input"
                    placeholder="请确认密码"
                  />
                  <button
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="password-toggle"
                  >
                    <svg v-if="showConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button @click="showPasswordModal = false" class="btn-cancel">取消</button>
            <button @click="changePassword" class="btn-submit btn-teal">
              <span class="btn-spinner" v-if="passwordLoading"></span>
              <span v-else>确认修改</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
    
    <Transition name="toast">
      <div v-if="toast.show" class="toast-overlay" @click="hideToast">
        <div class="toast-container glass-panel" @click.stop>
          <div class="toast-icon" :class="toast.type">
            <svg v-if="toast.type === 'success'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <svg v-else-if="toast.type === 'error'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <div class="toast-content">
            <h3 class="toast-title">{{ toast.title }}</h3>
            <p class="toast-message">{{ toast.message }}</p>
          </div>
          <button @click="hideToast" class="toast-close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authAPI, userAPI } from '../api/index.js'

const router = useRouter()
const route = useRoute()
const userInfo = ref(null)
const showUserMenu = ref(false)
const showProfileModal = ref(false)
const showPasswordModal = ref(false)
const loading = ref(false)
const passwordLoading = ref(false)

const profileForm = ref({
  id: '',
  username: '',
  password: '',
  role: '',
  email: '',
  created_at: ''
})

const passwordForm = ref({
  email: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const toast = ref({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

const showToast = (type, title, message) => {
  toast.value = { show: true, type, title, message }
  setTimeout(() => {
    hideToast()
  }, 3000)
}

const hideToast = () => {
  toast.value.show = false
}

const isActive = (path) => {
  if (path === '/dashboard') {
    return route.path === '/dashboard' || route.path === '/dashboard/'
  }
  return route.path === path
}

const navItems = [
  { path: '/dashboard', label: '概览', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>' },
  { path: '/dashboard/projects', label: '项目', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>' },
  { path: '/dashboard/testcases', label: '用例', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>' },
  { path: '/dashboard/executions', label: '执行', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>' },
  { path: '/dashboard/bugs', label: '缺陷', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>' },
  { path: '/dashboard/reports', label: '报告', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>' }
]

onMounted(() => {
  const storedUserInfo = localStorage.getItem('user_info')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }
  
  document.addEventListener('click', handleOutsideClick)
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const loadProfile = async () => {
  if (!userInfo.value?.id) return
  
  try {
    const response = await userAPI.getDetail(userInfo.value.id)
    profileForm.value = response.data
    if (profileForm.value.created_at) {
      const date = new Date(profileForm.value.created_at)
      profileForm.value.created_at = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }
  } catch (error) {
    console.error('加载个人资料失败:', error)
  }
}

const saveProfile = async () => {
  try {
    await userAPI.update(userInfo.value.id, {
      email: profileForm.value.email,
      role: profileForm.value.role
    })
    
    const updatedUserInfo = {
      ...userInfo.value,
      email: profileForm.value.email,
      role: profileForm.value.role
    }
    localStorage.setItem('user_info', JSON.stringify(updatedUserInfo))
    userInfo.value = updatedUserInfo
    
    showProfileModal.value = false
    showToast('success', '成功', '个人资料更新成功')
  } catch (error) {
    console.error('更新个人资料失败:', error)
    showToast('error', '错误', '更新失败：' + (error.response?.data?.detail || '未知错误'))
  }
}

const openProfileModal = async () => {
  await loadProfile()
  showProfileModal.value = true
}

const handleOutsideClick = (event) => {
  const userMenuContainer = document.querySelector('.user-menu-container')
  const modalOverlay = document.querySelector('.modal-overlay')
  
  if (showProfileModal.value || showPasswordModal.value) return
  
  if (userMenuContainer && !userMenuContainer.contains(event.target)) {
    showUserMenu.value = false
  }
}

const openPasswordModal = () => {
  passwordForm.value = {
    email: profileForm.value.email,
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
  showPasswordModal.value = true
}

const changePassword = async () => {
  if (!passwordForm.value.oldPassword) {
    showToast('warning', '提示', '请输入原密码')
    return
  }
  if (!passwordForm.value.newPassword) {
    showToast('warning', '提示', '请输入新密码')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    showToast('warning', '提示', '两次输入的密码不一致')
    return
  }
  if (passwordForm.value.newPassword.length < 6) {
    showToast('warning', '提示', '新密码长度不能少于6位')
    return
  }
  
  passwordLoading.value = true
  try {
    await userAPI.changePassword(userInfo.value.id, {
      old_password: passwordForm.value.oldPassword,
      new_password: passwordForm.value.newPassword
    })
    showToast('success', '成功', '密码修改成功')
    showPasswordModal.value = false
  } catch (error) {
    console.error('修改密码失败:', error)
    const detail = error.response?.data?.detail
    if (detail === 'OLD_PASSWORD_INCORRECT') {
      showToast('error', '错误', '原密码错误')
    } else {
      showToast('error', '错误', '修改失败：' + (detail || '未知错误'))
    }
  } finally {
    passwordLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user_info')
  sessionStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: var(--paper-cream);
  position: relative;
  overflow-x: hidden;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 1px solid rgba(232, 93, 4, 0.08);
  overflow: visible;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  overflow: visible;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  cursor: pointer;
  transition: all 0.4s var(--ease-smooth);
}

.nav-brand:hover {
  transform: translateX(-4px);
}

.brand-logo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.2);
  transition: transform 0.4s var(--ease-bounce), box-shadow 0.4s var(--ease-smooth);
}

.nav-brand:hover .brand-logo {
  transform: scale(1.08) rotate(-3deg);
  box-shadow: var(--shadow-lg), 0 0 30px rgba(232, 93, 4, 0.35);
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 1.35rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--ember-core), var(--ember-soft));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.brand-slogan {
  font-size: 0.7rem;
  color: var(--ink-soft);
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.nav-menu {
  display: flex;
  gap: var(--space-xs);
  align-items: center;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  color: var(--ink-muted);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.3s var(--ease-smooth);
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.06), rgba(250, 163, 7, 0.06));
  opacity: 0;
  transition: opacity 0.3s var(--ease-smooth);
  border-radius: var(--radius-md);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item:hover {
  color: var(--ember-core);
  transform: translateY(-2px);
}

.nav-item-active {
  color: var(--ember-core);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
}

.nav-item-active .nav-indicator {
  width: 100%;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s var(--ease-bounce);
}

.nav-item:hover .nav-icon {
  transform: scale(1.15) rotate(5deg);
}

.nav-label {
  position: relative;
  z-index: 1;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--ember-core), var(--ember-soft));
  transition: all 0.3s var(--ease-smooth);
  transform: translateX(-50%);
  border-radius: var(--radius-full);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  position: relative;
}

.notification-bell {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.04), rgba(250, 163, 7, 0.04));
  color: var(--ink-muted);
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
}

.notification-bell:hover {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.08));
  color: var(--ember-core);
  transform: scale(1.05);
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, var(--coral-primary), var(--coral-bright));
  border-radius: 50%;
  border: 2px solid white;
  transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s var(--ease-smooth);
}

.notification-bell:hover .notification-dot {
  transform: scale(1.3);
  box-shadow: 0 0 8px rgba(244, 63, 94, 0.6);
}

.user-menu-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 6px var(--space-md) 6px 6px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.user-menu-container:hover {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-bright));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 0 20px rgba(20, 184, 166, 0.25);
  transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s var(--ease-smooth);
}

.user-menu-container:hover .user-avatar {
  transform: scale(1.05);
  box-shadow: 0 0 25px rgba(20, 184, 166, 0.4);
}

.avatar-text {
}

.user-name {
  font-weight: 600;
  color: var(--ink-primary);
  font-size: 0.875rem;
}

.user-role-badge {
  font-size: 0.7rem;
  color: var(--teal-primary);
  background: linear-gradient(135deg, rgba(15, 118, 110, 0.08), rgba(94, 234, 212, 0.08));
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-weight: 600;
  text-transform: capitalize;
}

.user-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 280px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-sm);
  z-index: 1001;
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.04), rgba(250, 163, 7, 0.04));
  border-radius: var(--radius-md);
}

.dropdown-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-bright));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 0 15px rgba(20, 184, 166, 0.2);
}

.dropdown-info {
  flex: 1;
}

.dropdown-name {
  font-weight: 700;
  color: var(--ink-primary);
  font-size: 0.875rem;
  margin-bottom: 2px;
}

.dropdown-role {
  font-size: 0.75rem;
  color: var(--ink-soft);
  text-transform: capitalize;
}

.dropdown-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(232, 93, 4, 0.1), transparent);
  margin: var(--space-sm) 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: all 0.25s var(--ease-smooth);
  color: var(--ink-muted);
  border-radius: var(--radius-md);
}

.dropdown-item:hover {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.06), rgba(250, 163, 7, 0.06));
  color: var(--ember-core);
  padding-left: calc(var(--space-md) + 4px);
}

.dropdown-icon {
  flex-shrink: 0;
}

.dropdown-arrow {
  margin-left: auto;
  color: var(--slate-pale);
  transition: transform 0.3s var(--ease-smooth);
}

.dropdown-item:hover .dropdown-arrow {
  transform: translateX(4px);
  color: var(--ember-core);
}

.dropdown-item.danger {
  color: var(--coral-primary);
}

.dropdown-item.danger:hover {
  background: linear-gradient(135deg, rgba(190, 18, 60, 0.06), rgba(244, 63, 94, 0.06));
  color: var(--coral-deep);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 26, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: var(--space-xl);
}

.modal-container {
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  animation: scale-bounce 0.4s var(--ease-bounce);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.modal-header {
  padding: var(--space-xl);
  border-bottom: 1px solid rgba(232, 93, 4, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: inherit;
  z-index: 1;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.modal-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
}

.modal-title h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--ink-primary);
  font-weight: 700;
}

.btn-close {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: none;
  background: rgba(232, 93, 4, 0.04);
  color: var(--ink-soft);
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: rgba(232, 93, 4, 0.08);
  color: var(--ember-core);
  transform: rotate(90deg);
}

.modal-body {
  padding: var(--space-xl);
}

.profile-section {
  margin-bottom: var(--space-xl);
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--ink-primary);
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-sm);
  border-bottom: 2px solid rgba(232, 93, 4, 0.15);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.form-group {
  margin-bottom: var(--space-lg);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
  font-weight: 500;
  color: var(--ink-secondary);
  font-size: 0.875rem;
}

.label-icon {
  color: var(--ember-core);
}

.form-input,
.form-select {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  border: 2px solid rgba(232, 93, 4, 0.1);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s var(--ease-smooth);
  background: white;
  color: var(--ink-primary);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--ember-core);
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.1);
}

.form-input.disabled {
  background: var(--paper-muted);
  color: var(--ink-soft);
  cursor: not-allowed;
  border-color: transparent;
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 48px;
}

.password-toggle {
  position: absolute;
  right: var(--space-sm);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--ink-soft);
  cursor: pointer;
  padding: var(--space-xs);
  display: flex;
  align-items: center;
  transition: color 0.2s var(--ease-smooth);
}

.password-toggle:hover {
  color: var(--ember-core);
}

.btn-change-password {
  width: 100%;
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  border: 2px solid var(--ember-core);
  background: transparent;
  color: var(--ember-core);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
}

.btn-change-password:hover {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md), 0 0 20px rgba(232, 93, 4, 0.2);
}

.modal-footer {
  padding: var(--space-xl);
  border-top: 1px solid rgba(232, 93, 4, 0.08);
  display: flex;
  gap: var(--space-md);
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: inherit;
}

.btn-cancel,
.btn-submit {
  padding: var(--space-sm) var(--space-xl);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease-smooth);
  border: none;
}

.btn-cancel {
  background: rgba(232, 93, 4, 0.04);
  color: var(--ink-muted);
}

.btn-cancel:hover {
  background: rgba(232, 93, 4, 0.08);
  color: var(--ink-primary);
}

.btn-submit {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  box-shadow: var(--shadow-md), 0 0 15px rgba(232, 93, 4, 0.15);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg), 0 0 25px rgba(232, 93, 4, 0.25);
}

.btn-submit.btn-teal {
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-bright));
  box-shadow: var(--shadow-md), 0 0 15px rgba(20, 184, 166, 0.15);
}

.btn-submit.btn-teal:hover {
  box-shadow: var(--shadow-lg), 0 0 25px rgba(20, 184, 166, 0.25);
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.main-content {
  padding: var(--space-xl) 0;
  padding-top: calc(72px + var(--space-xl));
  min-height: calc(100vh - 72px);
  position: relative;
  z-index: 1;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
}

.toast-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 26, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.toast-container {
  border-radius: var(--radius-lg);
  padding: var(--space-lg) var(--space-xl);
  box-shadow: var(--shadow-xl);
  display: flex;
  align-items: center;
  gap: var(--space-md);
  max-width: 400px;
  animation: scale-bounce 0.3s var(--ease-bounce);
  border: 1px solid rgba(232, 93, 4, 0.08);
}

.toast-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.toast-icon.success {
  background: linear-gradient(135deg, var(--forest-primary), var(--forest-bright));
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

.toast-icon.error {
  background: linear-gradient(135deg, var(--coral-deep), var(--coral-bright));
  box-shadow: 0 0 20px rgba(244, 63, 94, 0.3);
}

.toast-icon.warning {
  background: linear-gradient(135deg, var(--amber-primary), var(--amber-soft));
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}

.toast-content {
  flex: 1;
}

.toast-title {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.toast-message {
  margin: 0;
  font-size: 0.875rem;
  color: var(--ink-soft);
}

.toast-close {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--ink-soft);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s var(--ease-smooth);
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(232, 93, 4, 0.06);
  color: var(--ember-core);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s var(--ease-smooth);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.dropdown-enter-active {
  animation: dropdown-in 0.3s var(--ease-bounce);
}

.dropdown-leave-active {
  animation: dropdown-out 0.2s var(--ease-smooth);
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes dropdown-out {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
}

.toast-enter-active {
  animation: scale-bounce 0.3s var(--ease-bounce);
}

.toast-leave-active {
  animation: fade-out 0.2s var(--ease-smooth);
}

@keyframes fade-out {
  to {
    opacity: 0;
    transform: scale(0.9);
  }
}

@media (max-width: 1024px) {
  .nav-container {
    padding: 0 var(--space-md);
  }
  
  .nav-label {
    display: none;
  }
  
  .content-wrapper {
    padding: 0 var(--space-md);
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .brand-name {
    font-size: 1.15rem;
  }
  
  .brand-slogan {
    display: none;
  }
  
  .user-name {
    display: none;
  }
  
  .user-role-badge {
    display: none;
  }
  
  .main-content {
    padding: var(--space-md) 0;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
