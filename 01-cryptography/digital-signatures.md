# Digital Signatures 🔏

## Introduction

Digital signatures are the cryptographic equivalent of handwritten signatures, providing authentication, non-repudiation, and data integrity in the digital world. They are fundamental to blockchain technology, ensuring that transactions are legitimate and unalterable.

## What is a Digital Signature? 🖋️

A digital signature is a mathematical scheme that demonstrates the authenticity of digital messages or documents. It provides:

- **Authentication**: Verifies the identity of the sender
- **Non-repudiation**: Prevents the sender from denying they sent the message
- **Integrity**: Ensures the message hasn't been tampered with

### Real-World Analogy 📝

Think of a digital signature like a tamper-evident seal on a package:
- Only you can create your unique seal (private key)
- Anyone can verify it's your seal (public key)
- If someone tampers with the package, the seal breaks (signature becomes invalid)

## How Digital Signatures Work 🔧

### The Process

```
1. Create Hash → 2. Sign Hash → 3. Attach Signature → 4. Verify Signature
    ↓               ↓                ↓                  ↓
[Document] →    [Private Key] →  [Document + Sig] → [Public Key]
```

### Step-by-Step Process

1. **Hashing**: Create a hash of the document/message
2. **Signing**: Encrypt the hash with your private key
3. **Verification**: Recipients decrypt with your public key and compare hashes

## Digital Signature Algorithms 📊

### 1. RSA (Rivest-Shamir-Adleman)
```python
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii

# Generate RSA key pair
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# Message to sign
message = "Alice sends 5 BTC to Bob"
message_hash = SHA256.new(message.encode())

# Create digital signature
signature = pkcs1_15.new(private_key).sign(message_hash)
signature_hex = binascii.hexlify(signature).decode()

print(f"Original message: {message}")
print(f"Message hash: {message_hash.hexdigest()}")
print(f"Digital signature: {signature_hex[:64]}...")

# Verify signature
try:
    pkcs1_15.new(public_key).verify(message_hash, signature)
    print("✅ Signature is valid!")
except (ValueError, TypeError):
    print("❌ Signature is invalid!")
```

### 2. ECDSA (Elliptic Curve DSA)
```python
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import binascii

# Generate ECDSA key pair (same as Bitcoin uses)
signing_key = SigningKey.generate(curve=SECP256k1)
verifying_key = signing_key.get_verifying_key()

# Message and hash
message = "Transfer 1.5 ETH to 0x742d35Cc6635C0532925a3b8D8Cf97E"
message_hash = hashlib.sha256(message.encode()).digest()

# Create signature
signature = signing_key.sign(message_hash)
signature_hex = binascii.hexlify(signature).decode()

print(f"Message: {message}")
print(f"Private key: {binascii.hexlify(signing_key.to_string()).decode()}")
print(f"Public key: {binascii.hexlify(verifying_key.to_string()).decode()}")
print(f"Signature: {signature_hex}")

# Verify signature
try:
    verifying_key.verify(signature, message_hash)
    print("✅ ECDSA signature verified!")
except:
    print("❌ ECDSA signature verification failed!")
```

## Digital Signatures in Blockchain 🔗

### Bitcoin Transaction Signatures

```python
class BitcoinTransaction:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.signatures = []
    
    def add_input(self, prev_tx_hash, output_index, script_sig):
        self.inputs.append({
            'prev_tx_hash': prev_tx_hash,
            'output_index': output_index,
            'script_sig': script_sig
        })
    
    def add_output(self, amount, recipient_address):
        self.outputs.append({
            'amount': amount,
            'recipient': recipient_address
        })
    
    def create_signature_hash(self, input_index):
        """Create the hash that will be signed"""
        # Simplified version - real Bitcoin uses more complex rules
        tx_data = f"{self.inputs[input_index]}{self.outputs}"
        return hashlib.sha256(tx_data.encode()).digest()
    
    def sign_input(self, input_index, private_key):
        """Sign a specific input"""
        sig_hash = self.create_signature_hash(input_index)
        signature = private_key.sign(sig_hash)
        self.signatures.append({
            'input_index': input_index,
            'signature': signature,
            'public_key': private_key.get_verifying_key()
        })
        return signature

# Example usage
tx = BitcoinTransaction()
tx.add_input("abc123...", 0, "")
tx.add_output(0.5, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

# Sign the transaction
private_key = SigningKey.generate(curve=SECP256k1)
signature = tx.sign_input(0, private_key)
print(f"Transaction signed: {binascii.hexlify(signature).decode()[:32]}...")
```

