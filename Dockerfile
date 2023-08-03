# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory to the working directory in the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir flask pandas

# Expose the port on which the Flask app will run (you can change this to match your app)
EXPOSE 5000

# Start the Flask app when the container starts
CMD ["python", "app.py"]
