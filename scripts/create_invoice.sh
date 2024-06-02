# POST to create_invoice
response=$( \
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"memo": "testing", "amount": 100}' \
    http://localhost:8000/api/funding/create_invoice \
)

# echo $response
# sudo apt install jq
payment_request=$(echo $response | jq -r '.payment_request')
checking_id=$(echo $response | jq -r '.checking_id')
checking_sig=$(echo $response | jq -r '.checking_sig')
qr_uri=$(echo $response | jq -r '.qr_uri')

# echo $invoice_url

cat <<EOF > index.html
<!DOCTYPE html>
<html>
<head>
    <title>Invoice Image</title>
</head>
<body>
    <p>payment_request: $payment_request</p>
    <p>checking_id: $checking_id</p>
    <p>checking_sig: $checking_sig</p>
    <p>is_paid: <span id="is_paid">not yet</span></p>
    <img src="data:image/png;base64,$qr_uri" alt="Invoice Image">
    <script>
    console.log("hello world")
    async function checkPayment() {
        try {
            const response = await fetch(\`http://localhost:8000/api/funding/check_invoice_payment?checking_id=$checking_id&checking_sig=$checking_sig\`);
            if (response.ok) {
                const data = await response.json();
                document.getElementById('is_paid').innerText = data.is_paid ? 'true' : 'false';
                if (!data.is_paid) {
                    setTimeout(checkPayment, 5000); // Poll every 5 seconds if not paid
                }
            } else {
                console.error('Failed to fetch payment status:', response.statusText);
            }
        } catch (error) {
            console.error('Error checking payment status:', error);
        }
    }

    checkPayment(); // Initial call to start polling
    </script>
</body>
</html>
EOF