### Ethereum Message Signatures

```python
import hashlib
from eth_account import Account
from eth_account.messages import encode_defunct

# Create Ethereum account
account = Account.create()
private_key = account.key
address = account.address

print(f"Ethereum Address: {address}")
print(f"Private Key: {private_key.hex()}")

# Sign a message (EIP-191 standard)
message = "I authorize this transaction"
message_hash = encode_defunct(text=message)
signed_message = account.sign_message(message_hash, private_key=private_key)

print(f"\nMessage: {message}")
print(f"Signature: {signed_message.signature.hex()}")
print(f"Recovery ID: {signed_message.v}")

# Verify signature
recovered_address = Account.recover_message(message_hash, signature=signed_message.signature)
print(f"\nOriginal address: {address}")
print(f"Recovered address: {recovered_address}")
print(f"Signature valid: {address.lower() == recovered_address.lower()}")
```

## Security Properties 🛡️

### Authentication
```python
def demonstrate_authentication():
    """Shows how signatures prove identity"""
    
    # Alice's keys
    alice_key = SigningKey.generate(curve=SECP256k1)
    alice_public = alice_key.get_verifying_key()
    
    # Bob's keys  
    bob_key = SigningKey.generate(curve=SECP256k1)
    bob_public = bob_key.get_verifying_key()
    
    # Alice signs a message
    message = "This message is from Alice"
    message_hash = hashlib.sha256(message.encode()).digest()
    alice_signature = alice_key.sign(message_hash)
    
    print("🔐 Authentication Test")
    print("=" * 50)
    
    # Verify with Alice's public key
    try:
        alice_public.verify(alice_signature, message_hash)
        print("✅ Verified: Message is from Alice")
    except:
        print("❌ Failed: Message is NOT from Alice")
    
    # Try to verify with Bob's public key (should fail)
    try:
        bob_public.verify(alice_signature, message_hash)
        print("❌ ERROR: Bob's key verified Alice's signature!")
    except:
        print("✅ Correct: Bob's key cannot verify Alice's signature")

demonstrate_authentication()
```

### Non-Repudiation
```python
class NonRepudiationDemo:
    def __init__(self):
        self.signed_messages = []
    
    def sign_contract(self, signer_name, private_key, contract_text):
        """Sign a contract - creates irrefutable proof"""
        timestamp = int(time.time())
        full_message = f"{contract_text}|{signer_name}|{timestamp}"
        message_hash = hashlib.sha256(full_message.encode()).digest()
        signature = private_key.sign(message_hash)
        
        record = {
            'signer': signer_name,
            'contract': contract_text,
            'timestamp': timestamp,
            'signature': signature,
            'public_key': private_key.get_verifying_key(),
            'message_hash': message_hash
        }
        
        self.signed_messages.append(record)
        return record
    
    def verify_contract(self, record_index):
        """Verify a signed contract"""
        if record_index >= len(self.signed_messages):
            return False, "Record not found"
        
        record = self.signed_messages[record_index]
        
        # Reconstruct the original message
        full_message = f"{record['contract']}|{record['signer']}|{record['timestamp']}"
        expected_hash = hashlib.sha256(full_message.encode()).digest()
        
        # Verify hash matches
        if expected_hash != record['message_hash']:
            return False, "Message hash mismatch"
        
        # Verify signature
        try:
            record['public_key'].verify(record['signature'], record['message_hash'])
            return True, f"Contract signed by {record['signer']} at {record['timestamp']}"
        except:
            return False, "Invalid signature"

# Demo usage
demo = NonRepudiationDemo()

# Alice signs a contract
alice_key = SigningKey.generate(curve=SECP256k1)
contract = "I agree to sell my car for $15,000"
record = demo.sign_contract("Alice", alice_key, contract)

print("📋 Non-Repudiation Demo")
print("=" * 50)
print(f"Contract: {contract}")
print(f"Signed by: Alice")
print(f"Timestamp: {record['timestamp']}")

# Later verification
is_valid, message = demo.verify_contract(0)
print(f"Verification result: {message}")
```

