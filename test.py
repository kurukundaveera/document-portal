# Test code for document ingestion and analysis using a PDFHandler and DocumentAnalyzer
# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

# # Path to the PDF you want to test 
# PDF_PATH = r"/Users/veerareddykurukunda/Documents/document_portal/data/document_analysis/sample.pdf"

# # Dummy file wrapper to simulate uploaded file(Stramlit style)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self.file_path = file_path
        
#     def getbuffer(self):
#         return open(self.file_path, "rb").read()
    
# def main():   # <-- moved outside class
#     try:
#         #----------------- STEP 1: DATA INGESTION -----------------
#         print("starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)
        
#         handler = DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")
        
#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")
        
#         #----------------- STEP 2: DATA ANALYSIS -----------------
#         print("starting metadata analysis...")
#         analyzer = DocumentAnalyzer()
#         analysis_result = analyzer.analyze_document(text_content)
        
#         #---------------- STEP 3: DISPLAY RESULTS -----------------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")
            
#     except Exception as e:
#         print(f"Test failed: {e}")
        
# if __name__ == "__main__":
#     main()

# import os

# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM    

# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(file_path.read_bytes())

# def test_compare_documents():
#     ref_path = Path("/Users/veerareddykurukunda/Documents/document_portal/data/document_compare/name_v1.pdf")
#     act_path = Path("/Users/veerareddykurukunda/Documents/document_portal/data/document_compare/name_v2.pdf")
    
#     class FakeUpload:
#         def __init__(self, file_path: Path):
#             self.name = file_path.name
#             self.buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self.buffer
        
#     comparator = DocumentIngestion()
#     ref_upload = FakeUpload(ref_path)
#     act_upload = FakeUpload(act_path)
    
#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
#     combined_text = comparator.combined_documents()
    
#     print("Combined text Preview (First 1000 chars):\n")     
#     print(combined_text[:1000]) 

#     llm_comparator = DocumentComparatorLLM()
#     comparison_df = llm_comparator.compare_documents(combined_text)
    
#     print("\n=== Comparison Result ===")
#     print(comparison_df.head())
    
# if __name__ == "__main__":
#     test_compare_documents()
    

## Testing code for document comparison

# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM    

# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(file_path.read_bytes())

# def test_compare_documents():
#     ref_path = Path("/Users/veerareddykurukunda/Documents/document_portal/data/document_compare/name_v1.pdf")
#     act_path = Path("/Users/veerareddykurukunda/Documents/document_portal/data/document_compare/name_v2.pdf")
    
#     class FakeUpload:
#         def __init__(self, file_path: Path):
#             self.name = file_path.name
#             self.buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self.buffer
        
#     comparator = DocumentIngestion()
#     ref_upload = FakeUpload(ref_path)
#     act_upload = FakeUpload(act_path)
    
#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
#     combined_text = comparator.combined_documents()
#     comparator.clean_old_sessions(keep_latest=3)
    
#     print("Combined text Preview (First 1000 chars):\n")     
#     print(combined_text[:1000]) 

#     llm_comparator = DocumentComparatorLLM()
#     comparison_df = llm_comparator.compare_documents(combined_text)
    
#     print("\n=== Comparison Result ===")
#     print(comparison_df.head())
    
# if __name__ == "__main__":
#     test_compare_documents()
    

#  Testing for multi document chat functionality

import os
import sys
import io
from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM    
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.single_document_chat.retrieval import ConversationalRAG


def test_document_ingestion_and_rag():
    try:
        test_files = [
            "data/multi_doc_chat/market_analysis_report.docx",
            "data/multi_doc_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf",
            "data/multi_doc_chat/sample.pdf",
            "data/multi_doc_chat/state_of_the_union.txt"
        ]
        
        uploaded_files = []
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"Test file does not exist: {file_path}")
        if not uploaded_files:
            print("No valid test files to upload")
            sys.exit(1)
        
        ingestor = DocumentIngestor()     
        retriever = ingestor.ingest_files(uploaded_files)
        
        for f in uploaded_files:
            f.close()
        
        session_id = "test multi_doc_chat" 
        
        rag = ConversationalRAG(session_id=session_id, retriever=retriever)   
        question = "What is attention is all you need paper about?"
        answer = rag.invoke(question)
        print("\n Question:", question)
        print("Answer:", answer)

    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
        
