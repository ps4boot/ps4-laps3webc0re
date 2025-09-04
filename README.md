# ![PS4](https://img.shields.io/badge/-PS4-003791?style=flat&logo=PlayStation) PS4 WebHost for OKage Lapsc0re 
(ONLY FW 11.00)

## Usage
Run the Python webhost with: (change your PS4 IP in webserver.py Line 128)
```bash
python webserver.py
```
The default port from Webhost is http://IP:8080.  
You can send the `.elf` file from any device that is on the same network as the PS4.
Just open the URL on your Device.

------

or for a simpel version that sends all the time a .elf file to your PS4:

(GoldHEN, Linux, Hen)
```bash
python server.py -i PS4IP -p 9045 -f ./ELFs/laps3c0re-PS4-11-00-***.elf
```
---

## Payload Locations

| Payload   | Internal Path                            | USB Path (first use copy the payload to USB) |
|-------------|----------------------------------------|--------------------------------------|
| **GoldHEN** | `/data/GoldHEN/payloads/payload.bin`   | `goldhen.bin`                        |
| **Linux**   | `/data/linux/payload.bin`              | `payload.bin`                        |
| **HEN**     | `/data/hen/payload.bin`                | `payload.bin`                        |

---




Preview

<img width="1235" height="604" alt="a" src="https://github.com/user-attachments/assets/2fe65eb3-81c2-4ba1-9e21-860fa80520bb" />



Important: 
progress / flask for python is needed !!







CREDITS:

@abc,@McCaulay, @iMrDJAi, 
All Developers in the PS4 Scene ......
