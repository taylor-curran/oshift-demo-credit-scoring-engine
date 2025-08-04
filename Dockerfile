FROM registry.bank.internal/openjdk:17-jre-slim@sha256:abc123def456789

LABEL maintainer="Banking Platform Team <platform@bank.internal>"
LABEL app.kubernetes.io/name="credit-scoring-engine"
LABEL app.kubernetes.io/version="3.1.0"
LABEL app.kubernetes.io/part-of="banking-platform"

RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

WORKDIR /app

COPY --chown=appuser:appuser target/credit-scoring-engine-3.1.0.jar app.jar

RUN mkdir -p /app/cache /tmp && \
    chown -R appuser:appuser /app /tmp && \
    chmod -R 755 /app && \
    chmod -R 1777 /tmp

USER 1001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
