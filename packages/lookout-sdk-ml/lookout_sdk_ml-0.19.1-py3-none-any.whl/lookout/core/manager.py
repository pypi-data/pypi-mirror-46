import logging
from typing import Iterable, Optional, Sequence

from google.protobuf.struct_pb2 import ListValue as ProtobufList
from google.protobuf.struct_pb2 import Struct as ProtobufStruct

from lookout.core.analyzer import Analyzer, AnalyzerModel, DummyAnalyzerModel, ReferencePointer
from lookout.core.api.event_pb2 import PushEvent, ReviewEvent
from lookout.core.api.service_analyzer_pb2 import EventResponse
from lookout.core.data_requests import DataService
from lookout.core.event_listener import EventHandlers
from lookout.core.metrics import submit_event
from lookout.core.model_repository import ModelRepository
from lookout.core.ports import Type


class AnalyzerManager(EventHandlers):
    """
    Manages several `Analyzer`-s: runs them and trains the models.

    Relies on a `ModelRepository` to retrieve and update the models. Also requires the address
    of the data (UAST, contents) gRPC service, typically running in the same Lookout server.
    """

    _log = logging.getLogger("AnalyzerManager")

    def __init__(self, analyzers: Iterable[Type[Analyzer]], model_repository: ModelRepository,
                 data_service: DataService):
        """
        Initialize a new instance of the AnalyzerManager class.

        :param analyzers: Analyzer types to manage (not instances!).
        :param model_repository: Injected implementor of the `ModelRepository` interface.
        :param data_service: gRPC data retrieval service to fetch UASTs and files.
        """
        self._model_repository = model_repository
        analyzers = [(a.__name__, a) for a in analyzers]
        analyzers.sort()
        self._analyzers = [a[1] for a in analyzers]
        self._data_service = data_service

    def __str__(self) -> str:
        """Summarize AnalyzerManager as a string."""
        return "AnalyzerManager(%s)" % self.version

    @property
    def version(self) -> str:
        """
        Return the version string that depends on all the managed analyzers.
        """
        return " ".join(self._model_id(a) for a in self._analyzers)

    def process_review_event(self, request: ReviewEvent) -> EventResponse:  # noqa: D401
        """
        Callback for review events invoked by EventListener.
        """
        base_ptr = ReferencePointer.from_pb(request.commit_revision.base)
        head_ptr = ReferencePointer.from_pb(request.commit_revision.head)
        response = EventResponse()
        response.analyzer_version = self.version
        comments = []
        for analyzer in self._analyzers:
            try:
                mycfg = self._protobuf_struct_to_dict(request.configuration[analyzer.name])
                self._log.info("%s config: %s", analyzer.name, mycfg)
            except (KeyError, ValueError):
                mycfg = {}
                self._log.debug("no config was provided for %s", analyzer.name)
            if analyzer.model_type != DummyAnalyzerModel:
                model = self._get_model(analyzer, base_ptr.url)
                if model is None:
                    self._log.info("training: %s", analyzer.name)
                    submit_event("%s.train" % analyzer.name, 1)
                    model = analyzer.train(base_ptr, mycfg, self._data_service)
                    self._model_repository.set(self._model_id(analyzer), base_ptr.url, model)
            else:
                model = DummyAnalyzerModel()
            self._log.debug("running %s", analyzer.name)
            submit_event("%s.analyze" % analyzer.name, 1)
            results = analyzer(model, head_ptr.url, mycfg).analyze(
                base_ptr, head_ptr, self._data_service)
            self._log.info("%s: %d comments", analyzer.name, len(results))
            submit_event("%s.comments" % analyzer.name, len(results))
            comments.extend(results)
        response.comments.extend(comments)
        return response

    def process_push_event(self, request: PushEvent) -> EventResponse:  # noqa: D401
        """
        Callback for push events invoked by EventListener.
        """
        ptr = ReferencePointer.from_pb(request.commit_revision.head)
        data_service = self._data_service
        for analyzer in self._analyzers:
            if analyzer.model_type == DummyAnalyzerModel:
                continue
            try:
                mycfg = self._protobuf_struct_to_dict(request.configuration[analyzer.name])
            except (KeyError, ValueError):
                mycfg = {}
            model = self._get_model(analyzer, ptr.url)
            if model is not None:
                must_train = analyzer.check_training_required(model, ptr, mycfg, data_service)
                if not must_train:
                    self._log.info("skipped training %s", analyzer.name)
                    continue
            self._log.debug("training %s", analyzer.name)
            submit_event("%s.train" % analyzer.name, 1)
            model = analyzer.train(ptr, mycfg, data_service)
            self._model_repository.set(self._model_id(analyzer), ptr.url, model)
        response = EventResponse()
        response.analyzer_version = self.version
        return response

    def warmup(self, urls: Sequence[str]):
        """
        Warm up the model cache (which supposedly exists in the injected `ModelRepository`). \
        We get the models corresponding to the managed analyzers and the specified list of \
        repositories.

        :param urls: The list of Git repositories for which to fetch the models.
        """
        self._log.info("warming up on %d urls", len(urls))
        for url in urls:
            for analyzer in self._analyzers:
                self._model_repository.get(self._model_id(analyzer), analyzer.model_type, url)

    @staticmethod
    def _model_id(analyzer: Type[Analyzer]) -> str:
        return "%s/%s" % (analyzer.name, analyzer.version)

    @staticmethod
    def _protobuf_struct_to_dict(configuration: ProtobufStruct) -> dict:
        mycfg = dict(configuration)
        stack = [mycfg]
        while stack:
            d = stack.pop()
            if isinstance(d, dict):
                keyiter = iter(d)
            elif isinstance(d, list):
                keyiter = range(len(d))
            else:
                keyiter = []
            for key in keyiter:
                if isinstance(d[key], ProtobufStruct):
                    d[key] = dict(d[key])
                    stack.append(d[key])
                elif isinstance(d[key], ProtobufList):
                    d[key] = list(d[key])
                    stack.append(d[key])
                else:
                    if isinstance(d[key], float) and d[key].is_integer():
                        d[key] = int(d[key])
        return mycfg

    def _get_model(self, analyzer: Type[Analyzer], url: str) -> Optional[AnalyzerModel]:
        model, cache_miss = self._model_repository.get(
            self._model_id(analyzer), analyzer.model_type, url)
        if cache_miss:
            self._log.info("cache miss: %s", analyzer.name)
        return model
