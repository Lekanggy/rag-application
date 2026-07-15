from ingest import load_faq_data
from pydantic import BaseModel


#Build the insruction of  LLM for document generation
data_gen_instructions = """
You emulate a student who's taking our course.
Formulate 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record.

The output should resemble how people ask questions
on the internet. Not too formal, not too short, not too long.
""".strip()


def get_documents(filer="llm-zoomcamp"):
    documents = load_faq_data()
    documents_llm = [doc for doc in documents if doc["course"] == filer]
    return documents_llm

#Hit
def hit_rate(example):
    cnt = 0
    for line in example:
        if 1 in line:
            cnt += 1
    return cnt/len(example)

#Mean Rank
def mrr(relevance):
    total_score = 0.0

    for line in relevance:
        for rank in range(len(line)):
            if line[rank] == 1:
                total_score = total_score + 1 / (rank + 1)
                break

    return total_score / len(relevance)



class Questions(BaseModel):
    questions: list[str]
