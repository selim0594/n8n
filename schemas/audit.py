from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class AuditReportOptions(BaseModel):
    days_abandoned_workflow: Optional[int] = Field(None, alias="daysAbandonedWorkflow")
    categories: Optional[List[str]] = None


class AuditReportSection(BaseModel):
    risk: str
    sections: List[Dict[str, Any]]


class AuditReport(BaseModel):
    credentials_risk_report: AuditReportSection = Field(alias="Credentials Risk Report")
    database_risk_report: AuditReportSection = Field(alias="Database Risk Report")
    filesystem_risk_report: AuditReportSection = Field(alias="Filesystem Risk Report")
    nodes_risk_report: AuditReportSection = Field(alias="Nodes Risk Report")
    instance_risk_report: AuditReportSection = Field(alias="Instance Risk Report")
