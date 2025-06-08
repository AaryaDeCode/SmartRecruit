import requests

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def upload_resume(self, file, jd_text):
        url = f"{self.base_url}/api/resumes/upload-resume/"
        files = {"file": (file.name, file, "application/pdf")}
        data = {"job_description": jd_text}
        response = requests.post(url, files=files, data=data)

        try:
            return response.json()
        except Exception as e:
            print("❌ Failed to decode JSON")
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            return {"error": "Could not parse response from server"}

