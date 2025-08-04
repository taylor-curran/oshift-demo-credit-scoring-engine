FROM registry.bank.internal/openjdk:17-jre-slim@sha256:aaa91ac49ceb8a0f1d6b40ca4c45c912409e5906229a1eeec5c8a8e793b6b5c5

LABEL maintainer="Platform Engineering <pe@banking.com>"
LABEL app.kubernetes.io/name="credit-scoring-engine"
LABEL app.kubernetes.io/version="3.1.0"
LABEL app.kubernetes.io/part-of="retail-banking"

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY target/credit-scoring-engine-3.1.0.jar app.jar

RUN chown -R appuser:appuser /app && \
    mkdir -p /tmp && \
    chown -R appuser:appuser /tmp

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health/liveness || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
