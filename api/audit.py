from fastapi import APIRouter, Depends, Body
from typing import Optional

from ..schemas.audit import AuditReport, AuditReportOptions
from ..services.audit import AuditService, get_audit_service

router = APIRouter()


@router.post("/", response_model=AuditReport)
async def generate_audit_report(
    options: Optional[AuditReportOptions] = Body(None),
    service: AuditService = Depends(get_audit_service),
) -> AuditReport:
    return await service.generate_report(options=options)
