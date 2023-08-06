
## dnscrypt

printDNSCryptProviderFingerprint("/var/lib/dnsdist/providerPublic.key")

## Generate signed data hash (tbsCertificate)

openssl asn1parse -in certs/example.com.chain.pem -out /dev/stdout -noout -strparse 4 | openssl dgst -sha256

## Run tests

python3 -m unittest discover


## Build and upload
    
    python3 setup.py sdist bdist_wheel
    python3 -m twine upload dist/*
