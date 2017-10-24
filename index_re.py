from konlpy.tag import Kkma
kkma = Kkma()


class attrDic:
    keywordList = []
    attrList = []

    def __init__(self):
        self.keywordList.append('냄새/NNG')
        self.attrList.append(['나/NP'])
        self.keywordList.append('가격/NNG')
        self.attrList.append(['착하/VA'])
        self.keywordList.append('배송/NNG')
        self.attrList.append(['빠르/VA'])

    def isAttr(self, keyword, attr):
        if keyword in self.keywordList:
            i = self.keywordList.index(keyword)
            if i > -1:
                return True
            else:
                return False
        else:
            return False

class ruleDetail:
    r1SCheck = False
    r1ECheck = False
    r2SCheck = False
    r2ECheck = False
    r3SCheck = False
    r3ECheck = False
    r1SList = []
    r1EList = []
    r2SList = []
    r2EList = []
    r3SList = []
    r3EList = []
    ruleDepth = 0
    def __init__(self, rule):
        if len(rule[0][0]) > 0: self.r1SCheck = True
        if len(rule[0][1]) > 0: self.r1ECheck = True
        if len(rule[1][0]) > 0: self.r2SCheck = True
        if len(rule[1][0]) > 0: self.r2ECheck = True
        if len(rule[2][0]) > 0: self.r3SCheck = True
        if len(rule[2][0]) > 0: self.r3ECheck = True

        self.r1SList = rule[0][0]
        self.r1EList = rule[0][1]
        self.r2SList = rule[1][0]
        self.r2EList = rule[1][1]
        self.r3SList = rule[2][0]
        self.r3EList = rule[2][1]

        if self.r3SCheck or self.r3ECheck: self.ruleDepth = 3
        elif self.r2SCheck or self.r2ECheck: self.ruleDepth = 2
        elif self.r1SCheck or self.r1ECheck: self.ruleDepth = 1

class applyRuleReport:
    applyYN = False
    context = []
    packaged= []
    def __init__(self, applyYn, context, packaged):
        self.context = context
        self.packaged = packaged
        self.applyYN = applyYn

class decoRuleCheckResult:
    result = []
    text = '\t'
    length = 0
    def __init__(self, result):
        self.result = result
        self.length = len(result)
        for i in range(len(result)):
            if type(result[i]) is chnkDetailT:
                self.text += result[i].text + ' '
            elif type(result[i]) is str:
                self.text += result[i] + ' '

class sumRuleCheckResult:
    processResult = -1
    depth = -1
    def __init__(self, processResult, depth):
        self.processResult = processResult
        self.depth = depth

