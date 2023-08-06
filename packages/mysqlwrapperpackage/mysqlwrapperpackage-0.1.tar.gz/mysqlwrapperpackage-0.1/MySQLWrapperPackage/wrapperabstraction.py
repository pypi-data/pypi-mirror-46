from abc import ABC, abstractmethod 

class MySQLWrapperAbstract(ABC):

    @abstractmethod
    def start():
        pass

    @abstractmethod
    def create_table(self, table_name, columns):
        pass

    @abstractmethod
    def insert_values(self, table, columns, values):
        pass

    @abstractmethod
    def fetch_all(self, table):
        pass

    @abstractmethod
    def fetch_limit(self, table, value):
        pass
    
    @abstractmethod
    def fetch_columns(self, table):
        pass
    
    @abstractmethod
    def update_table(self, table, column, new_value, conditional_column, conditional_value):
        pass
    
    @abstractmethod
    def delete_records(self, table, conditional_column, conditional_value):
        pass
    
    @abstractmethod
    def delete_table(self, table):
        pass
