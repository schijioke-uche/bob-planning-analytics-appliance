openssl pkey \
    -in "store/chubb_private_key.pem" \
    -pubout \
    -out "store/chubb_public_key.pem" &&
cat "store/chubb_public_key.pem"