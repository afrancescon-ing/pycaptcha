class PersistenceManagerInterface:
    """_summary_
    """

    def __init__(self):
        pass

    def push(self, uuid: str, value: str):
        """ Push a couple uuid-value into the persistence manager

        Args:
            uuid (str): unique identifier of the value
            value (str): value
        
        Returns:
            bool: the response of the pushing operation:
                  True if successful, False otherwise
        """
        return False

    def pop(self, uuid: str):
        """ Removes the couple id-value associated with the given uuid
            Returns the removed value

        Args:
            uuid (str): unique identifier for the entry

        Returns:
            Union (str | None): the removed value
        """
        return None