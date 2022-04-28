import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())
logger.addHandler(AzureEventHandler())
logger.setLevel(logging.DEBUG)
# exporter = AzureExporter()


exporter = AzureMonitorTraceExporter.from_connection_string(
    os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING']
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


def index(request):
    with tracer.start_as_current_span("webApp"):
        with tracer.start_as_current_span('client'):
            logger.debug('Request for index page received')
            return render(request, 'hello_azure/index.html')


@csrf_exempt
def hello(request):
    with tracer.start_as_current_span("webApp"):
        with tracer.start_as_current_span('client'):
            if request.method == 'POST':
                name = request.POST.get('name')

                if name is None or name == '':
                    logger.debug(
                        "Request for hello page received with no name or blank name -- redirecting")
                    return redirect('index')
                else:
                    logger.debug("Request for hello page received with name=%s" % name)
                    context = {'name': name}
                    return render(request, 'hello_azure/hello.html', context)
            else:
                return redirect('index')
