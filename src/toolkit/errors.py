class ToolkitError(Exception):
    pass

class EmptyExpressionError(ToolkitError):
    pass

class InvalidCharacterError(ToolkitError):
    pass

class MissingOperandError(ToolkitError):
    pass

class DivisionByZeroError(ToolkitError):
    pass

class UnknownUnitError(ToolkitError):
    pass

class IncompatibleUnitsError(ToolkitError):
    pass

class AbsoluteZeroError(ToolkitError):
    pass

class InvalidNumericValueError(ToolkitError):
    pass