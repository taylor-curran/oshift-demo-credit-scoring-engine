FROM registry.bank.internal/openjdk:17-jre-slim@sha256:4b972d1b8c8e8b8f8c8e8b8f8c8e8b8f8c8e8b8f8c8e8b8f8c8e8b8f8c8e8b8f

RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

WORKDIR /app

COPY target/credit-scoring-engine-3.1.0.jar app.jar

RUN mkdir -p /app/logs /tmp && \
    chown -R appuser:appuser /app /tmp

USER 1001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health/liveness || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
