import avro.schema
from avro.io import DatumReader, BinaryDecoder
import io

# Load the Avro schema
schema = avro.schema.parse(open("./schema.avsc", "rb").read())

# Create a DatumReader
reader = DatumReader(schema)

def decode(data):
    try:
        # Assuming data is in bytes
        byte_stream = io.BytesIO(data)
        decoder = BinaryDecoder(byte_stream)
        # Decode Avro data
        decoded_data = reader.read(decoder)
        return decoded_data
    except Exception as e:
        print(f"Error decoding Avro data: {e}")
        return None

# Example binary data (adjusted for the provided example)
binary_data = b'\x00\x00\x00\x00\x02\x00\x02\x08\nBerry\x02\x161.4.2.Final\x14postgresql\x10postgres\xb6\xce\xbd\xb4\x8cd\x00\nfalse\x08food\x0cpublic\x16ingredients\x02\xe0\x07\x02\xe0\xcf\xe9\x16\x00\x02c\x02\x98\xd3\xbd\xb4\x8cd\x00'

# Decode the provided binary data
decoded_data = decode(binary_data)
if decoded_data:
    # Adjust the decoded data structure to match the expected JSON output
    output_data = {
        "ingredient_id": decoded_data["ingredient_id"],  # Assuming "ingredient_id" is directly accessible
        "ingredient_name": decoded_data["ingredient_name"],  # Assuming "ingredient_name" is directly accessible
        "ingredient_price": decoded_data["ingredient_price"]  # Assuming "ingredient_price" is directly accessible
    }
    print(output_data)

