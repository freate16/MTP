import sys
import torch # CRITICAL: Import torch before other libraries to fix WinError 1114
import re
from pathlib import Path
import os
from dotenv import load_dotenv

# Setup paths to import existing modules
PROJECT_ROOT = Path(r"D:\Rubel\M.Tech\MTP\Phase 2")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
RAG_ROOT = PROJECT_ROOT / "chatbot" / "rag"
if str(RAG_ROOT) not in sys.path:
    sys.path.insert(0, str(RAG_ROOT))

# Load environment variables
env_path = PROJECT_ROOT / "chatbot" / "rag" / ".env"
load_dotenv(dotenv_path=env_path)

from chatbot.agentic_rag.tools import TOOLS, get_tool_descriptions

def agent_chat(messages: list[dict[str, str]], *, model: str, max_tokens: int, temperature: float, stop: list[str] | None = None) -> str:
    """Localized LLM call with support for stop sequences to prevent hallucinations."""
    from huggingface_hub import InferenceClient
    
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
    if not token:
        raise ValueError("Missing HF token. Put HF_TOKEN=... in .env or your environment.")

    client = InferenceClient(model=model, token=token)
    
    # We use stop sequences to force the LLM to stop after generating a tool call
    response = client.chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=stop
    )
    
    try:
        content = response.choices[0].message.content
    except AttributeError:
        content = response["choices"][0]["message"]["content"]
    
    return content

SYSTEM_PROMPT = """You are an autonomous Geospatial Reasoning Agent specialized in Glacial Lake Outburst Floods (GLOFs).
Your goal is to answer complex questions by reasoning step-by-step and calling specific tools to gather evidence.

You have access to the following tools:
{tool_descriptions}

Use the following format strictly:

Question: the input question you must answer
Thought: you should always think about what to do next. Decompose the problem if necessary.
Action: the name of the tool to use. Must be one of: {tool_names}
Action Input: the exact string argument to pass to the tool
Observation: the result of the tool
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer based on the evidence.
Final Answer: the final answer to the original input question. 

Rules:
1. For specific lakes or basins, you must ONLY answer using the data returned by the tools. Do not hallucinate data or guess Lake IDs. 
2. For general conceptual, scientific, or threshold questions (e.g., "What causes GLOFs?", "weather thresholds", "hazard index"), you MUST use BOTH the `query_knowledge_graph` tool AND the `search_scientific_papers` tool to gather comprehensive background context from all available sources before formulating your answer. Do NOT use specific Lake IDs from tool examples as "representative" cases unless specifically asked.
3. If the user provides a numeric Basin ID or Sub-catchment ID (e.g., '170067682'), you MUST first use `query_lakes_by_subcatchment` or `execute_python_code` to find the actual lakes in that basin. NEVER guess which lake belongs to a basin.
4. If a tool fails or returns no data, try a different approach or tool.
5. If the user asks a multi-step question, you must first find the lake properties, then find its risk, etc.
6. Your output MUST contain "Action:" and "Action Input:" if you want to use a tool.
7. ALWAYS STOP writing after you output "Action Input:". Wait for the Observation.
8. HYDROLOGICAL REASONING & CASCADING GLOFS: Water flows downhill. If asked which other lakes are affected by a GLOF from a source lake, first find the source lake's sub-catchment using `query_downstream_rivers_kg`. Then use `query_lakes_by_subcatchment` which will return all nearby lakes AND their elevations. A lake can only be flooded if its elevation is LOWER than the source lake. Just compare the elevations returned by the tool directly. Do NOT write Python code for this!
9. FLOOD SCENARIOS: If the user asks about the impact of a lake breach, buildings at risk, or "what happens if X lake fails", ALWAYS use the `simulate_glof_flood_impact` tool.
10. SATELLITE DETECTION: ONLY use the `detect_lakes_and_calculate_area` tool IF the user specifically requests "new satellite detection", "area trend analysis", or "calculate area from recent imagery". This tool is SLOW. You must pass 4 comma-separated arguments: 'lake_id, mode, start, end'. 'mode' must be 'yearly' (e.g. 2021) or 'monthly' (e.g. 2024-06). Example: "GL087099E27798N, monthly, 2024-06, 2025-01".
11. CONCEPTUAL QUESTIONS: Do not pick a random Lake ID from tool descriptions (like GL088561E28014N) to illustrate a general point. Use general scientific principles or findings from `search_scientific_papers`.
12. COORDINATE QUERIES: If the user provides lat/lon coordinates (e.g., "near 28.98 lat, 88.70 lon") and asks for averages, counts, or properties, you MUST use `execute_python_code` to buffer the point and query the GeoPackage. Do NOT say you cannot do it.
13. NAMED RIVER BASINS (Ganga, Indus, Brahmaputra, etc.): The GeoPackage does NOT contain basin names, only numeric Sub-catchment IDs. For questions about distributions, statistics, or properties within a named basin (e.g., "Elevation distribution in the Indus basin"), you MUST first use `search_scientific_papers`. These distributions are often pre-calculated in the scientific literature. If you need to perform custom analysis, use the papers to find which numeric Sub-catchment IDs belong to that basin first.
14. DATA INTEGRITY: NEVER manually type out or hardcode long lists of numbers, coordinates, or Lake IDs into a Python script (e.g., `elevations = [4239, 4201, ...]`). This is prone to error and truncation. Instead, use Python to query the GeoPackage file directly (`gpd.read_file`) and filter the data using IDs or ranges found in previous steps.
15. NAMED BASIN PRIORITIZATION: For questions about distributions or statistics in named basins/sub-basins (e.g., 'Indus Middle', 'Upper Ganga'), do NOT waste steps looking for numeric Sub-catchment IDs. Instead, use `search_scientific_papers` to find the pre-calculated statistics or tables directly. Only use `execute_python_code` if the papers fail to provide the summary or if the user asks for very specific lake-level calculations.
16. SUMMARY TABLE PREFERENCE: When using `search_scientific_papers`, look specifically for keywords like "Summary", "Distribution", "Table X", or "Statistical Analysis". Distributions (like elevation ranges) are ALWAYS provided as summary tables in the reports. NEVER attempt to manually count or extract individual lake elevations from long Annexure lists if a summary table exists.
17. DATA MISIDENTIFICATION WARNING: Be extremely careful with column headers. Do NOT confuse Serial Numbers, Lake IDs, or numeric codes with physical properties like Elevation, Area, or Volume. Always verify which column contains the actual physical value.
18. Once you have enough information, output "Final Answer:" followed by your final synthesized response.

"""

