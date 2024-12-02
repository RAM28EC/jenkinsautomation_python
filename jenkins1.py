#pip install python-jenkins
import jenkins

# Jenkins Server Details
JENKINS_URL = "http://your-jenkins-url:8080"
USERNAME = "your-username"
API_TOKEN = "your-api-token"

# Jenkins Job Name
JOB_NAME = "example-job"

# Initialize Jenkins Server Connection
def connect_to_jenkins():
    try:
        server = jenkins.Jenkins(JENKINS_URL, username=USERNAME, password=API_TOKEN)
        user_info = server.get_whoami()
        version = server.get_version()
        print(f"Connected to Jenkins (Version: {version}) as {user_info['fullName']}")
        return server
    except Exception as e:
        print(f"Error connecting to Jenkins: {e}")
        return None

# Trigger a Jenkins Job
def trigger_job(server, job_name, params=None):
    try:
        if params:
            server.build_job(job_name, parameters=params)
        else:
            server.build_job(job_name)
        print(f"Job '{job_name}' triggered successfully.")
    except Exception as e:
        print(f"Error triggering job '{job_name}': {e}")

# Get Build Status
def get_build_status(server, job_name):
    try:
        last_build_number = server.get_job_info(job_name)['lastBuild']['number']
        build_info = server.get_build_info(job_name, last_build_number)
        print(f"Job '{job_name}' - Build #{last_build_number} Status: {build_info['result']}")
    except Exception as e:
        print(f"Error fetching build status: {e}")

# Create a New Job
def create_job(server, job_name, config_xml):
    try:
        server.create_job(job_name, config_xml)
        print(f"Job '{job_name}' created successfully.")
    except Exception as e:
        print(f"Error creating job '{job_name}': {e}")

# Main Function
def main():
    # Connect to Jenkins
    server = connect_to_jenkins()
    if not server:
        return

    # Trigger the job (optional parameters can be passed as a dictionary)
    trigger_job(server, JOB_NAME, params={"BRANCH": "main", "ENV": "staging"})

    # Wait for some time before checking the status (optional)
    import time
    time.sleep(10)

    # Get the status of the last build
    get_build_status(server, JOB_NAME)

if __name__ == "__main__":
    main()
