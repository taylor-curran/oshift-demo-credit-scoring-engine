FROM registry.bank.internal/openjdk:17-jre-slim

# Create non-root user for security compliance (Rule 02)
RUN groupadd -r creditapp && useradd -r -g creditapp -u 1001 creditapp

# Set working directory
WORKDIR /app

# Copy the JAR file
COPY target/credit-scoring-engine-3.1.0.jar app.jar

# Create necessary directories with proper permissions
RUN mkdir -p /tmp /models && \
    chown -R creditapp:creditapp /app /tmp /models

# Switch to non-root user
USER 1001:1001

# Expose port
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
