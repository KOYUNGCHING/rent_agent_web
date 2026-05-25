# 居析 Jiaxi - 租屋地區資訊 Agent

輸入想租屋的區域，整合天氣、租金、交通、生活機能與空氣品質等公開資料，最後由 AI 產生容易閱讀的生活資訊摘要，未來可透過 LINE Bot 回覆使用者。

目前 repository 是 Flask 網站原型：首頁提供區域搜尋、生活情報卡，以及可展開的 AI 租屋顧問聊天視窗。`app.py` 中的台北車站、公館、中山與板橋資料是展示資料，尚未即時呼叫政府開放資料或 LLM。

## 專題目標

使用者輸入：

> 我今天想在台北車站附近租房子

預期系統流程：

```text
使用者訊息 / LINE Bot
        |
User Input Agent 解析地點與需求
        |
Location / Geocode Agent 取得座標
        |
Weather / Rental / Transport / Facility / Air Quality Tools
        |
Summary Agent (LLM) 生成生活資訊摘要
        |
回覆使用者
```

## 規劃資料來源

| 模組 | 用途 | 候選公開資料或 API |
| --- | --- | --- |
| Location / Geocode | 地名轉座標 | OpenStreetMap Nominatim |
| Weather | 溫度、降雨、天氣狀態 | 中央氣象署開放資料 |
| Rental Data | 租金範圍、行情參考 | 實價登錄租賃資料 |
| Transport | 捷運、公車、鐵路、YouBike | TDX 運輸資料 |
| Facility | 醫院、公園、超商、商圈 | OpenStreetMap / 政府開放資料 |
| Air Quality | AQI 與污染指標 | 環境部空氣品質資料 |
| Summary / LINE Bot | 統整文字與聊天介面 | Gemini / Google ADK / LINE Messaging API |

## 執行方式

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

在瀏覽器開啟 `http://127.0.0.1:5000`。

## API 接口

- `POST /api/insight`：傳入 `{"location": "台北車站附近"}`，回傳區域生活情報。
- `POST /api/chat`：傳入 `{"message": "台北車站租金如何？"}`，回傳聊天建議。
- `GET /health`：服務健康檢查。

目前租金、天氣、交通與空氣品質皆為介面展示用資料。之後可在 `app.py` 的 API route 中改接 Geocode、中央氣象署、TDX、環境部 AQI、租金資料與 LLM 統整模組，前端不需要重做。

## GitHub 協作

第一次使用 GitHub、如何下載專案、改程式與上傳更新，請見 [docs/GITHUB_TEAM_GUIDE.md](docs/GITHUB_TEAM_GUIDE.md)。
