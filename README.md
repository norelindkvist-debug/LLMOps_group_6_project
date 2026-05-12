# LLMOps_group_6_project: CSN Support Chatbot (RAG)

Denna applikation är en intelligent chatbot specialiserad på frågor rörande CSN, driven av en RAG-arkitektur (Retrieval-Augmented Generation) för att säkerställa hög tillförlitlighet i sina svar.

Applikationen består av tre huvuddelar:
- **Datainsamling/Vektordatabas**: LanceDB & Cohere embeddings.
- **Backend**: FastAPI & Pydantic AI-agenter.
- **Frontend**: Streamlit.

---

## 🚀 Kom igång (Setup Guide)

Följ dessa steg för att bygga databasen och starta både frontend och backend lokalt via Docker.

### 1. Miljövariabler (.env)
Du behöver API-nycklar för att systemet ska fungera (en för AI-modellen och en för att skapa vektor-embeddings).
Skapa en fil som heter `.env` i projektets **huvudmapp** (`LLMOps_group_6_project/.env`) och lägg in:

```env
OPENROUTER_API_KEY=din-openrouter-nyckel-här
COHERE_API_KEY=din-cohere-nyckel-här
```

### 2. Bygg vektordatabasen (Data Ingestion)
Innan du kan ställa frågor till chatboten måste du låta systemet processa och spara de underliggande texterna till den lokala databasen. 
Öppna din terminal i projektets **huvudmapp** och kör:

```bash
# Detta läser in markdown-filerna och bygger en LanceDB-databas
uv run python -m rag.setup.ingestion
```
*Notera: Databasen sparas i mappen `rag/knowledge_base`. Filerna här får inte raderas om du inte avser att bygga om databasen på nytt.*

### 3. Starta applikationen (Docker)
När databasen är redo, navigerar du in i `rag`-mappen och startar hela stacken via Docker Compose:

```bash
cd rag
docker compose up --build
```

### 4. Användning
När Docker-containrarna är igång (notera att backenden kan ta ett par sekunder extra att starta) kan du nå tjänsterna i din webbläsare:

- **Frontend (Chatbot UI):** [http://localhost:8501](http://localhost:8501)
- **Backend API (Swagger Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

*Felsökningstips: Om frontenden visar `Connection refused` direkt vid uppstart, klicka på "Rerun" eller ladda bara om sidan i webbläsaren. Det betyder bara att backenden var någon sekund långsammare med att starta.*