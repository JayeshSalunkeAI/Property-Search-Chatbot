"""
FastAPI Main Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatQuery, ChatResponse
from query_parser import QueryParser
from search_engine import SearchEngine
from summarizer import Summarizer
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="Property Search Chatbot",
    version="1.1.0",
    description="Chatbot To search Properties!"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (all LOCAL)
print("Initializing components...")
parser = QueryParser()
search_engine = SearchEngine(data_path=Config.DATA_PATH)
summarizer = Summarizer()
print("✓ All components initialized!")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Property Search Chatbot",
        "status": "running",
        "api_keys_required": False,
        "version": "1.1.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(query: ChatQuery):
    """
    Main chat endpoint - Processes queries
    
    Args:
        query: ChatQuery with user message
        
    Returns:
        ChatResponse with summary and properties
    """
    try:
        print(f"\n{'='*60}")
        print(f"Processing query: {query.message}")
        
        # 1. Parse query (LOCAL - regex based)
        filters = parser.parse(query.message)
        print(f"Extracted filters: {filters}")
        
        # 2. Search properties (LOCAL - pandas filtering)
        properties = search_engine.search(filters)
        print(f"Found {len(properties)} properties")
        
        # 3. Generate summary (LOCAL - rule based)
        summary = summarizer.generate_summary(properties, filters)
        print(f"Generated summary: {summary[:100]}...")
        
        print(f"{'='*60}\n")
        
        return ChatResponse(
            summary=summary,
            properties=properties,
            filters_applied=filters,
            total_results=len(properties)
        )
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "local",
        "api_keys_required": False
    }


@app.get("/stats")
def get_stats():
    """Get database statistics"""
    try:
        stats = search_engine.get_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting Property Search Chatbot")
    print("Thought about Properties")
    print("="*60 + "\n")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
