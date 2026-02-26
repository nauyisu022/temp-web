# Vercel 部署指南

## 🚀 快速部署（推荐）

### 方法 1：使用自动化脚本（最简单）

在项目根目录运行：

```bash
bash deploy_to_vercel.sh
```

脚本会自动：
1. 检查并安装 Node.js（如果需要）
2. 安装 Vercel CLI
3. 部署你的 dashboard

**首次使用会提示登录：**
- 选择登录方式（GitHub/GitLab/Bitbucket/Email）
- 在浏览器中完成授权
- 返回终端继续部署

---

### 方法 2：手动部署（分步骤）

#### 步骤 1：安装 Node.js

```bash
# 使用 Homebrew 安装
brew install node

# 验证安装
node --version
npm --version
```

#### 步骤 2：安装 Vercel CLI

```bash
npm install -g vercel
```

#### 步骤 3：登录 Vercel

```bash
vercel login
```

选择你喜欢的登录方式（推荐使用 GitHub）。

#### 步骤 4：部署

```bash
cd docs
vercel --prod
```

按提示操作：
1. **Set up and deploy?** → 选择 `Y`
2. **Which scope?** → 选择你的账号
3. **Link to existing project?** → 选择 `N`（首次部署）
4. **What's your project's name?** → 输入项目名（如：`ksp-eval-dashboard`）
5. **In which directory is your code located?** → 直接按回车（当前目录）

部署完成后会显示访问链接！

---

## 🌐 访问你的 Dashboard

部署成功后，Vercel 会提供一个链接，格式如下：

```
https://ksp-eval-dashboard.vercel.app/ksp_eval_dashboard.html
```

或者使用 Vercel 自动生成的域名：

```
https://ksp-eval-dashboard-xxxxx.vercel.app/ksp_eval_dashboard.html
```

---

## 📝 部署过程示例

```bash
$ cd docs
$ vercel --prod

Vercel CLI 33.0.0
? Set up and deploy "~/Documents/test/sft/sft_datagen_re/docs"? [Y/n] y
? Which scope do you want to deploy to? Your Name
? Link to existing project? [y/N] n
? What's your project's name? ksp-eval-dashboard
? In which directory is your code located? ./
Auto-detected Project Settings (Static):
- Build Command: N/A
- Development Command: None
- Install Command: N/A
- Output Directory: .
? Want to modify these settings? [y/N] n
🔗  Linked to your-name/ksp-eval-dashboard (created .vercel)
🔍  Inspect: https://vercel.com/your-name/ksp-eval-dashboard/xxxxx [1s]
✅  Production: https://ksp-eval-dashboard.vercel.app [2s]
```

---

## 🔄 更新 Dashboard

当你修改了 HTML 文件，想要更新线上版本：

```bash
cd docs
vercel --prod
```

Vercel 会自动部署新版本，通常 10-30 秒完成。

---

## ⚙️ 高级配置

### 自定义域名

1. 访问 https://vercel.com/dashboard
2. 进入你的项目
3. 点击 "Settings" > "Domains"
4. 添加你的域名
5. 按提示配置 DNS 记录

### 环境变量（如果需要）

在 `vercel.json` 中添加：

```json
{
  "env": {
    "MY_VARIABLE": "value"
  }
}
```

### 重定向规则

在 `vercel.json` 中配置：

```json
{
  "redirects": [
    {
      "source": "/",
      "destination": "/ksp_eval_dashboard.html"
    }
  ]
}
```

这样访问根路径会自动跳转到 dashboard。

---

## 🎯 Vercel 配置文件说明

项目中的 `vercel.json` 文件配置了部署参数：

```json
{
  "version": 2,
  "name": "ksp-eval-dashboard",
  "builds": [
    {
      "src": "**/*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

**说明：**
- `version: 2` - 使用 Vercel 平台 v2
- `name` - 项目名称
- `builds` - 指定如何构建静态文件
- `routes` - 路由规则

---

## 📊 Vercel 优势

✅ **全球 CDN** - 自动分发到全球边缘节点，访问速度快
✅ **自动 HTTPS** - 免费 SSL 证书
✅ **零配置** - 智能检测项目类型
✅ **实时预览** - 每次部署都有独立预览链接
✅ **分析功能** - 查看访问统计（需要升级）
✅ **自动优化** - 图片、字体等资源自动优化

---

## 🔧 常见问题

### Q: 部署后显示 404

**解决方法：**
1. 确保在 `docs` 目录下运行 `vercel` 命令
2. 检查文件名是否正确：`ksp_eval_dashboard.html`
3. 访问完整路径：`https://your-project.vercel.app/ksp_eval_dashboard.html`

### Q: 需要登录但无法打开浏览器

**解决方法：**
```bash
vercel login --email your-email@example.com
```
会发送验证邮件到你的邮箱。

### Q: 如何删除项目

**解决方法：**
1. 访问 https://vercel.com/dashboard
2. 找到项目，点击 "Settings"
3. 滚动到底部，点击 "Delete Project"

### Q: 部署失败

**解决方法：**
1. 检查网络连接
2. 确保已登录：`vercel whoami`
3. 清除缓存：`rm -rf .vercel` 然后重新部署
4. 查看详细日志：`vercel --debug`

### Q: 如何设置访问密码

Vercel 免费版不支持密码保护。可以：
1. 升级到 Pro 版（$20/月）使用 Password Protection
2. 在 HTML 中添加简单的 JavaScript 密码验证（不安全，仅防止普通用户）

---

## 💰 费用说明

**免费版（Hobby）：**
- ✅ 无限部署
- ✅ 100GB 带宽/月
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ⚠️ 不支持密码保护

**Pro 版（$20/月）：**
- ✅ 1TB 带宽/月
- ✅ 密码保护
- ✅ 分析功能
- ✅ 优先支持

对于展示 dashboard，免费版完全够用！

---

## 📱 移动端访问

Vercel 部署的网站自动支持移动端访问，确保你的 HTML 是响应式设计即可。

---

## 🔗 有用的链接

- Vercel 控制台：https://vercel.com/dashboard
- Vercel 文档：https://vercel.com/docs
- Vercel CLI 文档：https://vercel.com/docs/cli
- 状态页面：https://vercel-status.com/

---

## 📞 获取帮助

如果遇到问题：
1. 查看 Vercel 文档：https://vercel.com/docs
2. 查看部署日志：`vercel logs`
3. 在终端运行：`vercel --debug` 查看详细信息
4. 访问 Vercel 社区：https://github.com/vercel/vercel/discussions

---

## 🎉 部署成功后

分享你的 dashboard 链接给同事：

```
https://your-project.vercel.app/ksp_eval_dashboard.html
```

他们可以直接在浏览器中访问，无需任何配置！
