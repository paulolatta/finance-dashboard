from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])


def to_read(account: Account) -> AccountRead:
    return AccountRead(
        id=str(account.id),
        name=account.name,
        type=account.type,
        initial_balance=account.initial_balance,
        created_at=account.created_at,
    )


@router.get("/", response_model=list[AccountRead])
async def list_accounts(current_user: User = Depends(get_current_user)):
    accounts = await Account.find(Account.user_id == str(current_user.id)).to_list()
    return [to_read(a) for a in accounts]


@router.get("/{account_id}", response_model=AccountRead)
async def get_account(account_id: str, current_user: User = Depends(get_current_user)):
    account = await Account.get(account_id)
    if account is None or account.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return to_read(account)


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(payload: AccountCreate, current_user: User = Depends(get_current_user)):
    account = Account(**payload.model_dump(), user_id=str(current_user.id))
    await account.insert()
    return to_read(account)


@router.patch("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: str,
    payload: AccountUpdate,
    current_user: User = Depends(get_current_user),
):
    account = await Account.get(account_id)
    if account is None or account.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)

    await account.save()
    return to_read(account)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: str, current_user: User = Depends(get_current_user)):
    account = await Account.get(account_id)
    if account is None or account.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    await account.delete()