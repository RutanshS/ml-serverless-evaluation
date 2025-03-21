while true; do
    # curl -H "Host: react-example.demo.130.127.133.200.xip.io" http://130.127.133.200
    curl -X POST -H "Host: ml-image-classifier.demo.130.127.133.200.xip.io" -F "file=@image.png" http://130.127.133.200/predict
    # wrk -t50 -c1000 -d60s -H "Host: react-example.demo.130.127.133.200.xip.io" http://130.127.133.200
    # wrk -t50 -c1000 -d180s -H "Host: ml-image-classifier.demo.130.127.133.200.xip.io" -s upload.lua http://130.127.133.200/predict
    sleep 0.1
done