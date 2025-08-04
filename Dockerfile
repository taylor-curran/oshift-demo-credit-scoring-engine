FROM registry.access.redhat.com/ubi8/openjdk-17:1.18

USER root

# Install Python 3.9 for multi-buildpack support (Java + Python)
RUN microdnf install -y python39 python39-pip && \
    microdnf clean all

USER 185

COPY target/credit-scoring-engine-3.1.0.jar /deployments/app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/deployments/app.jar"]
