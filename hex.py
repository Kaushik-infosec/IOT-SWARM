import base64
data_base64 ="Ej4AAJeAgAAIzg=="
adata_base64 = "Ai0C4AEBAAAAADdy7f////8AAPf///////////8="
data_hex = base64.b64decode(data_base64).hex()  # Convert Base64 to raw bytes and then to hex.
print(data_hex)
