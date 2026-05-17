import re

# --- Simulated Knowledge Base ---
# In a real system, this would be a vector database or a structured knowledge graph.
# For this example, it's a list of (topic, content) tuples.
KNOWLEDGE_BASE = [
    ("Agentic RAG Definition", "Agentic RAG gives AI agents control over the retrieval process, allowing them to decide what, when, and how to retrieve information. This enhances accuracy and reduces hallucinations."),
    ("Traditional RAG Definition", "Traditional RAG augments LLMs with retrieved documents, but the LLM doesn't control the retrieval process. It's a more passive approach where context is simply provided."),
    ("Benefits of Agentic RAG", "Agentic RAG improves accuracy, reduces hallucinations, allows for more dynamic information gathering, and enables complex reasoning by leveraging various tools."),
    ("Limitations of Traditional RAG", "Traditional RAG can struggle with complex queries, may not always retrieve the most relevant information, and lacks the ability to adapt its retrieval strategy."),
    ("Comparison RAG vs Agentic RAG", "Traditional RAG is a passive, context-feeding mechanism. Agentic RAG is an active, agent-driven orchestration of retrieval tools and strategies."),
    ("Agentic RAG Architecture", "Agentic RAG typically involves an orchestrator agent, a set of specialized tools (e.g., search, database lookup, summarization), and an LLM for synthesis."),
    ("Example Agentic RAG Use Case", "An Agentic RAG system could analyze a complex legal query, decide to search case law, then summarize relevant precedents, and finally synthesize an answer, all orchestrated by the agent.")
]

# --- Simulated Retrieval Tools ---
# These functions represent different 'tools' an agent might use.

def simple_keyword_retriever(query: str, knowledge_base: list) -> str:
    """
    A basic retriever that finds documents containing keywords from the query.
    Simulates a general search tool.
    """
    query_keywords = set(query.lower().split())
    relevant_docs = []
    for topic, content in knowledge_base:
        if any(keyword in topic.lower() or keyword in content.lower() for keyword in query_keywords if len(keyword) > 2):
            relevant_docs.append(f"Topic: {topic}\nContent: {content}")
    return "\n---\n".join(relevant_docs) if relevant_docs else ""

def definition_retriever(term: str, knowledge_base: list) -> str:
    """
    A specialized retriever for finding definitions of a specific term.
    Simulates a 'definition lookup' tool.
    """
    term_lower = term.lower()
    for topic, content in knowledge_base:
        if f"{term_lower} definition" in topic.lower() or f"{term_lower} nedir" in topic.lower():
            return f"Definition of {term}: {content}"
    return ""

def comparison_retriever(term1: str, term2: str, knowledge_base: list) -> str:
    """
    A specialized retriever for comparing two terms.
    Simulates a 'comparison tool'.
    """
    term1_lower = term1.lower()
    term2_lower = term2.lower()
    for topic, content in knowledge_base:
        if (f"comparison {term1_lower} vs {term2_lower}" in topic.lower() or
            f"comparison {term2_lower} vs {term1_lower}" in topic.lower() or
            (term1_lower in topic.lower() and term2_lower in topic.lower() and "vs" in topic.lower()) or
            (term1_lower in content.lower() and term2_lower in content.lower() and "farkları" in content.lower())):
            return f"Comparison of {term1} and {term2}:\n{content}"
    return ""

# --- Agentic RAG System ---

def agentic_rag_system(user_query: str, knowledge_base: list) -> str:
    """
    This function simulates an Agentic RAG system.
    The 'agent' analyzes the user query and decides which retrieval 'tool'
    (or combination of tools) to use, demonstrating control over the retrieval process.
    """
    response_parts = []
    query_lower = user_query.lower()

    # --- Agent's Decision-Making Logic (Simulated) ---
    # This is the core 'agentic' part: deciding which tool to use based on query intent.

    # 1. Check for definition queries (e.g., "definition of X" or "X nedir")
    if "definition of" in query_lower or "nedir" in query_lower:
        # Agent decides to use the specialized definition_retriever tool
        match = re.search(r"(?:definition of|nedir)\s+([\w\s]+)", query_lower)
        if match:
            term = match.group(1).strip()
            retrieved = definition_retriever(term, knowledge_base)
            if retrieved:
                response_parts.append(retrieved)
            else:
                response_parts.append(f"Could not find a specific definition for '{term}'.")
        else:
            # Fallback to general search if term extraction fails
            retrieved = simple_keyword_retriever(user_query, knowledge_base)
            if retrieved:
                response_parts.append(f"General information related to your query:\n{retrieved}")

    # 2. Check for comparison queries (e.g., "compare X and Y" or "X ile Y farkları")
    elif "compare" in query_lower or "farkları" in query_lower:
        # Agent decides to use the specialized comparison_retriever tool
        match = re.search(r"compare\s+([\w\s]+)\s+and\s+([\w\s]+)", query_lower)
        if not match: # Try Turkish pattern
            match = re.search(r"([\w\s]+)\s+ile\s+([\w\s]+)\s+farkları", query_lower)
        
        if match:
            term1 = match.group(1).strip()
            term2 = match.group(2).strip()
            retrieved = comparison_retriever(term1, term2, knowledge_base)
            if retrieved:
                response_parts.append(retrieved)
            else:
                response_parts.append(f"Could not find a specific comparison between '{term1}' and '{term2}'.")
        else:
            # Fallback to general search if terms extraction fails
            retrieved = simple_keyword_retriever(user_query, knowledge_base)
            if retrieved:
                response_parts.append(f"General information related to your query:\n{retrieved}")

    # 3. Default to general keyword retrieval for other queries
    else:
        # Agent decides to use the general simple_keyword_retriever tool
        retrieved = simple_keyword_retriever(user_query, knowledge_base)
        if retrieved:
            response_parts.append(f"General information related to your query:\n{retrieved}")
        else:
            response_parts.append("No relevant information found for your query.")

    return "\n\n".join(response_parts) if response_parts else "I couldn't find any information for your query."

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Agentic RAG System Demo ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = agentic_rag_system(user_input, KNOWLEDGE_BASE)
        print(f"Agent: {response}\n")
