import random
import smtplib
import logging
import time
import re
import dns.resolver

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s')

logger = logging.getLogger()

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def fetch_mx(host):
    logger.info('正在尋找 SMTP Server')
    try:
        answers = dns.resolver.query(host, 'MX')
        res = [str(rdata.exchange)[:-1] for rdata in answers]
        logger.info('查詢結果有：%s' % res)
        return res
    except:
        return None


def verify(email):
    if(re.search(regex,email)):
        # 分開 email
        name, host = email.split('@')
        # 取得 domain mx
        host_key = fetch_mx(host)
        if host_key is None:
            return False
        # 隨機篩選一組 domain
        host = random.choice(host_key)
        logger.info('正在連接 Server...：%s' % host)
        rresult = None
        try :
            # 啟用 SMTP
            s = smtplib.SMTP(host, timeout=10)
            # 將命令發送到服務器
            helo = s.docmd('helo server')
            logger.debug(helo)
            # 指令設定來源
            send_from = s.docmd('MAIL FROM:<xxxxx@gmail.com>')
            # logger.debug(send_from)
            try :
                # 指令設定目標
                send_from = s.docmd('RCPT TO:<%s>' % email)
                # logger.debug(send_from)
                # 取得回傳狀態
                if send_from[0] == 250 or send_from[0] == 451:
                    return True 
                else:
                    return False 
            except:
                return False

            # 關閉 SMTP
            s.close()
        except:
            return False
    else:
        return False



if __name__ == '__main__':
    final_list = verify('xxxxxx@gmail.com')
    print(final_list)
