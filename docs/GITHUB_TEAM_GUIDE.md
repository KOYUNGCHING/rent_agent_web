# GitHub 新手協作教學：居析 Jiaxi

這份說明寫給第一次使用 GitHub 的組員。Git 是電腦上的「版本紀錄工具」，GitHub 是大家共享程式碼的網站。

## 組長第一次把專案放上 GitHub

### 1. 在 GitHub 建 repository

1. 登入 [GitHub](https://github.com/)。
2. 右上角 `+` 選 `New repository`。
3. Repository name 可填 `housing-area-insight-agent`。
4. 專題若可公開展示選 `Public`；若 API key 或未公開內容較多則選 `Private`。
5. 不要勾選新增 README、`.gitignore` 或 License，因為本機專案已經有檔案。
6. 按 `Create repository`，複製畫面上的 HTTPS URL，例如：

```text
https://github.com/你的帳號/housing-area-insight-agent.git
```

### 2. 將本機第一次上傳

在專案資料夾的 Terminal 執行，將 URL 換成自己的：

```bash
git remote add origin https://github.com/你的帳號/housing-area-insight-agent.git
git branch -M main
git push -u origin main
```

GitHub 若要求登入，依畫面以瀏覽器登入或使用 Personal Access Token。密碼欄不能直接填 GitHub 密碼。

### 3. 邀請隊友

Repository 頁面進入 `Settings` > `Collaborators` > `Add people`，輸入隊友的 GitHub 使用者名稱。隊友要接受邀請後才可上傳。

## 隊友第一次開始工作

### 1. 安裝工具與設定姓名

安裝 [Git](https://git-scm.com/downloads) 與 [Visual Studio Code](https://code.visualstudio.com/) 後，開啟 Terminal 執行：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的 GitHub Email"
```

### 2. 下載專案

從 GitHub repository 的綠色 `Code` 按鈕複製 HTTPS URL，執行：

```bash
git clone https://github.com/組長帳號/housing-area-insight-agent.git
cd housing-area-insight-agent
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Windows PowerShell 啟動虛擬環境請改用：

```powershell
.\.venv\Scripts\Activate.ps1
```

在瀏覽器打開 `http://127.0.0.1:5000`，看到首頁就代表環境完成。

## 每次開始寫程式的固定流程

不要多人一起直接改 `main`。每個功能開一個 branch，做完透過 Pull Request 合併。

例如負責串接天氣 API：

```bash
git switch main
git pull origin main
git switch -c feature/weather-api
```

完成一小段可說明的修改後：

```bash
git status
git add app.py requirements.txt
git commit -m "Add weather API integration"
git push -u origin feature/weather-api
```

在 GitHub 頁面按 `Compare & pull request`，寫清楚你改了什麼、怎麼測試，再請一位組員確認後按 `Merge`。

下一項功能請回到最新 `main` 再開新 branch：

```bash
git switch main
git pull origin main
git switch -c feature/air-quality-api
```

## 建議分工方式

| Branch 名稱 | 負責項目 | 可能修改內容 |
| --- | --- | --- |
| `feature/geocode` | 地名轉座標 | Nominatim 呼叫、座標資料格式 |
| `feature/weather-api` | 天氣 | 中央氣象署 API |
| `feature/transport-api` | 大眾運輸 | TDX API |
| `feature/air-quality-api` | 空氣品質 | 環境部 API |
| `feature/rental-data` | 租金資料 | 租賃實價資料整理 |
| `feature/line-bot` | LINE Bot | webhook 與訊息格式 |
| `feature/llm-summary` | AI 摘要 | Gemini / ADK tool calling |

## 絕對不要上傳的東西

API key、LINE channel secret、token 與密碼不能放在程式或 GitHub 中。請放在本機 `.env`，例如：

```dotenv
CWA_API_KEY=填入自己的金鑰
TDX_CLIENT_ID=填入自己的資料
TDX_CLIENT_SECRET=填入自己的資料
LINE_CHANNEL_SECRET=填入自己的資料
LINE_CHANNEL_ACCESS_TOKEN=填入自己的資料
GEMINI_API_KEY=填入自己的資料
```

`.env` 已被 `.gitignore` 忽略，不會被上傳。未來若要告訴隊友需要哪些欄位，請建立只放空白範例值的 `.env.example`。

## 三句口訣

1. 開始工作前：`git pull`，拿到大家最新進度。
2. 寫新功能時：開 `feature/...` branch，不直接在 `main` 寫。
3. 上傳前：`git status`，確認沒有 API key 或不該上傳的檔案。

## 常見狀況

### 我改壞了但還沒有 commit

先向組員詢問再處理；不要亂刪資料夾。VS Code 的 Source Control 可看到改過哪些行。

### `git push` 被拒絕

通常是沒有接受 repository 邀請，或遠端已有新版本。先截圖錯誤訊息給負責 Git 的組員，不要勉強使用強制推送。

### 我和隊友改到同一段，出現 conflict

保留畫面上的 conflict 內容，和改同一功能的隊友一起決定正確版本，再 commit。第一次遇到衝突不要自行猜測刪除。
