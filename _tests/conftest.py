import pytest
from unittest.mock import MagicMock, AsyncMock

from ..client import N8nClient
from ..services.workflows import WorkflowService
from ..services.users import UserService
from ..services.executions import ExecutionService
from ..services.credentials import CredentialService
from ..services.tags import TagService
from ..services.audit import AuditService
from ..services.source_control import SourceControlService
from ..services.variables import VariableService
from ..services.projects import ProjectService


@pytest.fixture
def mock_n8n_client() -> MagicMock:
    """Fixture to create a mock N8nClient with an async context manager."""
    mock_client = MagicMock(spec=N8nClient)
    async_http_client = AsyncMock()
    mock_client.get_client.return_value = async_http_client
    return mock_client


@pytest.fixture
def workflow_service(mock_n8n_client: MagicMock) -> WorkflowService:
    return WorkflowService(client=mock_n8n_client)


@pytest.fixture
def user_service(mock_n8n_client: MagicMock) -> UserService:
    return UserService(client=mock_n8n_client)


@pytest.fixture
def execution_service(mock_n8n_client: MagicMock) -> ExecutionService:
    return ExecutionService(client=mock_n8n_client)


@pytest.fixture
def credential_service(mock_n8n_client: MagicMock) -> CredentialService:
    return CredentialService(client=mock_n8n_client)


@pytest.fixture
def tag_service(mock_n8n_client: MagicMock) -> TagService:
    return TagService(client=mock_n8n_client)


@pytest.fixture
def audit_service(mock_n8n_client: MagicMock) -> AuditService:
    return AuditService(client=mock_n8n_client)


@pytest.fixture
def source_control_service(mock_n8n_client: MagicMock) -> SourceControlService:
    return SourceControlService(client=mock_n8n_client)


@pytest.fixture
def variable_service(mock_n8n_client: MagicMock) -> VariableService:
    return VariableService(client=mock_n8n_client)


@pytest.fixture
def project_service(mock_n8n_client: MagicMock) -> ProjectService:
    return ProjectService(client=mock_n8n_client)
