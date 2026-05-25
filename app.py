from __future__ import annotations

from datetime import datetime
from typing import Any

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


AREA_DATA: dict[str, dict[str, Any]] = {
    "台北車站": {
        "district": "中正區 / 大同區交界",
        "rent": "NT$ 13,000 - 23,000",
        "weather": "29°C · 陣雨機率 30%",
        "air": "AQI 54 · 普通",
        "traffic_score": "極便利",
        "traffic": "捷運藍線、紅線、台鐵、高鐵與客運轉乘集中，通勤選擇完整。",
        "lifestyle": "百貨、地下街、超商與餐飲密集，晚間人流較多。",
        "facilities": [
            {"icon": "＋", "name": "台大醫院", "detail": "捷運 1 站"},
            {"icon": "購", "name": "京站 / 地下街", "detail": "步行可達"},
            {"icon": "車", "name": "YouBike / 轉運站", "detail": "多站點"},
            {"icon": "園", "name": "二二八和平公園", "detail": "約 10 分鐘"},
        ],
        "summary": "適合重視跨區通勤與生活機能的租客，租金偏高，賞屋時可留意噪音與尖峰人潮。",
    },
    "公館": {
        "district": "中正區 / 大安區",
        "rent": "NT$ 10,000 - 18,000",
        "weather": "29°C · 陣雨機率 30%",
        "air": "AQI 48 · 良好",
        "traffic_score": "便利",
        "traffic": "捷運綠線與多線公車可達，前往台大、師大與市中心方便。",
        "lifestyle": "學生生活圈成熟，小吃、書店與日常採買選擇豐富。",
        "facilities": [
            {"icon": "學", "name": "臺灣大學", "detail": "步行可達"},
            {"icon": "購", "name": "公館商圈", "detail": "步行 3 分鐘"},
            {"icon": "河", "name": "自來水園區", "detail": "約 8 分鐘"},
            {"icon": "車", "name": "捷運公館站", "detail": "綠線"},
        ],
        "summary": "適合學生與喜歡活絡街區的租客，選屋時可注意夜市周邊音量及老屋採光。",
    },
    "中山": {
        "district": "中山區 / 大同區",
        "rent": "NT$ 15,000 - 27,000",
        "weather": "30°C · 陣雨機率 20%",
        "air": "AQI 57 · 普通",
        "traffic_score": "極便利",
        "traffic": "捷運紅線、綠線交會，前往台北車站與松山線商圈快速。",
        "lifestyle": "文創店家、百貨與餐廳密集，質感生活選擇多。",
        "facilities": [
            {"icon": "購", "name": "南西商圈", "detail": "步行可達"},
            {"icon": "園", "name": "心中山線形公園", "detail": "步行 2 分鐘"},
            {"icon": "車", "name": "中山捷運站", "detail": "紅 / 綠線"},
            {"icon": "醫", "name": "馬偕紀念醫院", "detail": "約 10 分鐘"},
        ],
        "summary": "交通與休閒表現出色，但熱門巷弄租金較高；適合將便利與生活風格放在前面的租客。",
    },
    "板橋": {
        "district": "新北市板橋區",
        "rent": "NT$ 11,000 - 21,000",
        "weather": "28°C · 陣雨機率 40%",
        "air": "AQI 50 · 良好",
        "traffic_score": "極便利",
        "traffic": "捷運、台鐵、高鐵與公車轉運匯集，往台北市或外縣市都方便。",
        "lifestyle": "百貨、公園與行政設施完整，住宅選擇比市中心更有彈性。",
        "facilities": [
            {"icon": "車", "name": "板橋車站", "detail": "多鐵共構"},
            {"icon": "園", "name": "新板萬坪都會公園", "detail": "步行可達"},
            {"icon": "購", "name": "大遠百", "detail": "步行約 6 分鐘"},
            {"icon": "醫", "name": "亞東醫院", "detail": "捷運 2 站"},
        ],
        "summary": "兼顧交通與居住空間的選擇，適合常跨縣市移動或希望租金相對有彈性的租客。",
    },
}


def resolve_area(query: str) -> tuple[str, dict[str, Any]]:
    normalized = query.strip()
    for area, info in AREA_DATA.items():
        if area in normalized:
            return area, info

    area_name = normalized
    for phrase in ("我今天想在", "我想在", "想在", "附近", "租房子", "租屋", "找房子", "找房"):
        area_name = area_name.replace(phrase, "")
    area_name = area_name.strip(" ，,。?？") or "指定區域"
    return area_name, {
        "district": "等待地理編碼定位",
        "rent": "資料串接後提供",
        "weather": "資料串接後提供",
        "air": "資料串接後提供",
        "traffic_score": "分析中",
        "traffic": "接入 TDX 後將分析附近大眾運輸站點與轉乘便利性。",
        "lifestyle": "接入 OpenStreetMap 或設施資料後將顯示生活機能。",
        "facilities": [
            {"icon": "車", "name": "交通站點", "detail": "待查詢"},
            {"icon": "購", "name": "採買設施", "detail": "待查詢"},
            {"icon": "醫", "name": "醫療院所", "detail": "待查詢"},
            {"icon": "園", "name": "休閒空間", "detail": "待查詢"},
        ],
        "summary": "這個區域尚未放入示意資料；串接 Agent 後會即時整理租金、交通、設施與環境品質。",
    }


def area_payload(query: str) -> dict[str, Any]:
    area, info = resolve_area(query)
    return {
        "area": area,
        "requested_query": query,
        "generated_at": datetime.now().strftime("%H:%M"),
        "demo": True,
        **info,
    }


@app.get("/")
def index() -> str:
    return render_template("index.html", initial_area=area_payload("台北車站"))


@app.post("/api/insight")
def insight() -> Any:
    body = request.get_json(silent=True) or {}
    query = str(body.get("location", "")).strip()
    if not query:
        return jsonify({"error": "請輸入想了解的租屋區域"}), 400
    return jsonify(area_payload(query))


@app.post("/api/chat")
def chat() -> Any:
    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()
    if not message:
        return jsonify({"error": "請輸入問題"}), 400

    area, info = resolve_area(message)
    if "租金" in message or "預算" in message:
        answer = f"{area}目前示意租金區間為 {info['rent']} / 月。之後串接租賃與實價資料後，我可以依房型和預算再細分。"
    elif "交通" in message or "捷運" in message or "通勤" in message:
        answer = f"{area}交通便利度為「{info['traffic_score']}」。{info['traffic']}"
    elif "空氣" in message or "天氣" in message:
        answer = f"{area}今天的示意資訊：{info['weather']}，空氣品質 {info['air']}。正式版會即時查詢氣象與環境資料。"
    elif any(keyword in message for keyword in ("醫院", "超商", "公園", "生活", "設施")):
        answer = f"{area}的生活觀察：{info['lifestyle']} 附近可關注 " + "、".join(
            item["name"] for item in info["facilities"]
        ) + "。"
    else:
        answer = f"{area}：{info['summary']} 你也可以問我租金、通勤、空氣品質或附近設施。"

    return jsonify({"reply": answer, "area": area, "demo": True})


@app.get("/health")
def health() -> Any:
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
