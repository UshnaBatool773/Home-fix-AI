import os
import json
import uuid
from datetime import datetime, date
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ============================================================
# HomeFix AI - Single-file Streamlit MVP
# The app automatically creates its demo provider/request data.
# Providers are fictional DEMO DATA and must not be presented
# as real businesses.
# ============================================================

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PROVIDERS_FILE = DATA_DIR / "providers.csv"
REQUESTS_FILE = DATA_DIR / "requests.csv"

SERVICE_CATEGORIES = [
    "AC Technician",
    "Plumber",
    "Electrician",
    "Appliance Repair",
    "Home Cleaner",
    "Painter",
    "Carpenter",
    "Locksmith",
]

REQUEST_STATUSES = ["Pending", "Confirmed", "Completed", "Cancelled"]

DEMO_PROVIDERS = [
    ["P001", "Ahmed Cooling Services", "AC Technician", "Lahore", 4.8, 800, 3500, "Today", "0300XXXXXXX", 6, "AC installation, cooling problems, leakage and maintenance."],
    ["P002", "CoolCare Experts", "AC Technician", "Lahore", 4.6, 1000, 4000, "Today", "0311XXXXXXX", 8, "Residential AC repair and seasonal maintenance."],
    ["P003", "Punjab AC Solutions", "AC Technician", "Faisalabad", 4.7, 900, 3200, "Tomorrow", "0322XXXXXXX", 7, "AC troubleshooting, servicing and water leakage support."],
    ["P004", "City Pipe Masters", "Plumber", "Lahore", 4.9, 700, 2800, "Today", "0333XXXXXXX", 9, "Leakage, blocked sinks, taps, pipes and bathroom plumbing."],
    ["P005", "Rapid Plumbing Care", "Plumber", "Faisalabad", 4.5, 600, 2500, "Today", "0344XXXXXXX", 5, "General household plumbing and emergency maintenance."],
    ["P006", "HomeFlow Plumbers", "Plumber", "Lahore", 4.7, 800, 3000, "Tomorrow", "0355XXXXXXX", 7, "Kitchen, bathroom and water-line repair services."],
    ["P007", "BrightLine Electric", "Electrician", "Lahore", 4.9, 700, 3000, "Today", "0301XXXXXXX", 10, "Lighting, switches, sockets, fans and household electrical work."],
    ["P008", "SafeSpark Electricians", "Electrician", "Faisalabad", 4.6, 800, 3200, "Today", "0312XXXXXXX", 6, "Residential electrical troubleshooting and installation."],
    ["P009", "PowerFix Home Electric", "Electrician", "Lahore", 4.7, 900, 3500, "Tomorrow", "0323XXXXXXX", 8, "Electrical fault finding, fixtures and wiring maintenance."],
    ["P010", "Appliance Aid", "Appliance Repair", "Lahore", 4.8, 1000, 4500, "Today", "0334XXXXXXX", 9, "Washing machine, refrigerator and microwave repair."],
    ["P011", "Home Appliance Clinic", "Appliance Repair", "Faisalabad", 4.5, 900, 4000, "Tomorrow", "0345XXXXXXX", 6, "General household appliance diagnostics and repair."],
    ["P012", "Quick Appliance Fix", "Appliance Repair", "Lahore", 4.6, 800, 3800, "Today", "0356XXXXXXX", 7, "Washing machine, fridge and small appliance support."],
    ["P013", "Sparkle Home Cleaners", "Home Cleaner", "Lahore", 4.9, 1200, 3000, "Today", "0306XXXXXXX", 5, "Home deep cleaning, kitchen and bathroom cleaning."],
    ["P014", "FreshNest Cleaning", "Home Cleaner", "Faisalabad", 4.6, 1000, 2800, "Tomorrow", "0317XXXXXXX", 4, "Regular and deep home cleaning packages."],
    ["P015", "CleanSpace Helpers", "Home Cleaner", "Lahore", 4.7, 900, 2600, "Today", "0328XXXXXXX", 6, "Residential cleaning and move-in/move-out cleaning."],
    ["P016", "ColorCraft Painters", "Painter", "Lahore", 4.8, 2500, 12000, "Today", "0339XXXXXXX", 11, "Interior wall painting and room refresh projects."],
    ["P017", "Punjab Paint Pros", "Painter", "Faisalabad", 4.5, 2200, 10000, "Tomorrow", "0340XXXXXXX", 8, "Residential painting and surface preparation."],
    ["P018", "Urban Wall Finishers", "Painter", "Lahore", 4.7, 2800, 14000, "Today", "0351XXXXXXX", 9, "Interior and exterior home painting."],
    ["P019", "WoodWorks Carpenter", "Carpenter", "Lahore", 4.9, 1000, 5000, "Today", "0307XXXXXXX", 12, "Furniture repair, doors, shelves and wooden fixtures."],
    ["P020", "CraftHome Carpentry", "Carpenter", "Faisalabad", 4.6, 900, 4500, "Tomorrow", "0318XXXXXXX", 7, "Custom wood repair and household carpentry."],
    ["P021", "Reliable Wood Fix", "Carpenter", "Lahore", 4.7, 1100, 5500, "Today", "0329XXXXXXX", 10, "Tables, cabinets, doors and general wood repairs."],
    ["P022", "SecureLock Services", "Locksmith", "Lahore", 4.9, 800, 3000, "Today", "0330XXXXXXX", 8, "Door lock repair, replacement and key-related services."],
    ["P023", "FastKey Locksmiths", "Locksmith", "Faisalabad", 4.6, 700, 2800, "Today", "0341XXXXXXX", 6, "Residential lock repair and replacement."],
    ["P024", "DoorSafe Experts", "Locksmith", "Lahore", 4.7, 900, 3200, "Tomorrow", "0352XXXXXXX", 9, "Door locks, handles and home access hardware."],
    ["P025", "Lahore Comfort AC", "AC Technician", "Lahore", 4.7, 900, 3800, "Tomorrow", "0308XXXXXXX", 7, "Split AC repair, cleaning and cooling diagnostics."],
    ["P026", "LeakLess Plumbing", "Plumber", "Lahore", 4.8, 750, 2900, "Today", "0319XXXXXXX", 8, "Leak detection, drains, taps and household pipes."],
    ["P027", "CircuitCare", "Electrician", "Lahore", 4.8, 800, 3300, "Today", "0320XXXXXXX", 9, "Safe residential electrical maintenance and fixtures."],
    ["P028", "FixRight Appliances", "Appliance Repair", "Lahore", 4.7, 900, 4200, "Tomorrow", "0331XXXXXXX", 8, "Home appliance inspection and repair."],
    ["P029", "NeatHome Services", "Home Cleaner", "Lahore", 4.8, 1000, 3200, "Tomorrow", "0342XXXXXXX", 5, "Residential cleaning for kitchens, rooms and common areas."],
    ["P030", "MasterFinish Painters", "Painter", "Lahore", 4.9, 3000, 15000, "Tomorrow", "0353XXXXXXX", 13, "Professional residential painting and finishing."],
]

