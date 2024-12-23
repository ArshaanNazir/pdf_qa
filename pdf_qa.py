import os
import json
from typing import List, Dict, Any
import argparse
import ast
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai_tools import PDFSearchTool



# Configure OpenAI
os.environ['OPENAI_API_KEY'] = "<YOUR_OPENAI_KEY>"


def setup_rag_tool(pdf_path: str) -> PDFSearchTool:
    """
    Creates a PDFSearchTool for the given PDF path (only once).
    """
    return PDFSearchTool(
        pdf=pdf_path,
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(model="gpt-4o-mini")
            ),
            embedder=dict(
                provider="huggingface",
                config=dict(model="BAAI/bge-small-en-v1.5")
            )
        )
    )

def setup_agent(rag_tool: PDFSearchTool) -> Agent:
    """
    Creates an Agent that uses the rag_tool. Only do this once.
    """
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)

    return Agent(
        role="PDF Researcher",
        goal="Search and analyze PDF content using RAG to provide clear, accurate answers. If you don't find anything, simply answer Data Not Available.",
        backstory="You are an expert at using RAG to find and analyze information in documents.",
        verbose=False,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool]
    )


def process_question(agent: Agent, question: str) -> Dict[str, str]:
    """
    Processes a single question using the *already created* agent.
    Returns a dict with {"question":..., "answer":...}.
    """
    try:
        # Construct a single task
        task = Task(
            description=f"Search the PDF and provide a clear answer for: {question}",
            agent=agent,
            expected_output="Clear answer based on PDF content",
            context=[{
                "role": "system",
                "description": "Search and answer based on PDF content",
                "question": question,
                "expected_output": "Clear answer based on PDF content"
            }]
        )

        # Run the crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )

        raw_result = str(crew.kickoff())

        return {
            "question": question,
            "answer": raw_result
        }

    except Exception as e:
        print(f"Error processing question: {str(e)}")
        return {
            "question": question,
            "answer": "Error processing question"
        }



def parse_questions_list(questions_str: str) -> List[str]:
    """
    Safely parse a string representation of a list into a Python list.
    e.g. --questions '["What is the name?", "Who is the CEO?"]'
    """
    try:
        questions = ast.literal_eval(questions_str)
        if not isinstance(questions, list):
            raise ValueError("Questions must be provided as a list")
        return questions
    except:
        raise ValueError("Invalid questions list format. Use format: [\"question1\", \"question2\"]")



def main():
    parser = argparse.ArgumentParser(description='Answer questions from a PDF document')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--questions', help='List of questions in format ["q1", "q2", ...]')

    args = parser.parse_args()

    try:
        questions = parse_questions_list(args.questions)
        rag_tool = setup_rag_tool(args.pdf_path)
        research_agent = setup_agent(rag_tool)

        all_results = {}
        for question in questions:
            print(f"\nProcessing question: {question}")

            result = process_question(research_agent, question)

            print("\nResult:")
            print(result["answer"])

            all_results[question] = result["answer"]

        print("\nAll Results:")
        print(json.dumps(all_results, indent=2))

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error processing questions: {str(e)}")


if __name__ == "__main__":
    main()