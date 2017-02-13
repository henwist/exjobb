import abc

class AbstractBus:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def read(self):
   raise NotImplementedError("Class %s doesn't implement " %(self.__class__.__name__))

  @abc.abstractmethod
  def write(self):
   raise NotImplementedError("Class %s doesn't implement " %(self.__class__.__name__))

class I2CBus(AbstractBus):

    def read(self):
        pass

    def write(self):
        pass


