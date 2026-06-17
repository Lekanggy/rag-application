INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

USER_PROMPT_TEMPLATE = """
Question:
{question}

Context:
{context}
"""

class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=USER_PROMPT_TEMPLATE,
        course="llm-zoomcamp",
        model="gpt-4o-mini"
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        results = self.index.search(
            query,
            boost_dict={"question": 2},
            filter_dict={"course": self.course},
            num_results=num_results
        )
        return results
    
    def build_context(self, search_results):
        context = ""
        for result in search_results:
            context += f"{result['section']}\n"
            context += f"Q: {result['question']}\n"
            context += f"A: {result['answer']}\n\n"
        return context
    
    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        prompt = self.prompt_template.format(
            question=query,
            context=context
        )
        return prompt.strip()
    
    def llm(self, prompt):
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        res = self.llm_client.responses.create(
            model=self.model,
            input=messages
        )
        return res.output_text
    
    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer

