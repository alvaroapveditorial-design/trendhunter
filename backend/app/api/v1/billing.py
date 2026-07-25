"""Stripe billing API endpoints."""

import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import sentry_sdk
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import require_session_email
from app.core.config import get_settings
from app.models.base import Subscription
from app.models.database import get_db
from app.schemas.schemas import (
    BillingPortalResponse,
    CheckoutSessionCreate,
    CheckoutSessionResponse,
)
from app.services.meta_capi import send_capi_event
from app.services.plausible_events import send_plausible_event

router = APIRouter()
settings = get_settings()

ACTIVE_SUBSCRIPTION_STATUSES = {"active", "trialing"}
EXPIRED_TRIAL_STATUSES = {"past_due", "unpaid", "canceled", "incomplete_expired"}


def _utc_from_stripe_timestamp(value: int | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)


def _require_stripe_config() -> None:
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PRO_PRICE_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe billing is not configured.",
        )


def create_stripe_checkout_session(email: str, include_trial: bool = True) -> dict:
    """Create a Stripe Checkout Session for the Pro subscription."""
    _require_stripe_config()
    success_url = f"{settings.APP_URL.rstrip('/')}/dashboard?checkout=success"
    cancel_url = f"{settings.APP_URL.rstrip('/')}/pricing?checkout=cancelled"

    data = {
        "mode": "subscription",
        "customer_email": email,
        "success_url": success_url,
        "cancel_url": cancel_url,
        "allow_promotion_codes": "true",
        "billing_address_collection": "auto",
        "line_items[0][price]": settings.STRIPE_PRO_PRICE_ID,
        "line_items[0][quantity]": "1",
        "metadata[plan]": "pro",
        "subscription_data[metadata][plan]": "pro",
    }
    if include_trial:
        data["subscription_data[trial_period_days]"] = str(settings.BILLING_TRIAL_DAYS)

    with httpx.Client(timeout=15) as client:
        response = client.post(
            f"{settings.STRIPE_API_URL.rstrip('/')}/v1/checkout/sessions",
            data=data,
            auth=(settings.STRIPE_SECRET_KEY, ""),
        )

    if response.status_code >= 400:
        sentry_sdk.capture_message(
            f"Stripe checkout session rejected: {response.status_code} {response.text[:300]}",
            level="error",
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe rejected the checkout session request.",
        )
    return response.json()


def create_stripe_billing_portal_session(customer_id: str) -> dict:
    """Create a Stripe Customer Portal Session."""
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe billing is not configured.",
        )

    data = {
        "customer": customer_id,
        "return_url": f"{settings.APP_URL.rstrip('/')}/dashboard",
    }

    with httpx.Client(timeout=15) as client:
        response = client.post(
            f"{settings.STRIPE_API_URL.rstrip('/')}/v1/billing_portal/sessions",
            data=data,
            auth=(settings.STRIPE_SECRET_KEY, ""),
        )

    if response.status_code >= 400:
        sentry_sdk.capture_message(
            f"Stripe billing portal session rejected: {response.status_code} {response.text[:300]}",
            level="error",
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe rejected the billing portal request.",
        )
    return response.json()


def _verify_stripe_signature(payload: bytes, signature_header: str | None) -> dict:
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe webhook secret is not configured.",
        )
    if not signature_header:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Stripe signature.")

    parts = {}
    for item in signature_header.split(","):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        parts.setdefault(key, []).append(value)

    timestamp = parts.get("t", [None])[0]
    signatures = parts.get("v1", [])
    if not timestamp or not signatures:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Stripe signature.")

    try:
        signed_at = int(timestamp)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Stripe timestamp.") from exc

    if abs(time.time() - signed_at) > 300:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expired Stripe signature.")

    signed_payload = f"{timestamp}.{payload.decode('utf-8')}".encode("utf-8")
    expected = hmac.new(
        settings.STRIPE_WEBHOOK_SECRET.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    if not any(hmac.compare_digest(expected, signature) for signature in signatures):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Stripe signature.")

    return json.loads(payload)


def _upsert_subscription(
    db: Session,
    *,
    email: str | None,
    status_value: str,
    stripe_customer_id: str | None,
    stripe_subscription_id: str | None,
    stripe_checkout_session_id: str | None = None,
    current_period_end: datetime | None = None,
    trial_end: datetime | None = None,
    cancel_at_period_end: bool = False,
) -> Subscription:
    query = None
    if stripe_subscription_id:
        query = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == stripe_subscription_id
        )
    elif stripe_checkout_session_id:
        query = db.query(Subscription).filter(
            Subscription.stripe_checkout_session_id == stripe_checkout_session_id
        )

    subscription = query.first() if query is not None else None
    if not subscription:
        subscription = Subscription(id=str(uuid4()), status=status_value)
        db.add(subscription)

    if email:
        subscription.email = email
    subscription.status = status_value
    subscription.plan = "pro"
    subscription.stripe_customer_id = stripe_customer_id
    subscription.stripe_subscription_id = stripe_subscription_id or subscription.stripe_subscription_id
    subscription.stripe_checkout_session_id = (
        stripe_checkout_session_id or subscription.stripe_checkout_session_id
    )
    subscription.current_period_end = current_period_end
    subscription.trial_end = trial_end
    subscription.cancel_at_period_end = cancel_at_period_end
    db.commit()
    db.refresh(subscription)
    return subscription


