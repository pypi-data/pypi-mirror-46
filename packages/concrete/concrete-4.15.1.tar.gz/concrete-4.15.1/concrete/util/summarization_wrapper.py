from ..summarization import (
    SummarizationService)
from .service_wrapper import (
    ConcreteServiceClientWrapper,
    ConcreteServiceWrapper,
    HTTPConcreteServiceClientWrapper,
    SubprocessConcreteServiceWrapper)


SummarizationClientWrapper = type(
    'SummarizationClientWrapper',
    (ConcreteServiceClientWrapper,),
    {'concrete_service_class': SummarizationService})


HTTPSummarizationClientWrapper = type(
    'HTTPSummarizationClientWrapper',
    (HTTPConcreteServiceClientWrapper,),
    {'concrete_service_class': SummarizationService})


SummarizationServiceWrapper = type(
    'SummarizationServiceWrapper',
    (ConcreteServiceWrapper,),
    {'concrete_service_class': SummarizationService})


SubprocessSummarizationServiceWrapper = type(
    'SubprocessSummarizationServiceWrapper',
    (SubprocessConcreteServiceWrapper,),
    {'concrete_service_wrapper_class': SummarizationServiceWrapper})