class applyRule:
    context = []
    decoRuleList = [
        [
            # ['착하/VA', 'ㄴ/ETD']['가격/NNG', '에다/JC']
            [
                [[], ['ETD']]
                , [['NNG'], []]
                , [[], []]
            ]
            , [
                'R1' # R1
                , '>'
                , 'R2' # R2
            ]
        ]
        , [
            # ['화질/NNG', '도/JX']['좋/VA', '고/ECE']
            [
                [['NNG'], []]
                , [['VA', 'VV'], []]
                , [[], []]
            ]
            , [
                'R1' # R1
                , '<'
                , 'R2' # R2
            ]
        ]
        , [
            # ['배터리/NNG', '가/JKS']['빨리/MAG']['닳/VV', '아서/ECD']
            [
                [['NNG'], []]
                , [['MAG'], []]
                , [['VA', 'VV'], []]
            ]
            , [
                'R1'  # R1
                , '<'
                , 'R2'  # R2
                , '>'
                , 'R3'
            ]
        ]
        , [
            # ['많이/MAG']['파/VV', '아/ECS']
            [
                [['MAG'], []]
                , [['VA', 'VV'], []]
                , [[], []]
            ]
            , [
                'R1'  # R1
                , '>'
                , 'R2'  # R2
            ]
        ]
        , [
            # ['가격/NNG', '도/JX']['저렴/XR', '하/XSA', '고/ECE']
            [
                [['NNG'], []]
                , [['XR'], []]
                , [[], []]
            ]
            , [
                'R1'  # R1
                , '>'
                , 'R2'  # R2
            ]
        ]
    ]

    sumRuleList = [
        # ['좋/VA', '은/ETD']['것/NNB']['같/VA', '아요/EFN']
        # ['하/VV', 'ㄹ/ETD']['수/NNB']['있/VV', '어서/ECD']]
        # ['믿/VV', '을/ETD']['수/NNB']['있/VV', '는/ETD']
        [
            [
                []
                , ['ETD']
            ]
            , [
                ['NNB']
                , ['NNB']
            ]
            , [
                ['VA', 'VV', 'VCN']
                , []
            ]
        ]
        # ['권하/VV', '고/ECE']['싶/VXA', '은/ETD']
        # ['챙기/VV', '어/ECS']['주/VXV', '고/ECE']
        # ['하/VV', '어/ECS']['주/VXV', '시/EPH', '고/ECE']
        # ['나쁘/VA', '지/ECD']['않/VXV', '고/ECE']
        , [
            [
                []
                , ['ECE', 'ECS', 'ECD']
            ]
            , [
                ['VXA', 'VXV']
                , []
            ]
            , [
                []
                , []
            ]
        ]
    ]

    def __init__(self, context):
        self.context = context

    def decoRuleCheck(self):
        ret = []
        t_ret = []
        for i in range(len(self.decoRuleList)):
            rDetail = ruleDetail(self.decoRuleList[i][0])
            processResult = self.ruleCheckProcess(rDetail)

            if processResult > -1:
                index = processResult
                for j in range(len(self.decoRuleList[i][1])):
                    if self.decoRuleList[i][1][j] == 'R1' or self.decoRuleList[i][1][j] == 'R2' or self.decoRuleList[i][1][j] == 'R3':
                        t_ret.append(self.context.chnkDetailList[index])
                        index += 1
                    elif self.decoRuleList[i][1][j] == '>' or self.decoRuleList[i][1][j] == '<':
                        t_ret.append(self.decoRuleList[i][1][j])
                ret.append(decoRuleCheckResult(t_ret))
                t_ret = []
        return ret

    def sumRuleCheck(self):
        ret = ''
        #t_ret = []
        for i in range(len(self.sumRuleList)):
            rDetail = ruleDetail(self.sumRuleList[i])
            processResult = self.ruleCheckProcess(rDetail)

            if processResult > -1:
                ret = sumRuleCheckResult(processResult, rDetail.ruleDepth)
                break

        return ret

    def ruleCheckProcess(self, rDetail):
        index = -1
        ret = []
        t_ret = []
        for i in range(self.context.length):
            r1SPass = False
            r1EPass = False
            r2SPass = False
            r2EPass = False
            r3SPass = False
            r3EPass = False

            detail = self.context.chnkDetailList[i]
            nextDetail = 'None'
            nextDetail1 = 'None'
            if i < len(self.context.chnkDetailList) - 1:
                nextDetail = self.context.chnkDetailList[i + 1]
            if i < len(self.context.chnkDetailList) - 2:
                nextDetail1 = self.context.chnkDetailList[i + 2]

            if rDetail.ruleDepth == 1:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    index = i
                    break

            if rDetail.ruleDepth == 2:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    if rDetail.r2SCheck:
                        if nextDetail != 'None' and nextDetail.sTag in rDetail.r2SList: r2SPass = True
                    if rDetail.r2ECheck:
                        if nextDetail != 'None' and nextDetail.eTag in rDetail.r2EList: r2EPass = True

                    if r2SPass or r2EPass:
                        index = i
                        break

            if rDetail.ruleDepth == 3:
                if rDetail.r1SCheck:
                    if detail.sTag in rDetail.r1SList: r1SPass = True
                if rDetail.r1ECheck:
                    if detail.eTag in rDetail.r1EList: r1EPass = True

                if r1SPass or r1EPass:
                    if rDetail.r2SCheck:
                        if nextDetail != 'None' and nextDetail.sTag in rDetail.r2SList: r2SPass = True
                    if rDetail.r2ECheck:
                        if nextDetail != 'None' and nextDetail.eTag in rDetail.r2EList: r2EPass = True

                    if r2SPass or r2EPass:
                        if rDetail.r3SCheck:
                            if nextDetail1 != 'None' and nextDetail1.sTag in rDetail.r3SList: r3SPass = True
                        if rDetail.r3ECheck:
                            if nextDetail1 != 'None' and nextDetail1.eTag in rDetail.r3EList: r3EPass = True

                        if r3SPass or r3EPass:
                            index = i
                            break
        return index

