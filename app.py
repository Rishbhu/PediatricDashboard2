# app.py
import streamlit as st
import math
from datetime import date

st.set_page_config(page_title="Patient Overview", layout="wide")

# ======================== THEME & GLOBAL CSS (Dark-blue) ========================
st.markdown("""
<style>
header[data-testid="stHeader"]{display:none !important;}
#MainMenu, footer{visibility:hidden !important;}
.block-container{padding-top:4px !important; padding-bottom:4px !important; max-width:1400px;}
[data-testid="stVerticalBlock"] > [style*="width"]{padding-top:2px !important; padding-bottom:2px !important;}
[data-testid="column"]{padding:0 6px !important;}

/* -------- Dark blue neutral theme -------- */
:root{
  --bg:#0F172A;                 /* page bg (deep slate/navy) */
  --band:#12263F;               /* top band bg */
  --band-border:#24425F;
  --side:#12213B;               /* left nav card */
  --ink:#F8FAFC;                /* default text: near-white */
  --heading:#FFFFFF;            /* headings: pure white */
  --muted:#C7D2FE;              /* readable light indigo */
  --card:#0B1426;               /* dark card surface */
  --border:#1E2A44;

  --brand-coral:#F97362;        /* accents */
  --brand-teal:#22D3EE;

  /* BAR CHART = ALL REDS */
  --bar1:#FCA5A5; --bar2:#F87171; --bar3:#EF4444; --bar4:#DC2626;

  /* Donut */
  --donut1:#F97362; --donut2:#22D3EE; --donut3:#38BDF8; --donut4:#93C5FD;
}

html, body, .stApp, [data-testid="stAppViewContainer"], .main {
  background: var(--bg) !important; color: var(--ink) !important;
}
*{ color: var(--ink); font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji","Segoe UI Emoji"; }
.muted{ color: var(--muted) !important; }

/* Left card - more compact */
.side{ background: var(--side); border:1px solid var(--band-border); border-radius:10px; padding:10px 14px; }
.side h3{ margin:0 0 6px; letter-spacing:.14em; color: var(--heading); font-weight:1000; font-size:18px; line-height:1.1; white-space:nowrap; }
.side p{ margin:2px 0 0; font-weight:800; font-size:13px; }

/* Top band - more compact */
.topband{ background: var(--band); border:1px solid var(--band-border); border-radius:10px; padding:10px 16px; margin-bottom:10px; position:relative; }
.kvgrid{display:grid; grid-template-columns:repeat(7, 1fr); gap:12px; align-items:center;}
.kv .label{ font-size:12px; font-weight:1000; letter-spacing:.12em; color: var(--heading); white-space:nowrap; }
.kv .val{ margin-top:2px; font-size:15px; font-weight:900; }
.baby{ width:38px;height:38px;border-radius:999px;border:2px solid var(--band-border); display:flex;align-items:center;justify-content:center;background:#0b1a30;font-size:18px; }

/* Premature icon in top right */
.premature-icon{ position:absolute; top:10px; right:16px; width:42px;height:42px;border-radius:999px;border:2px solid #F97362; display:flex;align-items:center;justify-content:center;background:#1a0f0f;font-size:20px; box-shadow:0 2px 8px rgba(249,115,98,0.3); }

/* Risk section at top */
.risk-header{ background:linear-gradient(135deg, #1a0f0f 0%, #2a1515 100%); border:2px solid #F97362; border-radius:12px; padding:12px 16px; margin-bottom:10px; box-shadow:0 4px 12px rgba(249,115,98,0.2); }
.risk-title{ font-weight:1000; font-size:20px; letter-spacing:.1em; color: #F97362; text-align:center; margin-bottom:8px; }
.risk-display{ display:flex; align-items:center; justify-content:space-around; gap:20px; }
.risk-percentage{ font-size:48px; font-weight:1000; color: #F97362; text-align:center; line-height:1; }
.risk-label{ font-size:14px; font-weight:800; color: var(--muted); text-align:center; margin-top:4px; letter-spacing:.1em; }

/* Headings - more compact */
.h2{font-weight:1000; font-size:19px; letter-spacing:.08em; color: var(--heading); white-space:nowrap; margin:6px 0 4px;}
.h3{font-weight:900;  font-size:16px; letter-spacing:.06em; color: var(--heading); white-space:nowrap; margin:4px 0 2px;}

/* Cards - more compact */
.card{background:var(--card); border:1px solid var(--border); border-radius:10px; padding:8px 12px;}
.card + .card{margin-top:6px;}

/* Flow (steps 1..6) - more compact */
.flowgrid{display:grid; grid-template-columns: 1fr 32px 1fr 32px 1fr; row-gap:12px; column-gap:10px; align-items:center; margin-top:6px;}
.stage{ background:#3A0E0E;border:1px solid #7A2E2E;border-radius:8px; padding:8px 10px;min-width:140px;text-align:center;font-weight:900; color:#FEE2E2; font-size:13px; transition:all .15s ease-in-out; }
.stage.active{ box-shadow:0 0 0 3px var(--brand-coral) inset; transform:translateY(-2px); }
.connector{height:3px;background:#7A2E2E;position:relative;border-radius:3px;}
.connector:after{content:"";position:absolute;right:-5px;top:-3px;border-left:8px solid #7A2E2E;border-top:6px solid transparent;border-bottom:6px solid transparent;}
.stepbadge{ width:24px;height:24px;border-radius:50%;border:2px dashed #CBD5E1;display:flex;align-items:center;justify-content:center; color:#E2E8F0;font-weight:900;background:#0B1426;margin:0 auto 4px; font-size:11px; }

/* Charts layout */
.donutwrap{display:flex;align-items:center;justify-content:flex-end; width:100%;}
.gaugewrap{display:flex;align-items:center;justify-content:center;}

/* Compact gauge for top */
.risk-gauge-wrap{display:flex;align-items:center;justify-content:center; padding:4px 0;}

/* Pill - more compact */
.pillbar{ height:36px;border-radius:999px;background:linear-gradient(90deg, #ef4444 0%, #fb923c 40%, #22c55e 100%); display:flex;align-items:center;justify-content:center;border:1px solid #1f2e4a; }
.pillbar .chip{background:#FFE680;color:#111;border:2px solid #d8b84f;border-radius:18px;padding:4px 10px;font-weight:1000; font-size:12px;}
.pillcaption{font-weight:1000;text-align:center;margin-top:6px;color:#E2E8F0; font-size:13px;}

/* Compact form elements */
[data-testid="stSelectbox"], [data-testid="stDateInput"], [data-testid="stNumberInput"], [data-testid="stTextArea"], [data-testid="stToggle"]{margin-bottom:6px !important;}
label{margin-bottom:3px !important;}
</style>
""", unsafe_allow_html=True)

