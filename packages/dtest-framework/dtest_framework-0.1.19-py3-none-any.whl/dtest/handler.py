from abc import ABCMeta, abstractmethod

class MqHandler:

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def connect(self): raise NotImplementedError

    @abstractmethod
    def publishResults(self): raise NotImplementedError

    @abstractmethod
    def closeConnection(self): raise NotImplementedError


class KvHandler:
    
    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def retrieve(self): raise NotImplementedError

    @abstractmethod
    def publish(self): raise NotImplementedError