class tokenPackageT:
    tokenList = [] # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
    length = 0;
    i = 0;

    def __init__(self, tokenList):
        self.tokenList = tokenList # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
        self.length = len(tokenList)

    def index(self, i):
        self.i = i
        return self.tokenList[i]

    def nextTag(self):
        if self.i < self.length - 1:
            return self.tokenList[self.i + 1].split('/')[1]
        else:
            return 'None'

class chnkDetailT:
    chnkList = [] # ['가격/NNG', '대비/NNG', '최고/NNG', '에/JKM', '요/JX']
    text = ''
    sToken = ''  # 가격/NNG
    sTag = '' # NNG
    eToken = ''  # 요/JX
    eTag = ''  # JX
    eToken_1 = 'None' # 에/JKM
    eTag_1 = 'None' # JKM
    length = 0;
    i = 0
    def __init__(self, chnkList):
        if len(chnkList) > 0:
            if type(chnkList[0]) is str:
                self.chnkList = chnkList  # ['가격/NNG', '대비/NNG', '최고/NNG', '에/JKM', '요/JX']
                self.text = str(chnkList)
                self.length = len(chnkList)
                self.sTag = chnkList[0].split('/')[1]  # NNG
                self.eTag = chnkList[-1].split('/')[1]  # JX
                self.sToken = chnkList[0]  # 가격/NNG
                self.eToken = chnkList[-1]  # 요/JX
                if len(chnkList) > 1:
                    self.eToken_1 = chnkList[-2]  # 에/JKM
                    self.eTag_1 = chnkList[-2].split('/')[1]  # JKM
            elif type(chnkList[0]) is chnkDetailT:
                for i in range(len(chnkList)):
                    self.chnkList.append(chnkList[i].chnkList)
                    self.text += chnkList[i].text
                    self.length += chnkList[i].length
                self.text = '[' + self.text + ']'
                self.sTag = chnkList[0].sTag
                self.eTag = chnkList[-1].sTag
                self.sToken = chnkList[0].sToken
                self.eToken = chnkList[0].eToken
                if len(chnkList) > 1:
                    self.eToken_1 = chnkList[-2].eToken
                    self.eTag_1 = chnkList[-2].eTag

class chnkPackageT:
    chnkDetailList = []
    length = 0
    i = 0
    text = ''

    def __init__(self, chnkDetailList):
        self.chnkDetailList = chnkDetailList
        self.length = len(chnkDetailList)
        for i in range(len(chnkDetailList)):
            self.text += chnkDetailList[i].text

    def index(self, i):
        self.i = i
        return self.chnkDetailList[i]

    def nextDetail(self):
        if self.i < self.length - 1:
            return self.chnkDetailList[self.i + 1]
        else:
            return 'None'

    def nextDetail1(self):
        if self.i < self.length - 2:
            return self.chnkDetailList[self.i + 2]
        else:
            return 'None'

    def beforeDetail(self):
        if self.i > 0:
            return self.chnkDetailList[self.i - 1]
        else:
            return 'None'

    def beforeDetail1(self):
        if self.i > 1:
            return self.chnkDetailList[self.i - 2]
        else:
            return 'None'

