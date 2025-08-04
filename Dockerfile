FROM registry.bank.internal/openjdk:17-jre-slim@sha256:4f53227f4f272720d5b1a75598a4ab096af27191435d3a9c5ac89f21fdc22d38

RUN groupadd -r creditapp && useradd -r -g creditapp creditapp

RUN mkdir -p /app /tmp /models && \
    chown -R creditapp:creditapp /app /tmp /models

COPY target/credit-scoring-engine-3.1.0.jar /app/app.jar

RUN chown creditapp:creditapp /app/app.jar && \
    chmod 444 /app/app.jar

USER creditapp

WORKDIR /app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
