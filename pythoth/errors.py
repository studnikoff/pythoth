"""
Custom exceptions
"""


class StrategyError(Exception):
    """Raises when instance is not Strategy object
    """    
    pass


class NoSignatureFileError(Exception):
    """Raises when there is no excel file on path
    """
    pass


class SignatureColumnsError(Exception):
    """Raises when format_type columns is absent
    """
    pass