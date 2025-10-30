# Feature: Automatic Content Downloader

## 1. Purpose

The `Content Downloader` feature is responsible for automatically downloading new or updated educational books and videos when an internet connection is available. This ensures the kiosk always has up-to-date content without manual intervention.

## 2. User Story

As an administrator, I want the system to automatically download new books and videos when connected to the internet, so that the content is always up-to-date without manual effort.

## 3. Expected Behavior/Outcome

The system periodically checks for an internet connection. If available, it connects to a pre-configured content source, downloads new or updated books and videos, and stores them locally in the `/content/books` and `/content/videos` directories. The process should be robust and handle network interruptions gracefully.

## 4. Detailed Implementation Plan

* **Configuration Schema**: Add to `app_config.json` a "content" section with:
  * "source_url": string URL for the content API endpoint
  * "check_interval_hours": number (e.g., 24 for daily checks)
  * "timeout_seconds": number for download timeouts
  * "enabled": boolean to toggle automatic downloads

* **Background Service**: Implement a threaded background process in `app.py` that starts a timer-based loop for periodic content checks. The thread will run independently from the main UI loop.

* **Modular Downloader Class**: Create `src/content_downloader.py` with a `ContentDownloader` class that:
  * Handles HTTP/HTTPS requests using `requests` library
  * Processes JSON responses with content lists and metadata
  * Supports extensible source types (currently HTTP API, configurable for FTP or other protocols)

* **Versioning and Comparison Logic**: Implement MD5 hash comparison to determine if local files differ from remote versions. Store local hash metadata in `content/local_metadata.json` to track versions and avoid unnecessary re-downloads.

* **Graceful Error Handling**: Include retry mechanisms for network failures, proper exception handling for invalid responses, and automatic resumption after interruptions.

* **Logging System**: Add console logging with timestamps for download operations, errors, and success confirmations. This aids debugging and monitoring.

## 5. Main Components

### src/content_downloader.py
This module contains the core downloading logic, including:
- Network connectivity checks
- API communication and data retrieval
- File download and local storage
- Metadata management for versioning

### Updated src/app.py
Integrates the background downloader thread and manages configuration loading.

### Updated config/app_config.json
Contains the content source configuration.

## 6. Configuration Example

```json
{
  "content": {
    "source_url": "https://api.content-provider.com/v1/list",
    "check_interval_hours": 24,
    "timeout_seconds": 60,
    "enabled": true
  }
}
```

## 7. Acceptance Criteria

* [x] A new configuration option exists in `app_config.json` for the content source.
* [x] The application can successfully connect to the specified source and download a sample file.
* [x] Downloaded files are correctly placed in their respective `/content` subdirectories.
* [x] The system does not re-download existing files unless they have been updated remotely.
* [x] The download process runs in the background without blocking the main UI.

## 8. Usage Example

Once enabled in the configuration, the downloader will automatically:
1. Check for internet connectivity
2. Query the content API for available files
3. Download only new or changed content
4. Log all operations to the console
5. Repeat the cycle based on the configured interval