# ======================== SVG HELPERS ========================
def arc_path(cx, cy, r, start_deg, end_deg):
    import math as _m
    start = _m.radians(start_deg); end = _m.radians(end_deg)
    x1, y1 = cx + r*_m.cos(start), cy + r*_m.sin(start)
    x2, y2 = cx + r*_m.cos(end),   cy + r*_m.sin(end)
    large = 1 if end - start > _m.pi else 0
    return f"M{x1:.3f},{y1:.3f} A{r:.3f},{r:.3f} 0 {large} 1 {x2:.3f},{y2:.3f}"

def semi_gauge_svg(pct:int=70, compact:bool=False)->str:
    pct = max(0, min(100, pct))
    if compact:
        # Smaller gauge for top display
        cx, cy, R, stroke = 100, 90, 70, 18
        filled = 180 * pct/100.0
        end_angle = 180 - filled
        base = arc_path(cx, cy, R, 180, 0)
        fill = arc_path(cx, cy, R, 180, end_angle)
        return f"""
        <svg width="240" height="160" viewBox="0 0 240 160">
          <g fill="none" stroke-linecap="round">
            <path d="{base}" stroke="#E9B98A" stroke-width="{stroke}" />
            <path d="{fill}" stroke="#F97362" stroke-width="{stroke}" />
          </g>
          <circle cx="{cx}" cy="{cy}" r="{R-14}" fill="#0B1426"/>
          <text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="42" font-weight="1000" fill="#F8FAFC">{pct}%</text>
        </svg>
        """
    else:
        cx, cy, R, stroke = 140, 130, 100, 26
        filled = 180 * pct/100.0
        end_angle = 180 - filled
        base = arc_path(cx, cy, R, 180, 0)
        fill = arc_path(cx, cy, R, 180, end_angle)
        return f"""
        <svg width="340" height="240" viewBox="0 0 340 240">
          <g fill="none" stroke-linecap="round">
            <path d="{base}" stroke="#E9B98A" stroke-width="{stroke}" />
            <path d="{fill}" stroke="#F97362" stroke-width="{stroke}" />
          </g>
          <circle cx="{cx}" cy="{cy}" r="{R-19}" fill="#0B1426"/>
          <text x="{cx}" y="{cy-3}" text-anchor="middle" font-size="62" font-weight="1000" fill="#F8FAFC">{pct}%</text>
        </svg>
        """

