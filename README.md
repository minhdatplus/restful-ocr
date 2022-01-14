Freeze dependencies: `pipdeptree --warn silence | grep -E '^\w+' > requirements.txt`

Detect GIF Image URL: `curl --location --request POST 'http://127.0.0.1:5000/ocr' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'image_url=https://tinbatdongsan.com/Layout/Capchar/CaptchaGenerator.aspx' \
--data-urlencode 'image_type=gif'`

Detect Image URL Local Path: `curl --location --request POST 'http://127.0.0.1:5000/ocr' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'image_url=/Users/mdplus/Workspace/Noviato/Project/PupAuto/captcha.png' \
--data-urlencode 'image_type=png'`

Detect Image URL Online Path: `curl --location --request POST 'http://127.0.0.1:5000/ocr' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'image_url=https://i.ibb.co/SyMt6NN/z3107219068821-09a934e4ebbca5d588d8f0f348a74424.jpg' \
--data-urlencode 'image_type=png'`
