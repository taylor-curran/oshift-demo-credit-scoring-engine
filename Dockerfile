FROM registry.access.redhat.com/ubi8/openjdk-17:1.16

LABEL name="credit-scoring-engine" \
      version="3.1.0" \
      description="Credit Scoring Engine for OpenShift"

USER root

RUN microdnf install -y python3 python3-pip && \
    microdnf clean all

COPY target/credit-scoring-engine-3.1.0.jar /deployments/app.jar

RUN mkdir -p /models /tmp && \
    chown -R 1001:0 /models /tmp && \
    chmod -R g+rwX /models /tmp

USER 1001

ENV JAVA_OPTS="-Xmx1536m -XX:+UseG1GC -XX:+UseStringDeduplication"

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/deployments/app.jar"]
