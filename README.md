# Observra GCP log test service

Small Cloud Run service for testing Observra cloud-log monitoring.

Endpoints:

- `/` health check
- `/api/success` structured successful request log
- `/api/error` structured HTTP 500 application error
- `/api/slow-error` delayed structured HTTP 504 error

## Deploy from source

```powershell
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com logging.googleapis.com
gcloud run deploy observra-log-test --source . --region us-central1 --allow-unauthenticated
```

Copy the service URL, then generate logs:

```powershell
curl https://YOUR_SERVICE_URL/
curl https://YOUR_SERVICE_URL/api/success
curl https://YOUR_SERVICE_URL/api/error
curl https://YOUR_SERVICE_URL/api/slow-error
```

In Observra, connect the same Google account, select this GCP project, select `observra-log-test`, then choose `stdout` or `stderr` and start monitoring.

View logs in Google Cloud Logs Explorer:

```text
resource.type="cloud_run_revision"
resource.labels.service_name="observra-log-test"
```