### Integrity Protection
```python
def integrity_demo():
    """Demonstrates how signatures detect tampering"""
    
    # Original message and signature
    original = "Transfer $1000 to Bob"
    key = SigningKey.generate(curve=SECP256k1)
    public_key = key.get_verifying_key()
    
    original_hash = hashlib.sha256(original.encode()).digest()
    signature = key.sign(original_hash)
    
    print("🔒 Integrity Protection Demo")
    print("=" * 50)
    print(f"Original: {original}")
    
    # Verify original (should pass)
    try:
        public_key.verify(signature, original_hash)
        print("✅ Original message signature valid")
    except:
        print("❌ Original message signature invalid")
    
    # Try with tampered message (should fail)
    tampered = "Transfer $10000 to Bob"  # Changed amount!
    tampered_hash = hashlib.sha256(tampered.encode()).digest()
    
    print(f"Tampered: {tampered}")
    try:
        public_key.verify(signature, tampered_hash)
        print("❌ ERROR: Tampered message verified!")
    except:
        print("✅ Correct: Tampered message rejected")

integrity_demo()
```

## Advanced Topics 🎓

### Multi-Signature (MultiSig)
```python
class MultiSigWallet:
    def __init__(self, required_signatures, total_signers):
        self.required = required_signatures
        self.total = total_signers
        self.signers = []
        self.transactions = []
    
    def add_signer(self, public_key, name):
        if len(self.signers) >= self.total:
            raise ValueError("Maximum signers reached")
        
        self.signers.append({
            'public_key': public_key,
            'name': name
        })
    
    def create_transaction(self, amount, recipient):
        tx_id = len(self.transactions)
        transaction = {
            'id': tx_id,
            'amount': amount,
            'recipient': recipient,
            'signatures': [],
            'executed': False
        }
        self.transactions.append(transaction)
        return tx_id
    
    def sign_transaction(self, tx_id, private_key):
        if tx_id >= len(self.transactions):
            return False, "Transaction not found"
        
        tx = self.transactions[tx_id]
        if tx['executed']:
            return False, "Transaction already executed"
        
        # Create signature hash
        tx_data = f"{tx['amount']}|{tx['recipient']}|{tx_id}"
        tx_hash = hashlib.sha256(tx_data.encode()).digest()
        signature = private_key.sign(tx_hash)
        
        # Find signer
        public_key = private_key.get_verifying_key()
        signer_name = None
        for signer in self.signers:
            if self.keys_equal(signer['public_key'], public_key):
                signer_name = signer['name']
                break
        
        if not signer_name:
            return False, "Unauthorized signer"
        
        # Check if already signed
        for existing_sig in tx['signatures']:
            if existing_sig['signer'] == signer_name:
                return False, "Already signed by this signer"
        
        tx['signatures'].append({
            'signature': signature,
            'signer': signer_name,
            'public_key': public_key
        })
        
        return True, f"Signed by {signer_name}"
    
    def execute_transaction(self, tx_id):
        if tx_id >= len(self.transactions):
            return False, "Transaction not found"
        
        tx = self.transactions[tx_id]
        if tx['executed']:
            return False, "Already executed"
        
        if len(tx['signatures']) < self.required:
            return False, f"Need {self.required} signatures, have {len(tx['signatures'])}"
        
        # Verify all signatures
        tx_data = f"{tx['amount']}|{tx['recipient']}|{tx_id}"
        tx_hash = hashlib.sha256(tx_data.encode()).digest()
        
        valid_signatures = 0
        for sig in tx['signatures']:
            try:
                sig['public_key'].verify(sig['signature'], tx_hash)
                valid_signatures += 1
            except:
                continue
        
        if valid_signatures >= self.required:
            tx['executed'] = True
            return True, f"Transaction executed with {valid_signatures} valid signatures"
        else:
            return False, f"Only {valid_signatures} valid signatures"
    
    def keys_equal(self, key1, key2):
        """Compare if two public keys are equal"""
        return key1.to_string() == key2.to_string()

# Demo MultiSig wallet
wallet = MultiSigWallet(2, 3)  # 2-of-3 multisig

# Create signers
alice_key = SigningKey.generate(curve=SECP256k1)
bob_key = SigningKey.generate(curve=SECP256k1)
carol_key = SigningKey.generate(curve=SECP256k1)

wallet.add_signer(alice_key.get_verifying_key(), "Alice")
wallet.add_signer(bob_key.get_verifying_key(), "Bob")
wallet.add_signer(carol_key.get_verifying_key(), "Carol")

print("🏛️ MultiSig Wallet Demo")
print("=" * 50)

# Create transaction
tx_id = wallet.create_transaction(100, "0x742d35Cc...")
print(f"Created transaction {tx_id}: Send 100 tokens")

# Alice signs
success, msg = wallet.sign_transaction(tx_id, alice_key)
print(f"Alice signing: {msg}")

# Bob signs  
success, msg = wallet.sign_transaction(tx_id, bob_key)
print(f"Bob signing: {msg}")

# Try to execute (should succeed with 2 signatures)
success, msg = wallet.execute_transaction(tx_id)
print(f"Execution: {msg}")
```

