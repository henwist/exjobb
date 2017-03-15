import abc

class AbstractBus:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def read(self):
   raise NotImplementedError("Class %s doesn't implement " %(self.__class__.__name__))

  @abc.abstractmethod
  def write(self):
   raise NotImplementedError("Class %s doesn't implement " %(self.__class__.__name__))

  @abc.abstractmethod
  def type(self):
      raise NotImplementedError("Class %s doesn't implement " %(self.__class__.__name__))
