# Use the Python image version X.XX as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /Task

# Copy the Gittask.py file from the local machine to the container
ADD Gittask.py .

# Copy the requirements.txt file from the local machine to the container
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 for external connections
EXPOSE 5000

# Define the default command to run when the container starts
CMD ["python", "Gittask.py"]