def bar_svg(counts)->str:
    W, H = 320, 190
    ymax = max(18, max(counts)+2)
    labels = [("Downs", counts[0], "var(--bar1)"),
              ("Turner", counts[1], "var(--bar2)"),
              ("DiGeorge", counts[2], "var(--bar3)"),
              ("Williams", counts[3], "var(--bar4)")]
    barw, gap, x0, y0 = 48, 28, 38, H-32
    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg += [f'<line x1="{x0-14}" y1="24" x2="{x0-14}" y2="{y0}" stroke="#E5E7EB" stroke-width="2"/>',
            f'<line x1="{x0-14}" y1="{y0}" x2="{W-18}" y2="{y0}" stroke="#E5E7EB" stroke-width="2"/>']
    x = x0
    for label, val, color in labels:
        height = int((val / ymax) * (y0-28))
        svg.append(f'<rect x="{x}" y="{y0-height}" width="{barw}" height="{height}" rx="8" fill="{color}"/>')
        svg.append(f'<text x="{x+barw/2}" y="{y0+18}" text-anchor="middle" font-size="12" fill="#F8FAFC" font-weight="900">{label}</text>')
        x += barw + gap
    svg.append("</svg>")
    return "".join(svg)

def donut_svg(segments)->str:
    cx, cy, R, stroke = 150, 140, 84, 36  # cx pushed right so donut isn't clipped
    start = -90
    svg = [f'<svg width="340" height="280" viewBox="0 0 340 280"><g fill="none" stroke-linecap="butt">']
    for label, pct, color in segments:
        sweep = 360*pct/100.0; end = start + sweep
        path = arc_path(cx, cy, R, start, end)
        svg.append(f'<path d="{path}" stroke="{color}" stroke-width="{stroke}"/>')
        import math as _m
        mid = _m.radians((start+end)/2.0)
        rx = (R+38)*_m.cos(mid) + cx; ry = (R+38)*_m.sin(mid) + cy
        svg.append(f'<text x="{rx:.1f}" y="{ry:.1f}" text-anchor="middle" font-size="12" fill="#F8FAFC" font-weight="900">{label}</text>')
        svg.append(f'<text x="{rx:.1f}" y="{ry+14:.1f}" text-anchor="middle" font-size="12" fill="#F8FAFC">{pct:.0f}%</text>')
        start = end
    svg.append('</g><circle cx="{cx}" cy="{cy}" r="{r}" fill="#0B1426"/></svg>'.format(cx=cx, cy=cy, r=R-24))
    return "".join(svg)

# ======================== SESSION DEFAULTS ========================
ss = st.session_state
defaults = dict(
    patient_id="123456789",
    dob=date(2025,10,1),
    gender="F",
    race_eth="Hispanic/Latino",
    weight_current=5.0,
    gest_weeks=0,
    gest_days=0,
)
for k,v in defaults.items():
    ss.setdefault(k, v)