KNOWLEDGE_BASE = [
    {
        "topic": "AC Technician",
        "text": "AC technicians handle cooling problems, water leakage, unusual AC behavior, servicing, installation and maintenance. Customers should avoid opening electrical components themselves."
    },
    {
        "topic": "Plumber",
        "text": "Plumbers handle leaking pipes, blocked sinks, taps, drains, water lines and common bathroom or kitchen plumbing issues."
    },
    {
        "topic": "Electrician",
        "text": "Electricians handle lights, switches, sockets, fans, household electrical faults and fixtures. Exposed wiring, sparks, burning smells and electrical shocks should be treated as safety hazards."
    },
    {
        "topic": "Appliance Repair",
        "text": "Appliance repair professionals handle washing machines, refrigerators, microwaves and other household appliance faults."
    },
    {
        "topic": "Home Cleaner",
        "text": "Home cleaners provide regular, deep, kitchen, bathroom and move-in or move-out cleaning services."
    },
    {
        "topic": "Painter",
        "text": "Painters handle interior and exterior residential painting, wall preparation and finishing."
    },
    {
        "topic": "Carpenter",
        "text": "Carpenters handle furniture, doors, cabinets, shelves and other wooden household repairs."
    },
    {
        "topic": "Locksmith",
        "text": "Locksmiths handle broken or damaged door locks, lock replacement, handles and residential access hardware."
    },
    {
        "topic": "Policy",
        "text": "Provider information in this student demo comes from the fictional provider CSV. Prices and availability are estimates in demo data. A request is Pending until the application changes its status. This prototype does not process payments."
    },
    {
        "topic": "Safety",
        "text": "HomeFix AI is not a certified technician. For gas leaks, fire, serious electrical danger or another immediate emergency, leave the dangerous area if safe to do so and contact the appropriate local emergency service or qualified professional. Do not attempt dangerous repairs."
    },
]