### Signature Aggregation
```python
def demonstrate_signature_aggregation():
    """Shows BLS signature aggregation (conceptual)"""
    
    # Multiple signers
    signers = []
    signatures = []
    message = "We all agree to this proposal"
    message_hash = hashlib.sha256(message.encode()).digest()
    
    # Each signer creates a signature
    for i in range(3):
        key = SigningKey.generate(curve=SECP256k1)
        signature = key.sign(message_hash)
        signers.append({
            'name': f"Signer_{i+1}",
            'public_key': key.get_verifying_key(),
            'signature': signature
        })
        signatures.append(signature)
    
    print("📊 Signature Aggregation Demo")
    print("=" * 50)
    print(f"Message: {message}")
    print(f"Number of signers: {len(signers)}")
    
    # Individual signature sizes
    individual_size = len(signatures[0])
    total_individual_size = individual_size * len(signatures)
    
    print(f"Individual signature size: {individual_size} bytes")
    print(f"Total size (individual): {total_individual_size} bytes")
    
    # Simulated aggregated signature (in real BLS, this would be much smaller)
    # For demonstration, we just concatenate (BLS actually adds them mathematically)
    aggregated_sig = b''.join(signatures)
    print(f"Simulated aggregated size: {len(aggregated_sig)} bytes")
    print(f"Space saved: {((total_individual_size - len(aggregated_sig)) / total_individual_size) * 100:.1f}%")
    
    # In real BLS signatures, you could verify all signatures at once
    print("✅ In BLS: All signatures verified simultaneously")

demonstrate_signature_aggregation()
```

## Common Attack Vectors 🚨

### 1. Signature Malleability
```python
def signature_malleability_demo():
    """Demonstrates signature malleability in ECDSA"""
    
    print("⚠️  Signature Malleability Demo")
    print("=" * 50)
    
    # Create original signature
    key = SigningKey.generate(curve=SECP256k1)
    message = "Send 1 BTC to Alice"
    message_hash = hashlib.sha256(message.encode()).digest()
    signature = key.sign(message_hash)
    
    print("Original transaction:")
    print(f"Message: {message}")
    print(f"Signature: {binascii.hexlify(signature).decode()[:32]}...")
    
    # In ECDSA, for signature (r,s), (r, -s mod n) is also valid
    # This is why Bitcoin implemented BIP 62
    print("\n⚠️  Warning: ECDSA signatures can be malleable!")
    print("Solution: Use canonical signatures (BIP 62) or deterministic nonces (RFC 6979)")

signature_malleability_demo()
```

