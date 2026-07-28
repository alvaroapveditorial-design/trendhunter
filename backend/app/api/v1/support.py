"""Public support contact form."""

from fastapi import APIRouter, status

from app.schemas.schemas import SupportContactCreate
from app.services.email_service import send_support_contact_email

router = APIRouter()


@router.post("/contact", status_code=status.HTTP_202_ACCEPTED)
def create_support_contact(payload: SupportContactCreate):
    """Relay a contact-form message to the support inbox. Always 202: the
    sender gets no signal about whether the relay email actually delivered,
    same as the rest of the app's outbound-email endpoints."""
    send_support_contact_email(payload.email, payload.message)
    return {"received": True}
