# GitHub Pages 部署指南（最简单方法）

由于命令行推送需要配置 SSH 或 token，这里提供两种更简单的方法：

---

## 方法 1：网页直接上传（最简单，5 分钟完成）

### 步骤：

1. **访问你的仓库：**
   https://github.com/nauyisu022/temp-web

2. **上传文件：**
   - 点击 "Add file" > "Upload files"
   - 把 `docs` 文件夹里的所有文件拖进去：
     - `ksp_eval_dashboard.html` ⭐（最重要）
     - `README.md`
     - 其他 `.md` 文件（可选）
   - 点击 "Commit changes"

3. **启用 GitHub Pages：**
   - 进入仓库的 Settings > Pages
   - Source 选择 `main` 分支
   - 点击 Save

4. **访问网站：**
   等待 1-2 分钟后访问：
   ```
   https://nauyisu022.github.io/temp-web/ksp_eval_dashboard.html
   ```

---

## 方法 2：完成 GitHub CLI 授权后推送

如果你想用命令行，请完成以下步骤：

### 1. 完成 GitHub 授权

- 访问：https://github.com/login/device
- 输入代码：`5C9C-1BBA`
- 点击授权

### 2. 授权完成后，运行：

```bash
cd /Users/wusiyuan/Documents/test/sft/sft_datagen_re/docs

# 检查授权状态
gh auth status

# 使用 gh 推送
gh repo view nauyisu022/temp-web --web

# 或者直接用 gh 命令推送
git remote remove origin
git remote add origin https://github.com/nauyisu022/temp-web.git
gh auth setup-git
git push -u origin main
```

### 3. 启用 GitHub Pages

- 进入 https://github.com/nauyisu022/temp-web/settings/pages
- Source 选择 `main` 分支
- 点击 Save

### 4. 访问网站

```
https://nauyisu022.github.io/temp-web/ksp_eval_dashboard.html
```

---

## 方法 3：使用 Personal Access Token

### 1. 创建 Token

- 访问：https://github.com/settings/tokens
- 点击 "Generate new token (classic)"
- 勾选 `repo` 权限
- 生成并复制 token

### 2. 推送代码

```bash
cd /Users/wusiyuan/Documents/test/sft/sft_datagen_re/docs

git remote remove origin
git remote add origin https://YOUR_TOKEN@github.com/nauyisu022/temp-web.git
git push -u origin main
```

把 `YOUR_TOKEN` 替换成你的 token。

---

## 推荐：方法 1（网页上传）

最简单、最快速，不需要配置任何东西！

上传完成后记得在 Settings > Pages 启用 GitHub Pages。

---

## 最终访问地址

```
https://nauyisu022.github.io/temp-web/ksp_eval_dashboard.html
```

这个地址可以公开分享给任何人！
