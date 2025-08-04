FROM registry.bank.internal/openjdk:17-jre-slim@sha256:9b9b7f3d2cae0c87baf6bffcb23bae2cee5eb5d91b28fd9f6af4cdcb6e9de671

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
