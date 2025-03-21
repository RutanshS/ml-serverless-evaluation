wrk.method = "POST"
wrk.headers["Content-Type"] = "image/jpeg"
wrk.body = assert(io.open("download.jpg", "rb")):read("*all")