class contextPackageT:
    chnkPackageList = []
    length = 0
    i = 0
    text = ''

    def __init__(self, chnkPackageList):
        self.chnkPackageList = chnkPackageList
        self.length = len(chnkPackageList)
        for i in range(len(chnkPackageList)):
            self.text += chnkPackageList[i].text

    def index(self, i):
        self.i = i
        return self.chnkPackageList[i]

    def nextContext(self):
        if self.i < self.length - 1:
            return self.chnkPackageList[self.i + 1]
        else:
            return 'None'

    def beforeContext(self):
        if self.i < self.length - 1:
            return self.chnkPackageList[self.i + 1]
        else:
            return 'None'

class textAnalyzer:
    text = ""
    tokenized = []
    tagList = []
    eList = ['EPH', 'EPT', 'EPP', 'EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR', 'ECE', 'ECS', 'ECD', 'ETN', 'ETD']  # 어미
    jList = ['JKS', 'JKC', 'JKG', 'JKO', 'JKM', 'JKI', 'JKQ', 'JC', 'JX']  # 관계언
    vList = ['VV', 'VA', 'VXV', 'VXA', 'VCP', 'VCN']  # 용언
    sList = ['SF', 'SE', 'SS', 'SP', 'SO', 'SW']
    exceptList = ['MAG', 'MAC']

    def __init__(self, text):
        self.text = text
        self.tokenized = self.tokenize()  # '화질/NNG', '도/JX', '좋/VA', '고/ECE' ...
        self.tagList = self.setTagList()  # NNG, JX, VA, ECE ...
        self.chnkPackage = self.setChnkPackage()  # ['화질/NNG', '도/JX']['좋/VA', '고/ECE'] ...
        self.contextPackage = self.setContextPackage()

    def tokenize(self):
        return ['/'.join(t) for t in kkma.pos(self.text)]

    def setTagList(self):
        tagList = []
        for i in range(len(self.tokenized)):
            tagList.append(self.tokenized[i].split('/')[1])
        return tagList

    def setChnkPackage(self): # '화질/NNG', '도/JX' >> ['화질/NNG', '도/JX'] '좋/VA', '고/ECE' >> ['좋/VA', '고/ECE']
        ret = []
        t_ret = []
        tokenPackage = tokenPackageT(self.tokenized)
        for i in range(len(self.tokenized)):
            token = tokenPackage.index(i)
            tag = token.split('/')[1]
            nextTag = tokenPackage.nextTag()

            if tag in self.sList or tag == 'EMO':  # 기호 및 Emoticon 제외
                continue

            t_ret.append(token)
            if nextTag in self.exceptList or nextTag in self.vList:  # MAG나 용언(동사, 형용사) 앞에서 나눔
                if len(t_ret) > 0:
                    ret.append(chnkDetailT(t_ret))
                t_ret = []
            if tag in self.eList or tag in self.jList:  # 어미나 관계언(조사)에서 나눔
                if nextTag in self.eList or nextTag in self.jList:  # 다음 토큰도 어미나 관계언이면 Pass
                    pass
                else:
                    if len(t_ret) > 0:
                        ret.append(chnkDetailT(t_ret))
                    t_ret = []
            if tag in self.exceptList:  # MAG나 기호에서 나눔
                if len(t_ret) > 0:
                    ret.append(chnkDetailT(t_ret))
                t_ret = []

            '''
            if token == '배송/NNG' and nextTag  == 'NNG':
                if len(t_ret) > 0:
                    ret.append(chnkDetailT(t_ret))
                t_ret = []
            '''

        if len(t_ret) > 0:
            ret.append(chnkDetailT(t_ret))
        t_ret = []
        return chnkPackageT(ret)

    def printChnkPackage(self):
        temp_string = ''
        for i in range(self.chnkPackage.length):
            detail = self.chnkPackage.index(i)
            temp_string += detail.text
        print(temp_string)

    def setContextPackage(self):
        t_ret = []
        ret = []

        eList = self.eList[:]  # eList와 self.eList가 동일한 참조를 가져 슬라이싱([:]) 추가
        if 'ETD' in eList:
            eList.pop(eList.index('ETD'))  # ['있/VV', '는/ETD']['브랜드/NNG', '에/JKM']

        detailList = self.chnkPackage
        for i in range(detailList.length):  # chnkDetail(['화질/NNG', '도/JX']), chnkDetail(['좋/VA', '고/ECE']) ...
            detail = detailList.index(i)
            nextDetail = detailList.nextDetail()
            t_ret.append(detail)

            if detail.eTag in eList:  # 기본적으로, 어미로 끝나면 줄나눔
                # if nextDetail != 'None' and nextDetail.sTag in eList:
                # pass
                if type(nextDetail) is chnkDetailT and (nextDetail.sTag == 'VXV' or nextDetail.sTag == 'VXA'):
                    # 어미 + 보조동사는 줄나눔 X : 하/XSV 고/ECE 있/VXV 었/EPT ...
                    # 어미 + 보조형용사는 줄나눔 X : ['권하/VV', '고/ECE'] ['싶/VXA', '은/ETD']
                    pass
                else:
                    if len(t_ret) > 0:
                        ret.append(chnkPackageT(t_ret))
                    t_ret = []

            ###########################################################################

            '''
            if detail.eToken == '요/JX':  # ~에요(에/JKM, 요/JX)로 끝나면 줄나눔
                if detail.eToken_1 == '에/JKM':
                    if len(t_ret) > 0:
                        ret.append(t_ret)
                    t_ret = []

            if detail.eToken == '하지만/MAC':  # ['콩알/NNG', '만/JX']['하지만/MAC']['과일/NNG', '맛/NNG', '이/JKS']
                if len(t_ret) > 0:
                    ret.append(t_ret)
                t_ret = []
            '''

        if len(t_ret) > 0:
            ret.append(chnkPackageT(t_ret))
        t_ret = []

        contextPackage = contextPackageT(ret)
        contextRePackage = self.setContextRePackage(contextPackage)

        return contextRePackage

    def setContextRePackage(self, contextPackage):
        for i in range(len(contextPackage.chnkPackageList)):
            index = applyRule(contextPackage.chnkPackageList[i]).sumRuleCheck()
            if type(index) is sumRuleCheckResult:
                ret = []
                t_ret = []
                jumpFlag = False
                for j in range(len(contextPackage.chnkPackageList[i].chnkDetailList)):
                    if j in range(index.processResult, index.processResult + index.depth):
                        if jumpFlag == False: jumpFlag = True
                        t_ret.append(contextPackage.chnkPackageList[i].chnkDetailList[j])
                    else:
                        if jumpFlag == True:
                            jumpFlag = False
                            ret.append(chnkDetailT(t_ret))
                            t_ret = []
                        ret.append(contextPackage.chnkPackageList[i].chnkDetailList[j])
                ret.append(chnkDetailT(t_ret))
                t_ret = []
                contextPackage.chnkPackageList[i] = chnkPackageT(ret)

        return contextPackage

    def printContextPackage(self):
        for i in range(self.contextPackage.length):
            context = self.contextPackage.index(i)
            print(context.text)

            decoResult = applyRule(context).decoRuleCheck()
            for j in range(len(decoResult)):
                print(decoResult[j].text)

