### Milvus Setup

[Requirement](https://milvus.io/docs/prerequisite-docker.md)

**Note:** Avoid using WSL to run Milvus because WSL has a separate virtual network from Windows. This can cause issues where the Windows machine and WSL have different IP addresses, preventing external devices from connecting to Milvus.

---

### Install & Run Milvus Standalone

Use `docker-compose.yml` file to install Milvus using Docker Compose and export port `19530` and `9091` for another computer to access.

#### **Start Milvus**

```bash
sudo docker compose up -d
```

#### **Check if the containers are running**

```bash
sudo docker-compose ps
```

Example output:

```bash
      Name                     Command                  State                            Ports
--------------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -advertise-client-url ...   Up             2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp, 0.0.0.0:9091->9091/tcp
```

#### **Stop and delete Milvus**

```bash
sudo docker compose down

sudo rm -rf volumes
```

---

### Establish a Connection Between Multiple Computers

#### **Export Ports**

**Milvus standalone typically runs on:**

- **Port `19530`** for **gRPC** communication (main API).
- **Port `9091`** for **HTTP** (RESTful API).

To allow other computers on the same WiFi network to access Milvus running on your computer, you **must expose these ports** by:

- Binding Milvus to `0.0.0.0` instead of `127.0.0.1` (default). *(This is already set in the `docker-compose.yml` file.)*
- Allowing inbound traffic on these ports in your firewall settings.
- Ensuring your router/network doesn't block external connections.

Follow this guide to open ports `19530` and `9091`:

[How to Open Ports in Your Firewall: Easy Windows & Mac Guide](https://www.wikihow.com/Open-Ports)