def run_reasoning_agent(question: str, max_steps: int = 8):
    tool_names = list(TOOLS.keys())
    tool_descriptions = get_tool_descriptions()
    
    prompt = SYSTEM_PROMPT.format(
        tool_descriptions=tool_descriptions,
        tool_names=", ".join(tool_names)
    )
    
    messages = [{"role": "system", "content": prompt}]
    messages.append({"role": "user", "content": f"Question: {question}"})
    
    print("="*60)
    print(f"[Agent Started] Question: {question}")
    print("="*60)
    
    for step in range(max_steps):
        # We tell the model to STOP after it provides the Action Input.
        # This prevents it from hallucinating the "Observation:" field.
        try:
            response = agent_chat(
                messages, 
                model="Qwen/Qwen3-4B-Instruct-2507", 
                max_tokens=1024, 
                temperature=0.1,
                stop=["Observation:", "Observation"]
            )
        except Exception as e:
            print(f"LLM Error: {e}")
            break
        
        # We append the LLM's response to the conversation history
        messages.append({"role": "assistant", "content": response})
        print(f"\n{response}\n")
        
        # Check if the agent reached the final answer
        if "Final Answer:" in response:
            print("="*60)
            print("[Agent Finished Successfully]")
            print("="*60)
            return
            
        # Parse Tool Call using Regex. Use re.DOTALL to capture multi-line code blocks
        action_match = re.search(r"Action:\s*(.*?)(?:\n|$)", response)
        action_input_match = re.search(r"Action Input:\s*(.*?)(?:\n(?=Observation:)|$)", response, re.DOTALL)
        
        if action_match and action_input_match:
            action_name = action_match.group(1).strip()
            action_input = action_input_match.group(1).strip()
            
            # Clean up YAML pipe or markdown blocks often added by LLMs
            if action_input.startswith("|"):
                action_input = action_input[1:].strip()
            
            # Remove ```python, ```py, or just ``` at the start
            action_input = re.sub(r"^```[a-zA-Z]*\n?", "", action_input)
            
            if action_input.endswith("```"):
                action_input = action_input[:-3]
            
            action_input = action_input.strip()
            
            # Strip triple double-quotes if the LLM wraps the code in them
            if action_input.startswith('"""') and action_input.endswith('"""'):
                action_input = action_input[3:-3].strip()
                
            # Strip quotes if the LLM added them (only for single-line strings)
            if "\n" not in action_input and action_input.startswith(("'", '"')) and action_input.endswith(("'", '"')):
                action_input = action_input[1:-1]
                
            if action_name in TOOLS:
                print(f"\n[EXECUTING TOOL]: {action_name}")
                print(f"--- Input ---\n{action_input}\n-------------")
                try:
                    observation = TOOLS[action_name](action_input)
                except Exception as e:
                    observation = f"Tool Execution Error: {str(e)}"
            else:
                observation = f"Error: {action_name} is not a valid tool. Choose from: {', '.join(tool_names)}"
                
            # Truncate print output for observation so console isn't flooded
            print_obs = observation if len(observation) < 300 else observation[:300] + "... [truncated]"
            print(f"[OBSERVATION]: {print_obs}")
            
            # Append REAL Observation to prompt so LLM can read it
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            # If the LLM format is broken but no final answer
            warning_msg = "Format Error: You must output 'Action:' and 'Action Input:' or 'Final Answer:'."
            print(f"[WARNING]: {warning_msg}")
            messages.append({"role": "user", "content": warning_msg})

    print("="*60)
    print("[Agent Stopped] Reached maximum steps without a final answer.")
    print("="*60)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Welcome to the Geospatial Reasoning Agent (GLOF Expert)")
    print("Type 'exit' or 'quit' to end the session.")
    print("="*60 + "\n")
    
    while True:
        try:
            user_question = input("\nYour Question: ").strip()
            if user_question.lower() in ['exit', 'quit']:
                print("Exiting agent. Goodbye!")
                break
            if not user_question:
                continue
                
            run_reasoning_agent(user_question)
        except KeyboardInterrupt:
            print("\nExiting agent. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
