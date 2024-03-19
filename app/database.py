import mysql.connector

class DatabaseConnection:
    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
                host = cls._config['DATABASE_HOST'],
                user = cls._config['DATABASE_USERNAME'],
                port = cls._config['DATABASE_PORT'],
                password = cls._config['DATABASE_PASSWORD']
            )
        
        return cls._connection
    

    @classmethod
    def set_config(cls, config):
        cls._config = config
    
    # @classmethod
    # def execute_query(cls, query, database_name=None, params=None):
    #     cursor = cls.get_connection().cursor()
    #     cursor.execute(query, params)
    #     cls._connection.commit()
    #     return cursor
    
    @classmethod
    def execute_query(cls, query, database_name=None, params=None):
        
        cursor = cls.get_connection().cursor()

        try:
            # cls._connection.reconnect()
            cursor.execute(query, params)
            # Use nextset to move to the next result set if available
            while cursor.nextset():
                # cursor= cls.close_connection()
                # cursor= cls.get_connection().cursor()
                pass  # Consume remaining result sets, if any
        except Exception as e:
            cls._connection.rollback()
            raise e  # Re-raise the exception after rollback
        else:
            cls._connection.commit()

        return cursor
    
    # @classmethod
    # def fetch_all(cls, query, database_name=None, params=None):
    #     cursor = cls.get_connection().cursor()
    #     cursor.execute(query, params)
    #     return cursor.fetchall()



    # @classmethod
    # def fetch_all(cls, query, database_name=None, params=None):
    #     cursor = cls.get_connection().cursor()

    #     try:
    #         cursor.execute(query, params)
    #         result = cursor.fetchall()
            
    #         # Fetch all remaining result sets and discard them
    #         while cursor.nextset():
    #             pass

    #     except Exception as e:
    #         cls._connection.rollback()
    #         raise e  # Re-raise the exception after rollback
    #     else:
    #         # Make sure to fetch and discard any remaining result sets after fetching the results
    #         while cursor.nextset():
    #             pass
    #         cls._connection.commit()

    #     return result

    @classmethod
    def fetch_all(cls, query, database_name=None, params=None):
        cursor = cls.get_connection().cursor()
        

        try:
            # cls._connection.reconnect()
            cursor.execute(query, params)
            result = cursor.fetchall()
          
            cursor.close()
            cursor= cls.get_connection().cursor()
            
            
            # Make sure to fetch and discard any remaining result sets
            while cursor.nextset():
                cursor.fetchall()
                # cursor.close()
                cursor= cls.close_connection()
                cursor= cls.get_connection().cursor()

        except Exception as e:
            cls._connection.rollback()
            raise e  # Re-raise the exception after rollback
        else:
            cls._connection.commit()

        return result

    # @classmethod
    # def fetch_one(cls, query, database_name=None, params=None):
    #     cursor = cls.get_connection().cursor()
    #     cursor.execute(query, params)
    #     return cursor.fetchone()



    @classmethod
    def fetch_one(cls, query, database_name=None, params=None):
        cursor= cls.get_connection().cursor()
        
        # cursor = cls.get_connection().cursor(buffered=True)
        #print(cls._connection.is_connected())
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            #cursor.close()
            
            #cursor= cls.close_connection()
            # # print("close conx")
            
            
            # print("get conx")
            #Fetch all remaining result sets and discard them
            # while cursor.nextset():
                
               
            #     pass
            cursor= cls.close_connection()
            cursor= cls.get_connection().cursor() 
            #cursor.close()
            # # # print("close conx")
            # cursor= cls.get_connection().cursor() 
            
            # print("get conx")

        except Exception as e:
             
            #cls._connection.rollback()
            #cursor= cls.close_connection()
           
            raise e  # Re-raise the exception after rollback
        else:
            cls._connection.commit()

        return result
    
    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
#--------------------------                
    # @classmethod
    # def set_config(cls, config):
    #     cls._config = config

    # @classmethod
    # def execute_query(cls, query, params=None):
    #     with cls.get_connection().cursor() as cursor:
    #         cursor.execute(query, params)
    #     cls._connection.commit()

    # @classmethod
    # def fetch_all(cls, query, params=None):
    #     with cls.get_connection().cursor() as cursor:
    #         cursor.execute(query, params)
    #         return cursor.fetchall()

    # @classmethod
    # def fetch_one(cls, query, params=None):
    #     with cls.get_connection().cursor() as cursor:
    #         cursor.execute(query, params)
    #         return cursor.fetchone()

    # @classmethod
    # def close_connection(cls):
    #     if cls._connection is not None:
    #         cls._connection.close()
    #         cls._connection = None
            
#-----------------------------            
# class DatabaseConnection:
#     _connection = None

#     @classmethod
#     def get_connection(cls):
#         if cls._connection is None:
#             cls._connection = mysql.connector.connect(
#                 host='127.0.0.1',
#                 user='root',
#                 port = "3306",
#                 password='root',
#                 database='chatnet'
#                 )
#         return cls._connection

#     @classmethod
#     def execute_query(cls, query, params=None):
#         cursor = cls.get_connection().cursor()
#         cursor.execute(query, params)
#         cls._connection.commit()
#         return cursor
    
#     @classmethod
#     def fetch_one(cls, query, params=None):
#         cursor = cls.get_connection().cursor()
#         cursor.execute(query, params)
#         return cursor.fetchone()
    
#     @classmethod
#     def fetch_all(cls, query, params=None):
#         cursor = cls.get_connection().cursor()
#         cursor.execute(query, params)
#         return cursor.fetchall()
    
#     @classmethod
#     def close_connection(cls):
#         if cls._connection is not None:
#             cls._connection.close()
#             cls._connection = None