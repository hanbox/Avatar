#-*- coding: utf-8 -*-


# 您需要先注册一个App，并将得到的API key和API secret写在这里。
# You need to register your App first, and enter you API key/secret.
API_KEY = "5ZHX86zdVNU1satcQaUDdxkm1j8ksNJ7"
API_SECRET = "At1XRbk4rpwg7BGZFK29V6XiWRvBXk-p"

# 网络图片的URL地址,调用demo前请填上内容
# The url of network picture, please fill in the contents before calling demo
face_one = 'http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic11.jpg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_two = 'demo.jpeg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_search = 'demo.jpeg'

#国际版的服务器地址
#the server of international version
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat
from facepp import API, File

def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


# First import the API class from the SDK
# 首先，导入SDK中的API类


def analyze_user(filepath, id_img):
    print filepath
    api = API(API_KEY, API_SECRET)
    ret = api.faceset.create(outer_id=id_img)
    # print_result("faceset create", ret)

    Face = {}
    res = api.detect(image_file=File(filepath))
    if res["faces"]:
        Face['person'] = res["faces"][0]["face_token"]
        res = api.face.analyze(image_file=File(filepath), face_tokens=Face['person'],return_attributes='gender,age,smiling,glass,headpose,facequality,blur')
        print_result("person", res)

    # res = api.detect(image_file=File(face_two))
    # print_result("person_two", res)
    # Face['person_two'] = res["faces"][0]["face_token"]

    # # 将得到的FaceToken存进Faceset里面
    # # save FaceToken in Faceset
    # api.faceset.addface(outer_id=id_test, face_tokens=Face.itervalues())

    # # 对待比对的图片进行检测，再搜索相似脸
    # # detect image and search same face
    # ret = api.detect(image_file=File(face_search))
    # print_result("detect", ret)
    # search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id=id_test)

    # # 输出结果
    # # print result
    # print_result('search', search_result)
    # print '=' * 60
    # for k, v in Face.iteritems():
    #     if v == search_result['results'][0]['face_token']:
    #         print 'The person with highest confidence:', k
    #         break

    api.faceset.delete(outer_id=id_img, check_empty=0)
    return res
