import hashlib
import json
import datetime
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from app.models import IdempotencyRecord, UsageBucket

def compute_body_hash(data: Any) -> str:
    if not data:
        return hashlib.sha256(b"").hexdigest()
    if isinstance(data, dict):
        raw = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
    elif isinstance(data, str):
        raw = data.encode("utf-8")
    else:
        raw = str(data).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def check_idempotency(
    scope_key: str,
    actor_uid: str,
    key: str,
    db: Session
) -> Optional[Dict[str, Any]]:
    """Check if a valid, unexpired idempotency record exists."""
    now = datetime.datetime.now(datetime.timezone.utc)
    rec = db.query(IdempotencyRecord).filter(
        IdempotencyRecord.scope_key == scope_key,
        IdempotencyRecord.actor_uid == actor_uid,
        IdempotencyRecord.key == key
    ).first()

    if rec:
        rec_exp = rec.expires_at
        if rec_exp is not None:
            if rec_exp.tzinfo is None:
                rec_exp = rec_exp.replace(tzinfo=datetime.timezone.utc)
            if rec_exp <= now:
                return None
        return {
            "status_code": rec.response_code,
            "data": rec.response_body
        }
    return None

def save_idempotency(
    scope_key: str,
    actor_uid: str,
    key: str,
    workspace_id: Any,
    method: str,
    path: str,
    body_data: Any,
    response_code: int,
    response_body: Any,
    db: Session,
    ttl_minutes: int = 60
):
    """Store response in idempotency record."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(minutes=ttl_minutes)
    body_hash = compute_body_hash(body_data)

    # Ensure clean json serializable dict
    if isinstance(response_body, dict):
        clean_response = json.loads(json.dumps(response_body, default=str))
    else:
        clean_response = response_body

    existing = db.query(IdempotencyRecord).filter(
        IdempotencyRecord.scope_key == scope_key,
        IdempotencyRecord.actor_uid == actor_uid,
        IdempotencyRecord.key == key
    ).first()

    if existing:
        existing.response_code = response_code
        existing.response_body = clean_response
        existing.expires_at = expires_at
    else:
        rec = IdempotencyRecord(
            scope_key=scope_key,
            actor_uid=actor_uid,
            key=key,
            workspace_id=workspace_id,
            method=method,
            path=path,
            body_hash=body_hash,
            response_code=response_code,
            response_body=response_body,
            expires_at=expires_at
        )
        db.add(rec)
    db.commit()

def record_usage_bucket(
    scope_key: str,
    kind: str,
    db: Session
):
    """Increment usage bucket count for rate-limiting and audit tracking."""
    now = datetime.datetime.now(datetime.timezone.utc)
    # Align to 1-minute bucket start
    bucket_start = now.replace(second=0, microsecond=0)

    bucket = db.query(UsageBucket).filter(
        UsageBucket.scope_key == scope_key,
        UsageBucket.bucket_start == bucket_start,
        UsageBucket.kind == kind
    ).first()

    if bucket:
        bucket.count += 1
    else:
        bucket = UsageBucket(
            scope_key=scope_key,
            bucket_start=bucket_start,
            kind=kind,
            count=1
        )
        db.add(bucket)
    db.commit()
