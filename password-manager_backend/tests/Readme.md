# Tests

Unit tests for the use case (application) layer, run with `pytest`. Each use
case is tested against a mocked repository interface — no database needed.

```bash
cd password-manager_backend
pip install -r requirements.txt
pytest
```

Run a single file or test:

```bash
pytest tests/application/use_case/test_sub_account_use_case.py
pytest tests/application/use_case/test_sub_account_use_case.py::TestCreateSubAccountUseCase::test_wraps_repository_errors
```

`pytest.ini` (at the project root) points `pytest` at `src/` and enables
`pytest-asyncio` for the async use cases (e.g. user creation).
