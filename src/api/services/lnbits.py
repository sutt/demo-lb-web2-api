import io
import base64
import qrcode
import httpx
from hashlib import sha256

from ..exceptions.lnbits import CouldNotCreateInvoice, CouldNotCheckInvoicePayment


def gen_qr_code(data: str) -> str:
    
    qr_pil = qrcode.make(data)
    
    buf = io.BytesIO()
    
    qr_pil.save(buf)
    
    qr_base64 = base64.b64encode(buf.getvalue())
    
    return qr_base64.decode('ascii')


class LNBitsService:
    _base_url: str
    _invoice_key: str
    _callback_secret: str

    @classmethod
    def init(cls, base_url: str, invoice_key: str, callback_secret: str):
        cls._base_url = base_url
        cls._invoice_key = invoice_key
        cls._callback_secret = callback_secret

    @classmethod
    async def create_invoice(cls, amount: int, memo: str = '', expiry_secs: int = 60*10) -> dict:
        headers = {
            'X-Api-Key': cls._invoice_key, 
            'Content-Type': 'application/json',
        }

        body = {
            'out': False,
            'amount': amount,
            'memo': memo,
            'expiry': expiry_secs, 
            'unit': 'sat', 
            # 'webhook': <url:string>, 
            # 'internal': <bool>,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{cls._base_url}/payments', headers=headers, json=body)

            if response.status_code >= 400:
                raise CouldNotCreateInvoice
            
        response_json = response.json()

        qr_uri = gen_qr_code(response_json['payment_request'])

        checking_sig = await cls.sign_data(response_json['checking_id'])

        return {
            'payment_request': response_json['payment_request'],
            'checking_id': response_json['checking_id'],
            'checking_sig': checking_sig,
            'qr_uri': qr_uri,

        }
    
    @classmethod
    async def check_invoice_payment(cls, checking_id: str,) -> bool:
        
        headers = {
            "X-Api-Key": cls._invoice_key,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{cls._base_url}/payments/{checking_id}', 
                headers=headers, 
            )

            if response.status_code >= 400:
                raise CouldNotCheckInvoicePayment
            
        response_json = response.json()
        
        return response_json.get('paid', False)
            
    @classmethod
    async def sign_data(cls, data: str) -> str:
        """
        Prepend the callback_secret to the data and hash it using SHA-256
        """
        return sha256(cls._callback_secret.encode() + data.encode()).hexdigest()
    
    @classmethod
    async def verify_signature(cls, data: str, signature: str) -> bool:
        """
        Verify signature is the result of hashing the callback_secret and data
        """
        return signature == await cls.sign_data(data)