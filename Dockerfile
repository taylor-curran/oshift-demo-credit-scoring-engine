FROM registry.bank.internal/openjdk:17-jre-slim

# Create non-root user
RUN groupadd -r creditapp && useradd -r -g creditapp -u 1001 creditapp

# Create necessary directories with proper permissions
RUN mkdir -p /app /tmp /app/logs /models && \
    chown -R creditapp:creditapp /app /tmp /app/logs /models

# Copy application jar
COPY --chown=creditapp:creditapp target/credit-scoring-engine-3.1.0.jar /app/app.jar

# Switch to non-root user
USER 1001

# Set working directory
WORKDIR /app

# Expose ports
EXPOSE 8080 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8081/actuator/health/liveness || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