# ======================== CONTROLS (Interactive) ========================
with st.expander("⚙️  Controls", expanded=False):
    tabs = st.tabs(["Visual Controls", "Patient Data"])
    with tabs[0]:
        c1, c2, c3 = st.columns([0.33, 0.37, 0.30])
        with c1:
            risk_pct = st.slider("Risk %", 0, 100, 70, 1)
        with c2:
            st.caption("Genetic Abnormalities (counts)")
            d = st.slider("Downs", 0, 30, 12, 1)
            t = st.slider("Turner", 0, 30, 10, 1)
            g = st.slider("DiGeorge", 0, 30, 16, 1)
            w = st.slider("Williams", 0, 30, 13, 1)
            counts = [d, t, g, w]
        with c3:
            st.caption("Shunt Size Distribution (raw numbers; auto-normalized)")
            s50 = st.number_input("5.0 mm", min_value=0.0, value=10.0, step=1.0)
            s40 = st.number_input("4.0 mm", min_value=0.0, value=18.0, step=1.0)
            s35 = st.number_input("3.5 mm", min_value=0.0, value=25.0, step=1.0)
            s30 = st.number_input("3.0 mm", min_value=0.0, value=47.0, step=1.0)
            raw_total = max(1.0, s50+s40+s35+s30)
            shunt_pcts = [round(100*s50/raw_total,1),
                          round(100*s40/raw_total,1),
                          round(100*s35/raw_total,1),
                          round(100*s30/raw_total,1)]
            st.caption(f"Normalized to 100% → {sum(shunt_pcts):.1f}%")
        st.caption("Highlight a complication (emphasizes stage)")
        hl = st.selectbox("", ["(none)","Cardiac Arrest","Reoperation Bleed","Sepsis","Chylothorax Intervention","Stroke","Sudden Hypoxemia"], index=0)

    with tabs[1]:
        st.subheader("Patient Header")
        a, b, c, dcol = st.columns([0.22, 0.20, 0.18, 0.40])
        with a:
            ss.patient_id = st.text_input("Patient ID", ss.patient_id)
            ss.gender     = st.selectbox("Gender", ["F","M","Intersex","Other"], index=["F","M","Intersex","Other"].index(ss.gender))
        with b:
            ss.dob        = st.date_input("DOB", value=ss.dob)
            ss.weight_current = st.number_input("Weight (kg)", min_value=0.0, value=float(ss.weight_current), step=0.1)
        with c:
            ss.race_eth   = st.text_input("Race/Ethnicity", ss.race_eth)
            ss.gest_weeks = st.number_input("Gest Age (weeks)", min_value=0, max_value=45, value=int(ss.gest_weeks))
            ss.gest_days  = st.number_input("Gest Age (days)",   min_value=0, max_value=6,  value=int(ss.gest_days))
        with dcol:
            st.info("Values here update the **top band** immediately. Use the Surgical section below for procedure-specific inputs. You can also sync current weight to 'Weight at Surgery'.")

        st.subheader("Surgical Inputs")
        left, right = st.columns(2)
        with left:
            date_of_surg = st.date_input("Date of Surgery", value=date(2025,10,18))
            age_months  = st.number_input("Age at Surgery (months)", min_value=0, max_value=60, value=0)
            age_days    = st.number_input("Age at Surgery (days)", min_value=0, max_value=31, value=0)
            sync_wt = st.checkbox("Use current Weight for 'Weight at Surgery'", value=True)
        with right:
            weight_kg   = st.number_input("Weight at Surgery (kg)", min_value=0.0, max_value=200.0,
                                          value=float(ss.weight_current) if sync_wt else 5.0, step=0.1)
            bmi_cat     = st.selectbox("Body Mass Index", ["Underweight","Normal","Overweight","Obese"], index=0)
            cpb_time    = st.number_input("CPB Time (minutes)", min_value=0, max_value=1000, value=0)
            tapvr       = st.selectbox("Concurrent TAPVR Repair", ["No","Yes"], index=0)

# ======================== LAYOUT ========================
nav, main = st.columns([0.20, 0.80], gap="small")

with nav:
    st.markdown('<div class="side"><h3>DASHBOARDS</h3><p>Patient Overview</p></div>', unsafe_allow_html=True)

