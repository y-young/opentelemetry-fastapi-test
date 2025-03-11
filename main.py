import os
from typing import Any
from opentelemetry.trace import Span

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


os.environ["OTEL_SEMCONV_STABILITY_OPT_IN"] = "http"

resource = Resource(attributes={SERVICE_NAME: "test-app"})

tracerProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def server_request_hook(span: Span, scope: dict[str, Any]):
    print("Scope:", scope)


FastAPIInstrumentor.instrument_app(app, server_request_hook=server_request_hook)
