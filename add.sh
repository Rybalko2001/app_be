declare -a bags=(
  '{"name": "Backpack", "brand": "Nike", "price": 99}'
  '{"name": "Checkered Tote Bag", "brand": "Louis Vuitton", "price": 1200}'
  '{"name": "Leather Handbag", "brand": "Gucci", "price": 850.00}'
  '{"name": "Duffel Bag", "brand": "Adidas", "price": 65}'
  '{"name": "Elegant Shoulder Bag", "brand": "Chanel", "price": 2300}'
)

for bag in "${bags[@]}"
do
  echo "Adding bag: $bag"
  response=$(curl -s -w "%{http_code}" -o /tmp/response.json -X POST "http://localhost:8000/api/" \
       -H "Content-Type: application/json" \
       -d "$bag")
  echo "Status code: $response"
  echo "Response body:"
  cat /tmp/response.json
  echo -e "\n"
  sleep 1
done