with main:
    # ================= RISK SECTION AT TOP - MAIN ATTRACTION =================
    st.markdown(f"""
    <div class="risk-header">
      <div class="risk-title">⚠️ PATIENT RISK ASSESSMENT ⚠️</div>
      <div class="risk-display">
        <div>
          <div class="risk-percentage">{risk_pct}%</div>
          <div class="risk-label">RISK LEVEL</div>
        </div>
        <div class="risk-gauge-wrap">
          {semi_gauge_svg(risk_pct, compact=True)}
        </div>
        <div>
          <div class="risk-percentage" style="font-size:36px;">{risk_pct}</div>
          <div class="risk-label">/ 100</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Top band (uses session values) with premature icon ---
    gest_label = f"{int(ss.gest_weeks)} weeks {int(ss.gest_days)} days"
    st.markdown(f"""
    <div class="topband">
      <div class="premature-icon">👶</div>
      <div class="kvgrid">
        <div class="kv"><div class="label">PATIENT&nbsp;ID</div><div class="val muted">{ss.patient_id}</div></div>
        <div class="kv"><div class="label">DOB</div><div class="val muted">{ss.dob.strftime("%m/%d/%Y")}</div></div>
        <div class="kv"><div class="label">GENDER</div><div class="val muted">{ss.gender}</div></div>
        <div class="kv"><div class="label">RACE/ETHNICITY</div><div class="val muted">{ss.race_eth}</div></div>
        <div class="kv"><div class="label">WEIGHT</div><div class="val muted">{ss.weight_current:.1f} kg</div></div>
        <div class="kv"><div class="label">GEST&nbsp;AGE</div><div class="val muted">{gest_label}</div></div>
        <div class="baby">👶</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: left text (dynamic from inputs), middle bars, right removed (risk moved to top)
    c1, c2 = st.columns([0.60, 0.40], gap="large")

    with c1:
        st.markdown('<div class="h2">FUNDAMENTAL&nbsp;DIAGNOSIS</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">short summary of diagnosis</div>', unsafe_allow_html=True)

        st.markdown('<div class="h2" style="margin-top:10px;">SURGICAL&nbsp;PROCEDURE</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="muted">Systemic-to-Pulmonary Shunt Placement</div>
        <div style="margin-top:6px; font-size:13px;">
          <b>DATE OF SURG:</b> {date_of_surg.strftime("%m/%d/%Y")}<br>
          <b>AGE AT SURGERY:</b> {age_months} months {age_days} days<br>
          <b>WEIGHT AT SURGERY:</b> {weight_kg:.1f} kg<br>
          <b>BODY MASS INDEX:</b> {bmi_cat}<br>
          <b>CPB TIME:</b> {cpb_time} minutes<br>
          <b>CONCURRENT TAPVR REPAIR:</b> {tapvr}
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="h2">GENETIC&nbsp;ABNORMALITIES</div>', unsafe_allow_html=True)
        st.markdown(bar_svg([d,t,g,w]), unsafe_allow_html=True)

    st.markdown("<hr style='border:none;height:8px;background:transparent;'>", unsafe_allow_html=True)

    # Row 2: flow (two rows, steps 1..6) + donut aligned right + pill
    c4, c5 = st.columns([0.58, 0.42], gap="large")

    with c4:
        st.markdown('<div class="h3">POST&nbsp;OPERATIVE&nbsp;COMPLICATIONS (STEPS&nbsp;1–6)</div>', unsafe_allow_html=True)
        def klass(name): return "stage active" if st.session_state.get('hl', None) == name else ("stage active" if False else "stage")

        # we still have a separate selector above; highlight logic retained
        def act(name): 
            return "stage active" if name == st.session_state.get('hl_sel', '') else "stage"

        # Row 1: Steps 1–3
        st.markdown(f"""
        <div class="flowgrid">
          <div><div class="stepbadge">1</div><div class="stage">Cardiac<br>Arrest</div></div>
          <div class="connector"></div>
          <div><div class="stepbadge">2</div><div class="stage">Reoperation<br>Bleed</div></div>
          <div class="connector"></div>
          <div><div class="stepbadge">3</div><div class="stage">Sepsis</div></div>
        </div>
        """, unsafe_allow_html=True)
        # Row 2: Steps 4–6
        st.markdown(f"""
        <div class="flowgrid" style="margin-top:6px;">
          <div><div class="stepbadge">4</div><div class="stage">Chylothorax<br>Intervention</div></div>
          <div class="connector"></div>
          <div><div class="stepbadge">5</div><div class="stage">Stroke</div></div>
          <div class="connector"></div>
          <div><div class="stepbadge">6</div><div class="stage">Sudden<br>Hypoxemia</div></div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="h2" style="text-align:center;">SHUNT&nbsp;SIZE</div>', unsafe_allow_html=True)
        segments = [("5.0 mm", shunt_pcts[0], "var(--donut1)"),
                    ("4.0 mm", shunt_pcts[1], "var(--donut2)"),
                    ("3.5 mm", shunt_pcts[2], "var(--donut3)"),
                    ("3.0 mm", shunt_pcts[3], "var(--donut4)")]
        st.markdown(f'<div class="donutwrap">{donut_svg(segments)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="h2" style="margin-top:8px; text-align:center;">SHUNT:WEIGHT</div>', unsafe_allow_html=True)
        st.markdown('<div class="pillbar"><span class="chip">PATIENT XYZ</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="pillcaption">3.5 MM: 5 KG</div>', unsafe_allow_html=True)
