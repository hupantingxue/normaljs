# -*- coding: utf-8 -*-

# 手机快捷支付服务器异步通知地址
SECURITY_NOTIFY_URL = ''

# 手机网页支付服务器异步通知地址
WAP_NOTIFY_URL = ''

# 手机网页支付页面同步通知地址
WAP_CALL_BACK_URL = ''

# 支付宝网关
ALIPAY_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm?'

# 支付宝安全验证地址
ALIPAY_VERIFY_URL = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'

# 支付宝合作身份证ID
PARTNER = '2088511842720240'

# 支付宝交易安全检验码，用于MD5加密
KEY = '4zgl71ds7z6xafhvhsxb01hjvb2d23jk'

# 支付宝商户私钥，用于RSA加密
PRIVATE_KEY = "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAMVyjYCn0Qh33oYT4dmv2875gKkZNTk3gN9aGSND9dtaNSfdronpHpQ1vzNBtmhLTnTIGdbybEfKcq4krpBiGZVdnZaJ99uMyEmrpTqM3OyIDb6JGIzSyexeTV6BCzDSIBSCJjGcCkPHjPAQbHWYhNJrWj+JzgyQCpZm7ahuk5HNAgMBAAECgYA/kDMxmdTXbw96BmiM1epjZTsgNPdHZjDctnqlObmqVg4KuXj4+M1ZVTwqWhtI1AV73vdClWR6cBgfK7vuy0YEmQhkwFP31X2B40Hiv9+UGTctFscxphkLAEyQATXEMgv8S5x8EC/Zl04QZCBYhjvEFrmAQ8cJCLLiXF8Gm+6zmQJBAOUha84lWRUYT/mbVLIeC/06DUZQadbW1TTMKykiq92ouZNpvbZC6NL2KDcFdUH0hGBklQjBtlQVSKd8h8Ys0lMCQQDcmf6bMqHNv6jsW1DgwpDvQWcsEFPw05oYKJhyBeothHSjD1rq/1G+c7F420KOw6CMC2XcCUslqD2q2JfZYcdfAkAWaSBsN0bxQ0F/PmwYR8wQZn8p42+WrciIs3d9PIDm2zvbaTo++2heSelBCG2hl9LiwrO4+Ylly/chOpLlFTk1AkBDlJWQG/G/o0BvsAXV5SUbdrDRqerdMyXY0s7o13EHIrXMok6bAT6clrq+qIT6UWnknTVGND6mOaUyqonSWYcHAkAW+PmdlCjxzrUHBCXI0cF5Ft3qnPqaBBptLrmSB/NvbrqqK1FQytJYINq2exKfdf/2xgv8/r03A4nPwAWdOZvB"

# 支付宝公钥，用于RSA验签
ALIPAY_PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDFco2Ap9EId96GE+HZr9vO+YCpGTU5N4DfWhkjQ/XbWjUn3a6J6R6UNb8zQbZoS050yBnW8mxHynKuJK6QYhmVXZ2WiffbjMhJq6U6jNzsiA2+iRiM0snsXk1egQsw0iAUgiYxnApDx4zwEGx1mITSa1o/ic4MkAqWZu2obpORzQIDAQAB"

# 字符编码
INPUT_CHARSET = 'utf-8'

# 签名方式，可选0001(RSA), MD5
SIGN_TYPE = 'MD5'

# 支付宝账户，所有订单款项都将打到这个账户。必须和支付宝分配的商户ID匹配。
EMAIL = '1933086609@qq.com'
