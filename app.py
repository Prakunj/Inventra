import streamlit as st
import time
import traceback
import pandas as pd
from datetime import datetime

from graph.workflow import build_graph


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
# Compile graph once per server lifecycle
# ─────────────────────────────────────────────
@st.cache_resource
def get_graph():
    return build_graph()


# Agent step labels shown during streaming
AGENT_STEPS = {
    "data":     ("📊", "Data Agent",     "Extracting intent & fetching inventory, vendor, weather data"),
    "decision": ("🧠", "Decision Agent",  "Analysing stock levels, vendor reliability & weather impact"),
    "ticket":   ("🎫", "Ticket Agent",    "Creating purchase ticket in the system"),
    "report":   ("📝", "Report Agent",    "Generating final structured report"),
}


def run_graph_with_steps(prompt: str) -> dict:
    """Stream the graph, rendering each agent step live inside an st.status box."""
    graph = get_graph()
    result_state: dict = {}

    with st.status("🤖 Running agents…", expanded=True) as status:
        try:
            for event in graph.stream({"user_query": prompt}):
                for node_name, node_output in event.items():
                    if node_name in AGENT_STEPS:
                        icon, label, desc = AGENT_STEPS[node_name]
                        st.markdown(
                            f"""
                            <div style="display:flex;align-items:flex-start;gap:10px;
                                        padding:0.5rem 0.6rem;border-radius:8px;
                                        background:#1a2234;border:1px solid #1e2d45;
                                        margin-bottom:6px;">
                              <span style="font-size:1rem;">{icon}</span>
                              <div>
                                <div style="font-size:0.82rem;font-weight:600;color:#a5b4fc;">
                                  {label} <span style="color:#86efac;font-size:0.75rem;">✓ done</span>
                                </div>
                                <div style="font-size:0.73rem;color:#64748b;margin-top:1px;">{desc}</div>
                              </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    if isinstance(node_output, dict):
                        result_state.update(node_output)

            status.update(label="✅ All agents completed", state="complete", expanded=False)

        except Exception as e:
            traceback.print_exc()   # full stack trace → Streamlit server log
            status.update(label="❌ Agent error", state="error", expanded=True)
            result_state = {"intent": "error", "report": f"⚠️ {e}"}

    return result_state


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
    border-bottom: 1px solid #1e2535; margin-bottom: 1rem;
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
    transition: all 0.2s ease !important;
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
    font-size: 0.8rem; color: #94a3b8;
}

/* ── Chat input bottom bar ── */
[data-testid="stBottom"] {
    background: #0f1117 !important;
    border-top: 1px solid #1e2535 !important;
}
[data-testid="stBottom"] > div { background: #0f1117 !important; }
[data-testid="stChatInput"] {
    background: #0f1117 !important;
    border: none !important; box-shadow: none !important;
}
[data-testid="stChatInput"] > div { background: #0f1117 !important; }
[data-testid="stChatInput"] textarea {
    background: #1e2535 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important; caret-color: #6366f1 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.25) !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 9px !important; border: none !important;
}
.stChatFloatingInputContainer { background: #0f1117 !important; border-top: 1px solid #1e2535 !important; }
.stChatFloatingInputContainer > div { background: #0f1117 !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] > div { color: #a5b4fc !important; }

/* ── DataFrame ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 4px; }

/* ── Error / warning ── */
.stAlert { border-radius: 10px !important; }

/* ── st.status widget ── */
[data-testid="stStatusWidget"] {
    background: #161b27 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 12px !important;
    color: #a5b4fc !important;
}
[data-testid="stStatusWidget"] summary {
    color: #a5b4fc !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}
[data-testid="stStatusWidget"] details > div {
    background: #0f1117 !important;
    border-top: 1px solid #1e2535 !important;
    padding: 0.75rem !important;
    border-radius: 0 0 12px 12px !important;
}
/* Running spinner icon colour */
[data-testid="stStatusWidget"] svg { color: #6366f1 !important; }

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
        "title":      title,
        "messages":   [],
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


def stock_badge(qty, threshold):
    if qty is None or threshold is None:
        return "—"
    if qty <= 0:
        return "🔴 Out of stock"
    if qty <= threshold * 0.5:
        return "🔴 Critical"
    if qty <= threshold:
        return "🟡 Low"
    return "🟢 Healthy"


# ─────────────────────────────────────────────
# Real result renderer — reads AgentState
# ─────────────────────────────────────────────
def render_real_result(state: dict):
    intent   = state.get("intent", "general")
    inv      = state.get("inventory_data")
    vendor   = state.get("vendor_data")
    weather  = state.get("weather_data")
    decision = state.get("decision")
    ticket   = state.get("ticket")
    report   = state.get("report", "")

    # ── REORDER ──────────────────────────────
    if intent == "reorder" and isinstance(inv, dict):
        qty       = inv.get("qty", "—")
        threshold = inv.get("reorder_threshold", "—")
        badge     = stock_badge(inv.get("qty"), inv.get("reorder_threshold"))

        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">🔄 Reorder Analysis — {inv.get('sku','—')} · {inv.get('name','—')}</div>
          <div class="result-card-body">
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Stock</span>{qty} units</div>
              <div class="metric-pill"><span class="mp-label">Threshold</span>{threshold} units</div>
              <div class="metric-pill"><span class="mp-label">Status</span>{badge}</div>
              <div class="metric-pill"><span class="mp-label">Region</span>{inv.get('region','—')}</div>
              <div class="metric-pill"><span class="mp-label">Category</span>{inv.get('category','—')}</div>
              <div class="metric-pill"><span class="mp-label">Unit Cost</span>${inv.get('unit_cost','—')}</div>
            </div>
        """, unsafe_allow_html=True)

        if isinstance(vendor, dict):
            st.markdown(f"""
            <div class="divider"></div>
            <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🏭 Vendor</div>
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Name</span>{vendor.get('name','—')}</div>
              <div class="metric-pill"><span class="mp-label">Lead Time</span>{vendor.get('lead_time_days','—')} days</div>
              <div class="metric-pill"><span class="mp-label">On-Time Rate</span>{vendor.get('on_time_delivery_rate','—')}%</div>
              <div class="metric-pill"><span class="mp-label">Reliability</span>{vendor.get('reliability_rating','—')}</div>
              <div class="metric-pill"><span class="mp-label">Min Order</span>{vendor.get('min_order_qty','—')} units</div>
            </div>
            """, unsafe_allow_html=True)

        if isinstance(weather, dict) and "error" not in weather:
            st.markdown(f"""
            <div class="divider"></div>
            <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🌦️ Weather — {weather.get('city','—')}</div>
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Condition</span>{weather.get('condition','—')}</div>
              <div class="metric-pill"><span class="mp-label">Temperature</span>{weather.get('temperature','—')}°C</div>
              <div class="metric-pill"><span class="mp-label">Humidity</span>{weather.get('humidity','—')}%</div>
            </div>
            """, unsafe_allow_html=True)

        if isinstance(decision, dict):
            reorder_badge = '<span class="badge badge-crit">REORDER REQUIRED</span>' if decision.get("reorder") else '<span class="badge badge-ok">NO REORDER NEEDED</span>'
            st.markdown(f"""
            <div class="divider"></div>
            <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🤖 AI Decision</div>
            <div style="background:#0f1923;border:1px solid #1e3a5f;border-radius:8px;padding:0.75rem;font-size:0.82rem;color:#cbd5e1;line-height:1.7;">
              {reorder_badge}&nbsp;
              Recommended Qty: <strong>{decision.get('recommended_qty','—')} units</strong><br>
              {decision.get('reason','')}
            </div>
            """, unsafe_allow_html=True)

        if isinstance(ticket, dict):
            if ticket.get("created"):
                st.markdown(f"""
                <div class="divider"></div>
                <div style="margin-bottom:0.5rem;font-size:0.8rem;font-weight:600;color:#a5b4fc;">🎫 Purchase Ticket Created</div>
                <div style="font-size:0.8rem;color:#94a3b8;display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
                  <span>TKT-{ticket.get('ticket_id','—')}</span>
                  <span class="badge badge-open">OPEN</span>
                  <span>Qty: {ticket.get('recommended_qty','—')}</span>
                  <span>Est. Cost: ${ticket.get('estimated_cost','—')}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="divider"></div>
                <div style="font-size:0.8rem;color:#64748b;">🎫 No ticket created — {ticket.get('reason','')}</div>
                """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── LOW STOCK ─────────────────────────────
    elif intent == "low_stock" and isinstance(inv, list):
        st.markdown('<div class="result-card"><div class="result-card-header">📉 Low Stock Report</div><div class="result-card-body">', unsafe_allow_html=True)

        if inv:
            rows = []
            for p in inv:
                rows.append({
                    "SKU":       p.get("sku"),
                    "Product":   p.get("name"),
                    "Category":  p.get("category"),
                    "Region":    p.get("region"),
                    "Qty":       p.get("qty"),
                    "Threshold": p.get("reorder_threshold"),
                    "Status":    stock_badge(p.get("qty"), p.get("reorder_threshold")),
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            critical = sum(1 for p in inv if (p.get("qty") or 0) <= (p.get("reorder_threshold") or 0) * 0.5)
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Total Low Stock</span>{len(inv)} products</div>
              <div class="metric-pill"><span class="mp-label">Critical (≤50% threshold)</span>{critical} products</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#86efac;font-size:0.85rem;">✅ All products are above reorder threshold.</p>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── INVENTORY LOOKUP ──────────────────────
    elif intent == "inventory_lookup" and isinstance(inv, list):
        st.markdown('<div class="result-card"><div class="result-card-header">📦 Inventory Search Results</div><div class="result-card-body">', unsafe_allow_html=True)

        if inv:
            rows = [{
                "SKU":       p.get("sku"),
                "Product":   p.get("name"),
                "Category":  p.get("category"),
                "Region":    p.get("region"),
                "Qty":       p.get("qty"),
                "Threshold": p.get("reorder_threshold"),
                "Unit Cost": f"${p.get('unit_cost',0):.2f}",
                "Health":    stock_badge(p.get("qty"), p.get("reorder_threshold")),
            } for p in inv]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.markdown('<p style="color:#94a3b8;font-size:0.85rem;">No products found matching your search.</p>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── CATEGORY LOOKUP ───────────────────────
    elif intent == "category_lookup" and isinstance(inv, list):
        category = inv[0].get("category", "Category") if inv else "Category"
        st.markdown(f'<div class="result-card"><div class="result-card-header">🏷️ Category — {category}</div><div class="result-card-body">', unsafe_allow_html=True)

        if inv:
            rows = [{
                "SKU":       p.get("sku"),
                "Product":   p.get("name"),
                "Region":    p.get("region"),
                "Qty":       p.get("qty"),
                "Threshold": p.get("reorder_threshold"),
                "Unit Cost": f"${p.get('unit_cost',0):.2f}",
                "Health":    stock_badge(p.get("qty"), p.get("reorder_threshold")),
            } for p in inv]
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            healthy  = sum(1 for p in inv if (p.get("qty") or 0) > (p.get("reorder_threshold") or 0))
            at_risk  = len(inv) - healthy
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-pill"><span class="mp-label">Total SKUs</span>{len(inv)}</div>
              <div class="metric-pill"><span class="mp-label">Healthy</span>{healthy}</div>
              <div class="metric-pill"><span class="mp-label">At Risk</span>{at_risk}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#94a3b8;font-size:0.85rem;">No products found in this category.</p>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── WEATHER + REGIONAL INVENTORY ──────────
    elif intent == "weather_inventory":
        if isinstance(weather, dict) and "error" not in weather:
            st.markdown(f"""
            <div class="result-card">
              <div class="result-card-header">🌦️ Weather & Inventory — {weather.get('region','')}</div>
              <div class="result-card-body">
                <div class="metric-row">
                  <div class="metric-pill"><span class="mp-label">City</span>{weather.get('city','—')}</div>
                  <div class="metric-pill"><span class="mp-label">Condition</span>{weather.get('condition','—')}</div>
                  <div class="metric-pill"><span class="mp-label">Temperature</span>{weather.get('temperature','—')}°C</div>
                  <div class="metric-pill"><span class="mp-label">Humidity</span>{weather.get('humidity','—')}%</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card"><div class="result-card-header">🌦️ Regional Inventory</div><div class="result-card-body">', unsafe_allow_html=True)

        if isinstance(inv, list) and inv:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            rows = [{
                "SKU":     p.get("sku"),
                "Product": p.get("name"),
                "Qty":     p.get("qty"),
                "Health":  stock_badge(p.get("qty"), p.get("reorder_threshold")),
            } for p in inv]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── FALLBACK — show report text ───────────
    else:
        if report:
            st.markdown(f"""
            <div class="result-card">
              <div class="result-card-header">💬 Inventra AI</div>
              <div class="result-card-body" style="color:#cbd5e1;font-size:0.85rem;line-height:1.75;">
                {report.replace(chr(10), '<br>')}
              </div>
            </div>""", unsafe_allow_html=True)
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
    # ── Welcome / landing screen ──
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
        <div class="example-chip">🔄 Reorder SKU-001</div>
        <div class="example-chip">📦 Search inventory for mixer</div>
        <div class="example-chip">🌦️ Weather impact on North region</div>
        <div class="example-chip">🏷️ Show all Apparel category items</div>
        <div class="example-chip">📊 Show me all Electronics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    prompt = st.chat_input("Ask Inventra anything about your inventory…")
    if prompt:
        sid = create_session(title=prompt[:42] + ("…" if len(prompt) > 42 else ""))
        active = st.session_state.sessions[sid]
        active["messages"].append({"role": "user", "content": prompt, "ts": now_ts()})

        result_state = run_graph_with_steps(prompt)

        active["messages"].append({
            "role":  "ai",
            "state": result_state,
            "ts":    now_ts(),
        })
        st.rerun()

else:
    # ── Active chat session ──
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

            render_real_result(msg.get("state", {}))

            st.markdown(f"""
                <div class="msg-ts">{msg['ts']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Input ──
    prompt = st.chat_input("Ask Inventra anything about your inventory…")
    if prompt:
        active["messages"].append({"role": "user", "content": prompt, "ts": now_ts()})

        result_state = run_graph_with_steps(prompt)

        active["messages"].append({
            "role":  "ai",
            "state": result_state,
            "ts":    now_ts(),
        })
        st.rerun()
