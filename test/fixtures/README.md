# Test fixtures

## Documents

`documents/` holds the documents indexed by the indexer integration tests. They are indexed **in place**: tests pass a
subdirectory straight to `IndexerService.index()` and nothing is copied.

Each scenario gets its own subdirectory because the indexer walks a directory recursively and indexes everything it
finds. Pointing a test at `documents/` itself would make its results depend on every other scenario's documents, so
adding a document for one test would break the counts asserted by the others.

| Directory      | Scenario                                                                    |
| -------------- | --------------------------------------------------------------------------- |
| `text/`        | A single Markdown document: chunk metadata and a published, active version. |
| `pdf/`         | Two pages, one line of text each: PDF extraction and page numbers.          |
| `scanned/`     | One page with no text layer: a PDF with no extractable text.                |
| `nested/`      | A document in a subdirectory: the source is recorded as a POSIX path.       |
| `large/`       | Longer than the splitter's 1500 character chunk size: multi-chunk indexing. |
| `unsupported/` | Extensions the indexer does not handle.                                     |
| `empty/`       | A zero byte document: no extractable text.                                  |
| `multiple/`    | Two documents, one of which the test makes unreadable: indexing carries on. |
| `symlink/`     | A symlink to `../outside`, which the indexer must refuse to follow.         |

`outside/` is deliberately outside `documents/` and is only the target of that symlink; it is never indexed.

Four tests are **not** in here, as they change or delete a document to drive the version lifecycle (content changes,
reverts, and removal) or need a genuinely empty directory, which git cannot track. Those use a temporary directory via
the `temp_documents_path` fixture, so they leave the working tree clean and survive a second run.

## Replacing the PDFs

Both PDFs are minimal, synthetic files: uncompressed, with a single standard font. Replacing them with PDFs produced by
real software (a word processor, LaTeX, or a browser's print-to-PDF) would exercise `pdfplumber` more realistically.
Drop a replacement in at the same path, keeping `pdf/report.pdf` to one line of text per page across two pages, and
`scanned/scanned.pdf` with no text layer.
