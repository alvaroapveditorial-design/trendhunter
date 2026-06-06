# AI Trend Hunter Frontend

Next.js dashboard for the AI Trend Hunter MVP.

## Local Development

Run the backend first:

```bash
cd ../backend
uvicorn app.main:app --reload --port 8000
```

Then run the frontend:

```bash
cd ../frontend
npm install
npm run dev
```

Open http://localhost:3000.

The dashboard includes **Run demo ingestion** and **Pull Hacker News** actions. Keep the backend running, click either action, and the page will revalidate with newly created or updated trends.

## Verification

```bash
npm run lint
npm run build
```

`npm run lint` runs TypeScript verification. The dashboard reads from `NEXT_PUBLIC_API_URL`, defaulting to `http://localhost:8000`.
