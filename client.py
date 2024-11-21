import socket
from rsa_utils import generate_keys_parallel, encrypt, decrypt

def run_client():
    HOST = "127.0.0.1"  # Localhost
    PORT = 5000         # Connect to Person A's port

    # Generate RSA keys
    print("Generating keys. This may take a moment....")
    public_key, private_key = generate_keys_parallel()
    print(f"Your Public Key: {public_key}")

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        # Receive Person A's public key
        person_a_public_key = tuple(map(int, client_socket.recv(1024).decode().split()))
        print(f"Received Person A's Public Key: {person_a_public_key}\n")
        
        # Send public key to Person A
        client_socket.send(f"{public_key[0]} {public_key[1]}".encode())
        print("waiting for response....")
        while True:
            # Receive and decrypt a message
            encrypted_message = list(map(int, client_socket.recv(1024).decode().split()))
            decrypted_message = decrypt(encrypted_message, private_key)
            print(f"Person A: {decrypted_message}")

            # Send an encrypted response
            response = input("You: ")
            encrypted_response = encrypt(response, person_a_public_key)
            client_socket.send(" ".join(map(str, encrypted_response)).encode())
            print("message sent. Waiting for response....")

if __name__ == "__main__":
    run_client()