### 2. Replay Attacks
```python
class ReplayProtectedSignature:
    def __init__(self):
        self.nonces = set()  # Track used nonces
    
    def sign_with_nonce(self, private_key, message, nonce):
        if nonce in self.nonces:
            raise ValueError("Nonce already used - replay attack prevented")
        
        # Include nonce in signature
        full_message = f"{message}|nonce:{nonce}"
        message_hash = hashlib.sha256(full_message.encode()).digest()
        signature = private_key.sign(message_hash)
        
        self.nonces.add(nonce)
        
        return {
            'message': message,
            'nonce': nonce,
            'signature': signature,
            'full_message': full_message
        }
    
    def verify_with_nonce(self, public_key, signed_data):
        if signed_data['nonce'] in self.nonces:
            # In real system, this would check if nonce was already processed
            pass
        
        # Reconstruct full message
        full_message = f"{signed_data['message']}|nonce:{signed_data['nonce']}"
        expected_hash = hashlib.sha256(full_message.encode()).digest()
        
        try:
            public_key.verify(signed_data['signature'], expected_hash)
            return True
        except:
            return False

# Demo replay protection
replay_protector = ReplayProtectedSignature()
key = SigningKey.generate(curve=SECP256k1)
public_key = key.get_verifying_key()

print("🔄 Replay Attack Protection Demo")
print("=" * 50)

# Sign message with nonce
signed_data = replay_protector.sign_with_nonce(
    key, 
    "Transfer 5 ETH to Bob", 
    12345
)
print(f"Signed: {signed_data['message']}")
print(f"Nonce: {signed_data['nonce']}")

# Verify signature
is_valid = replay_protector.verify_with_nonce(public_key, signed_data)
print(f"Verification: {'✅ Valid' if is_valid else '❌ Invalid'}")

# Try to reuse nonce (should fail)
try:
    replay_protector.sign_with_nonce(key, "Transfer 10 ETH to Carol", 12345)
    print("❌ ERROR: Replay attack succeeded!")
except ValueError as e:
    print(f"✅ Replay attack prevented: {e}")
```

## Practical Applications 💼

### 1. Document Signing
```python
class DocumentSigner:
    def __init__(self):
        self.signed_documents = []
    
    def sign_document(self, document_content, signer_name, private_key):
        timestamp = int(time.time())
        document_hash = hashlib.sha256(document_content.encode()).hexdigest()
        
        # Create signature payload
        signature_payload = f"{document_hash}|{signer_name}|{timestamp}"
        payload_hash = hashlib.sha256(signature_payload.encode()).digest()
        signature = private_key.sign(payload_hash)
        
        signed_doc = {
            'content': document_content,
            'content_hash': document_hash,
            'signer': signer_name,
            'timestamp': timestamp,
            'signature': signature,
            'public_key': private_key.get_verifying_key()
        }
        
        self.signed_documents.append(signed_doc)
        return len(self.signed_documents) - 1  # Return document ID
    
    def verify_document(self, doc_id):
        if doc_id >= len(self.signed_documents):
            return False, "Document not found"
        
        doc = self.signed_documents[doc_id]
        
        # Verify content hash
        actual_hash = hashlib.sha256(doc['content'].encode()).hexdigest()
        if actual_hash != doc['content_hash']:
            return False, "Document content has been modified"
        
        # Verify signature
        signature_payload = f"{doc['content_hash']}|{doc['signer']}|{doc['timestamp']}"
        payload_hash = hashlib.sha256(signature_payload.encode()).digest()
        
        try:
            doc['public_key'].verify(doc['signature'], payload_hash)
            return True, f"Document verified - signed by {doc['signer']} at {doc['timestamp']}"
        except:
            return False, "Invalid signature"

# Demo document signing
doc_signer = DocumentSigner()
alice_key = SigningKey.generate(curve=SECP256k1)

contract = """
EMPLOYMENT CONTRACT

Employee: John Doe
Employer: ABC Corporation
Salary: $75,000 per year
Start Date: January 1, 2024

This contract is legally binding...
"""

print("📄 Document Signing Demo")
print("=" * 50)

# Sign the contract
doc_id = doc_signer.sign_document(contract, "Alice Johnson (HR)", alice_key)
print(f"Contract signed by Alice, Document ID: {doc_id}")

# Verify the signature
is_valid, message = doc_signer.verify_document(doc_id)
print(f"Verification: {message}")
```

