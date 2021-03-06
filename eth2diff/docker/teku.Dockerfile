FROM ubuntu:18.04 AS build

ARG GIT_BRANCH="master"
ARG PRESET="preset_mainnet"

# Update ubuntu
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		ca-certificates \
		git \
		unzip \
		curl

# Install JAVA
RUN apt-get update && \
	apt-get install -y \
		openjdk-11-jdk

WORKDIR /app

RUN git clone \
	--branch "$GIT_BRANCH" \
	--depth 1 \
	https://github.com/PegaSysEng/teku.git

RUN cd teku && \
	# Build Teku
	./gradlew installDist

#
# Exporting compiled binaries 
#
FROM scratch AS export

# Copy over the CLI and libraries from the build phase
COPY --from=build /app/teku/build/install/teku .
