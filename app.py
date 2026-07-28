import streamlit as st
import time
import pandas as pd
from datetime import datetime


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Inventra AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

.stApp { background: #0f1117; color: #e8eaf0; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #1e2535 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

/* ── Brand ── */
.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 0 1rem 1.2rem 1rem;
    border-bottom: 1px solid #1e2535;
    margin-bottom: 1rem;
}
.sb-brand-icon {
    font-size: 1.4rem;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px; padding: 6px 8px; line-height: 1;
}
.sb-brand-text {
    font-size: 1.1rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 0.55rem 1rem !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    transition: all 0.2s ease !important; cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* ── Session card ── */
.session-card {
    background: #1e2535; border: 1px solid #252d40;
    border-radius: 10px; padding: 0.65rem 0.85rem;
    margin-bottom: 0.45rem; transition: all 0.18s ease;
}
.session-card.active {
    background: #1e2040; border-color: #6366f1;
    box-shadow: 0 0 0 1px #6366f166;
}
.session-title {
    font-size: 0.82rem; font-weight: 600; color: #cbd5e1;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.session-meta { font-size: 0.7rem; color: #64748b; margin-top: 2px; }
.sb-section-label {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em;
    color: #475569; text-transform: uppercase;
    padding: 0 1rem; margin: 0.8rem 0 0.5rem 0;
}

/* ── Chat header ── */
.chat-header {
    padding: 1.2rem 0 0.8rem 0;
    border-bottom: 1px solid #1e2535; margin-bottom: 1.5rem;
}
.chat-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; }
.chat-subtitle { font-size: 0.76rem; color: #64748b; margin-top: 3px; }

/* ── Messages ── */
.msg-row { display: flex; gap: 12px; margin-bottom: 1.2rem; animation: fadeUp 0.25s ease; }
.msg-row.user { flex-direction: row-reverse; }
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; flex-shrink: 0; margin-top: 2px;
}
.msg-avatar.ai  { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.msg-avatar.usr { background: linear-gradient(135deg, #0ea5e9, #38bdf8); }
.msg-bubble {
    max-width: 72%; padding: 0.75rem 1rem;
    border-radius: 14px; font-size: 0.88rem; line-height: 1.65;
}
.msg-bubble.ai {
    background: #1e2535; border: 1px solid #252d40; color: #cbd5e1;
    border-radius: 4px 14px 14px 14px;
}
.msg-bubble.user {
    background: linear-gradient(135deg, #312e81, #3730a3); color: #e0e7ff;
    border-radius: 14px 4px 14px 14px;
}
.msg-ts { font-size: 0.68rem; color: #475569; margin-top: 4px; }
.msg-ts.right { text-align: right; }

/* ── Result cards ── */
.result-card {
    background: #1a2234; border: 1px solid #1e2d45;
    border-radius: 12px; overflow: hidden; margin-top: 0.6rem;
}
.result-card-header {
    background: #1e2d45; padding: 0.5rem 0.9rem;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em;
    color: #7dd3fc; text-transform: uppercase;
}
.result-card-body { padding: 0.85rem; }

/* ── Metric pills ── */
.metric-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 0.5rem 0; }
.metric-pill {
    background: #0f1923; border: 1px solid #1e3a5f;
    border-radius: 8px; padding: 0.4rem 0.8rem;
    font-size: 0.8rem; color: #93c5fd;
    display: flex; flex-direction: column; gap: 1px;
}
.mp-label { font-size: 0.63rem; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; }

/* ── Badges ── */
.badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 0.68rem; font-weight: 600; }
.badge-crit { background: #7f1d1d; color: #fca5a5; }
.badge-warn { background: #713f12; color: #fde68a; }
.badge-ok   { background: #14532d; color: #86efac; }
.badge-open { background: #312e81; color: #c4b5fd; }
.badge-info { background: #1e3a5f; color: #93c5fd; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #252d40, transparent);
    margin: 0.9rem 0;
}

/* ── Welcome screen ── */
.welcome-wrap {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 3.5rem 1rem 2rem; text-align: center;
}
.welcome-icon { font-size: 3rem; margin-bottom: 1rem; }
.welcome-title {
    font-size: 1.8rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.welcome-sub {
    font-size: 0.88rem; color: #64748b;
    max-width: 420px; line-height: 1.65; margin-bottom: 2rem;
}
.example-grid { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; max-width: 600px; }
.example-chip {
    background: #1e2535; border: 1px solid #252d40;
    border-radius: 20px; padding: 0.5rem 1rem;
    font-size: 0.8rem; color: #94a3b8; cursor: pointer; transition: all 0.2s;
}

/* ── Chat input bar (bottom fixed strip) ── */
/* Force the entire bottom container to match the dark theme */
[data-testid="stBottom"] {
    background: #0f1117 !important;
    border-top: 1px solid #1e2535 !important;
}
[data-testid="stBottom"] > div {
    background: #0f1117 !important;
}
/* The inner white card Streamlit wraps around the input */
[data-testid="stChatInput"] {
    background: #0f1117 !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] > div {
    background: #0f1117 !important;
}
[data-testid="stChatInput"] textarea {
    background: #1e2535 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    caret-color: #6366f1 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.25) !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 9px !important;
    border: none !important;
}
/* Catch any remaining light wrappers Streamlit may inject */
.stChatFloatingInputContainer {
    background: #0f1117 !important;
    border-top: 1px solid #1e2535 !important;
}
.stChatFloatingInputContainer > div {
    background: #0f1117 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "active_session" not in st.session_state:
    st.session_state.active_session = None


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def create_session(title="New Chat"):
    sid = f"s_{int(time.time() * 1000)}"
    st.session_state.sessions[sid] = {
        "title": title,
        "messages": [],
        "created_at": datetime.now(),
    }
    st.session_state.active_session = sid
    return sid


def get_active():
    sid = st.session_state.active_session
    if sid and sid in st.session_state.sessions:
        return st.session_state.sessions[sid]
    return None


def now_ts():
    return datetime.now().strftime("%H:%M")


def relative_time(dt):
    s = int((datetime.now() - dt).total_seconds())
    if s < 60:    return "just now"
    if s < 3600:  return f"{s // 60}m ago"
    if s < 86400: return f"{s // 3600}h ago"
    return dt.strftime("%b %d")


def detect_intent(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["low stock", "low-stock", "below threshold", "running low"]): return "low_stock"
    if any(k in q for k in ["reorder", "re-order", "purchase", "order"]): return "reorder"
    if any(k in q for k in ["weather", "temperature", "forecast", "rain", "snow"]): return "weather"
    if any(k in q for k in ["category", "apparel", "footwear", "accessories"]): return "category_lookup"
    if any(k in q for k in ["search", "find", "look", "inventory", "sku"]): return "inventory_lookup"
    return "general"


# ─────────────────────────────────────────────
# Structured result renderers
# ─────────────────────────────────────────────
def render_result(intent: str, query: str):
    if intent == "low_stock":
        st.markdown('<div class="result-card"><div class="result-card-header">📉 Low Stock Report</div><div class="result-card-body">', unsafe_allow_html=True)
        df = pd.DataFrame({
            "SKU":       ["SKU-001", "SKU-047", "SKU-102", "SKU-215"],
            "Product":   ["Winter Jacket", "Snow Boots", "Thermal Gloves", "Fleece Hoodie"],
            "Region":    ["North", "North", "East", "West"],
            "Qty":       [12, 8, 5, 20],
            "Threshold": [50, 30, 25, 40],
            "Status":    ["🔴 Critical", "🔴 Critical", "🔴 Critical", "🟡 Low"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("""
        <div class="metric-row">
          <div class="metric-pill"><span class="mp-label">Total Low Stock</span>4 products</div>
          <div class="metric-pill"><span class="mp-label">Critical</span>3 products</div>
          <div class="metric-pill"><span class="mp-label">Action</span>Immediate reorder</div>
        </div>
        </div></div>""", unsafe_allow_html=True)

    elif intent == "reorder":
        st.markdown("""
        <div class="result-card">
          <div class="result-card-header">🔄 Reorder Analysis — SKU-001 · Winter Jacket</div>
          <div class="result-card-body">
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Current Stock</span>12 units</div>
              <div class="metric-pill"><span class="mp-label">Threshold</span>50 units</div>
              <div class="metric-pill"><span class="mp-label">Vendor</span>ArcticSupply Co.</div>
              <div class="metric-pill"><span class="mp-label">Lead Time</span>7 days</div>
              <div class="metric-pill"><span class="mp-label">Weather</span>❄️ Heavy Snow</div>
            </div>
            <div class="divider"></div>
            <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🤖 AI Decision</div>
            <div style="background:#0f1923;border:1px solid #1e3a5f;border-radius:8px;padding:0.75rem;font-size:0.82rem;color:#cbd5e1;line-height:1.7;">
              <span class="badge badge-crit">REORDER REQUIRED</span>&nbsp;
              Recommend ordering <strong>200 units</strong><br>
              Stock (12) is 76% below threshold. Heavy snow in North region will spike
              winter apparel demand. Vendor reliability: 97% on-time.
            </div>
            <div class="divider"></div>
            <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🎫 Purchase Ticket</div>
            <div style="font-size:0.8rem;color:#94a3b8;display:flex;align-items:center;gap:10px;">
              <span>TKT-2847</span>
              <span class="badge badge-open">OPEN</span>
              <span style="margin-left:auto;color:#475569;font-size:0.72rem;">Created just now</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    elif intent == "weather":
        st.markdown("""
        <div class="result-card">
          <div class="result-card-header">🌦️ Weather & Inventory Impact — North Region</div>
          <div class="result-card-body">
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Condition</span>❄️ Heavy Snow</div>
              <div class="metric-pill"><span class="mp-label">Temperature</span>-8°C</div>
              <div class="metric-pill"><span class="mp-label">Humidity</span>78%</div>
              <div class="metric-pill"><span class="mp-label">Rainfall</span>0 mm</div>
            </div>
            <div class="divider"></div>
            <div style="background:#0f1923;border:1px solid #1e3a5f;border-radius:8px;padding:0.75rem;font-size:0.82rem;color:#cbd5e1;line-height:1.7;">
              <span class="badge badge-warn">⚠️ DEMAND SPIKE EXPECTED</span><br><br>
              Heavy snow historically correlates with a <strong>35–50% increase</strong> in
              demand for winter apparel, footwear, and thermal accessories in this region.
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    elif intent == "inventory_lookup":
        st.markdown('<div class="result-card"><div class="result-card-header">📦 Inventory Search Results</div><div class="result-card-body">', unsafe_allow_html=True)
        df = pd.DataFrame({
            "SKU":         ["SKU-001", "SKU-034", "SKU-089"],
            "Product":     ["Winter Jacket", "Windbreaker", "Rain Jacket"],
            "Category":    ["Apparel", "Apparel", "Apparel"],
            "Region":      ["North", "West", "East"],
            "Qty":         [12, 145, 78],
            "Unit Cost":   ["$89.99", "$54.50", "$67.00"],
            "Health":      ["🔴 Critical", "🟢 Healthy", "🟢 Healthy"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    elif intent == "category_lookup":
        st.markdown('<div class="result-card"><div class="result-card-header">🏷️ Category Overview — Apparel</div><div class="result-card-body">', unsafe_allow_html=True)
        df = pd.DataFrame({
            "SKU":       ["SKU-001", "SKU-034", "SKU-056", "SKU-215"],
            "Product":   ["Winter Jacket", "Windbreaker", "Polo Shirt", "Fleece Hoodie"],
            "Region":    ["North", "West", "South", "West"],
            "Qty":       [12, 145, 320, 20],
            "Health":    ["🔴 Critical", "🟢 Healthy", "🟢 Healthy", "🟡 Low"],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("""
        <div class="metric-row">
          <div class="metric-pill"><span class="mp-label">Total SKUs</span>4</div>
          <div class="metric-pill"><span class="mp-label">Healthy</span>2</div>
          <div class="metric-pill"><span class="mp-label">At Risk</span>2</div>
        </div>
        </div></div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result-card">
          <div class="result-card-header">💬 Inventra AI</div>
          <div class="result-card-body" style="color:#94a3b8;font-size:0.85rem;line-height:1.7;">
            I can help with inventory queries, reorder decisions, low stock alerts,
            category lookups, and weather-based demand forecasting.<br><br>
            Try: <em>"Show me low stock products"</em> or <em>"Reorder SKU-001"</em>
          </div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-brand-icon">📦</div>
      <div class="sb-brand-text">Inventra AI</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  New Chat"):
        create_session()
        st.rerun()

    if st.session_state.sessions:
        st.markdown('<div class="sb-section-label">Recent Chats</div>', unsafe_allow_html=True)

        sorted_sessions = sorted(
            st.session_state.sessions.items(),
            key=lambda x: x[1]["created_at"],
            reverse=True,
        )

        for sid, sess in sorted_sessions:
            is_active = sid == st.session_state.active_session
            card_cls  = "session-card active" if is_active else "session-card"
            n_msgs    = len(sess["messages"])

            st.markdown(f"""
            <div class="{card_cls}">
              <div class="session-title">{sess['title']}</div>
              <div class="session-meta">
                {relative_time(sess['created_at'])} &nbsp;·&nbsp;
                {n_msgs} msg{"s" if n_msgs != 1 else ""}
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("open", key=f"btn_{sid}", help=f"Open: {sess['title']}"):
                st.session_state.active_session = sid
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;color:#475569;font-size:0.78rem;padding:2rem 1rem;">
          No chats yet.<br>Start a conversation above.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:1rem;left:0;width:18rem;text-align:center;
                color:#2d3748;font-size:0.65rem;">
      Inventra AI · Powered by Gemini
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────
active = get_active()

if active is None:
    # ── Welcome screen ──
    st.markdown("""
    <div class="welcome-wrap">
      <div class="welcome-icon">📦</div>
      <div class="welcome-title">Inventra AI</div>
      <div class="welcome-sub">
        Your intelligent inventory assistant. Ask about stock levels,
        reorder decisions, vendor performance, or demand forecasting.
      </div>
      <div class="example-grid">
        <div class="example-chip">📉 Show me low stock products</div>
        <div class="example-chip">🔄 Reorder SKU-001 Winter Jacket</div>
        <div class="example-chip">📦 Search inventory for jackets</div>
        <div class="example-chip">🌦️ Weather impact on North region</div>
        <div class="example-chip">🏷️ Show all Apparel category items</div>
        <div class="example-chip">📊 Generate inventory report</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    prompt = st.chat_input("Ask Inventra anything about your inventory…")
    if prompt:
        sid = create_session(title=prompt[:42] + ("…" if len(prompt) > 42 else ""))
        active = st.session_state.sessions[sid]
        active["messages"].append({"role": "user",  "content": prompt, "ts": now_ts()})
        active["messages"].append({
            "role": "ai", "content": "__result__",
            "intent": detect_intent(prompt), "query": prompt, "ts": now_ts(),
        })
        st.rerun()

else:
    # ── Active chat ──
    n_exchanges = len(active["messages"]) // 2

    st.markdown(f"""
    <div class="chat-header">
      <div class="chat-title">💬 {active['title']}</div>
      <div class="chat-subtitle">
        Started {relative_time(active['created_at'])} &nbsp;·&nbsp;
        {n_exchanges} exchange{"s" if n_exchanges != 1 else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Render messages
    for msg in active["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
              <div class="msg-avatar usr">👤</div>
              <div>
                <div class="msg-bubble user">{msg['content']}</div>
                <div class="msg-ts right">{msg['ts']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="msg-row">
              <div class="msg-avatar ai">🤖</div>
              <div style="flex:1;">
                <div class="msg-bubble ai">Here's what I found:</div>
            """, unsafe_allow_html=True)

            if msg.get("content") == "__result__":
                render_result(msg.get("intent", "general"), msg.get("query", ""))
            else:
                st.markdown(f"""
                <div class="result-card">
                  <div class="result-card-body" style="color:#cbd5e1;font-size:0.85rem;">
                    {msg['content']}
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""
                <div class="msg-ts">{msg['ts']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Input
    prompt = st.chat_input("Ask Inventra anything about your inventory…")
    if prompt:
        active["messages"].append({"role": "user",  "content": prompt, "ts": now_ts()})
        active["messages"].append({
            "role": "ai", "content": "__result__",
            "intent": detect_intent(prompt), "query": prompt, "ts": now_ts(),
        })
        st.rerun()