### 2. API Authentication
```python
class APIAuthenticator:
    def __init__(self):
        self.api_keys = {}  # Map API key ID to public key
    
    def register_api_key(self, key_id, public_key):
        self.api_keys[key_id] = public_key
    
    def create_signed_request(self, private_key, key_id, method, endpoint, payload=""):
        timestamp = int(time.time())
        
        # Create request signature
        request_string = f"{method}|{endpoint}|{payload}|{timestamp}"
        request_hash = hashlib.sha256(request_string.encode()).digest()
        signature = private_key.sign(request_hash)
        
        return {
            'method': method,
            'endpoint': endpoint,
            'payload': payload,
            'timestamp': timestamp,
            'key_id': key_id,
            'signature': binascii.hexlify(signature).decode()
        }
    
    def verify_request(self, request_data):
        # Check if API key exists
        if request_data['key_id'] not in self.api_keys:
            return False, "Invalid API key"
        
        public_key = self.api_keys[request_data['key_id']]
        
        # Check timestamp (prevent replay attacks)
        current_time = int(time.time())
        if abs(current_time - request_data['timestamp']) > 300:  # 5 minute window
            return False, "Request expired"
        
        # Verify signature
        request_string = f"{request_data['method']}|{request_data['endpoint']}|{request_data['payload']}|{request_data['timestamp']}"
        request_hash = hashlib.sha256(request_string.encode()).digest()
        signature = binascii.unhexlify(request_data['signature'])
        
        try:
            public_key.verify(signature, request_hash)
            return True, "Request authenticated"
        except:
            return False, "Invalid signature"

# Demo API authentication
auth = APIAuthenticator()
client_key = SigningKey.generate(curve=SECP256k1)
client_public = client_key.get_verifying_key()

print("🔐 API Authentication Demo")
print("=" * 50)

# Register client
auth.register_api_key("client_001", client_public)
print("Client registered with API key: client_001")

# Create signed request
request = auth.create_signed_request(
    client_key,
    "client_001", 
    "POST",
    "/api/transfer",
    '{"amount": 100, "recipient": "0x742d35..."}'
)

print(f"Request: {request['method']} {request['endpoint']}")
print(f"Signature: {request['signature'][:32]}...")

# Verify request
is_valid, message = auth.verify_request(request)
print(f"Authentication: {message}")
```

## Best Practices 🌟

### 1. Key Management
- **Generate keys securely**: Use cryptographically secure random generators
- **Protect private keys**: Never expose them in code or logs
- **Use hardware security modules (HSMs)** for high-value applications
- **Implement key rotation** for long-lived systems

### 2. Signature Implementation
- **Use established libraries**: Don't implement crypto primitives yourself
- **Validate inputs**: Check message format and signature structure
- **Include context**: Add domain separation to prevent signature reuse
- **Handle errors gracefully**: Don't leak information in error messages

### 3. Security Considerations
```python
# ✅ Good practices
def secure_signature_verification(public_key, message, signature):
    try:
        # 1. Validate input formats
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        
        # 2. Use constant-time comparison for signatures
        # (most libraries handle this automatically)
        
        # 3. Verify signature
        public_key.verify(signature, hashlib.sha256(message).digest())
        return True
        
    except Exception as e:
        # 4. Don't leak information in errors
        logger.info(f"Signature verification failed")  # Log for debugging
        return False  # Return generic failure

# ❌ Bad practices to avoid
def insecure_verification(public_key, message, signature):
    # Don't do this:
    # - Exposing detailed error information
    # - Not handling encoding properly
    # - Using weak hash functions
    try:
        public_key.verify(signature, hashlib.md5(message).digest())  # Weak hash!
        return True
    except ValueError as e:
        raise Exception(f"Signature failed because: {str(e)}")  # Information leak!
```

