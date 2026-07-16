import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


from ingest import load_faq_data, build_index
from rag_helper import RAGBase
from client import client2



def create_assistant():

    documents = load_faq_data()
    index = build_index(documents)

    return RAGBase(
        index=index,
        llm_client=client2,
        model="openai/gpt-oss-20b"
    )


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag(query)
    print(answer)