FROM registry.bank.internal/openjdk:17-jre-slim@sha256:abc123def456789012345678901234567890123456789012345678901234567890

RUN groupadd -r creditapp && useradd -r -g creditapp -u 1001 creditapp

WORKDIR /app

COPY target/credit-scoring-engine-3.1.0.jar app.jar

RUN chown -R creditapp:creditapp /app && \
    mkdir -p /tmp && \
    chown -R creditapp:creditapp /tmp && \
    mkdir -p /models && \
    chown -R creditapp:creditapp /models

USER 1001

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
