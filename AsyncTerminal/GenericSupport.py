"""
Contains all calls that don't assume a specific environment
    Don't use directly as AsyncTerminal's calls will automatically map to here
"""

class GenericSupport():
    OSEnvironment = "Generic"

    @classmethod
    def setup(cls):
        """
        Configures the support logic
        :returns: A reference to the support class for this environment
        """
        return cls

    @classmethod
    def cleanup(cls):
        """
        Cleans up on exit of AsyncTerminal
            Automatically called by Python on exit thanks to the registration done on package initialization
        """
        raise NotImplementedError()

    @classmethod
    def getChar(cls):
        """
        Blocking IO call to get next character typed as a String
        """
        raise NotImplementedError()