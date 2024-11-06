# frontend/Dockerfile

# Use an official Node runtime as a parent image
FROM node:16-alpine

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json /app/
RUN npm install

# Copy project files
COPY . /app/

# Build the app
RUN npm run build

# Install serve to serve the build
RUN npm install -g serve

# Expose the port
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]
