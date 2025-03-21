wrk.method = "POST"
wrk.headers["Host"] = "ml-image-classifier.demo.130.127.133.200.xip.io"
wrk.headers["Content-Type"] = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"

local boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
local filename = "image.png"
local filepath = "./image.png"
local filedata = ""

function init()
    local file = io.open(filepath, "rb")
    if not file then
        error("Failed to open file: " .. filepath)
    end
    filedata = file:read("*all")
    file:close()
end

function request()
    local body = "--" .. boundary .. "\r\n" ..
                 "Content-Disposition: form-data; name=\"file\"; filename=\"" .. filename .. "\"\r\n" ..
                 "Content-Type: image/png\r\n\r\n" ..
                 filedata .. "\r\n" ..
                 "--" .. boundary .. "--\r\n"
    
    wrk.body = body
    return wrk.format()
end