def ensure_data_files():
    if not PROVIDERS_FILE.exists():
        columns = [
            "provider_id", "provider_name", "service_category", "area",
            "rating", "price_min", "price_max", "availability", "phone",
            "experience_years", "description"
        ]
        pd.DataFrame(DEMO_PROVIDERS, columns=columns).to_csv(PROVIDERS_FILE, index=False)

    if not REQUESTS_FILE.exists():
        columns = [
            "request_id", "created_at", "customer_name", "phone", "area",
            "address", "problem_description", "service_category",
            "provider_id", "provider_name", "preferred_date", "preferred_time",
            "additional_notes", "status", "estimated_price"
        ]
        pd.DataFrame(columns=columns).to_csv(REQUESTS_FILE, index=False)

def load_providers():
    ensure_data_files()
    try:
        return pd.read_csv(PROVIDERS_FILE)
    except Exception:
        return pd.DataFrame(DEMO_PROVIDERS, columns=[
            "provider_id", "provider_name", "service_category", "area",
            "rating", "price_min", "price_max", "availability", "phone",
            "experience_years", "description"
        ])

def load_requests():
    ensure_data_files()
    try:
        return pd.read_csv(REQUESTS_FILE)
    except Exception:
        return pd.DataFrame()

def save_request(row):
    df = load_requests()
    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(REQUESTS_FILE, index=False)

def retrieve_knowledge(query, top_k=3):
    """Simple transparent RAG: keyword-overlap retrieval over the local KB."""
    words = set(
        word.lower().strip(".,!?;:()[]{}")
        for word in query.split()
        if len(word.strip(".,!?;:()[]{}")) > 2
    )
    scored = []
    for item in KNOWLEDGE_BASE:
        text_words = set(item["text"].lower().split())
        score = len(words.intersection(text_words))
        if item["topic"].lower() in query.lower():
            score += 3
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored[:top_k] if score > 0]

def get_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)

