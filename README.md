# Security-Information-and-Event-Management
A Security Information and Event Management (SIEM) tool from scratch is a fantastic way to understand how log parsing, threat detection, and real-time monitoring work under the hood.

A full-scale SIEM (like Splunk or ELK) requires complex databases, distributed agents, and advanced correlation engines. However, for a simple Python project, we can build a lightweight desktop application using tkinter that simulates log ingestion, applies basic detection rules, and generates alerts.

**How This Code Works**

**The Interface (_build_ui):**

Tkinter is used to split the screen into two main ScrolledText areas. The left is the "Raw Logs" (simulating something like /var/log/syslog or Windows Event Viewer), and the right is the "Alerts" dashboard.

**Threading (start_monitoring):**

If you run an infinite loop in Tkinter (like constantly waiting for logs), the GUI will freeze. To prevent this, the ingest_logs method is pushed to a background threading.Thread.

**Thread-Safe Updates (write_log / _insert_text):**

Tkinter is not thread-safe. You cannot directly modify a Tkinter widget from a background thread without risking a crash. The code uses self.after(0, ...) to safely schedule GUI updates on the main Tkinter thread.

**The Detection Engine (threat_signatures):**

This is the core of a SIEM. It compares incoming log strings against a predefined list of signatures. If a match is found (e.g., "brute force"), it triggers a visual alert in the right panel.

**How to Expand This for a Resume Project**

If you want to turn this simple mockup into a robust project to put on your resume, consider adding the following features:

**Real File Ingestion:**

Instead of using the random ingest_logs() simulator, use Python's open(file, 'r') combined with file.seek(0, 2) and file.readline() to "tail" an actual log file on your computer (like /var/log/auth.log on Linux).

**JSON Parsing:**

Modern SIEMs handle structured data. Have the SIEM read JSON logs and extract specific fields (like source_ip or event_id).

**External Integrations:**

Add a function that uses the requests library to send an email or a Discord/Slack webhook message whenever a critical alert is triggered.
