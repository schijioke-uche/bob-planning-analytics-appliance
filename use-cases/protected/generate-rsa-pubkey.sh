(
    set -eu
    umask 077

    KEY_DIR="."

    mkdir -p "$KEY_DIR"
    chmod 700 "$KEY_DIR"

    # Do not overwrite existing keys.
    for filename in private_key.pem public_key.pem; do
        if [ -e "$KEY_DIR/$filename" ] || [ -L "$KEY_DIR/$filename" ]; then
            printf 'ERROR: Already exists: %s\n' "$KEY_DIR/$filename" >&2
            exit 1
        fi
    done

    # Generate an RSA private key WITHOUT a password.
    openssl genpkey \
        -algorithm RSA \
        -pkeyopt rsa_keygen_bits:3072 \
        -out "$KEY_DIR/private_key.pem"

    # Extract the corresponding public key.
    openssl pkey \
        -in "$KEY_DIR/private_key.pem" \
        -pubout \
        -out "$KEY_DIR/public_key.pem"

    chmod 600 "$KEY_DIR/private_key.pem"

    # Display only the public key.
    printf '\nPUBLIC KEY:\n\n'
    cat "$KEY_DIR/public_key.pem"
)