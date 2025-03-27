## **🔧 Pwnagotchi Plugin (MQTT or HTTP, Configurable Format)**  

You can configure it like this in `/etc/pwnagotchi/config.toml`:  
```toml
main.plugins.mac_logger.enabled = true
main.plugins.mac_logger.mode = "mqtt"  # Choose "mqtt" or "http"

# MQTT Settings
main.plugins.mac_logger.mqtt.broker = "mqtt.example.com"
main.plugins.mac_logger.mqtt.port = 1883
main.plugins.mac_logger.mqtt.username = "your_username"
main.plugins.mac_logger.mqtt.password = "your_password"

# HTTP Settings
main.plugins.mac_logger.http.url = "http://your-http-server.com/api"
```

---

**🔥 Plugin Code (Supports MQTT or HTTP)**

### **🚀 Configurations**
#### **For MQTT:**
```toml
main.plugins.mac_logger.enabled = true
main.plugins.mac_logger.mode = "mqtt"
main.plugins.mac_logger.mqtt.broker = "mqtt.example.com"
main.plugins.mac_logger.mqtt.port = 1883
main.plugins.mac_logger.mqtt.username = "your_username"
main.plugins.mac_logger.mqtt.password = "your_password"
```

#### **For HTTP:**
```toml
main.plugins.mac_logger.enabled = true
main.plugins.mac_logger.mode = "http"
main.plugins.mac_logger.http.url = "http://your-http-server.com/api"
```

You can easily switch between **MQTT and HTTP** using the config file without modifying the script! 🚀  