## Real-World Examples 🌍

### Bitcoin Transaction
```python
# Simplified Bitcoin transaction signature verification
def verify_bitcoin_transaction():
    print("₿ Bitcoin Transaction Signature")
    print("=" * 50)
    
    # Example Bitcoin transaction data
    tx_data = {
        'version': 1,
        'inputs': [{
            'prev_tx': 'a1b2c3d4...',
            'output_index': 0,
            'script_sig': '304402207f3d...',  # DER-encoded signature
            'sequence': 0xffffffff
        }],
        'outputs': [{
            'value': 50000000,  # 0.5 BTC in satoshis
            'script_pubkey': '76a914...88ac'  # P2PKH script
        }],
        'locktime': 0
    }
    
    print("Transaction structure:")
    print(f"- Inputs: {len(tx_data['inputs'])}")
    print(f"- Outputs: {len(tx_data['outputs'])}")
    print(f"- Output value: {tx_data['outputs'][0]['value'] / 100000000} BTC")
    print("✅ Signature verification would happen here")

verify_bitcoin_transaction()
```

### Smart Contract Signature
```python
# Ethereum-style message signing for smart contracts
class ContractSigner:
    def __init__(self):
        self.domain = {
            'name': 'MyDApp',
            'version': '1',
            'chainId': 1,
            'verifyingContract': '0x742d35Cc6635C0532925a3b8D8Cf97E'
        }
    
    def create_typed_signature(self, private_key, message_data):
        # EIP-712 structured data signing
        message_json = json.dumps(message_data, sort_keys=True)
        message_hash = hashlib.sha256(message_json.encode()).digest()
        signature = private_key.sign(message_hash)
        
        return {
            'domain': self.domain,
            'message': message_data,
            'signature': binascii.hexlify(signature).decode()
        }

# Demo contract signing
contract_signer = ContractSigner()
user_key = SigningKey.generate(curve=SECP256k1)

permit_data = {
    'owner': '0x742d35Cc6635C0532925a3b8D8Cf97E',
    'spender': '0x8ba1f109551bD432803012645Hac136c',
    'value': 1000000000000000000,  # 1 token
    'nonce': 0,
    'deadline': 1735689600
}

signature_data = contract_signer.create_typed_signature(user_key, permit_data)
print("📝 Smart Contract Signature")
print(f"Contract: {signature_data['domain']['name']}")
print(f"Message: {json.dumps(permit_data, indent=2)}")
print(f"Signature: {signature_data['signature'][:32]}...")
```

## Quiz: Test Your Knowledge 📝

1. **What are the three main properties that digital signatures provide?**
   - Authentication, Non-repudiation, Integrity

2. **Why is ECDSA preferred over RSA for blockchain applications?**
   - Smaller key sizes, faster verification, better mobile performance

3. **What is signature malleability and why is it a problem?**
   - Multiple valid signatures for the same message, can change transaction IDs

4. **How do multisig wallets enhance security?**
   - Require multiple signatures, distribute trust, prevent single points of failure

5. **What is the purpose of including nonces in signatures?**
   - Prevent replay attacks, ensure message freshness

## Summary 🎯

Digital signatures are the backbone of blockchain security, providing:

- **Authentication**: Proof of sender identity
- **Non-repudiation**: Undeniable proof of message origin  
- **Integrity**: Detection of any message tampering
- **Trust without intermediaries**: Cryptographic proof instead of trusted parties

### Key Takeaways

1. **Private keys create signatures**, **public keys verify them**
2. **Hash the message first**, then sign the hash
3. **ECDSA is standard** for Bitcoin and Ethereum
4. **Multisig adds security** through distributed signing
5. **Proper implementation matters** - use established libraries

### Next Steps

- Learn about [Merkle Trees](merkle-trees.md) for efficient verification
- Explore [Bitcoin Transactions](../02-bitcoin/transactions-utxos.md) using signatures
- Understand [Smart Contract Security](../04-smart-contracts/security-best-practices.md)

---

**🔏 Digital signatures transformed the internet from "don't trust, verify" to "trust through verification" - the foundation of all blockchain technology.**