textList = []

textList.append('상품이 여기저기 색이 벗겨져 새 상품같지 않네요~누가 반송한 상품인건지...밤에 찍은거라 빛 때문에 잘 보이진 않지만~상품을 꺼냈을때 아이가 맘이 상했네요~교환 신청하고 쉽지만 아이가 그냥 사용하겠다네요~')
textList.append('수신거리가 짧고 배터리가 빨리 닳아서 좀 아쉽지만 ..  가지고 놀기 딱 좋네요.. 빠르고 배리굿 바퀴하나는 자가 도색함 ㅋㅋ')
textList.append('생일선물로 구매했는데 배송도 빠르고 가격도 저렴하고 상품도 너무 괜찮습니다  많이파세요~')
textList.append('해외배송이라늦을줄알았는데생각보다빠른배송에깜작놀랐네요 가성비굿이며 추천')
textList.append('대형마트에서 구매하려다가 가격비교해 보니 15,000원이나 저렴해서 구매했습니다. 배송도 총알이고..매우 만족함. 많이 파세여... 역시 장난감은 온라인이 저렴하네여..')
textList.append('무선조종 자동차 스마트토이 쎌토 Jeep패키지 RC카 조립다하고보니 스마트폰으로도 조종이되더라구요 신기해요 ㅋㅋ 잘 가지고 놀고있습니다 굿!!')
textList.append('애들 장난감으로 싼 가격은 아니지만, RC카 중에서는 저렴한편인데 가격대비 크기도 크고, 바퀴쪽 서스펜션이 스프링 타입으로 잘 돼 있어서 주행감이 좋습니다.  후륜구동이고,  파워도 좋은편이라 드리프트도 가능하고 속도도 빠르고 재미가 있습니다.  추가배터리 같이 구입해서 바꿔가며 사용하는데,  배터리 한개보다는 추천입니다.  단점: 차량의 전원스위치 작동이 불편합니다.  차량 커버를 탈거하고, 배터리케이스를 분리해야 켜고 끌수있는 스위치가 노출됩니다.  왜 이렇게 만들었는지......ㅋ 초딩 아들 장난감으로 RC카 5만원 이하제품 몇개 사봤는데,  지금까지 제품중에 가장 쓸만합니다.  추천해요~')

