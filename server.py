import socket
from rsa_utils import generate_keys_parallel, encrypt, decrypt

def run_server():
    HOST = "127.0.0.1"  # Localhost
    PORT = 5000         # Port for Person A (Server)

    # Generate RSA keys
    print("Generating keys. This may take a moment....")
    public_key, private_key = generate_keys_parallel()
    print(f"Your Public Key: {public_key}")
    print("Waiting for other person to connect...\n")

    # Start the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            conn, addr = server_socket.accept()
            print(f"Connected by: {addr}")
            
            # Send public key to Person B
            conn.send(f"{public_key[0]} {public_key[1]}".encode())
            print("Public key sent to Person B.")

            # Receive Person B's public key
            person_b_public_key = tuple(map(int, conn.recv(1024).decode().split()))
            print(f"Received Person B's Public Key: {person_b_public_key}\n")

            while True:
                # Send an encrypted message
                message = input("You: ")
                encrypted_message = encrypt(message, person_b_public_key)
                conn.send(" ".join(map(str, encrypted_message)).encode())
                print("Encrypted message sent.")

                # Receive and decrypt a message
                encrypted_response = list(map(int, conn.recv(1024).decode().split()))
                decrypted_response = decrypt(encrypted_response, private_key)
                print(f"Person B: {decrypted_response}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_server()
