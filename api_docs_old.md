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
      - `role` (str): Role of the message sender (e.g., 'system', 'user', 'assistant').
      - `content` (any): Content of the message.
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
      - `read_file_config` (dict): Configuration for reading the reference file. (See file config section below)
  - **Response:**
    - `documents` (list[dict]): List of indexed documents.
      - `id` (optional, str): Document unique identifier.
      - `content` (str): Document content.
      - `metadata` (optional, dict): Document metadata.
      - `file_name` (str): Name of the file associated with the document.
      - `file_path` (str): Path to the file associated with the document.
      - `page_number` (int): Page number of the document.
    - `flag` (int): Status flag (0: success, 1: no documents indexed, 2: error).

---

## Index Document (Background)

- **Name:** Index Document Background
- **Method:** POST
- **Endpoint:** `/api/v1/index_document/index_document_background`
- **Schema:**
  - Same as **Index Document** above.

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

Depending on the file type, the `read_file_config` object may have the following fields:

- **PDF:**
  - `force_ocr` (bool): Whether to use LLM for reading PDF files.
  - `use_llm_enhance` (bool): Whether to use LLM for enhancing PDF content.
  - `use_llm_extract` (bool): Whether to use LLM for extracting information from PDF files.
- **XLSX, CSV, TXT, MD, DOCX, PPTX:**
  - No additional fields (empty config object).
