import time
from fastapi import APIRouter, status, Query, HTTPException

from ..services.lnbits import LNBitsService
from ..schemas.lnbits import CreateInvoiceSchema


router = APIRouter(tags=['Funding'])


@router.post(
    '/create_invoice',
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_invoice(request: CreateInvoiceSchema):
    return await LNBitsService.create_invoice(request.amount, request.memo)


@router.get(
    '/check_invoice_payment',
    response_model=dict,
)
async def check_invoice_payment(
    checking_id: str = Query(...),
    checking_sig: str = Query(...),
):
    if not(await LNBitsService.verify_signature(data=checking_id, signature=checking_sig)):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid signature')
        pass

    poll_interval_secs = 5
    max_expiry_timeout_secs = 60*10
    max_error_count = 3
    
    error_count = 0
    is_paid = False
    routine_t0 = time.time()
    
    while (
        (is_paid == False) and 
        (error_count < max_error_count) and
        (time.time() - routine_t0 < max_expiry_timeout_secs)
        ):

        try:
            is_paid = await LNBitsService.check_invoice_payment(checking_id)
        except:
            error_count += 1
            
        if not is_paid:
            time.sleep(poll_interval_secs)

    return {'is_paid': is_paid}