def classify_problem(problem):
    """Use Groq for NLU, but force the result into controlled categories."""
    fallback = {
        "service_category": "Plumber",
        "problem": problem,
        "object_device": "",
        "symptoms": "",
        "urgency": "Normal",
        "area": "",
        "preferred_date": "",
        "preferred_time": "",
        "needs_follow_up": False,
        "follow_up_question": "",
    }

    client = get_client()
    if client is None:
        return keyword_classify(problem)

    system_prompt = f"""
You are HomeFix AI, a home-service triage assistant.
Your job is to understand a user's home problem and select exactly ONE service
from this controlled list:
{json.dumps(SERVICE_CATEGORIES)}

Never invent a service category. Never invent provider names, prices, or availability.
Extract only information actually present in the user's message.
If a useful detail is genuinely missing and would materially improve provider matching,
set needs_follow_up=true and ask ONE short question. Do not ask unnecessary questions.
Do not give repair instructions for dangerous work.

Return ONLY valid JSON with exactly these keys:
service_category, problem, object_device, symptoms, urgency, area,
preferred_date, preferred_time, needs_follow_up, follow_up_question

urgency must be one of: Normal, Urgent, Emergency.
For emergencies involving fire, gas leaks, serious electrical danger, or immediate danger,
use Emergency and give a short safety-focused follow-up.
"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": problem},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)

        if result.get("service_category") not in SERVICE_CATEGORIES:
            result["service_category"] = keyword_classify(problem)["service_category"]

        for key, value in fallback.items():
            result.setdefault(key, value)

        return result
    except Exception:
        return keyword_classify(problem)

def keyword_classify(problem):
    text = problem.lower()

    keyword_map = [
        ("AC Technician", ["ac", "air conditioner", "air conditioning", "cooling", "split unit"]),
        ("Plumber", ["pipe", "plumb", "sink", "tap", "faucet", "drain", "leak", "water"]),
        ("Electrician", ["electric", "electricity", "wiring", "wire", "socket", "switch", "light", "fan", "breaker"]),
        ("Appliance Repair", ["washing machine", "fridge", "refrigerator", "microwave", "oven", "appliance"]),
        ("Home Cleaner", ["clean", "cleaning", "dust", "deep clean"]),
        ("Painter", ["paint", "painting", "wall color", "walls"]),
        ("Carpenter", ["wood", "wooden", "table", "chair", "cabinet", "door", "shelf", "carpenter"]),
        ("Locksmith", ["lock", "locked", "key", "door lock", "locksmith"]),
    ]

    service = "Plumber"
    for category, keywords in keyword_map:
        if any(k in text for k in keywords):
            service = category
            break

    urgency = "Normal"
    if any(k in text for k in ["fire", "gas leak", "smoke", "spark", "exposed wire", "electric shock"]):
        urgency = "Emergency"
    elif any(k in text for k in ["urgent", "immediately", "asap", "emergency"]):
        urgency = "Urgent"

    return {
        "service_category": service,
        "problem": problem,
        "object_device": "",
        "symptoms": "",
        "urgency": urgency,
        "area": "",
        "preferred_date": "",
        "preferred_time": "",
        "needs_follow_up": False,
        "follow_up_question": "",
    }

def is_dangerous(problem):
    text = problem.lower()
    danger_terms = [
        "gas leak", "gas smell", "fire", "smoke", "exposed wire",
        "sparking wire", "electric shock", "electrical shock", "live wire",
        "burning smell", "short circuit"
    ]
    return any(term in text for term in danger_terms)

def match_providers(providers, service, area="", availability="Any", max_results=6):
    """Transparent scoring:
    - service match: 50 points
    - area match: 25 points
    - availability: 15 points
    - rating: up to 7 points
    - lower estimated price: up to 3 points

    Service is highest priority, followed by area, availability, rating and price.
    """
    df = providers.copy()
    if df.empty:
        return df

    df = df[df["service_category"].eq(service)].copy()
    if df.empty:
        return df

    area_clean = area.strip().lower()
    availability_clean = availability.strip().lower()

    scores = []
    for _, row in df.iterrows():
        score = 50

        if area_clean and area_clean != "any":
            if str(row["area"]).strip().lower() == area_clean:
                score += 25

        if availability_clean and availability_clean != "any":
            if str(row["availability"]).strip().lower() == availability_clean:
                score += 15

        score += float(row["rating"]) / 5 * 7

        price_min = float(row["price_min"])
        price_max = float(row["price_max"])
        price_bonus = max(0, 3 - (price_min / 5000))
        score += price_bonus

        scores.append(score)

    df["match_score"] = scores
    df = df.sort_values(["match_score", "rating"], ascending=[False, False])
    return df.head(max_results)

def money_range(row):
    return f"Rs. {int(row['price_min']):,} – {int(row['price_max']):,}"

def ask_ai_general(question):
    retrieved = retrieve_knowledge(question)
    context = "\n".join(
        f"- {item['topic']}: {item['text']}" for item in retrieved
    )

    client = get_client()
    if client is None:
        if retrieved:
            return "Based on the HomeFix AI knowledge base:\n\n" + "\n".join(
                f"• {item['text']}" for item in retrieved
            )
        return "Add your GROQ_API_KEY in the .env file to enable the AI assistant."

    system = f"""
