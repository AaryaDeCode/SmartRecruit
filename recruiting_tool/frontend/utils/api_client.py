import requests
# utils/api_client.py

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def upload_resume(self, filename, file_bytes, jd_text):
        files = {
            "file": (filename, file_bytes, "application/pdf")
        }
        data = {"job_description": jd_text}
        url = f"{self.base_url}/api/resumes/upload-resume/"
        response = requests.post(url, files=files, data=data)

        try:
            return response.json()
        except Exception as e:
            print("❌ Upload failed:", e)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            return {"error": "Upload failed"}
        


    