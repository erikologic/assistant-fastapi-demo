from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def instrument(app):
    AioHttpClientInstrumentor().instrument()

    resource = Resource(attributes={SERVICE_NAME: "assistant"})
    trace_provider = TracerProvider(resource=resource)
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    trace_provider.add_span_processor(processor)
    trace.set_tracer_provider(trace_provider)
    FastAPIInstrumentor.instrument_app(app)
