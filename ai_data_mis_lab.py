"""
AI, Gen-AI & Data Analytics/MIS Lab
Day 1 Companion App — Sessions S1 & S2
Executive Development Program (EDP) for Scale IV Executives — Canara Bank
Built for IIM Tiruchirappalli, Department of Finance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ============================================================
# PAGE CONFIG & THEME (consistent with Zonal Head's Dilemma app)
# ============================================================
st.set_page_config(page_title="AI & Data Analytics Lab | EDP Day 1", page_icon="📊", layout="wide")

PRIMARY = "#0B3D91"
ACCENT = "#D4A017"
GOOD = "#1E7B34"
WARN = "#B54708"
BAD = "#B3261E"

st.markdown(f"""
<style>
.main-title {{ color:{PRIMARY}; font-size:2.0rem; font-weight:800; margin-bottom:0; }}
.sub-title {{ color:{ACCENT}; font-size:1.0rem; font-weight:600; margin-top:0; }}
.info-box {{ background-color:#F4F6FB; border-left:6px solid {PRIMARY}; padding:1rem 1.2rem;
             border-radius:6px; margin-bottom:0.8rem; }}
.tier-low {{ background-color:#E9F6EC; border-left:6px solid {GOOD}; padding:0.9rem 1.1rem; border-radius:6px; }}
.tier-med {{ background-color:#FDF3E7; border-left:6px solid {WARN}; padding:0.9rem 1.1rem; border-radius:6px; }}
.tier-high {{ background-color:#FBEAEA; border-left:6px solid {BAD}; padding:0.9rem 1.1rem; border-radius:6px; }}
.section-header {{ background-color:{PRIMARY}; color:white; padding:0.5rem 0.9rem; border-radius:6px;
                    font-weight:700; font-size:1.05rem; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">AI &amp; Data Analytics Lab</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Day 1 Companion · Session 1 (AI &amp; Gen-AI in Banking) '
            '+ Session 2 (Data Analytics &amp; MIS)</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SESSION STATE
# ============================================================
def init_state():
    defaults = {
        "participant_name": "",
        "ai_answers": {"decision": None, "sensitive": None, "customer_facing": None, "explainable": None},
        "ai_tier_result": None,
        "s1_quiz_answers": {},
        "s1_quiz_score": None,
        "s2_quiz_answers": {},
        "s2_quiz_score": None,
        "mis_escalation_choice": [],
        "mis_escalation_rationale": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

with st.sidebar:
    st.markdown("### Participant")
    st.session_state.participant_name = st.text_input("Name", value=st.session_state.participant_name)
    st.markdown("---")
    st.caption("This app pairs with Sessions S1 (AI & Gen-AI in Banking) and S2 (Data Analytics & MIS) "
               "of the Canara Bank EDP. Work through Learn → Hands-On → Knowledge Check for each session, "
               "then download your combined summary from the final tab.")

top_tab1, top_tab2, top_tab3 = st.tabs([
    "🤖 Session 1 — AI & Gen-AI in Banking",
    "📊 Session 2 — Data Analytics & MIS",
    "🧾 Your Summary",
])

# ============================================================
# SESSION 1 — AI & GEN-AI IN BANKING
# ============================================================
with top_tab1:
    s1_learn, s1_tool, s1_quiz = st.tabs(["📘 Learn", "🧪 Hands-On: AI Use-Case Risk Classifier", "✅ Knowledge Check"])

    # ---------------- LEARN ----------------
    with s1_learn:
        st.markdown('<div class="info-box"><b>Why this matters for a Scale IV executive:</b> '
                     'You do not need to build AI models — you need to know which use cases require '
                     'tighter human oversight, and be able to defend that judgement to auditors, '
                     'customers, and the Board.</div>', unsafe_allow_html=True)

        with st.expander("Where Gen-AI is already live in Indian banking", expanded=True):
            st.markdown("""
- **Customer service & virtual assistants** — conversational chatbots handling FAQs, balance queries,
  and basic transaction requests across major Indian retail banks.
- **Credit underwriting & scoring** — alternative-data and ML-based scoring for MSME and retail loans,
  increasingly layered with Gen-AI for document summarisation.
- **Fraud & AML detection** — pattern-recognition models flagging anomalous transactions in real time.
- **Collections & recovery** — Gen-AI drafting/prioritising outreach scripts for delinquent accounts.
- **Internal productivity** — Gen-AI drafting credit appraisal notes, summarising policy documents, and
  supporting RM/branch staff with first-draft communications for human review.

*Treat the specific vendor/product names you've seen in the market as illustrative — the governance
principles below apply regardless of which vendor or model is used.*
            """)

        with st.expander("Governance principles — the direction regulators are moving"):
            st.markdown("""
- **Proportional governance**: the greater the customer/financial impact of an AI-driven decision, the
  greater the required human oversight, testing, and audit trail — not a one-size-fits-all control.
- **Accountability cannot be outsourced**: if a vendor's model gives incorrect output to a customer, the
  bank — not the vendor — carries regulatory and reputational accountability.
- **Explainability**: for anything customer-facing or decision-driving, the bank must be able to explain
  *why* a given output was produced, in plain language, to a regulator or an aggrieved customer.
- **Data protection interlock**: any use of customer data to train, fine-tune, or prompt an AI system
  sits squarely inside your DPDP Act, 2023 obligations — consent and purpose limitation apply to AI
  pipelines exactly as they do to any other processing.
- **Human-in-the-loop for adverse decisions**: a customer should not receive a purely algorithmic
  rejection (loan, service) without a meaningful path to human review.
- India's regulatory guidance in this space (including RBI-appointed expert committee recommendations on
  responsible AI adoption in financial services) continues to evolve — treat today's principles as a
  floor, not a ceiling.
            """)

        with st.expander("Common failure modes to watch for"):
            st.markdown("""
- **Hallucination** — Gen-AI producing fluent, confident, but factually wrong output (e.g., misquoting
  a loan eligibility rule to a customer).
- **Silent bias drift** — a scoring model trained on historical data quietly perpetuating past lending
  bias against a demographic or geography.
- **Vendor black-box risk** — adopting a third-party model without contractual rights to audit,
  explain, or exit.
- **Shadow AI** — staff using unauthorised public Gen-AI tools with customer data, outside any
  bank-sanctioned control.
            """)

    # ---------------- HANDS-ON TOOL ----------------
    with s1_tool:
        st.markdown("#### AI Use-Case Risk Classifier")
        st.write("Answer four questions about a use case — either a preset example or your own — "
                 "to see its risk tier and the governance controls it should trigger.")

        presets = {
            "— Answer manually for a use case of your own —": None,
            "Gen-AI FAQ chatbot (balance/product queries only)": (False, False, True, True),
            "Gen-AI drafting internal credit appraisal notes (human RM finalises)": (False, True, False, True),
            "Automated credit scoring — final loan approval/denial, no human review": (True, True, True, True),
            "Fraud-detection model flagging transactions for human analyst review": (False, True, False, True),
            "Facial-recognition based KYC/onboarding": (True, True, True, True),
        }
        choice = st.selectbox("Load an example (optional):", list(presets.keys()))

        preset_vals = presets[choice]
        q_labels = [
            ("decision", "Does the AI directly make or majority-drive a financial decision affecting "
                         "the customer (e.g. loan approval/denial) without meaningful human review?"),
            ("sensitive", "Does it use sensitive personal/financial data (income, credit history, "
                          "biometric, health)?"),
            ("customer_facing", "Is the system customer-facing, or does it directly determine an "
                                 "outcome the customer experiences?"),
            ("explainable", "Is the underlying logic hard to explain in plain language to a customer "
                            "or auditor (e.g. deep learning / Gen-AI vs a simple rule)?"),
        ]

        answers = {}
        for i, (key, label) in enumerate(q_labels):
            default = preset_vals[i] if preset_vals else st.session_state.ai_answers.get(key)
            idx = 0 if default is None else (0 if default else 1)
            resp = st.radio(label, ["Yes", "No"], index=idx, key=f"ai_q_{key}_{choice}", horizontal=True)
            answers[key] = (resp == "Yes")

        st.session_state.ai_answers = answers

        if st.button("🔍 Classify Risk Tier", type="primary"):
            yes_count = sum(answers.values())
            if yes_count <= 1:
                tier, cls, controls = "LOW", "tier-low", [
                    "Periodic review of outputs (e.g. quarterly sampling)",
                    "Basic logging of inputs/outputs for traceability",
                    "Named internal owner for the use case",
                ]
            elif yes_count == 2:
                tier, cls, controls = "MEDIUM", "tier-med", [
                    "Human-in-the-loop required before any adverse customer outcome",
                    "Documented testing before deployment and after material updates",
                    "Periodic bias/fairness audit on affected customer segments",
                    "Clear customer disclosure that AI is involved",
                ]
            else:
                tier, cls, controls = "HIGH", "tier-high", [
                    "Mandatory human sign-off before any adverse or high-value decision reaches the customer",
                    "Formal explainability documentation, reviewable by audit/regulator",
                    "Board-level or senior risk-committee oversight of the use case",
                    "Documented DPDP Act, 2023 compliance review (consent, purpose limitation, data minimisation)",
                    "Vendor due diligence with contractual audit/exit rights, if third-party",
                    "Explicit customer disclosure and a clear human escalation path",
                ]
            st.session_state.ai_tier_result = {"tier": tier, "yes_count": yes_count, "controls": controls,
                                                 "use_case": choice}

        if st.session_state.ai_tier_result:
            r = st.session_state.ai_tier_result
            css_cls = {"LOW": "tier-low", "MEDIUM": "tier-med", "HIGH": "tier-high"}[r["tier"]]
            st.markdown(f'<div class="{css_cls}"><b>Risk Tier: {r["tier"]}</b> '
                        f'({r["yes_count"]}/4 risk indicators triggered)</div>', unsafe_allow_html=True)
            st.markdown("**Recommended governance controls:**")
            for c in r["controls"]:
                st.write(f"- {c}")

    # ---------------- QUIZ ----------------
    with s1_quiz:
        st.markdown("#### Knowledge Check — AI & Gen-AI in Banking")
        s1_questions = [
            {
                "q": "Under emerging regulatory direction on AI in financial services, what principle "
                     "should govern deployment of a Gen-AI credit underwriting model?",
                "options": [
                    "Full automation without human review, to maximise speed",
                    "Proportional governance, with oversight scaled to the model's risk/impact",
                    "Deployment secrecy, to protect competitive advantage",
                    "No need for explainability if accuracy is high",
                ], "correct": 1,
                "explain": "Responsible-AI guidance emphasises proportionate governance — higher "
                           "customer/financial impact requires greater oversight, explainability, and audit.",
            },
            {
                "q": "A Gen-AI chatbot gives a customer incorrect information about loan eligibility, "
                     "leading to a complaint. Who is primarily accountable?",
                "options": [
                    "The AI vendor alone",
                    "No one — it was an automated system",
                    "The bank, since deployment and oversight accountability cannot be outsourced",
                    "The customer, for trusting the chatbot",
                ], "correct": 2,
                "explain": "Regulatory and reputational accountability for a deployed AI system sits with "
                           "the bank, regardless of whether a vendor built the underlying model.",
            },
            {
                "q": "Which of the following is a risk that is especially characteristic of Generative "
                     "AI (vs traditional rule-based systems)?",
                "options": [
                    "Hallucination — generating fluent but factually incorrect output",
                    "Slower processing speed in all cases",
                    "Higher hardware cost only",
                    "A strict requirement for physical, on-premise servers",
                ], "correct": 0,
                "explain": "Hallucination — confident, plausible, but wrong output — is a defining risk of "
                           "generative models and needs specific mitigation (human review, grounding).",
            },
            {
                "q": "Under the DPDP Act, 2023, what must a bank ensure before using customer data to "
                     "train or fine-tune an AI model?",
                "options": [
                    "Nothing — internal use is automatically exempt",
                    "A valid consent or other lawful basis, and purpose limitation",
                    "Only technical encryption; no consent is required",
                    "Model training is entirely outside the Act's scope",
                ], "correct": 1,
                "explain": "DPDP obligations (consent, purpose limitation, data minimisation) apply to AI "
                           "training pipelines exactly as they do to any other processing of personal data.",
            },
            {
                "q": "What is model explainability most important for in a banking AI context?",
                "options": [
                    "Making marketing materials look sophisticated",
                    "Enabling the bank to justify decisions to regulators, auditors, and customers",
                    "Reducing server costs",
                    "It isn't important if the model is accurate",
                ], "correct": 1,
                "explain": "A bank must be able to explain, in plain language, why an AI system produced "
                           "a given output — to a regulator during audit, or to an aggrieved customer.",
            },
        ]

        s1_answers = st.session_state.s1_quiz_answers
        for qi, item in enumerate(s1_questions):
            st.markdown(f"**Q{qi+1}. {item['q']}**")
            sel = st.radio("Choose one:", item["options"], index=s1_answers.get(qi, {}).get("idx", 0),
                           key=f"s1q_{qi}", label_visibility="collapsed")
            s1_answers[qi] = {"idx": item["options"].index(sel)}
            st.markdown("---")
        st.session_state.s1_quiz_answers = s1_answers

        if st.button("✅ Submit Session 1 Knowledge Check", type="primary"):
            score = sum(1 for qi, item in enumerate(s1_questions)
                        if s1_answers[qi]["idx"] == item["correct"])
            st.session_state.s1_quiz_score = (score, len(s1_questions))
            st.success(f"Score: {score}/{len(s1_questions)}")
            for qi, item in enumerate(s1_questions):
                correct = s1_answers[qi]["idx"] == item["correct"]
                icon = "✅" if correct else "❌"
                st.write(f"{icon} **Q{qi+1}** — Correct answer: *{item['options'][item['correct']]}*")
                st.caption(item["explain"])

# ============================================================
# SESSION 2 — DATA ANALYTICS & MIS
# ============================================================
with top_tab2:
    s2_learn, s2_tool, s2_quiz = st.tabs(["📘 Learn", "🧪 Hands-On: Zonal MIS Dashboard Simulator", "✅ Knowledge Check"])

    # ---------------- LEARN ----------------
    with s2_learn:
        st.markdown('<div class="info-box"><b>Why this matters for a Scale IV executive:</b> '
                     'MIS is only useful if it changes what you decide. This session is about reading '
                     'KPI patterns fast enough to escalate before a small issue becomes a large one.</div>',
                    unsafe_allow_html=True)

        with st.expander("Core KPIs a Zonal/Branch MIS should surface", expanded=True):
            st.markdown("""
| KPI | What it signals |
|---|---|
| **Gross NPA %** | Asset quality stress |
| **CASA Ratio %** | Low-cost deposit mix / funding cost pressure |
| **Credit-Deposit (CD) Ratio %** | Liquidity and balance-sheet stretch |
| **Cost-to-Income %** | Operating efficiency |
| **Digital Transaction Share %** | Channel migration / customer stickiness |
| **Complaint TAT (days)** | Service quality and escalation risk |
            """)

        with st.expander("Descriptive → Diagnostic → Predictive → Prescriptive analytics"):
            st.markdown("""
- **Descriptive** — *What happened?* (a dashboard showing last quarter's NPA%)
- **Diagnostic** — *Why did it happen?* (drilling into which segment/branch/product drove the NPA rise)
- **Predictive** — *What's likely to happen?* (forecasting which accounts are likely to slip into NPA)
- **Prescriptive** — *What should we do about it?* (recommended interventions, ranked by expected impact)

Most bank MIS today is strong on descriptive, weaker on diagnostic, and only beginning to build
predictive/prescriptive capability. As a Zonal Head, your job is to push past the descriptive layer
yourself when a dashboard alone doesn't explain *why*.
            """)

        with st.expander("What makes a dashboard 'decision-grade'"):
            st.markdown("""
- Thresholds and triggers that are pre-agreed, not judged fresh each time (so escalation isn't a matter
  of individual mood or memory).
- Trend visibility (3-4 quarters), not just a single snapshot — a bad number that's improving reads very
  differently from a bad number that's worsening.
- A named owner and an expected action for every red flag, not just a colour on a screen.
            """)

    # ---------------- HANDS-ON TOOL: MIS DASHBOARD SIMULATOR ----------------
    with s2_tool:
        st.markdown("#### Zonal MIS Dashboard Simulator — Trichy Zone (Illustrative Data)")
        st.caption("All branch names and figures below are fictional/synthetic, for training purposes only.")

        branches = ["Trichy Main", "Srirangam", "Thanjavur", "Karur", "Pudukkottai",
                    "Ariyalur", "Perambalur", "Musiri", "Lalgudi", "Manapparai"]
        quarters = ["Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26"]

        # Deterministic synthetic dataset
        import random
        random.seed(42)
        rows = []
        base_profile = {
            "Trichy Main": (2.1, 42, 78, 46, 52, 4),
            "Srirangam": (3.8, 35, 92, 51, 34, 9),
            "Thanjavur": (2.9, 39, 81, 48, 41, 5),
            "Karur": (4.6, 31, 96, 58, 27, 11),
            "Pudukkottai": (2.3, 44, 74, 44, 55, 3),
            "Ariyalur": (5.1, 28, 98, 61, 22, 13),
            "Perambalur": (3.1, 37, 85, 49, 38, 6),
            "Musiri": (2.6, 41, 79, 45, 47, 4),
            "Lalgudi": (4.2, 33, 91, 55, 29, 10),
            "Manapparai": (2.4, 43, 76, 45, 50, 4),
        }
        for b in branches:
            npa0, casa0, cd0, ci0, dig0, tat0 = base_profile[b]
            for qi, q in enumerate(quarters):
                drift = (qi - 1.5) * random.uniform(0.05, 0.25)
                rows.append({
                    "Branch": b, "Quarter": q,
                    "Gross NPA %": round(max(0.5, npa0 + drift * 1.3), 1),
                    "CASA %": round(max(15, casa0 - drift * 2.0), 1),
                    "CD Ratio %": round(min(105, cd0 + drift * 2.2), 1),
                    "Cost-to-Income %": round(min(70, ci0 + drift * 1.5), 1),
                    "Digital Txn Share %": round(max(10, dig0 - drift * 1.8), 1),
                    "Complaint TAT (days)": round(max(1, tat0 + drift * 0.8), 1),
                })
        df = pd.DataFrame(rows)

        THRESH = {
            "Gross NPA %": (">", 4.0),
            "CD Ratio %": ("range", 60, 90),
            "Cost-to-Income %": (">", 55.0),
            "Digital Txn Share %": ("<", 30.0),
            "Complaint TAT (days)": (">", 7.0),
        }

        def flag_count(row):
            n = 0
            if row["Gross NPA %"] > THRESH["Gross NPA %"][1]:
                n += 1
            if not (THRESH["CD Ratio %"][1] <= row["CD Ratio %"] <= THRESH["CD Ratio %"][2]):
                n += 1
            if row["Cost-to-Income %"] > THRESH["Cost-to-Income %"][1]:
                n += 1
            if row["Digital Txn Share %"] < THRESH["Digital Txn Share %"][1]:
                n += 1
            if row["Complaint TAT (days)"] > THRESH["Complaint TAT (days)"][1]:
                n += 1
            return n

        df["Red Flags"] = df.apply(flag_count, axis=1)

        sel_quarter = st.selectbox("Select quarter:", quarters, index=len(quarters) - 1)
        snap = df[df["Quarter"] == sel_quarter].sort_values("Red Flags", ascending=False).reset_index(drop=True)

        def highlight_flags(val):
            if isinstance(val, (int, float)) and val >= 3:
                return f"background-color:{BAD}22"
            elif isinstance(val, (int, float)) and val == 2:
                return f"background-color:{WARN}22"
            return ""

        st.markdown(f"**Snapshot — {sel_quarter}** (sorted by Red Flags, high to low)")
        st.dataframe(
            snap.drop(columns=["Quarter"]).style.applymap(highlight_flags, subset=["Red Flags"]),
            use_container_width=True, hide_index=True,
        )

        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            trend_kpi = st.selectbox("Trend view — choose a KPI:",
                                      ["Gross NPA %", "CASA %", "CD Ratio %", "Cost-to-Income %",
                                       "Digital Txn Share %", "Complaint TAT (days)"])
            trend_branches = st.multiselect("Branches to compare:", branches, default=branches[:4])
        with col2:
            fig = px.line(df[df["Branch"].isin(trend_branches)], x="Quarter", y=trend_kpi,
                          color="Branch", markers=True, height=380)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Your Decision — Which branches would you escalate this quarter?")
        st.session_state.mis_escalation_choice = st.multiselect(
            "Select branches to escalate for deeper review:", branches,
            default=st.session_state.mis_escalation_choice,
        )
        st.session_state.mis_escalation_rationale = st.text_area(
            "Rationale (1-2 sentences):", value=st.session_state.mis_escalation_rationale, height=90,
        )

        if st.button("🔍 Compare against auto-flagged branches", type="primary"):
            auto_flagged = snap[snap["Red Flags"] >= 2]["Branch"].tolist()
            st.markdown(f"**System auto-flag (≥2 red flags in {sel_quarter}):** "
                        f"{', '.join(auto_flagged) if auto_flagged else 'None'}")
            missed = [b for b in auto_flagged if b not in st.session_state.mis_escalation_choice]
            extra = [b for b in st.session_state.mis_escalation_choice if b not in auto_flagged]
            if missed:
                st.warning(f"You may have missed: {', '.join(missed)}")
            if extra:
                st.info(f"You flagged (not auto-flagged, may be a judgement call worth discussing): "
                        f"{', '.join(extra)}")
            if not missed and not extra:
                st.success("Your escalation list matches the system's auto-flagged branches.")

    # ---------------- QUIZ ----------------
    with s2_quiz:
        st.markdown("#### Knowledge Check — Data Analytics & MIS")
        s2_questions = [
            {
                "q": "A branch shows CASA ratio declining over 3 quarters while its CD ratio rises above "
                     "95%. What should a Zonal Head's MIS-driven first response be?",
                "options": [
                    "Ignore it — likely a seasonal fluctuation",
                    "Flag the branch for deeper diagnostic review — the combined trend signals "
                    "potential funding/liquidity stress",
                    "Immediately shut the branch",
                    "Increase lending further to boost income",
                ], "correct": 1,
                "explain": "A rising CD ratio alongside falling CASA is a classic funding-stress "
                           "signature that warrants diagnostic follow-up, not a snapshot judgement.",
            },
            {
                "q": "Descriptive analytics primarily answers which question?",
                "options": ["What happened?", "Why did it happen?", "What will happen next?",
                            "What should we do about it?"], "correct": 0,
                "explain": "Descriptive analytics reports what happened; diagnostic explains why, "
                           "predictive forecasts what's next, and prescriptive recommends action.",
            },
            {
                "q": "Which KPI is the most direct indicator of asset-quality stress in a branch/zone?",
                "options": ["CASA ratio", "Gross NPA %", "Digital transaction share",
                            "Complaint TAT"], "correct": 1,
                "explain": "Gross NPA % directly measures the proportion of loans turning delinquent — "
                           "the clearest asset-quality signal of the set.",
            },
            {
                "q": "What makes an MIS dashboard 'decision-grade' rather than merely descriptive?",
                "options": ["More colours and charts", "Pre-agreed thresholds/triggers tied to an "
                            "escalation protocol", "A larger file size", "A fixed weekly refresh "
                            "regardless of urgency"], "correct": 1,
                "explain": "Decision-grade MIS ties numbers to pre-agreed action thresholds so escalation "
                           "doesn't depend on who happens to be looking at the dashboard that day.",
            },
            {
                "q": "A Zonal Head notices digital transaction share is far below peer zones. Which "
                     "analytics approach helps determine the root cause?",
                "options": ["A purely descriptive dashboard (totals only)", "Diagnostic analytics — "
                            "drilling into segment/branch/demographic drivers behind the gap",
                            "Ignoring it since digital isn't a priority", "Predictive analytics only, "
                            "skipping diagnosis"], "correct": 1,
                "explain": "Root-cause investigation of an existing gap is a diagnostic task — "
                           "predictive analytics is for forecasting future states, not explaining today's.",
            },
        ]

        s2_answers = st.session_state.s2_quiz_answers
        for qi, item in enumerate(s2_questions):
            st.markdown(f"**Q{qi+1}. {item['q']}**")
            sel = st.radio("Choose one:", item["options"], index=s2_answers.get(qi, {}).get("idx", 0),
                           key=f"s2q_{qi}", label_visibility="collapsed")
            s2_answers[qi] = {"idx": item["options"].index(sel)}
            st.markdown("---")
        st.session_state.s2_quiz_answers = s2_answers

        if st.button("✅ Submit Session 2 Knowledge Check", type="primary"):
            score = sum(1 for qi, item in enumerate(s2_questions)
                        if s2_answers[qi]["idx"] == item["correct"])
            st.session_state.s2_quiz_score = (score, len(s2_questions))
            st.success(f"Score: {score}/{len(s2_questions)}")
            for qi, item in enumerate(s2_questions):
                correct = s2_answers[qi]["idx"] == item["correct"]
                icon = "✅" if correct else "❌"
                st.write(f"{icon} **Q{qi+1}** — Correct answer: *{item['options'][item['correct']]}*")
                st.caption(item["explain"])

# ============================================================
# SUMMARY TAB
# ============================================================
with top_tab3:
    st.markdown("#### Your Combined Session Summary")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Session 1 — AI & Gen-AI**")
        if st.session_state.s1_quiz_score:
            s, t = st.session_state.s1_quiz_score
            st.progress(s / t, text=f"Knowledge Check: {s}/{t}")
        else:
            st.caption("Knowledge Check not yet submitted.")
        if st.session_state.ai_tier_result:
            st.write(f"AI Risk Classifier result: **{st.session_state.ai_tier_result['tier']}** "
                     f"tier, for use case: *{st.session_state.ai_tier_result['use_case']}*")
        else:
            st.caption("AI Risk Classifier not yet used.")

    with c2:
        st.markdown("**Session 2 — Data Analytics & MIS**")
        if st.session_state.s2_quiz_score:
            s, t = st.session_state.s2_quiz_score
            st.progress(s / t, text=f"Knowledge Check: {s}/{t}")
        else:
            st.caption("Knowledge Check not yet submitted.")
        if st.session_state.mis_escalation_choice:
            st.write(f"Branches escalated: {', '.join(st.session_state.mis_escalation_choice)}")
        else:
            st.caption("MIS escalation decision not yet made.")

    st.markdown("---")
    lines = [
        "AI & DATA ANALYTICS LAB — SESSION SUMMARY",
        f"Participant: {st.session_state.participant_name or 'Unnamed'}",
        f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        "=" * 55, "",
        "SESSION 1 — AI & GEN-AI IN BANKING", "-" * 40,
    ]
    if st.session_state.s1_quiz_score:
        s, t = st.session_state.s1_quiz_score
        lines.append(f"Knowledge Check score: {s}/{t}")
    if st.session_state.ai_tier_result:
        r = st.session_state.ai_tier_result
        lines.append(f"Use case assessed: {r['use_case']}")
        lines.append(f"Risk tier: {r['tier']} ({r['yes_count']}/4 indicators)")
        lines.append("Recommended controls:")
        for c in r["controls"]:
            lines.append(f"  - {c}")

    lines += ["", "SESSION 2 — DATA ANALYTICS & MIS", "-" * 40]
    if st.session_state.s2_quiz_score:
        s, t = st.session_state.s2_quiz_score
        lines.append(f"Knowledge Check score: {s}/{t}")
    if st.session_state.mis_escalation_choice:
        lines.append(f"Branches escalated: {', '.join(st.session_state.mis_escalation_choice)}")
        lines.append(f"Rationale: {st.session_state.mis_escalation_rationale}")

    report_text = "\n".join(lines)
    st.download_button(
        "⬇️ Download Summary (.txt)",
        data=io.BytesIO(report_text.encode("utf-8")),
        file_name=f"ai_data_mis_summary_{(st.session_state.participant_name or 'participant').replace(' ', '_')}.txt",
        mime="text/plain",
    )

st.markdown("---")
st.caption("EDP Day 1 Companion App · Sessions S1 & S2 · IIM Tiruchirappalli, Department of Finance")