def _subscription_amount(data_object: dict) -> tuple[float, str] | tuple[None, None]:
    items = data_object.get("items", {}).get("data", [])
    price = items[0].get("price", {}) if items else {}
    unit_amount = price.get("unit_amount")
    currency = price.get("currency")
    if unit_amount is None or not currency:
        return None, None
    return unit_amount / 100, currency.upper()


def handle_stripe_event(db: Session, event: dict) -> None:
    """Persist subscription state from relevant Stripe webhook events."""
    event_type = event.get("type")
    event_id = event.get("id") or ""
    data_object = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        new_status = data_object.get("subscription_status") or "trialing"
        subscription = _upsert_subscription(
            db,
            email=data_object.get("customer_email"),
            status_value=new_status,
            stripe_customer_id=data_object.get("customer"),
            stripe_subscription_id=data_object.get("subscription"),
            stripe_checkout_session_id=data_object.get("id"),
        )
        send_capi_event(
            "StartTrial",
            email=subscription.email,
            event_id=event_id,
            event_source_url=f"{settings.APP_URL.rstrip('/')}/pricing",
        )
        send_plausible_event(
            "Trial Started" if new_status == "trialing" else "Checkout Completed",
            path="/pricing",
        )
        return

    if event_type in {"customer.subscription.created", "customer.subscription.updated", "customer.subscription.deleted"}:
        stripe_subscription_id = data_object.get("id")
        previous_status = (
            db.query(Subscription)
            .filter(Subscription.stripe_subscription_id == stripe_subscription_id)
            .first()
        )
        previous_status = previous_status.status if previous_status else None

        new_status = data_object.get("status", "incomplete")
        subscription = _upsert_subscription(
            db,
            email=None,
            status_value=new_status,
            stripe_customer_id=data_object.get("customer"),
            stripe_subscription_id=stripe_subscription_id,
            current_period_end=_utc_from_stripe_timestamp(data_object.get("current_period_end")),
            trial_end=_utc_from_stripe_timestamp(data_object.get("trial_end")),
            cancel_at_period_end=bool(data_object.get("cancel_at_period_end", False)),
        )

        if previous_status == "trialing" and new_status == "active":
            value, currency = _subscription_amount(data_object)
            custom_data = {"currency": currency, "value": value} if value is not None else {}
            send_capi_event(
                "Purchase",
                email=subscription.email,
                event_id=event_id,
                event_source_url=f"{settings.APP_URL.rstrip('/')}/dashboard",
                custom_data=custom_data,
            )
            send_plausible_event("Trial Converted", path="/dashboard")
        elif previous_status == "trialing" and new_status in EXPIRED_TRIAL_STATUSES:
            send_plausible_event("Trial Expired", path="/dashboard", props={"status": new_status})


@router.post("/checkout", response_model=CheckoutSessionResponse)
def create_checkout_session(payload: CheckoutSessionCreate, db: Session = Depends(get_db)):
    """Start a Stripe Checkout subscription. Grants a free trial only the first time an email is seen."""
    previous = (
        db.query(Subscription)
        .filter(Subscription.email == payload.email)
        .order_by(Subscription.created_at.desc())
        .first()
    )
    if previous and previous.status in ACTIVE_SUBSCRIPTION_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have an active subscription for this email. Manage it from your dashboard instead of starting a new trial.",
        )

    session = create_stripe_checkout_session(payload.email, include_trial=previous is None)
    return CheckoutSessionResponse(
        checkout_url=session["url"],
        session_id=session["id"],
    )


@router.post("/portal", response_model=BillingPortalResponse)
def create_billing_portal(
    email: str = Depends(require_session_email),
    db: Session = Depends(get_db),
):
    """Create a Stripe Customer Portal session for the authenticated user's own subscription.

    The email is taken exclusively from the signed session cookie, never from
    the request body -- this used to trust a client-supplied email, which let
    anyone who knew a customer's email address obtain a live link to that
    customer's Stripe billing portal (view invoices, change card, cancel).
    """
    subscription = (
        db.query(Subscription)
        .filter(Subscription.email == email, Subscription.stripe_customer_id.is_not(None))
        .order_by(Subscription.created_at.desc())
        .first()
    )
    if not subscription or not subscription.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Stripe customer found for this email.",
        )

    session = create_stripe_billing_portal_session(subscription.stripe_customer_id)
    return BillingPortalResponse(portal_url=session["url"])


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    """Receive Stripe webhook events and persist subscription state."""
    payload = await request.body()
    event = _verify_stripe_signature(payload, stripe_signature)
    handle_stripe_event(db, event)
    return {"received": True}
