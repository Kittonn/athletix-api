from fastapi import APIRouter, HTTPException, status
from ..internal.customer import Customer
from ..internal.account import Account
from ..database import stadium
from ..models.auth import RegisterModel, LoginModel
from ..utils.password import get_password_hash, verify_password
from ..utils.jwt import create_access_token

router = APIRouter(prefix='/auth', tags=['auth'], responses={
                   404: {'description': 'Not found'}})


@router.post('/register')
async def register(body: RegisterModel):
  if stadium.get_user_by_email(body.email) is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Email already exists')

  if stadium.get_user_by_fullname(body.fullname) is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Fullname already exists')

  if stadium.get_user_by_phone_number(body.phone_number) is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Phone number already exists')

  account = Account(password=get_password_hash(body.password))

  person = Customer(fullname=body.fullname, email=body.email, phone_number=body.phone_number, address=body.address, birth_date=body.birth_date,
                    emergency_contact_fullname=body.emergency_contact_fullname, emergency_contact_phone_number=body.emergency_contact_phone_number, account=account)

  new_person = stadium.add_user(person)

  return {
      "access_token": create_access_token(data={"sub": new_person['id']})
  }


@router.post('/login')
async def login(body: LoginModel):
  user = stadium.get_user_by_email(body.email)

  if user is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

  if not verify_password(body.password, user['account']['password']):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Password is incorrect')
    
  return {
      "access_token": create_access_token(data={"sub": user['id']})
  }
