# API Documentation

## Health Check

- **Name:** Health Check
- **Method:** GET
- **Endpoint:** `/health`
- **Schema:**
  - No parameters.
- **Response:**
  - `status` (str): Always "ok" if the service is healthy.

---

## Generate Response

- **Name:** Generate Response
- **Method:** POST
- **Endpoint:** `/api/v1/generate_response/generate_response`
- **Schema:**
  - **Request:**
    - `messages` (list[dict]): List of messages for the RAG operation.
      - `role` (str): Role of the message sender (e.g., 'user', 'assistant').
      - `content` (any): Content of the message.
      - `tool_calls` (optional, list[any]): List of tool calls associated with the message.
    - `client` (dict): Client information for the RAG operation.
      - `id` (str): Client identifier.
    - `rag_config` (dict): Configuration for the RAG operation, including LLM configurations.
      - `llm_config` (dict): LLM configuration for RAG.
        - `model_path` (optional, str): Path to the LLM model. Default: "gpt-4.1-mini".
        - `base_url` (optional, str): Base URL for the LLM service.
        - `api_key` (optional, str): API key for the LLM service.
        - `temperature` (optional, float): Temperature for LLM responses. Default: 0.01.
      - `top_k` (optional, int): Number of top documents to retrieve. Default: 5.
  - **Response:**
    - `answer` (str): The generated answer from the RAG operation.
    - `citations` (optional, list[dict]): List of citations used to generate the answer.
      - `file_name` (str): Name of the cited file.
      - `file_path` (str): Path to the cited file.
      - `page_number` (int): Page number in the cited file.
      - `page_content` (str): Content from the cited page.
    - `flag` (int): Status flag (0: success, 1: no answer found, 2: error).

---

## Index Document

- **Name:** Index Document
- **Method:** POST
- **Endpoint:** `/api/v1/index_document/index_document`
- **Schema:**
  - **Request:**
    - `client` (dict): Client information for indexing documents.
      - `id` (str): Client identifier.
    - `input_files` (list[dict]): List of input files to be indexed.
      - `remote_file_path` (optional, str): Path to the remote reference file.
      - `local_file_path` (optional, str): Path to the reference file.
      - `file_name` (optional, str): Name of the reference file.
      - `file_type` (str): Type of the reference file (e.g., 'pdf', 'docx').
      - `read_file_config` (dict): Configuration for reading the reference file (see File Config Object below).
  - **Response:**
    - `statuses` (list[dict]): List of statuses for each indexed document.
      - `file_path` (str): Path to the file being indexed.
      - `file_name` (optional, str): Name of the file being indexed.
      - `status` (str): Current status of the indexing process ("pending", "in_progress", "completed", "failed").

---

## Index Document (Background)

- **Name:** Index Document Background
- **Method:** POST
- **Endpoint:** `/api/v1/index_document/index_document_background`
- **Schema:**
  - **Request:**
    - `client` (dict): Client information for indexing documents.
      - `id` (str): Client identifier.
    - `input_files` (list[dict]): List of input files to be indexed (see above).
    - `ids` (list[str]): List of IDs for the background task. Used to track the indexing process.
  - **Response (FastAPI):**
    - `message` (str): "Indexing started in the background".
    - `task_ids` (list[str]): List of task IDs for background jobs.
  - **Response (Celery):**
    - Each task will return a status for the indexed document:
        - `file_path` (str): Path to the file being indexed.
        - `file_name` (optional, str): Name of the file being indexed.
        - `status` (str): Current status of the indexing process ("pending", "in_progress", "completed", "failed").

---

## Get LLM Config Keys

- **Name:** Get LLM Config Keys
- **Method:** GET
- **Endpoint:** `/api/v1/get_llm_configs/get_llm_config_keys`
- **Schema:**
  - No parameters.
- **Response:**
  - List of strings: LLM configuration keys.

---

## Get LLM Config

- **Name:** Get LLM Config
- **Method:** GET
- **Endpoint:** `/api/v1/get_llm_configs/get_llm_config`
- **Schema:**
  - **Request:**
    - `key` (str): The key of the LLM configuration to retrieve.
  - **Response:**
    - `model_path` (optional, str): Path to the LLM model.
    - `base_url` (optional, str): Base URL for the LLM service.
    - `api_key` (optional, str): API key for the LLM service.
    - `temperature` (optional, float): Temperature for LLM responses.

---

## Get Read File Config

- **Name:** Get Read File Config
- **Method:** GET
- **Endpoint:** `/api/v1/get_read_file_config/get_read_file_config`
- **Schema:**
  - **Request:**
    - `key` (str): The file extension (pdf, docx, pptx, ...)
  - **Response:**
    - File config object (see below).

---

## File Config Object

- **PDF:**
  - `force_ocr` (bool): Whether to use LLM for reading PDF files.
  - `use_llm_enhance` (bool): Whether to use LLM for enhancing PDF content.
  - `use_llm_extract` (bool): Whether to use LLM for extracting information from PDF files.
- **DOCX, TXT, XLSX, PPTX, MD, CSV:**
  - (May have specific fields depending on implementation.)

---

**Note:**
- For background indexing, the FastAPI response returns task IDs, while the actual document status/result is returned by Celery workers.
- All endpoints return errors in the form `{ "error": <error_message> }` with appropriate HTTP status codes.
