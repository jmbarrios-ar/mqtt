import machine
from umqtt.simple import MQTTClient
import time

# Configuración de la red Wi-Fi
WIFI_SSID = "nombre_de_tu_wifi"
WIFI_PASSWORD = "contraseña_de_tu_wifi"

# Configuración del servidor MQTT
MQTT_BROKER = "direccion_del_broker_mqtt"
CLIENT_ID = "esp8266"

# Callback para manejar los mensajes recibidos
def sub_cb(topic, msg):
    print((topic, msg))

# Conexión Wi-Fi
def connect_wifi():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando a WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Conexión WiFi exitosa')
    print('Dirección IP:', sta_if.ifconfig()[0])

# Conexión MQTT
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(b"topic_sub")
    print("Conexión MQTT exitosa")
    return client

# Programa principal
def main():
    connect_wifi()
    client = connect_mqtt()

    # Publicación de mensajes
    while True:
        client.publish(b"topic_pub", b"hola desde ESP8266")
        client.check_msg()
        time.sleep(5)

if __name__ == "__main__":
    main()