You are HomeFix AI, a concise home-service assistant.
Use the retrieved local knowledge below when relevant.
Do not invent providers, prices, availability or company policies.
Do not give dangerous repair instructions.
If the user describes an emergency such as fire, gas leak, serious electrical
danger or immediate danger, prioritize safety and recommend appropriate emergency
or qualified professional help.
You are not a certified technician.

RETRIEVED KNOWLEDGE:
{context if context else "No directly relevant local knowledge was retrieved."}
"""
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"I couldn't reach the AI service right now. You can still use provider search and booking. ({type(exc).__name__})"

def render_provider_card(row, index):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(str(row["provider_name"]))
            st.write(f"**{row['service_category']}** • {row['area']}")
            st.write(str(row["description"]))
        with col2:
            st.metric("Rating", f"{float(row['rating']):.1f}/5")
            st.caption(f"Match score: {float(row['match_score']):.1f}")
        a, b, c = st.columns(3)
        a.write(f"**Price**\n{money_range(row)}")
        b.write(f"**Availability**\n{row['availability']}")
        c.write(f"**Experience**\n{int(row['experience_years'])} years")

        if st.button("Select Provider", key=f"provider_{row['provider_id']}_{index}", use_container_width=True):
            st.session_state.selected_provider = row.to_dict()
            st.session_state.page = "📅 My Service Request"
            st.rerun()

def home_page():
    st.title("🏠 HomeFix AI")
    st.markdown("### Tell us what's wrong. We'll help you find the right professional.")
    st.info("This is a student project using fictional DEMO DATA for service providers.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Services", "8")
    c2.metric("Demo Providers", "30")
    c3.metric("AI Matching", "✓")
    c4.metric("Booking Requests", len(load_requests()))

    st.markdown("#### Try an example")
    examples = [
        "My AC is leaking water and not cooling.",
        "My kitchen sink is blocked.",
        "My washing machine is leaking.",
        "I need an electrician.",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.assistant_prompt = example
            st.session_state.page = "💬 AI Assistant"
            st.rerun()

    st.markdown("#### Available services")
    cols = st.columns(4)
    icons = ["❄️", "🚰", "⚡", "🔧", "🧹", "🎨", "🪚", "🔐"]
    for i, service in enumerate(SERVICE_CATEGORIES):
        cols[i % 4].write(f"{icons[i]} **{service}**")

def assistant_page():
    st.title("💬 AI Assistant")
    st.caption("Describe your home problem in natural language.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    default_prompt = st.session_state.pop("assistant_prompt", "")
    prompt = st.chat_input("Example: My AC is leaking water and isn't cooling.")
    if default_prompt and not prompt:
        prompt = default_prompt

    if prompt:
        if not prompt.strip():
            st.warning("Please describe the problem.")
            return

        st.session_state.chat_history.append({"role": "user", "content": prompt})

        if is_dangerous(prompt):
            response = (
                "⚠️ **Safety first:** this may involve a dangerous home hazard. "
                "Do not attempt electrical, gas or fire-related repairs yourself. "
                "Move away from the hazard if it is safe to do so and contact the "
                "appropriate emergency service or a qualified professional."
            )
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            return

        with st.spinner("Understanding your problem..."):
            result = classify_problem(prompt)

        service = result["service_category"]
        area = result.get("area", "")

        response = f"**Recommended service:** {service}\n\n"
        response += f"I understood the problem as: **{result.get('problem', prompt)}**."

        if result.get("urgency") in ["Urgent", "Emergency"]:
            response += f"\n\n**Urgency:** {result['urgency']}"

        if result.get("needs_follow_up") and result.get("follow_up_question"):
            response += f"\n\n**Quick question:** {result['follow_up_question']}"

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.last_analysis = result

        providers = load_providers()
        matches = match_providers(providers, service, area=area)

        st.markdown("### Recommended professionals")
        if matches.empty:
            st.warning("No matching demo providers were found. Try another area or service.")
        else:
            for i, (_, row) in enumerate(matches.head(3).iterrows()):
                render_provider_card(row, i)

def find_professional_page():
    st.title("🔧 Find a Professional")
    providers = load_providers()

    c1, c2, c3 = st.columns(3)
    service = c1.selectbox("Service", SERVICE_CATEGORIES)
    areas = ["Any"] + sorted(providers["area"].dropna().unique().tolist())
    area = c2.selectbox("Area", areas)
    availability = c3.selectbox("Availability", ["Any", "Today", "Tomorrow"])

    matches = match_providers(
        providers,
        service,
        area=area,
        availability=availability,
        max_results=10,
    )

    st.caption(f"Showing up to 10 providers. Demo data only. Found {len(matches)} match(es).")

    if matches.empty:
        st.warning("No providers match these filters.")
    else:
        for i, (_, row) in enumerate(matches.iterrows()):
            render_provider_card(row, i)

def booking_page():
    st.title("📅 My Service Request")

    selected = st.session_state.get("selected_provider")
    if not selected:
        st.info("Select a provider first from the AI Assistant or Find a Professional page.")
        return

    st.success(
        f"Selected provider: **{selected['provider_name']}** — "
        f"{selected['service_category']} — {selected['area']}"
    )

    with st.form("booking_form"):
        c1, c2 = st.columns(2)
        customer_name = c1.text_input("Customer name *")
        phone = c2.text_input("Phone number *")

        c3, c4 = st.columns(2)
        area = c3.text_input("Area *", value=str(selected.get("area", "")))
        address = c4.text_input("Address *")

        problem = st.text_area(
            "Problem description *",
            value=st.session_state.get("last_analysis", {}).get("problem", "")
        )

        c5, c6 = st.columns(2)
        preferred_date = c5.date_input("Preferred date *", min_value=date.today())
        preferred_time = c6.selectbox(
            "Preferred time *",
            ["Morning (9 AM–12 PM)", "Afternoon (12 PM–4 PM)", "Evening (4 PM–8 PM)"]
        )

        additional_notes = st.text_area("Additional notes")
        submitted = st.form_submit_button("Submit Service Request", use_container_width=True)

    if submitted:
        required = [customer_name.strip(), phone.strip(), area.strip(), address.strip(), problem.strip()]
        if not all(required):
            st.error("Please fill all required fields.")
            return

        request_id = "HF-" + uuid.uuid4().hex[:8].upper()
        estimated_price = f"Rs. {int(selected['price_min']):,} – Rs. {int(selected['price_max']):,}"

        row = {
            "request_id": request_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": customer_name.strip(),
            "phone": phone.strip(),
            "area": area.strip(),
            "address": address.strip(),
            "problem_description": problem.strip(),
            "service_category": selected["service_category"],
            "provider_id": selected["provider_id"],
            "provider_name": selected["provider_name"],
            "preferred_date": preferred_date.isoformat(),
            "preferred_time": preferred_time,
            "additional_notes": additional_notes.strip(),
            "status": "Pending",
            "estimated_price": estimated_price,
        }

        save_request(row)
        st.session_state.last_request = row
        st.session_state.selected_provider = None

        st.balloons()
        st.success(f"Request submitted successfully. Request ID: **{request_id}**")
        st.info("Status: **Pending**. This demo does not automatically confirm appointments.")

def dashboard_page():
    st.title("📊 Dashboard")
    requests = load_requests()

    if requests.empty:
        st.info("No service requests have been submitted yet.")
        return

    total = len(requests)
    most_service = requests["service_category"].mode().iloc[0] if not requests["service_category"].mode().empty else "N/A"
    most_area = requests["area"].mode().iloc[0] if not requests["area"].mode().empty else "N/A"

    def price_mid(value):
        try:
            numbers = [int(x.replace(",", "")) for x in value.replace("Rs.", "").replace("–", "-").split("-") if x.strip().replace(",", "").isdigit()]
            return sum(numbers) / len(numbers) if numbers else 0
        except Exception:
            return 0

    avg_price = requests["estimated_price"].apply(price_mid).mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Requests", total)
    c2.metric("Most Requested Service", most_service)
    c3.metric("Most Requested Area", most_area)
    c4.metric("Average Estimated Price", f"Rs. {avg_price:,.0f}")

    st.markdown("### Requests by Service")
    service_counts = requests["service_category"].value_counts()
    st.bar_chart(service_counts)

    st.markdown("### Request Status Distribution")
    status_counts = requests["status"].value_counts()
    st.bar_chart(status_counts)

    st.markdown("### Submitted Requests")
    display_cols = [
        "request_id", "customer_name", "service_category",
        "provider_name", "area", "preferred_date",
        "preferred_time", "status"
    ]
    st.dataframe(requests[display_cols], use_container_width=True, hide_index=True)

def about_page():
    st.title("ℹ️ About HomeFix AI")
    st.markdown("""
