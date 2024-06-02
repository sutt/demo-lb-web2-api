class LNBitsException(Exception):
    """LNBits base exception"""
    pass


class CouldNotCreateInvoice(LNBitsException):
    pass


class CouldNotCheckInvoicePayment(LNBitsException):
    pass


class CheckingSignatureInvalid(LNBitsException):
    pass