'''
textList.append('냄새가좀나서 받자마자 세탁했는데.. 목안늘어났으면 좋겠네용ㅠㅠ')
textList.append('착한 가격에다 빠른배송 맘에듬니다 연근 조림할때 넣었더니 윤기가 좌르르하니맛있네요')
textList.append('홈플러스 간단히 장보기 조은거 같아요ㆍ배송조 빠르구요ㆍ 부산오데ㅣㅇ 양도 좋고 가격도 착하고 맛도 괜찬은거같아요ㆍ')
textList.append('빠르고 친절한 배송에 정해진 시간에 오니까 너무 편리하네요  가격도 시중가에 비해 훨씬 저렴하네요')
textList.append('들깨가루를 구입을 하였는데 가격도 좋고 빠른 배송으로 빠르게 구입을 할수 있어서 너무 좋았습니다 다른 사람에게도 권하고 싶은 제품입니다 감사합니다')
textList.append('주위분들이 비타민이 좋다하여 부모님과 제가 먹으려고 2개 구입했습니다. 추석명절전이라 추석전에 도착할까 걱정 많이했는데 다행히 도착하여 부모님께 잘 선물해 드렸습니다. 빠른 배송 감사드리며, 몇번을 포장하여 안전하게 도착했습니다. 비타민 잘 먹고 부모님과 제가 올 겨울에는 감기 걱정없이 보냈으면 합니다.')
textList.append('딸기맛 사탕 구입하다가 이걸로 바꿨는데. 가격도 나쁘지 않고. 크기는 콩알만 하지만 과일맛이 여러가지라서 좋네요. 어차피 향이랑 색소 차이라서 녹으면 설탕 맛입니다. 배송 많이 느립니다. 한시간 넘게 느려요.')
textList.append('배송빠르고 가격싸고 사은품챙겨주고 무엇보다 믿을수있는 브랜드에 업체가 확실하여 주져없이 주문했어요  최~~~고!!!!')
textList.append('사이즈 넉넉하지 않고')
textList.append('사이즈 넉넉하지 아니하고')
textList.append('사이즈 넉넉하고 프린트도 예뻐서 마음에 들어요 동생도 보더니 예쁘다고 자기꺼도 사달래네요 배송도 빠르고 만족합니다 많이 파세요!')
textList.append('아직 안 써봐서 뭐라 할 수는 없지만  일단 배송 빨랐어요 이번엔 꼭 임신 됐으면 좋겠네요^^ 다른분들도 이쁜아기 낳고 행복하세요^^')
textList.append('아직 안 써봐서 뭐리 할 수는 없지만  일단 배송 빨랐어요 이번엔 꼭 임신 됐으면 좋겠네요^^ 다른분들도 이쁜아기 낳고 행복하세요^^')
textList.append('배송 정말 하루만에 오네요 천천히 와도 되는데.. 맛은 초코가 좀더 맛있는겨 같아요 그래도 잘 먹을게요')
textList.append('초기불량으로 교환요청했는데 보낼생각을 안하다가 글 남기니까 배송하네요 ㅋㅋㅋ')
textList.append('아이가 태어나서 부터 먹던 제품 이렇게 포장부터 다른 안전 배송은 처음이네요.  좋아요. 굿')
textList.append('화질도 좋고, 소리도 잘 들리고 가격대비 최고에요! 추석 연휴라서 배송 안 될꺼라 생각하고 있었는데  대체휴일에도 배송 해 주시고... 덕분에 애들이 너무 좋아하네요! 진심 감사합니다~^^ 번창하세요??')
textList.append('추석연휴에 주문하는 바람에 연휴끝나고도 한참후에 받을줄 알았더니.. 까만날돌아오자마자 총알배송! 1600짜리 이렇게 싼것도 없는데 정말 잘샀어요!')
textList.append('여기서 두번사먹어봐서 가격이저렴하게올라왔길래 믿고샀습니다. 근데..고추양념만너무많이들어있고 갓김치포기는몇개안되네요..차라리 이렇게파실거면 싸게팔지말고 원래파시던가격으로파세요~~ 배송은맘에들었으나 상품은별로네요;;; 재구매는 좀생각해봐야할것같네요.')
textList.append('배송은 빠르네요 발도편하고 부담없이 신기 좋아요 근데... 앞에 리본이 삐뚤해요~ 신을때마다 잘 정리하고 신어야겠어요')
textList.append('새집으로 이사와서 새집증후군이 생기는듯하여 주문했어요~ 배송이 어떻게 올지 궁금했는데 엄청 잘싸져서 왔네요. 감사합니다. 잘키울게요~ 이 아이는 하루하루 다르게 크네요.')
textList.append('브릿츠 스피커 작은거 쓰다가 이번에 새로나온 제품 구매했네요 라디오도 나와서 쉽게 들을 수 있을 거 같네요 배송도 엄청 빨리와서 더더욱 좋아요')
textList.append('배송빨라서 좋았습니다. 기존와이파이가 고장나서 구매하게 되었는데 속도, 인식률등등 다방면적으로마음에 드네요~~ 문의가있어 전화드렸더니 친절하게 응대해주셔서 기분좋았습니다~^^')
textList.append('좋은 선물이 되었어요  명절연휴 끝나고 또 추가주문했는데 금액이 좀 오른거죠? 그래도 먹기에도 선물로도 고급지고 맘에 들어요 좋아요 좋아요 롯데**에서 7만원대에 팔더군요 70미리 60개~')
textList.append('아버지 생신 선물로 사드렸는데 이쁘네요.')
textList.append('가격도 매우 저렴하고 일단 맛이 입맛에 당길 정도로 칼칼하고 부드러워요 맛있어요 배송도 빠르고 친절합니다')
textList.append('가격도매우저렴히고일단맛이입맛에당길정도로칼칼하고브두워요 맛있어요 배송도빠르고친절합니다')
textList.append('재작년에 에넥스에서 보트 사서 아주 만족스럽게 사용하고 있는데 이번에 튜브두개 또 샀네요...튜브 마무리나 두께가 확실히 두껍고 안전해 보여서 좋네요... ')
textList.append('인터넷 이미지 보다 훨씬 더 크고 튼튼하네요 색상도 밝은 아이보리 색상으로 훨씬 이쁘네요 배송도 빠르고 배송기사님도 친철합니다. 적극 추천합니다.')
textList.append('터래기가 자알 안 까끼요.  또 문제는 같은 모델인데도 상표가 제각각..  여튼 전에 삿던 카이저가 괜찮아 상표 보고 선물용으로 20개 구매했는데 주고 욕 먹는거 아닌지..')
'''

for i in range(len(textList)):
    tokenSet = textAnalyzer(textList[i])
    #print(tokenSet.tokenized)
    #print(tokenSet.tagList)
    #tokenSet.printChnkPackage()
    tokenSet.printContextPackage()
    #tokenSet.printChnkListDep2()
    print('')