**HomeFix AI** is a student Generative AI + Business Analytics project.

### How it works
1. The customer describes a home problem.
2. Groq's LLM performs natural-language understanding and selects one controlled service category.
3. A transparent Pandas scoring system ranks fictional demo providers.
4. The customer selects a provider and submits a request.
5. Requests are stored in a local CSV file.
6. The dashboard turns request data into simple business analytics.
7. A small local knowledge base provides simple RAG for service/policy questions.

### Important
- Provider records are **fictional DEMO DATA**.
- Prices and availability are demo estimates.
- The application does not process payments.
- HomeFix AI is not a certified technician.
- Never use the AI as a substitute for qualified emergency or repair professionals.
""")

    with st.expander("RAG explanation"):
        st.write(
            "The MVP uses simple local retrieval rather than a vector database. "
            "It finds relevant knowledge-base entries using keyword overlap and "
            "passes those entries to Groq before answering general service/policy questions. "
            "Provider filtering stays structured in Pandas because exact category, area "
            "and availability matching is more reliable than asking an LLM to search providers."
        )

def main():
    st.set_page_config(
        page_title="HomeFix AI",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <style>
    .main { background: #f7fafc; }
    .stButton > button { border-radius: 10px; }
    [data-testid="stMetric"] { border: 1px solid #e5e7eb; padding: 10px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

    ensure_data_files()

    st.sidebar.title("🏠 HomeFix AI")
    st.sidebar.caption("AI Home Service Assistant")
    st.sidebar.warning("Provider data is fictional DEMO DATA.")

    pages = [
        "🏠 Home",
        "💬 AI Assistant",
        "🔧 Find a Professional",
        "📅 My Service Request",
        "📊 Dashboard",
        "ℹ️ About",
    ]

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    page = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state.page))
    st.session_state.page = page

    st.sidebar.markdown("---")
    st.sidebar.caption("AI: Groq")
    st.sidebar.caption("Data: Pandas + CSV")
    st.sidebar.caption("RAG: Local keyword retrieval")

    if page == "🏠 Home":
        home_page()
    elif page == "💬 AI Assistant":
        assistant_page()
    elif page == "🔧 Find a Professional":
        find_professional_page()
    elif page == "📅 My Service Request":
        booking_page()
    elif page == "📊 Dashboard":
        dashboard_page()
    elif page == "ℹ️ About":
        about_page()

if __name__ == "__main__":
    main()
