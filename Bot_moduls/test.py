from connect_database import astraSession
from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.cassandra import Cassandra
from setting import ASTRA_DB_KEYSPACE, HUGGING_FACE_MODEL_NAME, OPENAI_API_KEY

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
myEmbedding = HuggingFaceInstructEmbeddings(model_name=HUGGING_FACE_MODEL_NAME)

#
myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="qa_mini_demo",
)
text_splitter = CharacterTextSplitter(        
    separator = "\n\n",
    chunk_size = 500,
    chunk_overlap  = 50,       
    length_function = len,
)

print("Loading data from projects") 
loader = JSONLoader('/home/antv/Documents/ChatBox_InstantNoodles/output.jsonl', jq_schema='.content', json_lines=True)
documents = loader.load()
documents = text_splitter.split_documents(documents[:30])

print("\nGenerating embeddings and storing in AstraDB")
for line in range(50, len(documents), 50):
    print("Inserting %i data." % line)
    myCassandraVStore.add_documents(documents[line-50:line])
    print("Inserted %i data.\n" % line)

print("Inserted %i data.\n" % len(documents))

vectorIndex = VectorStoreIndexWrapper(vectorstore=myCassandraVStore)

first_question = True
while True:
    if first_question:
        query_text = input("\nEnter your question (or type 'quit' to exit): ")
        first_question = False
    else:
        query_text = input("\nWhat's your next question (or type 'quit' to exit): ")

    if query_text.lower() == 'quit':
        break

    # print("QUESTION: \"%s\"" % query_text)
    # answer = vectorIndex.query(query_text, llm=llm).strip()
    # print("ANSWER: \"%s\"\n" % answer)

    print("DOCUMENTS BY RELEVANCE:")
    for doc, score in myCassandraVStore.similarity_search_with_score(query_text, k=4):
        print("  %0.4f \"%s ...\"" % (score, doc.page_content[:60]))