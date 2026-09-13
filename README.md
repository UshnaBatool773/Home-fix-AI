# HomeFix AI — AI Home Service Assistant

HomeFix AI is a student Generative AI + Business Analytics web application built with Python and Streamlit.

A customer can describe a home problem in natural language, such as:

> My AC is leaking water and isn't cooling.

The application uses Groq for natural-language understanding, maps the problem to a controlled home-service category, finds suitable fictional demo providers, ranks them, and allows the customer to submit a service request.

## Important: Demo Data

All service providers included in this project are **fictional DEMO DATA** created for a student project.

Do not present the providers, phone numbers, prices, ratings, or availability as real businesses or real market information.

---

## Features

- AI home-problem understanding with Groq
- Controlled service classification
- Smart clarification questions
- 8 home-service categories:
  - AC Technician
  - Plumber
  - Electrician
  - Appliance Repair
  - Home Cleaner
  - Painter
  - Carpenter
  - Locksmith
- Provider matching with Pandas
- Transparent provider scoring
- Provider cards
- Booking/service request form
- Request IDs
- Pending request status
- Local CSV storage
- Request dashboard
- Business analytics
- Simple local RAG knowledge base
- Safety handling for dangerous electrical/gas/fire situations
- `.env` API-key support
- Friendly error handling
- No paid APIs required

---

## Technology

- Python
- Streamlit
- Groq API
- Pandas
- python-dotenv
- CSV
- Local keyword-based RAG

---

## Project structure

After the first run, the application creates the `data` folder automatically.

```text
homefix_ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
└── data/
    ├── providers.csv
    └── requests.csv
```

You only need the three supplied files to start:

```text
app.py
requirements.txt
README.md
```

`providers.csv` and `requests.csv` are generated automatically by `app.py`.

---

## 1. Install Python

Use Python 3.10+.

Check your Python installation:

```powershell
python --version
```

or:

```powershell
py --version
```

---

## 2. Open the project in VS Code

Put these files in one folder:

```text
homefix_ai/
├── app.py
├── requirements.txt
└── README.md
```

Open that folder in VS Code.

---

## 3. Create a virtual environment

In the VS Code terminal:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, you can run Streamlit using the virtual environment's Python directly, or use Command Prompt:

```cmd
.venv\Scripts\activate
```

---

## 4. Install requirements

```powershell
python -m pip install -r requirements.txt
```

---

## 5. Create your Groq API key

Create a Groq API key from the Groq developer console.

Do not put the key directly inside `app.py`.

Create a new file named:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Optional model setting:

```env
GROQ_MODEL=llama-3.3-70b-versatile
```

Do not upload `.env` to GitHub.

A safe `.gitignore` should contain:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
data/requests.csv
```

If you create `.env.example`, use:

```env
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## 6. Run the application

With the virtual environment activated:

```powershell
streamlit run app.py
```

If the `streamlit` command is not recognized:

```powershell
python -m streamlit run app.py
```

Streamlit will show a local address, normally:

```text
http://localhost:8501
```

Open it in your browser.

---

## 7. Demo flow

Use this exact demonstration for a project presentation.

### Step 1 — Home

Open HomeFix AI.

### Step 2 — AI Assistant

Enter:

```text
My AC is leaking water and not cooling.
```

The AI should identify:

```text
AC Technician
```

### Step 3 — Provider matching

The application searches the structured provider CSV and displays suitable fictional demo providers.

### Step 4 — Select a provider

Click:

```text
Select Provider
```

### Step 5 — Booking

Enter:

- Customer name
- Phone
- Area
- Address
- Problem
- Preferred date
- Preferred time
- Additional notes

### Step 6 — Submit

The application generates an ID such as:

```text
HF-AB12CD34
```

The initial status is:

```text
Pending
```

### Step 7 — Dashboard

Open:

```text
📊 Dashboard
```

The new request appears in the table and the analytics update automatically.

---

## Example questions

Try:

```text
My kitchen sink is blocked and water isn't going down.
```

Expected category:

```text
Plumber
```

Try:

```text
My lights keep going off.
```

Expected category:

```text
Electrician
```

Try:

```text
My washing machine is making a strange noise.
```

Expected category:

```text
Appliance Repair
```

Try:

```text
I need someone to paint my bedroom.
```

Expected category:

```text
Painter
```

Try:

```text
My wooden table is broken.
```

Expected category:

```text
Carpenter
```

Try:

```text
My door lock is broken.
```

Expected category:

```text
Locksmith
```

---

## How AI classification works

The AI does not create arbitrary provider categories.

The application gives Groq a controlled list:

```text
AC Technician
Plumber
Electrician
Appliance Repair
Home Cleaner
Painter
Carpenter
Locksmith
```

Groq performs natural-language understanding and returns a structured JSON result.

The application then validates the returned service against the controlled list.

If the Groq API is unavailable, a simple keyword-based fallback classifier is used so the application can still demonstrate its core functionality.

---

## How provider matching works

Provider filtering is handled with Pandas rather than asking the LLM to invent or search providers.

The application first filters providers by:

```text
service_category
```

Then it ranks them using a transparent score.

### Scoring

```text
Service match       = 50 points
Area match          = 25 points
Availability match  = 15 points
Rating              = up to 7 points
Price               = up to 3 points
```

This means service category has the highest priority.

Area is the next important factor, followed by availability, rating and price.

This approach is intentionally simple and explainable for a student project.

---

## How RAG works

The MVP includes a small local knowledge base inside `app.py`.

It contains information about:

- Services
- Basic FAQs/service information
- Safety
- Policies

The application performs simple keyword-overlap retrieval.

The retrieved information is then supplied to Groq before it answers general service/policy questions.

Provider filtering does **not** use RAG because structured CSV filtering is more reliable for exact provider attributes such as:

- Service
- Area
- Availability
- Rating
- Price

This is a simple RAG implementation suitable for an MVP.

A future version could replace the keyword retrieval with embeddings and a vector database.

---

## Booking storage

Requests are stored locally in:

```text
data/requests.csv
```

The request contains:

- Request ID
- Creation time
- Customer
- Phone
- Area
- Address
- Problem
- Service
- Provider
- Preferred date
- Preferred time
- Notes
- Status
- Estimated price range

The application starts every new request with:

```text
Pending
```

It does not falsely claim that the provider confirmed the booking.

---

## Business Analytics

The dashboard shows:

- Total service requests
- Most requested service
- Most requested area
- Average estimated price
- Requests by service category
- Request status distribution
- Submitted request table

This provides the Business Analytics component of the project.

---

## Safety

HomeFix AI does not provide dangerous repair instructions.

If a user mentions situations such as:

- Gas leak
- Fire
- Exposed/live wiring
- Electrical shock
- Sparks
- Smoke
- Burning electrical smell

the application gives a safety-focused response and recommends appropriate emergency or qualified professional help.

The application does not claim that the AI is a certified technician.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`

Run:

```powershell
python -m pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'groq'`

Run:

```powershell
python -m pip install groq
```

### Groq/API error

Check `.env`:

```env
GROQ_API_KEY=your_actual_key
```

Then restart Streamlit.

The application has a basic classifier fallback, so provider search can still work without the AI API.

### Streamlit is not recognized

Use:

```powershell
python -m streamlit run app.py
```

### Provider CSV is missing

This is expected on the first run. `app.py` automatically creates:

```text
data/providers.csv
```

### Requests disappeared

Requests are stored in:

```text
data/requests.csv
```

Do not delete that file if you want to keep your demo requests.

---

## Deployment

This project can be deployed as a Streamlit application.

For deployment, add the Groq API key through the hosting platform's secrets/environment-variable system rather than committing `.env`.

Never commit:

```text
.env
```

or a real API key to GitHub.

---

## Future improvements

Possible next versions:

1. Real provider accounts
2. Provider login/dashboard
3. Customer authentication
4. PostgreSQL/Supabase database
5. Real appointment availability
6. Provider verification
7. Location-based matching
8. Map integration
9. Notifications
10. Online payments
11. Provider acceptance/rejection
12. Admin panel
13. Embedding-based RAG
14. Vector database
15. Better analytics
16. Multilingual Urdu/English support
17. Real-time booking confirmation

These should be treated as future improvements rather than requirements for the student MVP.

---

## Project limitations

This is an educational prototype.

It does not currently:

- Verify real professionals
- Make real phone calls
- Process payments
- Guarantee provider availability
- Guarantee quoted prices
- Automatically confirm appointments
- Provide certified repair advice
- Use real business/provider data

All provider records are fictional demo records.
