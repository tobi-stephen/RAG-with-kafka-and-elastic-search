## Retrieval Augmented Generation with OpenAI, Kafka and ElasticSearch

The repo is an attempt to build a POC chat application that derives context from a stream of preloaded data and generate better response using a combination of semantic search from in ElasticSearch and OpenAI GPT completion API.


The application has a number of components including
- Flask Application: REST API for querying the system.
- Search Client: An ElasticSearch based application which will serve as a Vector DB for the generated vector embeddings.
- Kafka Producer: The Producer app streams data from `conversations.json` to a kafka topic and optionally can be further processed and transformed to another kafka topic (using Flink or Kafka streams).
- Kafka Consumer: The Consumer app(s) reads from the kafka topic in order to generate embeddings using OpenAI and indexed to an ElasticSearch store
- LLM module: The module handles embedding generation and completion request using OpenAI
- Vector Database, LLM, Data Streaming platform: Though I tested this using local setups of ElasticSearch and Apache Kafka clusters - An easier approach will be to use fully managed versions provided by Elastic, Confluent, and OpenAI APIs, thus allowing you to focus on the important business logic.


### Resources
- https://www.confluent.io/resources/online-talk/retrieval-augmented-generation-RAG-Generative-AI/

- https://search-labs.elastic.co/search-labs/blog/rag-with-llamaIndex-and-elasticsearch?utm_source=GaggleAMP-Elastic&utm_medium=LinkedIn%20%28GaggleAMP%29&utm_campaign=none%20%28GaggleAMP%29&utm_content=implement-a-qa-experience-using-a-rag-technique-with-elasticsea-4447892&activity_id=4447892

- https://www.kai-waehner.de/blog/2024/01/29/genai-demo-with-kafka-flink-langchain-and-openai/