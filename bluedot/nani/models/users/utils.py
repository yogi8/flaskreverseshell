from passlib.hash import pbkdf2_sha512


class Utils:

    @staticmethod
    def hash_password(password):
        """
        :param password: The sha512 password as input parameter
        :return: reurns A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        :param password: hashed password as input parameter
        :param hashed_password: pbkdf2_sha512 password from database against that user
        :return: reuturns True if matches else False.
        """
        return pbkdf2_sha512.verify(password, hashed_password)