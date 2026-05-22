# Vibe Coding Log: Brute-Force Defender Project

## Part 1: Initial Structural Design Prompt
**Situation:** Instead of just asking for simple code, I acted as a System Architect to request the AI to design a complete Microservices infrastructure, ensuring isolation and observability.

<img width="1377" height="692" alt="image" src="https://github.com/user-attachments/assets/44ee34c3-2c09-417f-a6e0-90dce06c0442" />
<img width="1602" height="879" alt="image" src="https://github.com/user-attachments/assets/385394d3-9b28-4803-b866-ce76b33843ca" />
<img width="1279" height="618" alt="image" src="https://github.com/user-attachments/assets/16e9b9d4-f888-41ad-910b-9db1e7619a78" />
<img width="1137" height="697" alt="image" src="https://github.com/user-attachments/assets/59fb73bd-d1af-4696-8f5b-44e20064ed59" />
<img width="1283" height="660" alt="image" src="https://github.com/user-attachments/assets/df106ac1-d722-483c-949a-7c6882e52835" />
<img width="1008" height="541" alt="image" src="https://github.com/user-attachments/assets/611da009-add6-486d-a288-bddc2a1b56ad" />
<img width="1268" height="538" alt="image" src="https://github.com/user-attachments/assets/0202ace6-e961-40a0-a14c-7db583bba88c" />

**Feasibility assessment for real-world environment:** Although there are still several shortcomings in the design, integrating too many features would overload the system. Since the main goal is to focus on core logical thinking and system workflow (Read logs -> Analyze -> Block), I decided to avoid overcomplicating the issue.

<img width="1004" height="618" alt="image" src="https://github.com/user-attachments/assets/1d714ec2-9a03-4ed1-bc9e-abd8d259597c" />
<img width="1110" height="599" alt="image" src="https://github.com/user-attachments/assets/333e56c4-99cb-4eec-a1ca-d38e6cf24832" />
<img width="1274" height="598" alt="image" src="https://github.com/user-attachments/assets/02f08183-1333-4bf0-bf2e-45364bf0b9ae" />
<img width="1163" height="648" alt="image" src="https://github.com/user-attachments/assets/71aeb45b-d763-4c7d-9921-3f8c9df9078b" />

---

## Part 2: Debugging Process When AI Wrote Incorrect Code

**🐛 Bug 1: Docker Socket Permission Denied** 
**Situation:** On the first launch, the system reported an error indicating no permission to access `/var/run/docker.sock`.

<img width="1265" height="604" alt="image" src="https://github.com/user-attachments/assets/e2c50127-5b79-4916-baa5-0500e7feea72" />

**Prompt I used:**
"Based on this log, I understand that the system is denying access to the Docker Socket file. Is it because I ran the command without sudo privileges, or is my Linux user not added to the docker group? Act as a DevOps Engineer, briefly explain the root cause of this error, and provide the most accurate fix command for me."

**Resolution:** AI guided me to add the user to the docker group or run with sudo.
<img width="1302" height="654" alt="image" src="https://github.com/user-attachments/assets/fa21eede-8c40-4778-b193-0e16ce139a24" />


**🐛 Bug 2: TLS Network Error During Image Build**
**Situation:** When building the `attacker-bot` container, the `apk add` command failed with a TLS: unspecified error.

<img width="1023" height="639" alt="image" src="https://github.com/user-attachments/assets/56c1c7f5-8305-484c-9dbc-30842725fd06" />

**Prompt I used:**
"I used sudo and managed to run it, but this error appeared. I suspect there is no network connection to download the apk package. Please guide me on how to fix Docker network/DNS issues on this Linux virtual machine. Should I add DNS configuration to the `/etc/docker/daemon.json` file or restart the network service?"

**Resolution:** I forced the AI to add `network: host` to the build block. This was a great lesson on network handling in complex Lab environments.
<img width="1060" height="624" alt="image" src="https://github.com/user-attachments/assets/4c8bf090-f842-41a3-9409-ada191a800f9" />
<img width="1020" height="632" alt="image" src="https://github.com/user-attachments/assets/513d104c-2182-467e-9066-0eced26ae2b2" />


**🐛 Bug 3: Silent Library Conflicts (`http+docker`)**
**Situation:** The container crashed immediately upon starting due to the error `Not supported URL scheme http+docker`.

<img width="1307" height="577" alt="image" src="https://github.com/user-attachments/assets/dc364fe7-d9d7-4a4e-b748-92e039f0b55f" />

**Prompt I used:**
"It worked but a new issue occurred: the `security-watcher` container crashed right at startup with the error: `Error while fetching server API version: Not supported URL scheme http+docker`. I diagnose this as a version conflict between the `docker` library and the `requests` (or `urllib3`) library that we just added. Please reset the versions in `requirements.txt` to be compatible.
Also, my terminal has a font rendering issue with accented Vietnamese (producing special characters). Please rewrite all print lines (`logger.info`, `echo`...) in `watcher.py` and `attack.sh` into accentless Vietnamese (e.g., 'Phat hien tan cong').
Please provide the new contents of `requirements.txt`, `watcher.py`, and `attack.sh`."

**Resolution:** I instructed the AI to pin `urllib3<2.0.0`. This deepened my understanding of the importance of Dependency management.
<img width="1045" height="615" alt="image" src="https://github.com/user-attachments/assets/34a3c299-e552-428d-822a-a8c4bb9425f9" />

<img width="973" height="655" alt="image" src="https://github.com/user-attachments/assets/2e290fa7-60a5-4b49-be41-e6370a36f4a6" />

**🐛 Bug 4: Silent Telegram Alerts (Runtime Network Error)**
**Situation:** Successfully blocked the IP, but no Telegram message was sent to my phone.
<img width="1158" height="604" alt="image" src="https://github.com/user-attachments/assets/e75268f4-5b6a-472b-ae5d-87dbdc0a3828" />

**Prompt I used:**
"IP blocked, but Telegram remains silent. Please add debug logs printing the Status Code and Response Body of the Telegram API, and configure `network_mode: host` to let the container escape the virtual Docker network."

**Resolution:** After switching to `network_mode: host`, the system's network became fully functional. Lesson learned: Docker's virtual Bridge network can sometimes be a barrier for applications that need to make external API calls.

**🐛 Bug 5: Permission Error Checking Docker Network**

**Situation:** When using the `ping` command to test connectivity, the system reported a `permission denied (are you root?)` error because the n8n Docker image is secured and doesn't allow standard users to run network commands.

**Prompt to AI:** "I got a permission denied error when pinging from within the n8n container. How can I run this command with root privileges?"

**Result:** Thanks to the AI, I learned how to use the `-u root` flag in the `docker exec` command to bypass permissions and confirm that the network was fully established after switching to `network_mode: host`. The Telegram Timer Monitoring system is now 100% operational.
<img width="1053" height="71" alt="image" src="https://github.com/user-attachments/assets/aa0dab56-e022-4c57-80e5-932e7eb019d7" />

<img width="1257" height="617" alt="image" src="https://github.com/user-attachments/assets/a0c9f4c2-e6fa-4413-bb74-b3369c598103" />
