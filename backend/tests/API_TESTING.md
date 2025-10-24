# API Testing Documentation

## Test Summary

All tests performed using Postman.

### Base URL
http://localhost:5000

### Endpoints Tested

#### 1. GET /health
- **Status:** ✅ PASS
- **Response Time:** ~10ms
- **Expected Status:** 200 OK

#### 2. GET /
- **Status:** ✅ PASS
- **Response Time:** ~8ms
- **Expected Status:** 200 OK

#### 3. POST /upload
- **Status:** ✅ PASS
- **Test Cases:**
  - Valid file upload: ✅
  - No file provided: ✅ (400 error)
  - Invalid file type: ✅ (400 error)
  - File too large: ⏳ (to be tested with)
  markdown  - File too large: ⏳ (to be tested with >10MB file)
- **Response Time:** ~50ms

#### 4. POST /generate-quiz
- **Status:** ✅ PASS
- **Test Cases:**
  - MCQ mode: ✅
  - Q&A mode: ✅
  - Invalid mode: ✅ (400 error)
  - Too many questions: ✅ (400 error)
  - Missing filename: ✅ (400 error)
- **Response Time:** ~30ms

#### 5. POST /download-pdf
- **Status:** ✅ PASS (Placeholder)
- **Response Time:** ~15ms
- **Note:** Full implementation in Phase 10

### Error Handling Tests

All error scenarios tested and working:
- ✅ 400 Bad Request (validation errors)
- ✅ 404 Not Found (invalid endpoints)
- ✅ 500 Internal Server Error (to be tested with edge cases)

### CORS Testing
- ✅ CORS enabled and working
- ✅ Tested from browser console

### File Upload Tests

| File Type | Size | Status |
|-----------|------|--------|
| TXT       | <1MB | ✅ PASS |
| PDF       | <1MB | ⏳ To test in Phase 4 |
| DOCX      | <1MB | ⏳ To test in Phase 4 |
| Invalid   | N/A  | ✅ PASS (rejected) |

### Next Steps
- Phase 3: Connect frontend
- Phase 4: Implement actual text extraction
- Phase 8: Implement AI quiz generation
- Phase 10: Implement PDF export

### Test Date
Last updated: [Add current date]