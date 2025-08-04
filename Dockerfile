FROM registry.access.redhat.com/ubi8/openjdk-17

USER root

RUN microdnf install -y python3 python3-pip && \
    microdnf clean all

COPY target/credit-scoring-engine-3.1.0.jar /deployments/app.jar

RUN chown -R 1001:0 /deployments && \
    chmod -R g+rw /deployments

USER 1001

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/deployments/app.jar"]
