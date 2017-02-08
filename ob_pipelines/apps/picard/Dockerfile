FROM openjdk:8

RUN apt-get update && apt-get install -y python-pip
RUN pip install boto3

# Install Picard
ADD https://github.com/broadinstitute/picard/releases/download/2.8.3/picard.jar /

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "java", "-jar", "/picard.jar"]