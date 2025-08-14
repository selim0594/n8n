import pytest
from unittest.mock import MagicMock

from ..services.audit import AuditService
from ..schemas.audit import AuditReport, AuditReportOptions


@pytest.mark.asyncio
async def test_generate_audit_report(audit_service: AuditService, mock_n8n_client: MagicMock):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Credentials Risk Report": {"risk": "low", "sections": []},
        "Database Risk Report": {"risk": "low", "sections": []},
        "Filesystem Risk Report": {"risk": "low", "sections": []},
        "Nodes Risk Report": {"risk": "low", "sections": []},
        "Instance Risk Report": {"risk": "low", "sections": []},
    }
    mock_n8n_client.get_client().__aenter__.return_value.post.return_value = mock_response

    options = AuditReportOptions(days_abandoned_workflow=30)
    result = await audit_service.generate_report(options)

    assert isinstance(result, AuditReport)
    assert result.credentials_risk_report.risk == "low"
    mock_n8n_client.get_client().__aenter__.return_value.post.assert_called_once_with(
        "/audit",
        json={"additionalOptions": {"daysAbandonedWorkflow": 30}}
    )
