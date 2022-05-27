import subprocess,requests




def getdockerlog(command):
    res=''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            res+=line.decode().strip()+'\n'
    return res




def weixinboot(text_str):
    header={"Content-Type":"application/json"}
    param={
  "msgtype": "text",
  "text": {
    "content": text_str
  }
}
    requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6346fd17-bc3b-493c-b30e-58c8f99d003f',headers=header,json=param)

weixinboot(getdockerlog('ls'))
#weixinboot()