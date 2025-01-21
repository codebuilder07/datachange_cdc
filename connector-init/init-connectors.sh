CONNECTORS_DIR="/configs"

for CONFIG_FILE in $CONNECTORS_DIR/*.json; do
    echo "Creating connector from file: $CONFIG_FILE"
    curl -X POST -H "Content-Type: application/json" \
        -d @"$CONFIG_FILE" http://localhost:8083/connectors
done