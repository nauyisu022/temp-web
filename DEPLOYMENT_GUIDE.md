# HTML 部署指南

本文档介绍如何将 `ksp_eval_dashboard.html` 托管到网上供他人访问。

## 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **GitHub Pages** | 免费、稳定、支持自定义域名 | 需要 GitHub 账号 | 推荐用于长期托管 |
| **Netlify Drop** | 最简单、拖拽即可 | 免费版有限制 | 快速分享 |
| **Vercel** | 速度快、自动 HTTPS | 需要账号 | 专业项目 |
| **临时分享** | 无需注册 | 链接有效期短 | 临时演示 |

---

## 方案 1：GitHub Pages（推荐）

### 步骤：

1. **创建 GitHub 仓库**
   - 访问 https://github.com/new
   - 仓库名称：`ksp-eval-dashboard`（或任意名称）
   - 选择 **Public**（公开）
   - 点击 "Create repository"

2. **部署文件**
   ```bash
   # 在项目根目录执行
   bash deploy_to_github_pages.sh
   ```
   
   或手动部署：
   ```bash
   cd docs
   git init
   git add .
   git commit -m "Deploy dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ksp-eval-dashboard.git
   git push -u origin main
   ```

3. **启用 GitHub Pages**
   - 进入仓库的 Settings > Pages
   - Source 选择 `main` 分支
   - 点击 Save

4. **访问网站**
   - 等待 1-2 分钟
   - 访问：`https://YOUR_USERNAME.github.io/ksp-eval-dashboard/ksp_eval_dashboard.html`

### 优点：
- ✅ 完全免费
- ✅ 稳定可靠
- ✅ 支持自定义域名
- ✅ 自动 HTTPS

---

## 方案 2：Netlify Drop（最快速）

### 步骤：

1. 访问 https://app.netlify.com/drop
2. 将 `docs` 文件夹直接拖拽到页面上
3. 立即获得一个可访问的链接（如：`https://random-name-123.netlify.app/ksp_eval_dashboard.html`）

### 优点：
- ✅ 无需注册（但注册后可以管理）
- ✅ 30 秒完成部署
- ✅ 自动 HTTPS

---

## 方案 3：Vercel

### 步骤：

1. 安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```

2. 部署：
   ```bash
   cd docs
   vercel --prod
   ```

3. 按提示登录并确认

### 优点：
- ✅ 全球 CDN 加速
- ✅ 部署速度快
- ✅ 自动 HTTPS

---

## 方案 4：临时分享（用于快速演示）

### transfer.sh（命令行）

```bash
cd docs
tar -czf dashboard.tar.gz ksp_eval_dashboard.html
curl --upload-file dashboard.tar.gz https://transfer.sh/dashboard.tar.gz
```

会返回一个下载链接，有效期 14 天。

### 其他临时托管服务：

- **file.io**: https://www.file.io/
- **tmpfiles.org**: https://tmpfiles.org/

---

## 推荐流程

**如果你想快速分享给别人看（5 分钟内）：**
→ 使用 Netlify Drop（方案 2）

**如果你想长期托管、专业展示：**
→ 使用 GitHub Pages（方案 1）

---

## 注意事项

1. **文件大小**：确保 HTML 文件不要太大（建议 < 10MB）
2. **隐私**：这些方案都是公开访问的，不要包含敏感信息
3. **更新**：如果需要更新内容，重新部署即可覆盖

---

## 自定义域名（可选）

如果你有自己的域名，可以在 GitHub Pages 或 Netlify 中配置：

### GitHub Pages:
1. 在仓库根目录创建 `CNAME` 文件
2. 内容填写你的域名（如：`dashboard.yourdomain.com`）
3. 在域名 DNS 设置中添加 CNAME 记录指向 `YOUR_USERNAME.github.io`

### Netlify:
1. 在 Netlify 控制台进入 Domain settings
2. 添加自定义域名
3. 按提示配置 DNS

---

## 故障排除

### GitHub Pages 404 错误
- 确保仓库是 Public
- 检查 Settings > Pages 是否正确配置
- 等待 5-10 分钟让 GitHub 构建完成

### 样式或脚本不加载
- 检查 HTML 中的资源路径是否使用相对路径
- 确保所有依赖文件都已上传

### 需要密码保护
- GitHub Pages 不支持密码保护（除非使用 GitHub Pro）
- 可以使用 Netlify 的密码保护功能（付费）
- 或者使用 Vercel 的 Password Protection

---

## 联系与支持

如有问题，可以查看：
- GitHub Pages 文档：https://docs.github.com/pages
- Netlify 文档：https://docs.netlify.com/
- Vercel 文档：https://vercel.com/docs
